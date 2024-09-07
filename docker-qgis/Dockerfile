ARG ARCH=arm64v8
FROM ${ARCH}/ubuntu:noble

# Install dependencies and QGIS
RUN apt-get update && apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    gnupg software-properties-common wget \
    python3-pip xvfb iputils-ping glibc-tools git \
    # Add QGIS repository
    && wget -O /etc/apt/keyrings/qgis-archive-keyring.gpg https://download.qgis.org/downloads/qgis-archive-keyring.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/qgis-archive-keyring.gpg] https://qgis.org/ubuntu-ltr noble main" | tee /etc/apt/sources.list.d/qgis.list \
    && apt-get update \
    # Install QGIS and other dependencies
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    qgis qgis-plugin-grass python3-qgis \
    libgdal-dev libgeos-dev libproj-dev \
    libspatialite-dev libspatialindex-dev libsqlite3-dev \
    libexpat1-dev libfcgi-dev \
    libgsl-dev libpq-dev \
    libexiv2-dev libzip-dev \
    python3-dev python3-setuptools \
    libprotobuf-dev protobuf-compiler

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set environment variables
ENV LANG=C.UTF-8
ENV QT_QPA_PLATFORM=offscreen
ENV QGIS_PREFIX_PATH=/usr
ENV PYTHONPATH=${QGIS_PREFIX_PATH}/share/qgis/python:${PYTHONPATH}
ENV XDG_RUNTIME_DIR=/root
ENV LD_PRELOAD="/lib/aarch64-linux-gnu/libSegFault.so"
ENV SEGFAULT_SIGNALS="abrt segv"
ENV LIBC_FATAL_STDERR_=1

# Allow local development for `libqfieldsync` and qfieldcloud-sdk-python
ENV PYTHONPATH=/libqfieldsync:/qfieldcloud-sdk-python:${PYTHONPATH}

WORKDIR /usr/src/app

# Install regular dependencies that rarely change
COPY requirements.txt /tmp/
RUN pip3 install --break-system-packages --ignore-installed -r /tmp/requirements.txt

# Install `libqfieldsync` dependency
COPY requirements_libqfieldsync.txt /tmp/
RUN pip3 install --break-system-packages --use-deprecated=legacy-resolver -r /tmp/requirements_libqfieldsync.txt

COPY schemas schemas
COPY qfc_worker qfc_worker
COPY entrypoint.py .

ENTRYPOINT ["/bin/sh", "-c", "/usr/bin/xvfb-run -a \"$@\"", ""]
CMD ["python3"]
