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
