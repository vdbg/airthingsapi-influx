import datetime
import logging
import json
import requests
from requests import HTTPError

# API documentation: https://developer.airthings.com/consumer-api-docs/


class Device:
    def __init__(self, conf: dict) -> None:
        print(conf)
        self.id: str = conf["id"]
        self.type: str = conf["deviceType"]
        self.name: str = conf["segment"]["name"]
        self.location: str = conf["location"]["name"]


class AirthingsConnector:
    def __init__(self, conf: dict) -> None:
        self._clientId: str = conf["clientID"]
        self._clientSecret: str = conf["clientSecret"]
        self._enabled_devices: set[str] = set(conf["devices"])
        self._devices: list[Device] = None
        self._fields_rename: dict[str, str] = conf["fields_rename"]
        self._measurement: str = conf["measurement"]
        self._auth_url: str = conf["auth_url"]
        self._api_url: str = conf["api_url"]
        self._auth_token: str = None

    def __get_auth_token(self) -> str:
        try:
            logging.debug(f"Getting authentication token")
            token_response = requests.post(
                self._auth_url,
                data={
                    "grant_type": "client_credentials",
                    "scope": "read:device:current_values",
                },
                allow_redirects=False,
                auth=(self._clientId, self._clientSecret),
            )
            return token_response.json()["access_token"]
        except HTTPError as e:
            logging.error("Unable to get authentication token", exc_info=e)
            raise

    def __fetch_data(self, path: str) -> json:
        if not self._auth_token:
            self._auth_token = self.__get_auth_token()
        url = f"{self._api_url}{path}"
        logging.debug(f"Calling {url}")
        try:
            response = requests.get(url=url, headers={"Authorization": f"Bearer {self._auth_token}"})
            ret = response.json()
            logging.debug(f"Response: {ret}")
            return ret
        except HTTPError as e:
            self._auth_token = None
            logging.error("Unable to get data", exc_info=e)
            return None

    def __get_enabled_devices(self) -> list[Device]:
        if not self._devices:
            logging.info("Querying list of devices")
            data = self.__fetch_data("devices")
            if not data:
                raise Exception("Unable to get list of devices")
            data = [Device(d) for d in data["devices"]]
            if self._enabled_devices:
                data = [d for d in data if d.id in self._enabled_devices]
            self._devices = data

            logging.info(f"Found these devices: {self._devices}")
        return self._devices

    def fetch_data(self) -> list:
        records = []

        for device in self.__get_enabled_devices():
            data: dict = self.__fetch_data(f"devices/{device.id}/latest-samples")["data"]
            time = datetime.datetime.fromtimestamp(data["time"], tz=datetime.timezone.utc)  # airthings returns an epoch time
            logging.debug(f"Processing measurements from {time}")
            record = {
                "measurement": self._measurement,
                "tags": {"host": device.id, "name": device.name, "location": device.location, "type": device.type},
                "time": time
            }
            logging.debug(f"Data before transform: {data}")
            for key, newKey in self._fields_rename.items():
                if key in data:
                    value = data.pop(key)
                if newKey:
                    data[newKey] = value

            logging.debug(f"Data after transform: {data}")
            record["fields"] = data
            records.append(record)
        return records