ARG PYTHON_IMAGE="python"
ARG PYTHON_IMAGE_TAG="3.11.7-slim-bookworm"

# Rootless stuff
ARG USERNAME=
ARG USERUID=
ARG USERGID=
ARG USERHOME=
ARG FLASK_RUN_HOST=
ARG FLASK_RUN_PORT=

FROM ${PYTHON_IMAGE}:${PYTHON_IMAGE_TAG}

# Rootless ARGs, tweakable by building the image
ARG USERNAME="python-user"
ARG USERUID="60000"
ARG USERGID="60000"
ARG USERHOME="/home/${USERNAME}"

# Flask server ARGs, tweakable by building the image
ARG FLASK_RUN_HOST="0.0.0.0"
ARG FLASK_RUN_PORT="5000"

ENV USERNAME="${USERNAME}"
ENV USERUID="${USERUID}"
ENV USERGID="${USERGID}"
ENV USERHOME="${USERHOME}"

# These are tweakable, for whatever reason it may be
ENV FLASK_RUN_HOST="${FLASK_RUN_HOST}"
ENV FLASK_RUN_PORT="${FLASK_RUN_PORT}"

# Hardcoded here
ENV FLASK_APP="app.py"
ENV API_MODE="false"

# Python stuff
ENV PIP_DISABLE_PIP_VERSION_CHECK="1"

USER 0

# Rootless user with home
RUN groupadd --gid ${USERGID} ${USERNAME} && \
    useradd --no-log-init --create-home --gid ${USERGID} --home-dir ${USERHOME} --uid ${USERUID} ${USERNAME}

USER ${USERNAME}

WORKDIR ${USERHOME}

# Otherwise local pipenv won't be executable
ENV PATH="${PATH}:${USERHOME}/.local/bin"

COPY app.py Pipfile Pipfile.lock requirements.txt ${USERHOME}/

RUN pip install --user --no-cache-dir -r requirements.txt && \
    pipenv install --deploy --ignore-pipfile

EXPOSE ${FLASK_RUN_PORT}/tcp

ENTRYPOINT ["pipenv"]
