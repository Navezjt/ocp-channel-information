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

The Flask app will run on http://localhost:5000. You can access the OpenShift version information API using the following endpoint:

```
http://localhost:5000/api/upgrades_info?channel=<channel>&version=<version>
```

Replace `<channel>` with either 'fast', 'stable', or 'candidate', and `<version>` with the desired OpenShift version (e.g., '4.14', '4.12', etc.).

## Running with Podman

### Prerequisites

Make sure you have Podman installed on your machine.

You can build and tweak it with `--build-arg` on the following ARGs:

- `FLASK_RUN_HOST`    # Default Flask ENV variable as per Flask's documentation
- `FLASK_RUN_PORT`    # Default Flask ENV variable as per Flask's documentation
- `PYTHON_IMAGE`      # Default Python container image to be used
- `PYTHON_IMAGE_TAG`  # Default Python image tag to be used
- `USERGID`           # Default user GID for rootless user creation
- `USERHOME`          # Default user HOME directory for rootless user creation - composed by /home/${USERNAME}
- `USERUID`           # Default user UID for rootless user creation
- `USERNAME`          # Default user NAME for rootless user creation

The following default values are provided for convenience:

- `FLASK_RUN_HOST="0.0.0.0"`
- `FLASK_RUN_PORT="5000"`
- `PYTHON_IMAGE="python"`
- `PYTHON_IMAGE_TAG="3.11.7-slim-bookworm"`
- `USERGID="60000"`
- `USERHOME="/home/${USERNAME}"`
- `USERNAME="python-user"`
- `USERUID="60000"`

All of the above ARGs will be ENV variables at runtime. Additionally, the following ENV variables are hardcoded in the [Containerfile](Containerfile):

- `API_MODE="false"`
- `FLASK_APP="app.py"`
- `FLASK_RUN_HOST="${FLASK_RUN_HOST}"`
- `FLASK_RUN_PORT="${FLASK_RUN_PORT}"`
- `PATH="${PATH}:${USERHOME}/.local/bin"`
- `PIP_DISABLE_PIP_VERSION_CHECK="1"`

### Build Podman Image

```bash
podman build -t openshift-channel-app:latest .
```

### Run Podman Container

#### Run as Command-Line Script

```bash
podman run --rm openshift-channel-app:latest run python app.py --channel <channel> --version <version>
```

#### Run as Flask API

```bash
podman run --rm -p 5000:5000 openshift-channel-app:latest run flask run
```

Then, access the API at your localhost:

```
http://localhost:5000
http://localhost:5000/api/upgrades_info?channel=<channel>&version=<version>
```

Valid channels are:

- candidate
- eus
- fast
- stable

## Example

```bash
$ podman run --rm openshift-channel-app:latest run python app.py --channel eus --version 4.14
4.14.2
4.14.6
4.14.7
4.14.1
4.14.0
4.14.3
4.14.5
4.14.4
[...]
```
