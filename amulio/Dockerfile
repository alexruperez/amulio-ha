# syntax=docker/dockerfile:1

ARG PYTHON_IMAGE=python:3.15-slim
FROM ${PYTHON_IMAGE} AS amule-builder

ARG AMULE_REF=7958b6926910b1f59b477b146bcf8882139f9558
ARG WX_REF=5ff25322553c1870cf20a2e1ba6f20ed50d9fe9a

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential ca-certificates cmake git libboost-dev libcrypto++-dev \
        libcurl4-openssl-dev libglib2.0-dev libgtk-3-dev libwxgtk3.2-dev \
        pkg-config zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
RUN git clone https://github.com/wxWidgets/wxWidgets.git wxwidgets \
    && git -C wxwidgets checkout --force "$WX_REF" \
    && git -C wxwidgets submodule update --init --recursive \
    && cd wxwidgets \
    && ./configure --prefix=/opt/wx --with-gtk=3 --with-libcurl --enable-unicode \
        --enable-shared --disable-debug --disable-mediactrl --disable-webview \
        --disable-richtext --disable-aui \
    && make -j"$(nproc)" \
    && make install
RUN git clone https://github.com/amule-org/amule.git amule \
    && git -C amule checkout --force "$AMULE_REF" \
    && cmake -S amule -B amule-build \
        -DCMAKE_PREFIX_PATH=/opt/wx \
        -DCMAKE_INSTALL_PREFIX=/opt/amule \
        -DBUILD_MONOLITHIC=NO \
        -DBUILD_DAEMON=YES \
        -DBUILD_AMULEAPI=YES \
        -DBUILD_ED2K=NO \
        -DCRYPTOPP_INCLUDE_PREFIX=crypto++ \
        -DENABLE_NLS=NO \
        -DENABLE_UPNP=NO \
        -DENABLE_IP2COUNTRY=NO \
    && cmake --build amule-build -j"$(nproc)" \
    && cmake --install amule-build

FROM ${PYTHON_IMAGE} AS amulio-builder
COPY --from=ghcr.io/astral-sh/uv:0.9.25 /uv /usr/local/bin/uv
ARG AMULIO_REF=088334409a4c3aeb7973411b07450c3250058f15
ENV UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /src
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates git \
    && rm -rf /var/lib/apt/lists/* \
    && git clone https://github.com/alexruperez/amulio.git app \
    && git -C app checkout --detach "$AMULIO_REF"
WORKDIR /src/app
RUN uv sync --locked --no-dev --no-editable

FROM ${PYTHON_IMAGE}
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        bash ca-certificates coreutils gosu jq libcrypto++8 libcurl4 libglib2.0-0 \
        libgtk-3-0 libpcre2-32-0 \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/local/lib/python*/site-packages/* \
    && useradd --system --uid 10001 --create-home --home-dir /var/lib/amule amule

COPY --from=amule-builder /opt/wx /opt/wx
COPY --from=amule-builder /opt/amule /opt/amule
COPY --from=amulio-builder /opt/venv /opt/venv
COPY --from=amulio-builder /src/app/src /app/src
COPY rootfs/usr/local/bin/amulio-ha-run /usr/local/bin/amulio-ha-run

RUN chmod 755 /usr/local/bin/amulio-ha-run \
    && mkdir -p /data/config /data/incoming /data/temp /data/amulio /data/secrets \
    && chown -R amule:amule /data /var/lib/amule

ENV PATH="/opt/venv/bin:/opt/amule/bin:$PATH" \
    LD_LIBRARY_PATH="/opt/wx/lib" \
    PYTHONPATH="/app/src" \
    PYTHONUNBUFFERED=1
EXPOSE 8000 4662 4672/udp
ENTRYPOINT ["/usr/local/bin/amulio-ha-run"]
