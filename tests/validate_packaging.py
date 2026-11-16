from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "amulio" / "config.yaml"
RUNNER = ROOT / "amulio" / "rootfs" / "usr" / "local" / "bin" / "amulio-ha-run"
DOCKERFILE = ROOT / "amulio" / "Dockerfile"


def main() -> None:
    config = yaml.safe_load(CONFIG.read_text())
    required = {"name", "version", "slug", "description", "arch", "options", "schema"}
    assert required <= config.keys()
    assert config["slug"] == "amulio"
    assert config["arch"] == ["amd64", "aarch64"]
    assert config["ingress"] is True
    assert config["ingress_port"] == 8000
    assert config["ports"]["8000/tcp"] is None
    assert config["ports"]["4662/tcp"] is None
    assert config["ports"]["4672/udp"] is None
    assert config["options"]["public_url"].startswith("http")
    assert config["map"] == [{"type": "data", "path": "/data"}]
    assert config.get("docker_api") is None
    assert config.get("homeassistant_api") is None
    assert config.get("hassio_api") is None

    runner = RUNNER.read_text()
    assert "AMULE_API_BASE_URL=http://127.0.0.1:4713/api/v0" in runner
    assert "AMULE_API_ADMIN_PASSWORD_FILE=$SECRET_DIR/amuleapi_admin_password" in runner
    assert "--bind=127.0.0.1" in runner
    assert "/data/temp" not in runner.split("AMULIO_ALLOWED_MEDIA_ROOTS=", 1)[1].splitlines()[0]

    dockerfile = DOCKERFILE.read_text()
    assert "ARG AMULIO_REF=088334409a4c3aeb7973411b07450c3250058f15" in dockerfile
    assert "COPY --from=amule-builder /opt/amule /opt/amule" in dockerfile
    print("HAOS packaging contract: valid")


if __name__ == "__main__":
    main()
