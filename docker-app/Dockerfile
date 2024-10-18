ARG ARCH=arm64v8

##########################
# BUILDER                #
##########################

# Name the build stage 'build'
FROM arm64v8/ubuntu:22.04 AS build

# Install necessary packages
RUN apt-get update && \
    apt-get install -y software-properties-common gnupg

# Remove the PPA addition since it may not support arm64
# RUN add-apt-repository ppa:ubuntugis/ppa && \
#     apt-get update

# Install GDAL and dependencies
RUN apt-get install -y libgdal-dev gdal-bin

# Upgrade setuptools and pip
RUN apt-get install -y python3-pip && \
    pip3 install --upgrade pip setuptools

RUN pip uninstall -y setuptools && pip install setuptools

# Install specific versions of numpy and GDAL
RUN pip3 install --no-cache-dir numpy==1.23.5
RUN pip3 install --no-cache-dir GDAL==3.4.1

# Disable annoying pip version check
ARG PIP_DISABLE_PIP_VERSION_CHECK=1

# Do not create and use redundant cache dir in the current user home
ARG PIP_NO_CACHE_DIR=1

# Install psycopg2 requirements
RUN apt-get install -y libpq-dev python3-dev gcc

# Install `pip-compile` (as part of `pip-tools`)
RUN pip3 install pip-tools

# Install pip dependencies
COPY ./requirements/requirements.txt /requirements/requirements.txt
RUN pip3 install -r /requirements/requirements.txt

# Save space by removing unnecessary files
RUN [ -d /usr/local/lib/python3.10/site-packages/botocore/data ] && find /usr/local/lib/python3.10/site-packages/botocore/data -type f ! -name "endpoints.json" -delete || echo "Directory does not exist, skipping deletion"

##########################
# BASE                   #
##########################

FROM ${ARCH}/python:3.10-slim-bullseye as base

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

# Install dependencies
RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin gettext \
    libpq-dev python3-dev gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools==58.0.4

##########################
# WORKER WRAPPER RUNTIME #
##########################

FROM base as worker_wrapper_runtime

# Set environment variable for GDAL
ARG GDAL_VERSION=3.4.1
ENV GDAL_VERSION=${GDAL_VERSION}

# Create the user and group
RUN groupadd -r app && useradd -r -g app app

# Copy and install dependencies
COPY ./requirements/requirements_worker_wrapper.txt requirements.txt
RUN pip install --upgrade setuptools && SETUPTOOLS_USE_DISTUTILS=stdlib pip install -r requirements.txt

# Copy application files
COPY . .

# Set ownership
RUN chown -R app:app .

# Switch to the app user
USER app

# Configure GDAL environment
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal && \
    export C_INCLUDE_PATH=/usr/include/gdal && \
    pip install GDAL==${GDAL_VERSION}

##########################
# WEBSERVER RUNTIME      #
##########################

FROM base as webserver_runtime

# Set environment variable for GDAL
ARG GDAL_VERSION=3.4.1
ENV GDAL_VERSION=${GDAL_VERSION}

# Create the user and group
RUN groupadd -r app && useradd -r -g app app

# Copy and install dependencies
COPY ./requirements/requirements.txt requirements.txt
RUN SETUPTOOLS_USE_DISTUTILS=stdlib pip install -r requirements.txt

# Copy application files
COPY . .

# Set ownership
RUN chown -R app:app .

# Switch to the app user
USER app

# Configure GDAL environment
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal && \
    export C_INCLUDE_PATH=/usr/include/gdal && \
    pip install GDAL==${GDAL_VERSION}
