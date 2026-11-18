"""Entry point for Gerbong Terakhir ke Stasiun Senja (Track 99: Resonance)."""

from __future__ import annotations

import argparse
import json
import os
import sys

# Ensure portable env vars and local .venv are active before importing pygame or cv2.
from src.core import paths

paths.ensure_local_venv()

from src.core.asset_manager import AssetManager  # noqa: E402
from src.core.director import DirectorContext, SceneDirector  # noqa: E402

# Static scene imports ensure PyInstaller bundles dynamically imported scene modules.
from src.scenes import (  # noqa: E402, F401
    carriage_story_scene,
    gerbong_5_intro,
    placeholder_scene,
    title_screen,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track 99: Resonance")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run headless verification frames and check portable userdata output.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        os.environ["SDL_AUDIODRIVER"] = "dummy"

    import pygame

    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    settings = paths.load_settings()
    save_data = paths.load_save("slot_1")
    win_size = tuple(settings.get("resolution", [1280, 720]))
    screen = pygame.display.set_mode((int(win_size[0]), int(win_size[1])))
    pygame.display.set_caption("Gerbong Terakhir ke Stasiun Senja — Track 99: Resonance")

    assets = AssetManager()
    ctx = DirectorContext(
        assets=assets,
        settings=settings,
        save_data=save_data,
        screen_size=(int(win_size[0]), int(win_size[1])),
    )
    director = SceneDirector(ctx)
    clock = pygame.time.Clock()

    if args.self_test:
        from src.core.cg_cutscene import ALL_CG_SLIDES, CG_SEQUENCES, WutheringWavesCGOverlay
        from src.core.save_and_menus import load_game_from_slot, save_game_to_slot

        gallery_file = paths.SAVES_DIR / "gallery_unlocked.json"
        had_gallery = gallery_file.exists()
        prev_gallery = gallery_file.read_text(encoding="utf-8") if had_gallery else None
        slot10_file = paths.SAVES_DIR / "slot_10.json"
        had_slot10 = slot10_file.exists()
        prev_slot10 = slot10_file.read_text(encoding="utf-8") if had_slot10 else None

        try:
            # 1. Exercise TitleScreen + Load Modal + CG Gallery Modal
            director.jump_to_scene("title_screen")
            title_scene = director.current_scene
            for _ in range(3):
                director.update(1.0 / 30.0)
                director.render(screen)
            title_scene.save_modal.open("load")
            title_scene.render(screen)
            title_scene.save_modal.close()
            title_scene.gallery_modal.open()
            title_scene.render(screen)
            title_scene.gallery_modal.close()

            # 2. Verify all 25 CGs, 10 CG sequences, 7 BGMs & 10 WAV SFX
            for sfx_key in (
                "click",
                "footstep",
                "text_blip",
                "paper",
                "door",
                "chime",
                "ticket_punch",
                "phone_vibrate",
                "wind_petals",
                "memory_ache",
            ):
                assets.play_sfx(sfx_key, volume=0.01)

            cg_tester = WutheringWavesCGOverlay(assets, (int(win_size[0]), int(win_size[1])))
            for seq_id in CG_SEQUENCES:
                assert CG_SEQUENCES[seq_id].slides
                assert cg_tester.start_sequence(seq_id, save_data=None, force=True), f"Missing CG seq: {seq_id}"
                cg_tester.render(screen)
                cg_tester.stop()
            for slide in ALL_CG_SLIDES:
                assert cg_tester.start_single_cg(slide.cg_id), f"Missing CG: {slide.cg_id}"
                cg_tester.render(screen)
                cg_tester.stop()

            # 3. Verify PauseMenu & 10-Slot Save/Load Round-Trip
            save_game_to_slot(
                10,
                {
                    "current_scene": "gerbong_3_burnout",
                    "resume_scene": "gerbong_3_burnout",
                    "collected_cassettes": [1, 2, 3],
                    "active_cassette": 3,
                    "elapsed_total_seconds": 612.5,
                },
            )
            loaded10 = load_game_from_slot(10)
            assert loaded10 is not None and loaded10["current_scene"] == "gerbong_3_burnout"

            # 4. Exercise Gerbong 5 -> 7 items + Pak Kondektur + Shockwave
            director.ctx.save_data["collected_cassettes"] = [1, 2, 3, 4]
            director.ctx.save_data["cassette_unlocked"] = [1, 2, 3, 4]
            director.ctx.save_data["active_cassette"] = 0
            director.ctx.save_data["elapsed_total_seconds"] = 0.0
            director.ctx.save_data["seen_cg"] = []
            director.jump_to_scene("gerbong_5_intro")
            g5 = director.current_scene
            for frame_idx in range(14):
                if frame_idx == 1 and hasattr(g5, "cutscene"):
                    g5.cutscene.stop()
                    g5._begin_prolog_cg()
                elif frame_idx == 2 and hasattr(g5, "cg_overlay"):
                    g5.cg_overlay.stop()
                elif frame_idx == 3:
                    g5.trigger_cassette(1)
                    g5.dialogue.hide()
                    g5.target_walk_x = 640.0
                elif frame_idx == 5:
                    for pk in ("ticket_99", "tea", "pocket_watch", "phone_cracked", "cassette_d_sealed", "hotspot:route_board"):
                        g5.inspect_prop(pk)
                    g5.talk_to_conductor()
                    g5.door_unlocked = True
                    g5.dialogue.hide()
                elif frame_idx == 7:
                    g5.dialogue.hide()
                    g5.trigger_cassette(2)
                    g5.is_sitting = True
                elif frame_idx == 9:
                    g5.trigger_cassette(3)
                elif frame_idx == 11:
                    g5.trigger_cassette(4)
                    g5.is_sitting = False
                director.update(0.20)
                director.render(screen)

            director.pause_menu.open()
            director.update(0.05)
            director.render(screen)
            director.pause_menu.close()

            # 5. Exercise Gerbong 4, 3, 2, 1 + Mini-Games + CG Overlays + Finale
            for sid in ("gerbong_4_childhood", "gerbong_3_burnout", "gerbong_2_crossroads", "gerbong_1_dawn"):
                director.jump_to_scene(sid)
                scene = director.current_scene
                if hasattr(scene, "cg_overlay") and scene.cg_overlay.active:
                    scene.cg_overlay.render(screen)
                    scene.cg_overlay.stop()
                if hasattr(scene, "story") and scene.story.props:
                    for p in scene.story.props:
                        scene.inspect_prop(p)
                    scene.dialogue.hide()
                if hasattr(scene, "start_passenger_conversation"):
                    scene.start_passenger_conversation()
                    scene.dialogue.hide()
                if sid == "gerbong_4_childhood" and hasattr(scene, "plane_game"):
                    scene.plane_game.open()
                    scene.plane_game.render(screen)
                    scene.plane_game.close()
                elif sid == "gerbong_2_crossroads" and hasattr(scene, "kintsugi_game"):
                    scene.kintsugi_game.open()
                    scene.kintsugi_game.render(screen)
                    scene.kintsugi_game.close()
                if hasattr(scene, "open_tuner"):
                    scene.open_tuner()
                    scene.tuner.auto_tuning = True
                    scene.tuner.trigger_ripple(scene.story.required_cassette)
                    scene._apply_cassette(scene.story.required_cassette, play_sfx=False)
                for frame_idx in range(6):
                    if frame_idx == 2 and hasattr(scene, "complete_harmonization"):
                        scene.complete_harmonization(with_cutscene=True)
                    elif frame_idx == 4:
                        if hasattr(scene, "cutscene") and scene.cutscene.active:
                            scene.cutscene.stop()
                        if hasattr(scene, "cg_overlay") and scene.cg_overlay.active:
                            scene.cg_overlay.render(screen)
                            scene.cg_overlay.stop()
                        if sid == "gerbong_1_dawn" and hasattr(scene, "_trigger_dawn_station_ending"):
                            scene._trigger_dawn_station_ending()
                            scene.cutscene.stop()
                            scene._finish_ending_sequence()
                        else:
                            scene._trigger_resonance_banner()
                    director.update(0.10)
                    director.render(screen)

            # 6. Keep initial launch state pristine before shutdown
            director.ctx.save_data.clear()
            director.ctx.save_data.update(
                {
                    "slot": "slot_1",
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
            )
            director.shutdown()
        finally:
            if had_gallery and prev_gallery is not None:
                gallery_file.write_text(prev_gallery, encoding="utf-8")
            elif gallery_file.exists():
                gallery_file.unlink()
            if had_slot10 and prev_slot10 is not None:
                slot10_file.write_text(prev_slot10, encoding="utf-8")
            elif slot10_file.exists():
                slot10_file.unlink()

        audit = assets.scan_unused_assets(include_manifest=True)
        summary = {
            "root_dir": str(paths.ROOT_DIR),
            "userdata_files": sorted(
                p.relative_to(paths.ROOT_DIR).as_posix()
                for p in paths.USERDATA_DIR.rglob("*")
                if p.is_file()
            ),
            "loaded_real_assets_count": len(assets.loaded_assets),
            "loaded_real_assets": sorted(assets.loaded_assets),
            "missing_fallback_assets": sorted(assets.fallback_assets),
            "unused_on_disk": audit["unused_on_disk"],
        }
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        pygame.quit()
        return 0

    running = True
    while running:
        dt = min(0.05, clock.tick(60) / 1000.0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                director.handle_event(event)

        director.update(dt)
        director.render(screen)
        pygame.display.flip()

    director.shutdown()
    pygame.quit()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback

        crash_log = paths.LOGS_DIR / "last_crash.txt"
        crash_log.parent.mkdir(parents=True, exist_ok=True)
        crash_log.write_text(traceback.format_exc(), encoding="utf-8")
        raise
