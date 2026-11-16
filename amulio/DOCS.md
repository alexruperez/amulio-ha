# aMulio Home Assistant app

## Install

1. In Home Assistant OS, open **Settings → Apps → Install app**.
2. Open the menu, select **Repositories**, and add `https://github.com/alexruperez/amulio-ha`.
3. Select **aMulio**, install it, then open **Configuration**.
4. Set `public_url` to the LAN or HTTPS URL that the Stremio client can actually reach. Do **not** use the Home Assistant Ingress URL.
5. Save, start the app, and open the app through Ingress to copy the private Stremio manifest URL.

## Options

- **Public URL**: the reachable origin used in manifest and playback URLs. For LAN usage it can be the HAOS host and enabled port `8000`; for remote use it must be your HTTPS reverse-proxy or tunnel origin.
- **aMule peer TCP / Kad UDP ports**: the listener ports used inside aMule. Enable their matching app network mappings only if you deliberately allow inbound peer traffic.
- **Preferred languages**: comma-separated metadata languages.
- **Allow season packs**: lets searches return TV season packs.

## Storage and backups

All runtime data is app-owned under `/data`:

- `/data/config`: aMule configuration;
- `/data/amulio`: aMulio database and state;
- `/data/incoming`: completed media;
- `/data/temp`: incomplete downloads;
- `/data/secrets`: locally generated signing and control secrets.

Hot backups exclude incomplete downloads and logs. They do include completed media by default, so account for that capacity or manage media exports separately before relying on HA backups.

## Network and security

Ingress is only the administrative UI. Stremio must reach `public_url` independently, because it does not have an authenticated Ingress session. EC and amuleapi bind to loopback inside the container and are never host-published.

Peer ports are disabled by default. Without them, aMule can run with Low ID/firewalled Kad and reduced reachability. This app never moves downloads to another aMulio node or a central VPS.

The app requests no Home Assistant API, Supervisor API, Docker socket, host network, host PID namespace, hardware access, or additional capabilities.

## Limitations

The app is experimental. The initial image is published for `amd64` and `aarch64`; test it with legal content only. Report defects at [GitHub Issues](https://github.com/alexruperez/amulio-ha/issues).

## License

Apache-2.0. The underlying application is [aMulio](https://github.com/alexruperez/amulio).
