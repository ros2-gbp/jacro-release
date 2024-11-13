"""Test jacro functionalities."""

import os
from pathlib import Path

import pytest
from ament_index_python.packages import PackageNotFoundError

import jacro
from jacro.template_processor import load_mappings


def test_text():
    """Test process_text function."""
    assert (
        jacro.process_text("Hello, {{ name }}!", {"name": "world"}) == "Hello, world!"
    )


def test_file():
    """Test process_text."""
    assert (
        jacro.process_file("tests/hello.txt", {"names": ["r1", "r2", "r3"]})
        == """1. Hello r1!
2. Hello r2!
3. Hello r3!
"""
    )

    output_filename = jacro.process_file(
        "tests/hello.txt",
        {"names": ["r1", "r2", "r3"]},
        save=True,
    )
    with Path(output_filename).open() as f:
        assert (
            f.read()
            == """1. Hello r1!
2. Hello r2!
3. Hello r3!
"""
        )


def test_load_mappings():
    """Test load_mappings function."""
    assert load_mappings(["arg:='100'"]) == {"arg": "100"}
    assert load_mappings(["arg:=asd"]) == {"arg": "asd"}
    assert load_mappings(["arg:=1", "arg2:='asd'"]) == {"arg": 1, "arg2": "asd"}
    assert load_mappings(["arg:=1", "arg2:=['a1', 'a2', 'a3']"]) == {
        "arg": 1,
        "arg2": ["a1", "a2", "a3"],
    }
    assert load_mappings(["arg2:=[1, 2, 3]"]) == {
        "arg2": [1, 2, 3],
    }
    assert load_mappings(["arg2:=[a1, a2, a3]"]) == {
        "arg2": ["a1", "a2", "a3"],
    }


def test_ament_prefix_path_not_set(monkeypatch):
    """Test ros_pkg_path function with AMENT_PREFIX_PATH not set."""
    monkeypatch.delenv("AMENT_PREFIX_PATH", raising=False)
    with pytest.raises(EnvironmentError):  # noqa: PT011
        jacro.process_text("{{ ros_pkg_path('std_msgs') }}")


def test_empty_ament_prefix_path(monkeypatch):
    """Test ros_pkg_path function with empty AMENT_PREFIX_PATH."""
    monkeypatch.setenv("AMENT_PREFIX_PATH", "")
    with pytest.raises(EnvironmentError):  # noqa: PT011
        jacro.process_text("{{ ros_pkg_path('std_msgs') }}")


def test_non_existing_pkg(monkeypatch):
    """Test ros_pkg_path function with empty AMENT_PREFIX_PATH."""
    with pytest.raises(PackageNotFoundError):
        jacro.process_text("{{ ros_pkg_path('non_existing_package') }}")


def test_ros_pkg_path():
    """Test substituting ament packages."""
    assert (
        jacro.process_text("{{ ros_pkg_path('std_msgs') }}")
        == f"/opt/ros/{os.environ['ROS_DISTRO']}/share/std_msgs"
    )
