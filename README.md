# aMulio Home Assistant app

[![Open your Home Assistant instance and add the aMulio app repository](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Falexruperez%2Famulio-ha)

This repository packages [aMulio](https://github.com/alexruperez/amulio) as a Home Assistant OS app. The portable aMulio application and its Docker reference deployment live in the [main aMulio repository](https://github.com/alexruperez/amulio).

## Product contract

Each aMulio installation is an independent node:

- install it on Home Assistant OS, a home server, or a VPS;
- media, queue, aMule configuration and database remain on that node;
- the node provides a private, tokenised Stremio addon URL;
- add that URL in Stremio to send searches and downloads to that node;
- completed files are served back from that node with HTTP range support.

This repository is the HAOS packaging track. The portable application and Docker Compose reference deployment remain in the [`amulio`](https://github.com/alexruperez/amulio) repository.

## Design boundaries

- aMule EC and amuleapi remain private within the app.
- Home Assistant Ingress is for administration only; it is not the Stremio manifest/playback URL.
- Default downloads live in the app's persistent `/data` storage. An optional finished-media mapping may target HA `/media` or `/share`; temporary data is never offered for playback.
- Public Stremio use requires a user-configured reachable HTTPS origin. LAN-only use stays supported.
- Peer-port exposure is opt-in. With no inbound ports, aMule can operate with reduced P2P connectivity; this does not redirect downloads to any other host.

## Status

Pre-alpha packaging track. The first deliverable is a least-privileged multi-architecture app image that supervises `amuled`, `amuleapi`, and aMulio with persistent HAOS storage.

## References

- [aMulio source and Docker deployment](https://github.com/alexruperez/amulio)
- [aMulio portable self-hosted addon plan](https://github.com/alexruperez/amulio/blob/main/docs/DEVELOPMENT_PLAN.md)
- [Home Assistant app configuration](https://developers.home-assistant.io/docs/apps/configuration/)
