from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient
import logging


class InfluxConnector:

    def __init__(self, conf: dict):
        self.bucket: str = conf["bucket"]
        self.token: str = conf["token"]
        self.org: str = conf["org"]
        self.url: str = conf["url"]
        logging.debug(f"Influx url: {self.url}")

    def __get_client(self) -> InfluxDBClient:
        return InfluxDBClient(url=self.url, token=self.token, org=self.org, debug=False)

    def add_samples(self, records) -> None:
        if not records:
            return

        logging.info(f"Importing {len(records)} record(s) to influx")
        with self.__get_client() as client:
            with client.write_api() as write_api:
                write_api.write(bucket=self.bucket, record=records)
