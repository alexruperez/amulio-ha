## 0.1.2

- Accept boolean `false` app options during bootstrap; Home Assistant serializes disabled options as JSON `false`, which must not be treated as a missing value.

## 0.1.1

- Make runtime bootstrap failures visible in app logs and fail explicitly when aMule configuration cannot be generated.
- Add start-phase diagnostics for aMule EC, loopback-only amuleapi, and the aMulio HTTP API.

## 0.1.0

- First experimental Home Assistant OS app release.
- Runs `amuled`, `amuleapi` and aMulio as one S6-supervised app with persistent node-local storage.
- Publishes signed multi-architecture images for `amd64` and `aarch64`.
