"""Smoke tests for the native Rust extension."""

from my_project import add, version


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_add_large_numbers():
    assert add(2**32, 1) == 2**32 + 1


def test_version():
    v = version()
    assert isinstance(v, str)
    assert len(v.split(".")) == 3  # semver: major.minor.patch
