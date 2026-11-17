from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "amulio"
CONFIG = APP / "config.yaml"
RUNNER = APP / "rootfs" / "usr" / "local" / "bin" / "amulio-ha-run"
SERVICE = APP / "rootfs" / "etc" / "services.d" / "amulio" / "run"
DOCKERFILE = APP / "Dockerfile"


def main() -> None:
    config = yaml.safe_load(CONFIG.read_text())
    required = {"name", "version", "slug", "description", "image", "arch", "options", "schema"}
    assert required <= config.keys()
    assert config["slug"] == APP.name
    assert config["arch"] == ["aarch64", "amd64"]
    assert config["homeassistant"] >= "2026.2.0"
    assert config["init"] is False
    assert config["ingress"] is True
    assert config["ingress_port"] == 8000
    assert "webui" not in config
    assert config["image"] == "ghcr.io/alexruperez/amulio-ha"
    assert all(port is None for port in config["ports"].values())
    assert config["options"]["public_url"].startswith("http")
    assert config["options"]["max_file_size_gb"] == 0
    assert config["options"]["inbound_peer_ports_enabled"] is False
    assert set(config["options"]) == set(config["schema"])
    assert not {"docker_api", "homeassistant_api", "hassio_api", "host_network", "host_pid"} & config.keys()

    runner = RUNNER.read_text()
    assert "AMULE_API_BASE_URL=http://127.0.0.1:4713/api/v0" in runner
    assert "AMULE_API_ADMIN_PASSWORD_FILE=$SECRET_DIR/amuleapi_admin_password" in runner
    assert "ensure_secret manager_admin_password" in runner
    assert "ensure_secret manager_bootstrap_token" in runner
    assert "AMULIO_ADMIN_PASSWORD_FILE=$SECRET_DIR/manager_admin_password" in runner
    assert "AMULIO_ADMIN_BOOTSTRAP_TOKEN_FILE=$SECRET_DIR/manager_bootstrap_token" in runner
    assert 'chmod 600 "$path"' in runner
    assert "--bind=127.0.0.1" in runner
    assert "AMULIO_ALLOWED_MEDIA_ROOTS=/data/incoming" in runner
    assert "AMULIO_INBOUND_PEER_PORTS_ENABLED=$INBOUND_PEER_PORTS_ENABLED" in runner
    assert "AMULIO_DEFAULT_RESULT_LIMIT=$MAX_RESULTS" in runner
    assert "AMULIO_DEFAULT_MAX_SIZE_GB=$MAX_FILE_SIZE_GB" in runner
    assert "AMULIO_ALLOWED_MEDIA_ROOTS=/data/temp" not in runner
    assert "trap 'on_error $LINENO' ERR" in runner
    assert "starting runtime bootstrap" in runner
    assert 'export HOME="$AMULE_HOME"' in runner
    assert 'export XDG_CONFIG_HOME="$AMULE_HOME/.config"' in runner
    assert "waiting for aMule EC on 127.0.0.1:4712" in runner
    assert "starting aMulio HTTP API on 0.0.0.0:8000" in runner
    assert 'jq -er "$1" "$OPTIONS_FILE"' not in runner
    assert 'value=$(jq -r "$1" "$OPTIONS_FILE")' in runner
    assert '>/dev/null 2>&1 || true' not in runner.split('if [[ ! -f "$CONFIG_DIR/amule.conf" ]]', 1)[1].split('EC_PASSWORD_MD5=', 1)[0]

    service = SERVICE.read_text()
    assert service.startswith("#!/usr/bin/with-contenv bashio")
    assert "exec /usr/local/bin/amulio-ha-run" in service

    dockerfile = DOCKERFILE.read_text()
    assert "ARG BUILD_FROM=ghcr.io/home-assistant/base:3.24" in dockerfile
    assert "FROM ${BUILD_FROM}" in dockerfile
    assert "COPY rootfs /" in dockerfile
    assert "ARG AMULIO_REF=b7e7f7394c37635e8f98569a2a2a9cf0fea1e0e4" in dockerfile
    assert "-DCRYPTOPP_INCLUDE_PREFIX=cryptopp" in dockerfile
    assert "-DCRYPTOPP_INCLUDE_PREFIX=crypto++" not in dockerfile
    assert "libpcre2-32" in dockerfile
    assert "org.opencontainers.image.title=\"Home Assistant App: aMulio\"" in dockerfile
    assert "ENTRYPOINT" not in dockerfile
    assert "HEALTHCHECK" in dockerfile

    for name in ("DOCS.md", "CHANGELOG.md", "translations/en.yaml", "translations/es.yaml"):
        assert (APP / name).is_file(), name
    assert (APP / "icon.png").is_file()
    assert (APP / "logo.png").is_file()
    assert (ROOT / "THIRD_PARTY_NOTICES.md").is_file()
    assert (ROOT / "THIRD_PARTY_LICENSES_amule_GPL-2.0-or-later.md").is_file()
    print("HAOS app packaging contract: valid")


if __name__ == "__main__":
    main()
