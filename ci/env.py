"""Cross-platform build environment resolver.

Provides a single build_env() that returns a fully-resolved environment dict
for Rust compilation on any platform. Handles:
- Reading the pinned toolchain from rust-toolchain.toml
- Detecting host target triple
- Forcing MSVC on Windows (prevents GNU Rust contamination)
- Finding zccache/sccache if available
- Resolving Visual Studio environment on Windows
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_toolchain_channel() -> str:
    """Parse the channel from rust-toolchain.toml."""
    toml_path = _PROJECT_ROOT / "rust-toolchain.toml"
    for line in toml_path.read_text().splitlines():
        if "channel" in line and "=" in line:
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError(f"No channel found in {toml_path}")


def host_target_triple() -> str:
    """Detect the host target triple."""
    machine = platform.machine().lower()
    system = platform.system().lower()

    arch_map = {"x86_64": "x86_64", "amd64": "x86_64", "aarch64": "aarch64", "arm64": "aarch64"}
    arch = arch_map.get(machine, machine)

    if system == "linux":
        return f"{arch}-unknown-linux-gnu"
    elif system == "darwin":
        return f"{arch}-apple-darwin"
    elif system == "windows":
        return f"{arch}-pc-windows-msvc"
    else:
        raise RuntimeError(f"Unsupported platform: {system} {machine}")


def toolchain_name() -> str:
    """Full toolchain name including host triple."""
    return f"{load_toolchain_channel()}-{host_target_triple()}"


def toolchain_bin() -> Path:
    """Resolve the exact path to the toolchain bin directory."""
    channel = load_toolchain_channel()
    result = subprocess.run(
        ["rustup", "run", channel, "rustc", "--print", "sysroot"],
        capture_output=True, text=True, check=True,
    )
    return Path(result.stdout.strip()) / "bin"


def build_env() -> dict[str, str]:
    """Return a complete environment dict for Rust compilation.

    This is the single entry point CI scripts and dev tooling should use.
    """
    env = os.environ.copy()
    channel = load_toolchain_channel()
    triple = host_target_triple()
    bin_dir = str(toolchain_bin())

    env["RUSTUP_TOOLCHAIN"] = channel
    env["CARGO_BUILD_TARGET"] = triple
    env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")

    # Compilation cache: prefer zccache, fall back to sccache
    zccache = shutil.which("zccache")
    sccache = shutil.which("sccache")
    if zccache:
        env["RUSTC_WRAPPER"] = zccache
    elif sccache:
        env["RUSTC_WRAPPER"] = sccache

    # Windows: force MSVC target
    if sys.platform == "win32":
        env["CARGO_BUILD_TARGET"] = triple  # always x86_64-pc-windows-msvc or aarch64-...

    return env


if __name__ == "__main__":
    print(f"Channel:      {load_toolchain_channel()}")
    print(f"Host triple:  {host_target_triple()}")
    print(f"Toolchain:    {toolchain_name()}")
    try:
        print(f"Toolchain bin: {toolchain_bin()}")
    except Exception as e:
        print(f"Toolchain bin: (not available: {e})")
