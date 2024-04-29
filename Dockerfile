# ------------------------------
# Multistage Docker File
# ------------------------------
# ------------------------------
# IMAGE: Target 'base' image
# docker build --file Dockerfile --target base -t pw-base .
# docker run -it --rm pw-base
# ------------------------------
ARG UBUNTU_RELEASE=22.04
FROM ubuntu:${UBUNTU_RELEASE} AS base
LABEL maintainer="Gayle Livermore <gayle.livermore@calix.com>"
ENV LANG="C.UTF-8"
ENV LC_ALL="C.UTF-8"
ENV LC_CTYPE="C.UTF-8"
ENV TZ=America/Chicago
ENV SHELL=/bin/bash
RUN chsh -s /bin/bash
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# hadolint ignore=DL3008
RUN echo "===> Adding build dependencies..."  && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends --yes \
    git \
    libfontconfig1 \
    ca-certificates \
    wget \
    curl && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Basic install of git check
RUN ["git", "--version"]

# ------------------------------
# IMAGE: Target 'pythonbase' for base of all images that need Python
# docker build --file Dockerfile --target pythonbase -t pw-pythonbase .
# docker build --no-cache --file Dockerfile --target pythonbase -t pw-pythonbase .
# docker run -it --rm pw-pythonbase
# ------------------------------
FROM base AS pythonbase
# Using distro python3 (3.10) - todo upgrade
# hadolint ignore=DL3008
RUN echo "===> Adding build dependencies..."  && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends --yes \
    python3 \
    build-essential \
    openssh-client \
    python3-dev \
    python3-pip \
    python3-pycurl && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
# It is a good idea to upgrade package management tools to latest
# hadolint ignore=DL3013
RUN echo "===> Installing pip ..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir --upgrade setuptools wheel pyinstaller && \
    python3 -m pip install --no-cache-dir --upgrade pipenv && \
    python3 -m pip list

# ------------------------------
# IMAGE: Target 'dev' for code development - no Python pkgs loaded
# docker build --file Dockerfile --target dev -t pw-dev .
# docker run -it --rm pw-dev
# docker container run -it -d -v pw:/development -v ~/.ssh:/root/ssh -v ~/.gitconfig:/root/.gitconfig pw-dev
# docker container run -it -v pw:/development -v ~/.ssh:/root/ssh -v ~/.gitconfig:/root/.gitconfig pw-dev
# ------------------------------
FROM pythonbase AS dev
WORKDIR /
ARG PROJECT_DIR=/development
RUN echo "===> creating working directory..."  && \
    mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

# ------------------------------
# IMAGE: Target 'qa' for static code analysis and unit testing
# Future: Consider benefit lint shell script in addition to below
# Install the latest static code analysis tools
# docker build --file Dockerfile --target qa -t pw-qa .
# docker run -it --rm pw-qa
# docker run -i --rm -v ${PWD}:/code pw-qa pylint --exit-zero --rcfile=setup.cfg **/*.py
# docker run -i --rm -v ${PWD}:/code pw-qa flake8 --exit-zero
# docker run -i --rm -v ${PWD}:/code pw-qa bandit -r --ini setup.cfg
# docker run -i --rm -v $(pwd):/code -w /code pw-qa black --check --exclude pw/tests/ pw/ || true
# docker run -i --rm -v ${PWD}:/code pw-unittest pytest --with-xunit --xunit-file=pyunit.xml --cover-xml --cover-xml-file=cov.xml pw/tests/*.py
# Removed the following - not enabling playwright with this repo
# RUN echo "===> Installing playwright system dependencies and rendering engine . . ." && \
#     apt-get update && \
#     apt-get upgrade -y && \
#     #playwright install --with-deps chromium && \
#     apt-get autoremove && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*
# ------------------------------
# FROM dev AS qa
# WORKDIR /
# COPY Pipfile .
# COPY Pipfile.lock .
# # Ensure linting tools are latest 
# # hadolint ignore=DL3013
# RUN echo "===> Installing python pkgs . . ." && \
#     pipenv install --dev --deploy --system && \
#     pip install --upgrade --no-cache-dir pylint flake8 bandit black
# WORKDIR /code/

# ------------------------------
# IMAGE: Target 'builder' builds production app utilizing pipenv
# docker build --file Dockerfile --target app -t pw:app .
# docker run -it --rm pw:app
# docker run -it --rm pw:app sh
# Example running a single locust file:
# all-on-one-line: docker run -it --rm -v $PWD/config:/config -e LOCUST_TESTDATA_FILENAME="config/locust_test_data.yaml" -e LOCUST_DEVICES_FILENAME="config/devices.yaml" -p 8088:8089 pw:app locust --stop-limit 600s --locustfile locustfiles/smxapi_sub_l3bng_data_crud.py
# docker run -d -it --rm \
#     -v $PWD/config:/config \
#     -e LOCUST_TESTDATA_FILENAME ="mylocust/config/gtt_crud.yaml" \
#     -e LOCUST_DEVICES_FILENAME="mylocust/config/devices.yaml" \
#     -p 8088:8089 \
#     pw:app locust --locustfile locustfiles/locust_smxapi_gtt_crud.py
# docker run -it --rm \
#     -v $PWD/config:/config \
#     -e LOCUST_PARAMS_FILE="config/gtt_crud.yaml" \
#     -e LOCUST_DEVICES_FILE="config/devices.yaml" \
#     -p 8088:8089 \
#     --name st_locust st-locust:app sh
# docker run -it --rm --name st-locust st-locust:app 
# docker run -it --rm --name st-locust st-locust:app sh
# ------------------------------
# FROM pythonbase as app
# RUN echo "===> Installing specific python package versions ..."
# WORKDIR /
# COPY Pipfile .
# COPY Pipfile.lock .
# RUN pipenv install --system --deploy --ignore-pipfile
# COPY ./locustfiles /locustfiles/
# RUN echo "===> Setting working directories..." && \
#     mkdir /config
# VOLUME /config
# CMD ["locust", "--help"]
