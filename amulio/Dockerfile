# https://contributors.home-assistant.io/apps/guides/dockerfile/
ARG BUILD_FROM=ghcr.io/home-assistant/base:3.24

FROM ${BUILD_FROM} AS amule-builder
ARG AMULE_REF=7958b6926910b1f59b477b146bcf8882139f9558
ARG WX_REF=5ff25322553c1870cf20a2e1ba6f20ed50d9fe9a
RUN apk add --no-cache \
    build-base ca-certificates cmake git boost-dev crypto++-dev curl-dev \
    glib-dev gtk+3.0-dev pkgconf zlib-dev
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
       -DCRYPTOPP_INCLUDE_PREFIX=cryptopp \
       -DENABLE_NLS=NO \
       -DENABLE_UPNP=NO \
       -DENABLE_IP2COUNTRY=NO \
    && cmake --build amule-build -j"$(nproc)" \
    && cmake --install amule-build

FROM ${BUILD_FROM} AS amulio-builder
COPY --from=ghcr.io/astral-sh/uv:0.9.25 /uv /usr/local/bin/uv
ARG AMULIO_REF=8b64886b71bae101b02e8513e77cfadfb5d87a87
ENV UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv
RUN apk add --no-cache ca-certificates git python3
WORKDIR /src
RUN git clone https://github.com/alexruperez/amulio.git app \
    && git -C app checkout --detach "$AMULIO_REF"
WORKDIR /src/app
RUN uv sync --locked --no-dev --no-editable

FROM ${BUILD_FROM}
RUN apk add --no-cache \
    ca-certificates coreutils crypto++ libcurl libgcc glib gtk+3.0 libstdc++ \
    libpcre2-32 pcre2 python3 su-exec jq \
    && adduser -D -u 10001 -h /var/lib/amule amule
COPY --from=amule-builder /opt/wx /opt/wx
COPY --from=amule-builder /opt/amule /opt/amule
COPY --from=amulio-builder /opt/venv /opt/venv
COPY --from=amulio-builder /src/app/src /app/src
COPY rootfs /
RUN chmod 755 /usr/local/bin/amulio-ha-run /etc/services.d/amulio/run \
    && mkdir -p /data/config /data/incoming /data/temp /data/amulio /data/secrets \
    && chown -R amule:amule /data /var/lib/amule
ENV PATH="/opt/venv/bin:/opt/amule/bin:$PATH" \
    LD_LIBRARY_PATH="/opt/wx/lib" \
    PYTHONPATH="/app/src" \
    PYTHONUNBUFFERED=1
HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
    CMD python3 -c 'import urllib.request; urllib.request.urlopen("http://127.0.0.1:8000/health")'
LABEL \
    org.opencontainers.image.title="Home Assistant App: aMulio" \
    org.opencontainers.image.description="Self-hosted aMule node and private Stremio addon" \
    org.opencontainers.image.source="https://github.com/alexruperez/amulio-ha" \
    org.opencontainers.image.licenses="Apache-2.0"
