# va-sid

<p align="center">
  <img src="assets/logo.png" alt="va-sid logo" width="256">
</p>

<!-- badges:start -->
<p align="center">
  <a href="https://github.com/zstarczali/VA-SID/blob/main/Cargo.toml"><img src="https://img.shields.io/badge/version-1.0.0-4c1" alt="Version"></a>
  <a href="https://github.com/zstarczali/VA-SID/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-GPL--3.0--or--later-blue" alt="License: GPL-3.0-or-later"></a>
  <a href="https://www.rust-lang.org/"><img src="https://img.shields.io/badge/Rust-2021-B7410E?logo=rust&logoColor=white" alt="Rust 2021"></a>
  <a href="https://github.com/binaryfields/resid-rs"><img src="https://img.shields.io/badge/SID-reSID%20%7C%20VA%20SID%20Core-6c5eb5" alt="SID engines"></a>
  <a href="https://vice-emu.sourceforge.io/"><img src="https://img.shields.io/badge/C64-6510%20%7C%20CIA%20%7C%20VIC--II-555" alt="C64 chips"></a>
  <a href="https://www.c64va.pro/register/donate.php"><img src="https://img.shields.io/badge/donate-PayPal-00457C?logo=paypal&logoColor=white" alt="Donate"></a>
</p>
<p align="center">
  <a href="https://github.com/zstarczali/VA-SID/commits/main"><img src="https://img.shields.io/github/last-commit/zstarczali/VA-SID/main" alt="Last commit"></a>
  <a href="https://github.com/zstarczali/VA-SID/graphs/commit-activity"><img src="https://img.shields.io/github/commit-activity/m/zstarczali/VA-SID" alt="Commit activity"></a>
  <a href="https://github.com/zstarczali/VA-SID/issues"><img src="https://img.shields.io/github/issues/zstarczali/VA-SID" alt="Issues"></a>
  <a href="https://github.com/zstarczali/VA-SID/stargazers"><img src="https://img.shields.io/github/stars/zstarczali/VA-SID?style=flat" alt="Stars"></a>
</p>
<p align="center">
  <a href="https://www.c64va.pro/"><img src="https://img.shields.io/badge/used%20by-C64%20Visual%20Assembler-8a2be2" alt="C64 Visual Assembler"></a>
  <a href="https://github.com/zstarczali/SID-Studio"><img src="https://img.shields.io/badge/used%20by-VA%20SID%20Studio-8a2be2" alt="VA SID Studio"></a>
</p>
<!-- badges:end -->

<p align="center">
  <img src="assets/banner.png" alt="VA-SID: C64 SID emulation in Rust">
</p>

The Commodore 64 SID emulation shared by [C64 Visual Assembler](https://www.c64va.pro/) and
[VA SID Studio](https://github.com/zstarczali/SID-Studio).

| Module | Contents |
|--------|----------|
| `sid_core` | VA SID Core: the Rust SID synthesizer, 6581 and 8580 (with the 8580 digi boost) |
| `sid_chip` | One SID chip on VA SID Core or reSID (`SidEngine`, `SidChip`) |
| `mos6510`, `c64` | Cycle-exact 6510, CIA 6526 / 6526A, VIC-II timing and the CPU port (VICE ports) |
| `sid_file` | A C64 running a .sid (PSID / RSID) tune: playback, seeking, register dump, 2SID / 3SID |
| `session` | The SID Editor preview renderer and the .sid playback sessions behind the apps' Tauri commands |

The crate does not depend on Tauri. The apps wrap the `session` functions in their own commands
(`render_sid_preview`, `release_sid_preview`, `render_sid_file`, `sid_file_info`, `sid_register_dump`,
`release_sid_file`) and run the blocking ones on `spawn_blocking`.

## Use

```toml
va-sid = { git = "https://github.com/zstarczali/VA-SID.git", rev = "<sha>" }
```

For local work on the crate and an app at the same time, in the app's `src-tauri/Cargo.toml`
(not to be committed):

```toml
[patch."https://github.com/zstarczali/VA-SID.git"]
va-sid = { path = "../../VA-SID" }
```

## Tests

```
cargo test
```

The ignored tests are manual checks on real tunes (`SID_SMOKE_DIR`, `SID_DUMP_IN` / `SID_DUMP_OUT`).
`samples/` holds the two tunes the tests play. `scripts/sid-reference` is the diagnostic comparison
of VA SID Core with VICE's mos6581_8580 (it predates the cycle-clocked core API and needs updating).

## Logo

`assets/logo.svg` is the source; `python assets/make_logo.py` renders `logo.png` and `banner.png`
(Pillow + Microsoft Edge). The banner uses the C64 Pro Mono font by Style.

## License

GPL-3.0-or-later (see [LICENSE](LICENSE)). It contains reSID by Dag Lem, Rust port by Sebastian
Jastrzebski (`vendor/resid-rs`, GPL-3.0-or-later, with one fix, see its `VENDORED.md`); ports of
VICE code in `src/mos6510.rs` and `src/c64/` (copyright the VICE Team, GPL-2.0-or-later); and in
`src/sid_core.rs` and `vendor/sid-wave-tables` code and data derived from Dag Lem's `mos6581_8580`
(GPL-2.0-or-later), as identified in the source.
