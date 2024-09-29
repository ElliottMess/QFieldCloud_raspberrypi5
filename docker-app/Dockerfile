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

# Install specific versions of numpy and GDAL
RUN pip3 install --no-cache-dir numpy==1.23.5
RUN pip3 install --no-cache-dir GDAL==$(gdal-config --version)

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
RUN find /usr/local/lib/python3.10/site-packages/botocore/data -type f ! -name "endpoints.json" -delete

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
    binutils libproj-dev gdal-bin gettext graphviz

# Copy the dependencies from the build stage
COPY --from=build /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# **Add this command to force reinstall setuptools**
RUN pip install --upgrade --force-reinstall setuptools

# Install debug dependencies if needed
ARG DEBUG_BUILD
RUN if [ "$DEBUG_BUILD" = "1" ]; then pip3 install debugpy ipython; fi

# Add app user
RUN addgroup --system app && adduser --system app --ingroup app

# Create directories
RUN mkdir staticfiles mediafiles

# Create an empty JSON fixture
RUN echo '{}' > fixture.json

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_CONFIG=/usr/bin/gdal-config

# Copy the rest of your Dockerfile as is...
# (Ensure you include the rest of your stages and commands)

# Install GDAL Python bindings
RUN pip install --no-cache-dir numpy==1.23.5 && \
    pip install --no-cache-dir GDAL==$(gdal-config --version)

##########################
# WEBSERVER RUNTIME      #
##########################

# a separate stage for webserver runtime environment
FROM base as webserver_runtime
ENV LOGGER_SOURCE=app
COPY ./requirements/requirements_runtime.txt requirements/requirements_runtime.txt
RUN pip3 install -r requirements/requirements_runtime.txt
EXPOSE 8000

COPY . .
RUN chown -R app:app .
USER app

##########################
# WEBSERVER TEST         #
##########################

RUN export GDAL_VERSION=$(gdal-config --version) && \
    pip install GDAL==${GDAL_VERSION}

# a separate stage for webserver test environment
FROM base as webserver_test
ENV LOGGER_SOURCE=app
COPY ./requirements/requirements_test.txt requirements/requirements_test.txt
RUN pip3 install -r requirements/requirements_test.txt
EXPOSE 8000

COPY . .
RUN chown -R app:app .
USER app

# Configure GDAL
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal
RUN pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==`gdal-config --version`
COPY ./requirements/requirements_runtime.txt requirements/requirements_runtime.txt
RUN pip3 install -r requirements/requirements_runtime.txt

##########################
# WORKER WRAPPER RUNTIME #
##########################

# a separate stage for worker wrapper runtime environment
FROM base as worker_wrapper_runtime
ENV LOGGER_SOURCE=worker_wrapper
COPY ./requirements/requirements_worker_wrapper.txt requirements/requirements_worker_wrapper.txt
RUN pip3 install -r requirements/requirements_worker_wrapper.txt

COPY . .
RUN chown -R app:app .
USER app

# Configure GDAL
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal
RUN pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==`gdal-config --version`
COPY ./requirements/requirements_worker_wrapper.txt requirements/requirements_worker_wrapper.txt
RUN pip3 install -r requirements/requirements_worker_wrapper.txt