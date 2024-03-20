import re


def test_package_version() -> None:
    from shushu import __version__

    assert re.match(r"\d+\.\d+\.\d+", __version__)
