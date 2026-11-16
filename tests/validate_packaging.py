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
    assert config["image"] == "ghcr.io/alexruperez/amulio-ha"
    assert all(port is None for port in config["ports"].values())
    assert config["options"]["public_url"].startswith("http")
    assert not {"docker_api", "homeassistant_api", "hassio_api", "host_network", "host_pid"} & config.keys()

    runner = RUNNER.read_text()
    assert "AMULE_API_BASE_URL=http://127.0.0.1:4713/api/v0" in runner
    assert "AMULE_API_ADMIN_PASSWORD_FILE=$SECRET_DIR/amuleapi_admin_password" in runner
    assert "--bind=127.0.0.1" in runner
    assert "AMULIO_ALLOWED_MEDIA_ROOTS=/data/incoming" in runner
    assert "AMULIO_ALLOWED_MEDIA_ROOTS=/data/temp" not in runner

    service = SERVICE.read_text()
    assert service.startswith("#!/usr/bin/with-contenv bashio")
    assert "exec /usr/local/bin/amulio-ha-run" in service

    dockerfile = DOCKERFILE.read_text()
    assert "ARG BUILD_FROM=ghcr.io/home-assistant/base:3.24" in dockerfile
    assert "FROM ${BUILD_FROM}" in dockerfile
    assert "COPY rootfs /" in dockerfile
    assert "-DCRYPTOPP_INCLUDE_PREFIX=cryptopp" in dockerfile
    assert "-DCRYPTOPP_INCLUDE_PREFIX=crypto++" not in dockerfile
    assert "org.opencontainers.image.title=\"Home Assistant App: aMulio\"" in dockerfile
    assert "ENTRYPOINT" not in dockerfile
    assert "HEALTHCHECK" in dockerfile

    for name in ("DOCS.md", "CHANGELOG.md", "translations/en.yaml", "translations/es.yaml"):
        assert (APP / name).is_file(), name
    print("HAOS app packaging contract: valid")


if __name__ == "__main__":
    main()
