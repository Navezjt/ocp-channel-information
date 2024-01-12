# OpenShift Channel Information

This application shows current available versions in a specified channel (stable, fast or candidate). It can be run either as a command-line script or as a Flask API.

## Running as a Command-Line Script

### Prerequisites

Make sure you have Python installed on your machine.

### Usage

```bash
python app.py --channel <channel> --version <version>
```

Replace <channel> with either 'fast', 'stable', or 'candidate', and <version> with the desired OpenShift version (e.g., '4.14', '4.12', etc.).

## Running as a Flask API

### Prerequisites

Make sure you have Python and Flask installed on your machine.

### Usage

```bash
python app.py --api
```

The Flask app will run on http://127.0.0.1:5000. You can access the OpenShift version information API using the following endpoint:
http://127.0.0.1:5000/api/upgrades_info?channel=<channel>&version=<version>

Replace <channel> with either 'fast', 'stable', or 'candidate', and <version> with the desired OpenShift version (e.g., '4.14', '4.12', etc.).

## Running with Docker

### Prerequisites

Make sure you have Docker installed on your machine.

### Build Docker Image

```bash
docker build -t openshift-channel-app .
```

### Run Docker Container

Run as Command-Line Script

```bash
docker run openshift-channel-app --channel <channel> --version <version>
```

Run as Flask API
```bash
docker run -d --rm -e API_MODE=true -p 5000:5000 openshift-channel-app --api
```

Access the API at:
http://127.0.0.1:5000/api/upgrades_info?channel=<channel>&version=<version>

Replace <channel> with either 'fast', 'stable', or 'candidate', and <version> with the desired OpenShift version (e.g., '4.14', '4.12', etc.).

## Example

```bash
docker run openshift-channel-app --channel fast --version 4.14
```

This command will display the available versions for the specified channel.



