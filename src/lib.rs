//! C64 SID emulation shared by C64 Visual Assembler and VA SID Studio.
//!
//! - [`sid_core`]: VA SID Core, the Rust SID synthesizer (6581 / 8580)
//! - [`sid_chip`]: one SID chip on VA SID Core or reSID ([`resid`], vendored)
//! - [`mos6510`], [`c64`]: cycle-exact 6510, CIA and VIC-II timing (VICE ports)
//! - [`sid_file`]: a C64 running a .sid (PSID / RSID) tune
//! - [`session`]: the editor preview and .sid playback sessions behind the apps' Tauri commands

pub mod c64;
pub mod mos6510;
pub mod session;
pub mod sid_chip;
pub mod sid_core;
pub mod sid_file;
