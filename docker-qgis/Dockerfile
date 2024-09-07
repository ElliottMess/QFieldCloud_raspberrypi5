ARG ARCH=arm64v8
FROM ${ARCH}/ubuntu:noble

# Install dependencies
RUN apt-get update && apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    gnupg software-properties-common wget \
    python3-pip xvfb iputils-ping glibc-tools git \
    build-essential cmake \
    libqt5core5a libqt5gui5 libqt5network5 \
    libqt5widgets5 libqt5xml5 \
    libgdal-dev libgeos-dev libproj-dev \
    libspatialite-dev libspatialindex-dev libsqlite3-dev \
    flex bison \
    libexpat1-dev libfcgi-dev \
    libgsl-dev libpq-dev libqca-qt5-2-dev \
    libqca-qt5-2-plugins qtbase5-dev \
    qttools5-dev qttools5-dev-tools \
    qtpositioning5-dev libqt5svg5-dev \
    libqt5serialport5-dev qtlocation5-dev \
    qt3d5-dev libqt5opengl5-dev \
    libqwt-qt5-dev libqt5scintilla2-dev \
    libqca-qt5-2-dev libqt5xmlpatterns5-dev \
    pyqt5-dev pyqt5-dev-tools python3-pyqt5 \
    python3-pyqt5.qsci python3-pyqt5.qtsvg python3-pyqt5.qtwebkit \
    libexiv2-dev libzip-dev \
    libspatialindex-dev python3-dev python3-pip \
    libpython3-dev python3-setuptools

# Clone QGIS
RUN git clone --depth 1 --branch release-3_28 https://github.com/qgis/QGIS.git /tmp/QGIS

# Build QGIS
RUN cd /tmp/QGIS && \
    mkdir build && \
    cd build && \
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DWITH_GUI=OFF \
        -DWITH_DESKTOP=OFF \
        -DWITH_SERVER=OFF \
        -DWITH_CUSTOM_WIDGETS=OFF \
        -DWITH_BINDINGS=OFF \
        -DWITH_GRASS=OFF \
        -DWITH_GRASS7=OFF && \
    make -j$(nproc) && \
    make install && \
    ldconfig
    
# Install QGIS Python bindings
RUN pip3 install --no-cache-dir PyQGIS

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set environment variables
ENV LANG=C.UTF-8
ENV QT_QPA_PLATFORM=offscreen
ENV QGIS_PREFIX_PATH=/usr/local
ENV PYTHONPATH=${QGIS_PREFIX_PATH}/share/qgis/python:${PYTHONPATH}

WORKDIR /usr/src/app

# crashes to STDERR
ENV LD_PRELOAD="/lib/x86_64-linux-gnu/libSegFault.so"
ENV SEGFAULT_SIGNALS="abrt segv"
ENV LIBC_FATAL_STDERR_=1

# other env
ENV LANG=C.UTF-8
ENV XDG_RUNTIME_DIR=/root
# allow local development for `libqfieldsync`, requires `/libqfieldsync` to be a mounted host directory
ENV PYTHONPATH=/libqfieldsync:${PYTHONPATH}
ENV PYTHONPATH=/qfieldcloud-sdk-python:${PYTHONPATH}

# Install regular dependencies that rarely change
COPY requirements.txt /tmp/
RUN pip3 install --break-system-packages --ignore-installed -r /tmp/requirements.txt

# Install `libqfieldsync` dependecy since it changes more frequently compared to regular dependencies
COPY requirements_libqfieldsync.txt /tmp/
RUN pip3 install --break-system-packages --use-deprecated=legacy-resolver -r /tmp/requirements_libqfieldsync.txt

COPY schemas schemas
COPY qfc_worker qfc_worker
COPY entrypoint.py .

ENTRYPOINT ["/bin/sh", "-c", "/usr/bin/xvfb-run -a \"$@\"", ""]
CMD ["python3"]