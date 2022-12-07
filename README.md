# Airthings API to InfluxDB

Allows for importing data to [InfluxDB](https://www.influxdata.com/) v2 for [Airthings](https://www.airthings.com/) cloud-connected devices.


## Requirements

- An [Airthings](https://www.airthings.com/) device that's connected to the cloud, such as the [View Plus](https://www.airthings.com/view-plus) device.
- A device with either [Docker](https://www.docker.com/) or Python installed.
- [InfluxDB](https://en.wikipedia.org/wiki/InfluxDB) v2 installed on this device or another device, and a bucket created in influxDB.

## Setup

### With Docker

Dependency: Docker installed.

1. Download and run the Docker image: `sudo docker run --name airthings-api -v config.yaml:/app/config.yaml vdbg/airthings-api-influx:latest`
2. Copy the template config file from the image: `sudo docker cp airthings-api:/app/template.config.yaml config.yaml`
3. Edit `config.yaml` by following the instructions in the file
4. Start the container again to verify the settings are correct: `sudo docker start airthings-api -i`
5. Once the settings are finalized, `Ctrl-C` to stop the container, `sudo docker container rm airthings-api` to delete it
6. Start the container with the final settings:

``
sudo docker run \
  -d \
  --name airthings-api \
  -v /path_to_your/config.yaml:/app/config.yaml \
  --memory=100m \
  --pull=always \
  --restart=always \
  vdbg/airthings-api-influx:latest
``

### Without Docker

Dependency: Python3 and pip3 installed. `sudo apt-get install python3-pip` if missing on raspbian.

1. Git clone this repository and cd into directory
2. `cp template.config.yaml config.yaml`
3. Edit file `config.yaml` by following the instructions in the file
4. `pip3 install -r requirements.txt`
5. `python3 main.py` or `./main.py`

## Cloud vs. Local considerations

For Airthings devices that provide local querying capabilities, a recommended alternative is to use BLE instead.
Some starting code is provided in [Airthing's github](https://github.com/airthings).

This script is better suited for Airthings devices that do not provide local querying capabilies but do provide cloud APIs, such as Airthings [View Plus](https://www.airthings.com/view-plus). Note that there's an inherent risk with having a strong cloud dependency, as exemplified by one of [Airthings competitors](https://www.reddit.com/r/Awair/comments/y7i5ku/awair_discontinues_support_for_v1_devices/).
