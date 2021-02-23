# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [git] - 2021-02-22
### Added
- Add package installer variables from `goxel.sh` and `policy-daily.sh`
  (same as from `policy-hourly.sh`) to `api.rc`.

### Changed
- Rename `p3tk` to `P3TK_PKG`.
- Rename `INSTALL_CMD` to `INSTALL_BIN` and `install_bin` to
  `INSTALL_CMD` for clarity so that `INSTALL_CMD` includes options,
  but `INSTALL_BIN` is just the binary name.
- Make `goxel.sh` use `api.rc`.
- Move scripts out of distro-specific directories. Make more scripts
  cross-distro compatible.

### Fixed
- Make policy-daily.sh and policy-hourly.sh installer commands match.
  - `policy-hourly.sh` did not have the refresh command.
- Use the correct path for install_any.py in the web installer (and move
  the code for that to the new `setup.sh`)
- Change `apt-add-repositoty` to `apt-add-repository` in "everyone/wine-2016-04-12.deb.sh"
