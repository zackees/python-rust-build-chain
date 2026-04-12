# python-rust-build-chain

A universal, opinionated build chain template for Python+Rust projects. One template, every platform, maximum caching, zero foot-guns.

[![CI](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml)

## Build Matrix

| | Build | Lint | Test |
|---|---|---|---|
| **Linux x86_64** | [![Build](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) | [![Lint](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) | [![Test](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) |
| **Linux aarch64** | [![Build](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) | [![Lint](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) | [![Test](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) |
| **macOS ARM** | [![Build](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) | [![Lint](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) | [![Test](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) |
| **macOS x86_64** | [![Build](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) | | |
| **Windows x86_64** | [![Build](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) | [![Lint](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) | [![Test](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) |
| **Windows aarch64** | [![Build](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zackees/python-rust-build-chain/actions/workflows/ci.yml) | | |

> macOS x86_64 and Windows aarch64 are cross-compiled; lint and test run only on native targets.

## What This Is

A **GitHub template repository** that provides everything needed to build a Python package backed by Rust, targeting all major platforms with a single CI configuration.

**The opinionated stack:**

| Layer | Tool | Why |
|---|---|---|
| Rust build | [Maturin](https://github.com/PyO3/maturin) | Correct wheel tags, auditwheel compliance, zero hand-rolling |
| Python ABI | [PyO3](https://pyo3.rs/) with `abi3-py310` | One wheel per platform covers all Python 3.10+ |
| Python toolchain | [uv](https://github.com/astral-sh/uv) | Fast venv/dependency management, 5s vs 83s for Python setup on Windows |
| Compilation cache | [zccache](https://github.com/zackees/zccache) | 3-layer caching (~200ms warm vs ~3,200ms sccache), replaces sccache + Swatinem/rust-cache |
| Toolchain safety | `_cargo` trampoline | Forces MSVC on Windows, reads pinned version from `rust-toolchain.toml` |
| Linux cross-compile | [Zig](https://ziglang.org/) via `maturin --zig` | manylinux2014 compliance without Docker |
| Linting | clippy + ruff | Rust + Python in one `./lint` command |

## Project Structure

```
python-rust-build-chain/
├── pyproject.toml              # Maturin backend, abi3-py310, uv config
├── Cargo.toml                  # Workspace root (single version source)
├── Cargo.lock                  # Committed
├── rust-toolchain.toml         # Pinned Rust version
├── .python-version             # Pinned Python for local dev
│
├── src/my_project/             # Python package
│   ├── __init__.py             # Re-exports from _native
│   └── py.typed                # PEP 561 marker
│
├── crates/
│   ├── my-project-core/        # Pure Rust library (all logic here)
│   │   └── src/lib.rs
│   └── my-project-py/          # PyO3 bindings (thin shim)
│       ├── build.rs
│       └── src/lib.rs
│
├── tests/                      # Python tests (pytest)
│
├── _cargo                      # Toolchain trampoline (forces MSVC on Windows)
├── _rustc                      # Toolchain trampoline
├── _rustfmt                    # Toolchain trampoline
├── install                     # Lazy bootstrap (uv + Rust + deps)
├── lint                        # clippy + ruff in one command
│
├── ci/
│   └── env.py                  # Cross-platform build environment resolver
│
└── .github/
    ├── actions/setup/           # Composite: toolchain + 4-layer cache (zccache + uv)
    └── workflows/
        ├── ci.yml               # Matrix CI (6 platforms, 2 files total)
        ├── _build-and-test.yml  # Reusable: build + lint + test
        └── release.yml          # Build all wheels + publish to PyPI
```

## Quick Start

```bash
# Clone and bootstrap
git clone https://github.com/zackees/python-rust-build-chain
cd python-rust-build-chain
./install

# Build the Rust extension into the Python package
uv run maturin develop

# Run tests
uv run pytest

# Lint everything
./lint
```

## Foot Guns This Template Eliminates

| Problem | Where It Bit Us | How We Fix It |
|---|---|---|
| Wrong wheel tags (`py3-none` for native code) | zccache | Maturin generates correct `cp310-abi3` tags |
| `requires-python >= 3.9` with `abi3-py310` | zccache | Template enforces `>=3.10` |
| Hand-rolled METADATA/WHEEL/RECORD | zccache, fbuild | Maturin handles it |
| Version drift across files | fbuild | Single source in `Cargo.toml` workspace |
| 25-30 workflow files | running-process, fastled-wasm | Single matrix workflow (2 files) |
| sccache + rust-cache target overlap | running-process | Replaced both with single zccache action |
| Hidden maturin compilation in `uv sync` | running-process | `--no-install-project` in CI |
| Chocolatey GNU Rust on Windows | fastled-wasm, zccache | `_cargo` trampoline |
| No manylinux audit | zccache, fbuild | `auditwheel show` in CI |
| Windows ARM `python3.lib` naming | fastled-wasm | Documented workaround in CI |
| Toolchain version drift | zccache | Single `rust-toolchain.toml` |

## 4-Layer Caching Strategy

```
Build request
  └─> zccache warm    ─── target/ metadata restored? ──> cargo skips rustc entirely (~200ms)
       │
       NO
       └─> zccache compilation cache ──> cached .o/.rlib per unit (~1ms per hit)
       └─> zccache registry cache ──> cargo registry index + crate downloads
       └─> uv cache ──> cached Python packages
       └─> Full rebuild (rare after first run)
```

- **Layer 1 — zccache compilation**: Per-unit object cache (~1ms per warm hit vs ~170ms for sccache)
- **Layer 2 — zccache registry**: Cargo registry index, crate downloads, git deps
- **Layer 3 — zccache target metadata**: Fingerprints + dep-info; `warm` restores .rlib/.rmeta so cargo skips rustc
- **Layer 4 — uv cache**: Python package cache keyed on `uv.lock`

All three Rust caching layers are handled by a single [`zackees/zccache`](https://github.com/zackees/zccache) action, replacing the old sccache + Swatinem/rust-cache dual setup. PR builds restore caches but skip saving to conserve GHA cache budget.

## Platform Targets

| Target | Runner | Method | Notes |
|---|---|---|---|
| `x86_64-unknown-linux-gnu` | `ubuntu-24.04` | `maturin --zig` | manylinux2014 |
| `aarch64-unknown-linux-gnu` | `ubuntu-24.04-arm` | `maturin --zig` | manylinux2014 |
| `aarch64-apple-darwin` | `macos-15` | native | ARM Mac |
| `x86_64-apple-darwin` | `macos-14` | cross-compile | Intel Mac |
| `x86_64-pc-windows-msvc` | `windows-2025` | native | MSVC forced |
| `aarch64-pc-windows-msvc` | `windows-2025` | cross-compile | PyO3 workaround |

## Derived From

Built from hard-won lessons across these projects:
- [zackees/zccache](https://github.com/zackees/zccache) — Rust compilation cache with PyO3 bindings
- [zackees/running-process](https://github.com/zackees/running-process) — Process management with 6-platform CI
- [zackees/fastled-wasm](https://github.com/zackees/fastled-wasm) — WASM compiler toolchain
- [fastled/fbuild](https://github.com/fastled/fbuild) — Embedded firmware build system

See [Issue #1](https://github.com/zackees/python-rust-build-chain/issues/1) for the full pain log and [Issue #2](https://github.com/zackees/python-rust-build-chain/issues/2) for what worked.

## License

MIT
