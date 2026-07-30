"""Tests for the Kconfig helpers (chip fragment + menuconfig launcher)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from stmtool.kconfig import chip_kconfig_fragment, run_menuconfig
from stmtool.project import chip_family


def test_chip_family_derives_from_name() -> None:
    assert chip_family("STM32F407VG") == "stm32f4"
    assert chip_family("STM32G070RB") == "stm32g0"


def test_chip_kconfig_fragment_contents() -> None:
    fragment = chip_kconfig_fragment("STM32F407VG")
    assert "config STM32_FAMILY_STM32F4" in fragment
    assert "def_bool y" in fragment
    assert 'default "STM32F407VG"' in fragment


def test_run_menuconfig_prepares_env_and_fragment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sdk_root = tmp_path / "sdk-root"
    (sdk_root / "sdk").mkdir(parents=True)
    (sdk_root / "sdk" / "Kconfig").write_text('mainmenu "t"\n')
    project = tmp_path / "proj"
    project.mkdir()

    captured: dict[str, Any] = {}

    def fake_run(cmd: list[str], **kwargs: Any) -> Any:
        captured["cmd"] = cmd
        captured["env"] = kwargs["env"]

        class _Result:
            returncode = 0

        return _Result()

    monkeypatch.setattr("stmtool.kconfig.subprocess.run", fake_run)

    rc = run_menuconfig(sdk_root, "STM32F407VG", project)

    assert rc == 0
    assert captured["cmd"][1:3] == ["-m", "menuconfig"]
    assert captured["env"]["srctree"] == str(sdk_root / "sdk")
    assert captured["env"]["KCONFIG_CONFIG"] == str(project / ".config")
    fragment = Path(captured["env"]["STM32_KCONFIG_CHIP_FRAGMENT"])
    assert fragment.is_file()
    assert "STM32_FAMILY_STM32F4" in fragment.read_text()
