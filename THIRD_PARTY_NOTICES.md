# Third-party licenses

The MIT license in [LICENSE](LICENSE) applies to original va-sid code by Zsolt Tarczali.
It does not relicense third-party code or derived code with their own license terms.

- `vendor/resid-rs`: reSID by Dag Lem, Rust port by Sebastian Jastrzebski;
  GPL-3.0-or-later. See its [license](vendor/resid-rs/LICENSE) and `VENDORED.md` (one fix).
- `src/mos6510.rs` and `src/c64/`: include ports of VICE code, copyright the VICE Team,
  GPL-2.0-or-later. Their existing copyright and license notices remain in force.
- `src/sid_core.rs` and `vendor/sid-wave-tables`: include code and data derived from
  Dag Lem's `mos6581_8580` implementation, GPL-2.0-or-later, as identified in the source.

Distributions combining the MIT code with these GPL components must also comply with the
applicable GPL terms; the crate as a whole is not available solely under MIT.
