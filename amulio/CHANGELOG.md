## 0.1.13

- Trust the actual container default gateway used by Home Assistant Ingress, discovered at runtime from `/proc/net/route`, in addition to the resolved Supervisor service address.
- Keep the trusted-proxy allowlist narrow and runtime-derived; do not assume a static Home Assistant network address.

## 0.1.12

- Use Home Assistant Ingress SSO for the download manager only after resolving the runtime Supervisor address and configuring it as a trusted proxy source.
- Do not generate or expose manager credentials when Supervisor resolution succeeds; retain the file-only generic recovery flow only if resolution fails.
- Pin the image build to the exact core SSO commit.

## 0.1.11

- Generate file-only admin-manager credentials and a fragment-only bootstrap link for the Home Assistant Ingress configuration page.
- Pin the image build to the aMulio admin bootstrap session support.

## 0.1.10

- Update aMulio to support Stremio's `HEAD` playback probes without queuing an incomplete download.

## 0.1.9

- Add Supervisor options for global Stremio manifest limits and stream display preferences.
- Add an explicit inbound-peer setting; enable it only after mapping both optional eD2K and Kad ports in Home Assistant.
- Clarify that opening Stremio is a platform-dependent deep link and mobile clients require an HTTPS public URL.

## 0.1.8

- Update the pinned aMulio core revision to keep configuration assets inside the Home Assistant Ingress prefix.
- Show the expected limited inbound peer reachability when optional peer ports are not exposed, including Low ID and firewalled Kad guidance.
- Hide optional profile management when it has not been explicitly enabled.

## 0.1.7

- Update the pinned aMulio core revision to preserve the Home Assistant Ingress prefix when opening the configuration interface.

## 0.1.6

- Replace the temporary original aMulio artwork with the official unmodified aMule application icon, with GPL-2.0-or-later attribution and license notice.

## 0.1.5

- Add original aMulio icon and logo assets for the Home Assistant app store and app page.

## 0.1.4

- Include Alpine's `libpcre2-32` runtime dependency required by the wxWidgets build used by aMule.

## 0.1.3

- Set a writable aMule home directory before first-run configuration creation and include the bounded bootstrap log when that creation fails.

## 0.1.2

- Accept boolean `false` app options during bootstrap; Home Assistant serializes disabled options as JSON `false`, which must not be treated as a missing value.

## 0.1.1

- Make runtime bootstrap failures visible in app logs and fail explicitly when aMule configuration cannot be generated.
- Add start-phase diagnostics for aMule EC, loopback-only amuleapi, and the aMulio HTTP API.

## 0.1.0

- First experimental Home Assistant OS app release.
- Runs `amuled`, `amuleapi` and aMulio as one S6-supervised app with persistent node-local storage.
- Publishes signed multi-architecture images for `amd64` and `aarch64`.
