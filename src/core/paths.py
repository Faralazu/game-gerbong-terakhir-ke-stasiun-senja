"""Self-contained portable path, environment, and JSON persistence manager.

Ensures that whether running from Python source or a PyInstaller --onedir build,
all saves, logs, settings, and temporary files stay strictly inside the game's
own folder and never leak into Windows %APPDATA% or %TEMP%.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def _resolve_root_dir() -> Path:
    """Resolve the portable game root folder (folder containing .exe or main.py)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


ROOT_DIR: Path = _resolve_root_dir()
ASSETS_DIR: Path = ROOT_DIR / "assets"
USERDATA_DIR: Path = ROOT_DIR / "userdata"
SAVES_DIR: Path = USERDATA_DIR / "saves"
LOGS_DIR: Path = USERDATA_DIR / "logs"
TEMP_DIR: Path = USERDATA_DIR / "temp"
VAULT_DIR: Path = ROOT_DIR / "_asset_vault"
DRAFTS_DIR: Path = VAULT_DIR / "drafts"
UNUSED_ARCHIVE_DIR: Path = VAULT_DIR / "unused_archive"


def configure_portable_env() -> None:
    """Ensure local folders exist and redirect temp/appdata env vars inside ROOT_DIR."""
    for folder in (
        ASSETS_DIR,
        USERDATA_DIR,
        SAVES_DIR,
        LOGS_DIR,
        TEMP_DIR,
    ):
        folder.mkdir(parents=True, exist_ok=True)

    # Keep all third-party libraries (SDL, OpenCV, Pillow, etc.) strictly portable.
    temp_str = str(TEMP_DIR)
    userdata_str = str(USERDATA_DIR)
    os.environ["TEMP"] = temp_str
    os.environ["TMP"] = temp_str
    os.environ["TMPDIR"] = temp_str
    os.environ["APPDATA"] = userdata_str
    os.environ["LOCALAPPDATA"] = userdata_str
    os.environ["XDG_CONFIG_HOME"] = userdata_str
    os.environ["XDG_DATA_HOME"] = userdata_str
    os.environ["XDG_CACHE_HOME"] = temp_str


# Configure immediately on import so subsequent library imports inherit local env vars.
configure_portable_env()


_REQUIRED_MODULES: tuple[str, ...] = ("pygame", "cv2", "numpy", "PIL")


def _current_python_has_deps() -> bool:
    """Return True if the active Python interpreter already has all runtime libraries."""
    return all(importlib.util.find_spec(mod) is not None for mod in _REQUIRED_MODULES)


def _venv_python_is_usable(venv_python: Path) -> bool:
    """Verify that .venv Python exists and works on the current machine."""
    if not venv_python.exists():
        return False
    try:
        probe = subprocess.run(
            [str(venv_python), "-c", "import pygame, cv2, numpy, PIL"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=15,
            check=False,
        )
        return probe.returncode == 0
    except OSError:
        return False


def ensure_local_venv() -> None:
    """Use active Python if ready, or re-exec via valid local .venv Python."""
    if getattr(sys, "frozen", False):
        return
    if _current_python_has_deps():
        return

    venv_dir = ROOT_DIR / ".venv"
    venv_python = venv_dir / "Scripts" / "python.exe"
    if (
        os.environ.get("_TRACK99_VENV_ACTIVE") != "1"
        and Path(sys.prefix).resolve() != venv_dir.resolve()
        and _venv_python_is_usable(venv_python)
    ):
        env = os.environ.copy()
        env["_TRACK99_VENV_ACTIVE"] = "1"
        rc = subprocess.call([str(venv_python), *sys.argv], env=env)
        sys.exit(rc)

    print(
        "\n============================================================\n"
        " Library game (pygame-ce, opencv-python, numpy, pillow)\n"
        " belum terpasang atau .venv berasal dari perangkat lain.\n\n"
        " Cara menginstal (cukup sekali di awal):\n"
        "   1. Klik 2x file: INSTALL_LIBRARIES.bat\n"
        "   2. Atau lewat terminal: pip install -r requirements.txt\n"
        "============================================================\n"
    )
    sys.exit(1)


def asset_path(rel_path: str | Path) -> Path:
    """Return an absolute path inside the local assets/ directory."""
    return ASSETS_DIR / Path(rel_path)


def userdata_path(rel_path: str | Path) -> Path:
    """Return an absolute path inside the local userdata/ directory."""
    target = USERDATA_DIR / Path(rel_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def vault_path(rel_path: str | Path) -> Path:
    """Return an absolute path inside the local _asset_vault/ directory."""
    target = VAULT_DIR / Path(rel_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def read_json(path: Path, default: Any = None) -> Any:
    """Read JSON safely from disk, returning default on missing or invalid data."""
    if not path.exists():
        return {} if default is None else default
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {} if default is None else default


def write_json(path: Path, data: Any) -> Path:
    """Write JSON atomically inside the target path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    tmp_path.replace(path)
    return path


DEFAULT_SETTINGS: dict[str, Any] = {
    "resolution": [1280, 720],
    "fullscreen": False,
    "bgm_volume": 0.75,
    "sfx_volume": 0.85,
    "show_director_hud": False,
    "persona_cutin_fx": True,
    "slow_cozy_sway": True,
}


def load_settings() -> dict[str, Any]:
    """Load portable game settings from userdata/saves/settings.json."""
    settings_file = SAVES_DIR / "settings.json"
    merged = dict(DEFAULT_SETTINGS)
    loaded = read_json(settings_file, default={})
    if isinstance(loaded, dict):
        merged.update(loaded)
    if not settings_file.exists():
        write_json(settings_file, merged)
    return merged


def save_settings(data: dict[str, Any]) -> Path:
    """Persist portable game settings into userdata/saves/settings.json."""
    merged = dict(DEFAULT_SETTINGS)
    merged.update(data)
    return write_json(SAVES_DIR / "settings.json", merged)


def load_save(slot: str = "slot_1") -> dict[str, Any]:
    """Load player progress from userdata/saves/<slot>.json."""
    save_file = SAVES_DIR / f"{slot}.json"
    default_save: dict[str, Any] = {
        "slot": slot,
        "current_scene": "title_screen",
        "resume_scene": "gerbong_5_intro",
        "collected_cassettes": [1],
        "cassette_unlocked": [1],
        "active_cassette": 0,
        "elapsed_total_seconds": 0.0,
        "harmonized_carriages": [],
        "inspected_props": [],
        "completed_minigames": [],
        "seen_cg": [],
        "ticket_stubs": 0,
        "ending_reached": False,
        "notes": {},
    }
    loaded = read_json(save_file, default=None)
    if isinstance(loaded, dict):
        default_save.update(loaded)
        # Keep collected_cassettes and cassette_unlocked synchronized
        c_list = loaded.get("collected_cassettes", loaded.get("cassette_unlocked", [1]))
        normalized = sorted({1, *(int(c) for c in c_list if int(c) in (1, 2, 3, 4))})
        default_save["collected_cassettes"] = normalized
        default_save["cassette_unlocked"] = list(normalized)
    return default_save


def write_save(data: dict[str, Any], slot: str = "slot_1") -> Path:
    """Persist player progress into userdata/saves/<slot>.json."""
    return write_json(SAVES_DIR / f"{slot}.json", data)
