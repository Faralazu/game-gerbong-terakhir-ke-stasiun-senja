"""Portable Asset Auditor & Self-Contained EXE/ZIP Builder.

Commands:
  python tools/build_portable.py --audit
  python tools/build_portable.py --archive-unused
  python tools/build_portable.py --build
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.core import paths  # noqa: E402

paths.ensure_local_venv()

from src.core.asset_manager import AssetManager  # noqa: E402

APP_NAME = "GerbongTerakhir_StasiunSenja"


def run_audit(archive_unused: bool = False) -> int:
    am = AssetManager()
    report = am.scan_unused_assets(include_manifest=True)
    manifest = paths.read_json(paths.LOGS_DIR / "used_assets_manifest.json", default={})
    missing = manifest.get("missing_fallback_assets", [])

    print("=== AUDIT ASSET PORTABEL ===")
    print(f"Total file di assets/         : {len(report['disk_files'])}")
    print(f"Asset aktif terpakai          : {len(report['active_used'])}")
    for item in report["active_used"]:
        print(f"  [USED]    assets/{item}")

    print(f"Asset tidak terpakai di disk  : {len(report['unused_on_disk'])}")
    for item in report["unused_on_disk"]:
        print(f"  [UNUSED]  assets/{item}")

    print(f"Asset masih mode Draft/Fallback: {len(missing)}")
    for item in missing:
        print(f"  [DRAFT]   assets/{item}")

    if archive_unused and report["unused_on_disk"]:
        moved = am.archive_unused_assets()
        print(f"\nDipindahkan ke _asset_vault/unused_archive/: {len(moved)} file.")
    return 0


def build_portable_zip(include_all_assets: bool = False) -> int:
    dist_dir = ROOT_DIR / "dist"
    target_dir = dist_dir / APP_NAME
    work_dir = ROOT_DIR / ".build_tmp"
    zip_base = dist_dir / APP_NAME

    if target_dir.exists():
        shutil.rmtree(target_dir)
    if work_dir.exists():
        shutil.rmtree(work_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onedir",
        "--noconsole",
        "--name",
        APP_NAME,
        "--contents-directory",
        "_engine",
        "--paths",
        str(ROOT_DIR),
        "--collect-submodules",
        "src",
        "--hidden-import",
        "src.scenes.title_screen",
        "--hidden-import",
        "src.scenes.gerbong_5_intro",
        "--hidden-import",
        "src.scenes.carriage_story_scene",
        "--hidden-import",
        "src.scenes.placeholder_scene",
        "--distpath",
        str(dist_dir),
        "--workpath",
        str(work_dir),
        "--specpath",
        str(work_dir),
        str(ROOT_DIR / "main.py"),
    ]
    print("Menjalankan PyInstaller (--onedir portable mode)...")
    res = subprocess.run(cmd, cwd=str(ROOT_DIR), check=False)
    if res.returncode != 0:
        print("PyInstaller gagal! Kode keluar:", res.returncode)
        return res.returncode

    # Copy only active used assets (or all assets if requested / manifest empty)
    manifest = paths.read_json(paths.LOGS_DIR / "used_assets_manifest.json", default={})
    used_set = set(manifest.get("used_assets", []))
    dst_assets = target_dir / "assets"
    dst_assets.mkdir(parents=True, exist_ok=True)

    copied_count = 0
    for src_file in paths.ASSETS_DIR.rglob("*"):
        if not src_file.is_file():
            continue
        rel = src_file.relative_to(paths.ASSETS_DIR).as_posix()
        if not include_all_assets and used_set and rel not in used_set:
            continue
        out_file = dst_assets / rel
        out_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, out_file)
        copied_count += 1

    # Fresh self-contained userdata folders (never leaking outside this folder)
    for sub in ("saves", "logs", "temp"):
        (target_dir / "userdata" / sub).mkdir(parents=True, exist_ok=True)

    readme_txt = (
        "GERBONG TERAKHIR KE STASIUN SENJA (Track 99: Resonance)\n"
        "======================================================\n"
        "Game ini 100% PORTABEL:\n"
        "1. Ekstrak seluruh isi ZIP ke folder mana saja.\n"
        "2. Jalankan GerbongTerakhir_StasiunSenja.exe.\n"
        "3. Semua save game (10 slot), galeri CG, settings, dan log tersimpan di ./userdata/.\n\n"
        "Kontrol:\n"
        "- A / D, Panah, atau Klik Lantai : Berjalan\n"
        "- E atau Klik Benda / Penumpang  : Interaksi, Duduk/Berdiri, atau Pindah Gerbong\n"
        "- SPACE / Klik                   : Lanjut Dialog / Putar Walkman\n"
        "- 1..4 atau TAB / Klik Walkman   : Pilih Kaset Emosi\n"
        "- T                              : Buka Mini-game / Waveform Tuner\n"
        "- ESC atau Klik [Menu]           : Pause Menu (Simpan / Muat 10 Slot & Galeri)\n"
    )
    (target_dir / "CARA_MAIN.txt").write_text(readme_txt, encoding="utf-8")

    zip_path = shutil.make_archive(str(zip_base), "zip", root_dir=str(dist_dir), base_dir=APP_NAME)
    shutil.rmtree(work_dir, ignore_errors=True)

    print(f"\nBuild portabel selesai! ({copied_count} file asset aktif dibundel)")
    print(f"Folder EXE : {target_dir}")
    print(f"File ZIP   : {zip_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Portable build & asset audit tool")
    parser.add_argument("--audit", action="store_true", help="Audit active vs unused assets.")
    parser.add_argument("--archive-unused", action="store_true", help="Move unused assets to _asset_vault/unused_archive/.")
    parser.add_argument("--build", action="store_true", help="Build portable --onedir EXE and ZIP.")
    parser.add_argument("--include-all-assets", action="store_true", help="Include all assets instead of only active used assets.")
    args = parser.parse_args()

    if args.audit or args.archive_unused:
        rc = run_audit(archive_unused=args.archive_unused)
        if not args.build:
            return rc

    if args.build:
        return build_portable_zip(include_all_assets=args.include_all_assets)

    if not (args.audit or args.archive_unused or args.build):
        parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
