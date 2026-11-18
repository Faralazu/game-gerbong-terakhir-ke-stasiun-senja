"""Modular "Kill Your Darlings" Scene Director & 45-minute Pacing Debugger.

Allows toggling experimental scenes/mechanics on/off, hot-swapping order via
userdata/scene_playlist.json, tracking real-time pacing budgets against the
45-minute runtime target, jumping scenes instantly ([ / ]), hot-reloading
assets (F5), and archiving unused assets (F9).
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import pygame

from src.core import paths
from src.core.persona_ui import DiagonalWipeTransition, clear_ui_caches, get_ui_font
from src.core.save_and_menus import PauseMenuModal

if TYPE_CHECKING:
    from src.core.asset_manager import AssetManager


DEFAULT_PLAYLIST: list[dict[str, Any]] = [
    {
        "id": "title_screen",
        "title": "Menu Utama: Track 99",
        "module": "src.scenes.title_screen",
        "class_name": "TitleScreenScene",
        "target_minutes": 0.5,
        "enabled": True,
        "notes": "Layar judul Persona dengan opsi mulai, lanjut, atau preview fajar",
    },
    {
        "id": "gerbong_5_intro",
        "title": "Gerbong 5: Keheningan & Efek WOW",
        "module": "src.scenes.gerbong_5_intro",
        "class_name": "Gerbong5IntroScene",
        "target_minutes": 4.5,
        "enabled": True,
        "notes": "Sketsa B&W -> Tekan PLAY Walkman -> Shockwave Senja",
    },
    {
        "id": "gerbong_4_childhood",
        "title": "Gerbong 4: Taman Bermain Masa Kecil",
        "module": "src.scenes.carriage_story_scene",
        "class_name": "CarriageStoryScene",
        "target_minutes": 10.0,
        "enabled": True,
        "notes": "Bima Kecil & pesawat kertas (Kaset SENJA + Waveform Tuner)",
    },
    {
        "id": "gerbong_3_burnout",
        "title": "Gerbong 3: Ruang Tunggu & Ekspektasi",
        "module": "src.scenes.carriage_story_scene",
        "class_name": "CarriageStoryScene",
        "target_minutes": 10.0,
        "enabled": True,
        "notes": "Nadia & beban ekspektasi (Kaset HUJAN & DETAK ala Persona)",
    },
    {
        "id": "gerbong_2_crossroads",
        "title": "Gerbong 2: Persimpangan Penyesalan",
        "module": "src.scenes.carriage_story_scene",
        "class_name": "CarriageStoryScene",
        "target_minutes": 10.0,
        "enabled": True,
        "notes": "Bayangan Raka & penerimaan diri (Kaset HUJAN)",
    },
    {
        "id": "gerbong_1_dawn",
        "title": "Gerbong 1 & Masinis: Stasiun Fajar",
        "module": "src.scenes.carriage_story_scene",
        "class_name": "CarriageStoryScene",
        "target_minutes": 10.0,
        "enabled": True,
        "notes": "Senja, All-Out Resonance Kaset FAJAR & Peron Stasiun Fajar",
    },
]


@dataclass
class DirectorContext:
    """Shared state passed to all scenes and updated by Director."""

    assets: AssetManager
    settings: dict[str, Any]
    save_data: dict[str, Any]
    screen_size: tuple[int, int] = (1280, 720)
    toggles: dict[str, bool] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.toggles:
            self.toggles = {
                "persona_cutin_fx": bool(self.settings.get("persona_cutin_fx", True)),
                "slow_cozy_sway": bool(self.settings.get("slow_cozy_sway", True)),
            }


class BaseScene:
    """Interface for all modular carriage scenes."""

    def __init__(self, scene_cfg: dict[str, Any], ctx: DirectorContext) -> None:
        self.cfg = scene_cfg
        self.ctx = ctx

    def on_enter(self) -> None:
        """Called whenever this scene becomes active."""

    def on_exit(self) -> None:
        """Called right before leaving this scene."""

    def on_hot_reload(self) -> None:
        """Called after F5 asset reload so cached scene layers refresh."""

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Return 'next_scene' or 'prev_scene' to request navigation, else None."""
        return None

    def update(self, dt: float) -> str | None:
        """Advance scene state by dt seconds; optionally return navigation action."""
        return None

    def render(self, surface: pygame.Surface) -> None:
        """Draw the scene onto the display surface."""


def _fmt_mmss(seconds: float) -> str:
    total = max(0, int(seconds))
    mins, secs = divmod(total, 60)
    return f"{mins:02d}:{secs:02d}"


class SceneDirector:
    """Controls modular scene playlist, pacing budgets, and F1 debug overlay."""

    def __init__(self, ctx: DirectorContext) -> None:
        self.ctx = ctx
        self.playlist_path = paths.userdata_path("scene_playlist.json")
        self.playlist = self._load_or_init_playlist()
        self.active_scenes = [s for s in self.playlist if s.get("enabled", True)]
        if not self.active_scenes:
            self.active_scenes = list(DEFAULT_PLAYLIST)

        self.current_index = 0
        self.scene_elapsed = 0.0
        self.total_elapsed = float(ctx.save_data.get("elapsed_total_seconds", 0.0))
        self.overlay_visible = bool(ctx.settings.get("show_director_hud", False))
        self.ctx.toggles["director_bar_visible"] = self.overlay_visible
        self._toast_text = ""
        self._toast_timer = 0.0
        self.transition = DiagonalWipeTransition()
        self.pause_menu = PauseMenuModal(ctx.assets, ctx.screen_size)
        self.pause_btn_rect = pygame.Rect(888, 14, 88, 32)
        self.current_scene: BaseScene | None = None

        start_id = ctx.save_data.get("current_scene", "title_screen")
        for idx, cfg in enumerate(self.active_scenes):
            if cfg["id"] == start_id:
                self.current_index = idx
                break
        self._load_scene_at(self.current_index, with_wipe=False)

    def _load_or_init_playlist(self) -> list[dict[str, Any]]:
        if not self.playlist_path.exists():
            paths.write_json(self.playlist_path, DEFAULT_PLAYLIST)
            return list(DEFAULT_PLAYLIST)
        loaded = paths.read_json(self.playlist_path, default=DEFAULT_PLAYLIST)
        if isinstance(loaded, list) and loaded:
            # Upgrade legacy placeholder playlists automatically
            has_title = any(s.get("id") == "title_screen" for s in loaded)
            uses_placeholder = any("placeholder_scene" in str(s.get("module", "")) for s in loaded)
            if not has_title or uses_placeholder:
                paths.write_json(self.playlist_path, DEFAULT_PLAYLIST)
                return list(DEFAULT_PLAYLIST)
            return loaded
        return list(DEFAULT_PLAYLIST)

    def _show_toast(self, msg: str, duration: float = 3.0) -> None:
        self._toast_text = msg
        self._toast_timer = duration

    def _load_scene_at(self, index: int, with_wipe: bool = True) -> None:
        if self.current_scene is not None:
            self.current_scene.on_exit()

        self.current_index = index % len(self.active_scenes)
        cfg = self.active_scenes[self.current_index]
        module = importlib.import_module(cfg["module"])
        scene_cls = getattr(module, cfg["class_name"])
        self.current_scene = scene_cls(cfg, self.ctx)
        self.scene_elapsed = 0.0
        self.current_scene.on_enter()
        self.ctx.save_data["current_scene"] = cfg["id"]
        if cfg["id"] != "title_screen":
            self.ctx.save_data["resume_scene"] = cfg["id"]
        if with_wipe:
            self.transition.trigger()
        self.ctx.assets.save_manifest()

    def jump_scene(self, delta: int) -> None:
        self.ctx.assets.play_sfx("door", volume=0.28)
        self._load_scene_at(self.current_index + delta, with_wipe=True)
        if self.overlay_visible:
            cfg = self.active_scenes[self.current_index]
            self._show_toast(f"Scene -> {cfg['title']}")

    def jump_to_scene(self, scene_id: str) -> None:
        for idx, cfg in enumerate(self.active_scenes):
            if cfg["id"] == scene_id:
                self.ctx.assets.play_sfx("door", volume=0.28)
                self._load_scene_at(idx, with_wipe=True)
                if self.overlay_visible:
                    self._show_toast(f"Scene -> {cfg['title']}")
                return

    def _can_pause_now(self) -> bool:
        cfg = self.active_scenes[self.current_index]
        if cfg["id"] == "title_screen":
            return False
        is_cutscene = bool(
            (getattr(self.current_scene, "cutscene", None) and self.current_scene.cutscene.active)
            or (getattr(self.current_scene, "cg_overlay", None) and self.current_scene.cg_overlay.active)
        )
        return not is_cutscene

    def _apply_loaded_save(self, loaded_dict: dict[str, Any]) -> None:
        self.ctx.save_data.clear()
        self.ctx.save_data.update(loaded_dict)
        c_list = self.ctx.save_data.get(
            "collected_cassettes",
            self.ctx.save_data.get("cassette_unlocked", [1]),
        )
        normalized = sorted({1, *(int(c) for c in c_list if int(c) in (1, 2, 3, 4))})
        self.ctx.save_data["collected_cassettes"] = normalized
        self.ctx.save_data["cassette_unlocked"] = list(normalized)
        self.ctx.save_data.setdefault("seen_cg", [])
        self.ctx.save_data.setdefault("harmonized_carriages", [])
        self.ctx.save_data.setdefault("inspected_props", [])
        self.ctx.save_data.setdefault("completed_minigames", [])
        self.ctx.save_data.setdefault("ticket_stubs", 0)
        self.total_elapsed = float(self.ctx.save_data.get("elapsed_total_seconds", 0.0))
        target = str(
            self.ctx.save_data.get("resume_scene")
            or self.ctx.save_data.get("current_scene")
            or "gerbong_5_intro"
        )
        if target == "title_screen":
            target = "gerbong_5_intro"
        self.jump_to_scene(target)

    def _handle_pause_result(self, res: tuple[str, Any] | None) -> None:
        if res is None:
            return
        kind, payload = res
        if kind == "saved" and isinstance(payload, tuple):
            slot_idx, _saved_dict = payload
            self._show_toast(f"Progres disimpan ke Slot {slot_idx:02d}")
        elif kind == "loaded" and isinstance(payload, dict):
            self._apply_loaded_save(payload)
            self._show_toast("Data permainan dimuat!")
        elif kind == "main_menu":
            self.jump_to_scene("title_screen")

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.pause_menu.active:
            res = self.pause_menu.handle_event(event, self.ctx.save_data)
            self._handle_pause_result(res)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self._can_pause_now():
                self.pause_menu.open()
                self.ctx.assets.play_sfx("click", volume=0.20)
                return
            if event.key == pygame.K_F1:
                self.overlay_visible = not self.overlay_visible
                self.ctx.toggles["director_bar_visible"] = self.overlay_visible
                self.ctx.settings["show_director_hud"] = self.overlay_visible
                paths.save_settings(self.ctx.settings)
                return
            if event.key == pygame.K_F2:
                val = not self.ctx.toggles["persona_cutin_fx"]
                self.ctx.toggles["persona_cutin_fx"] = val
                self.ctx.settings["persona_cutin_fx"] = val
                paths.save_settings(self.ctx.settings)
                self._show_toast(f"Idea Toggle [F2] Cut-In FX: {'ON' if val else 'OFF'}")
                return
            if event.key == pygame.K_F3:
                val = not self.ctx.toggles["slow_cozy_sway"]
                self.ctx.toggles["slow_cozy_sway"] = val
                self.ctx.settings["slow_cozy_sway"] = val
                paths.save_settings(self.ctx.settings)
                self._show_toast(f"Idea Toggle [F3] Train Sway: {'ON' if val else 'OFF'}")
                return
            if event.key == pygame.K_F5:
                clear_ui_caches()
                stats = self.ctx.assets.reload_all()
                if self.current_scene is not None:
                    self.current_scene.on_hot_reload()
                self.ctx.assets.save_manifest()
                self._show_toast(
                    f"Hot-Reload [F5]: {stats['real_count']} Real / {stats['fallback_count']} Draft"
                )
                return
            if event.key == pygame.K_F9:
                moved = self.ctx.assets.archive_unused_assets()
                self._show_toast(
                    f"Archive Unused [F9]: {len(moved)} file dipindah ke _asset_vault/unused_archive"
                )
                return
            if event.key == pygame.K_LEFTBRACKET:
                self.jump_scene(-1)
                return
            if event.key == pygame.K_RIGHTBRACKET:
                self.jump_scene(1)
                return

        if (
            self._can_pause_now()
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.pause_btn_rect.collidepoint(event.pos)
        ):
            self.pause_menu.open()
            self.ctx.assets.play_sfx("click", volume=0.20)
            return

        if self.current_scene is not None:
            self._handle_nav_action(self.current_scene.handle_event(event))

    def _start_new_game(self) -> None:
        self.total_elapsed = 0.0
        self.ctx.save_data.clear()
        self.ctx.save_data.update(
            {
                "slot": "slot_1",
                "current_scene": "gerbong_5_intro",
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
        self.jump_to_scene("gerbong_5_intro")

    def _handle_nav_action(self, action: str | None) -> None:
        if action == "next_scene":
            self.jump_scene(1)
        elif action == "prev_scene":
            self.jump_scene(-1)
        elif action == "new_game":
            self._start_new_game()
        elif action == "reload_save":
            self._apply_loaded_save(dict(self.ctx.save_data))
        elif isinstance(action, str) and action.startswith("goto:"):
            self.jump_to_scene(action.split(":", 1)[1])

    def update(self, dt: float) -> None:
        if self._toast_timer > 0:
            self._toast_timer = max(0.0, self._toast_timer - dt)
        self.transition.update(dt)
        if self.pause_menu.active:
            self.pause_menu.update(dt)
            return
        self.scene_elapsed += dt
        self.total_elapsed += dt
        self.ctx.save_data["elapsed_total_seconds"] = round(self.total_elapsed, 2)
        if self.current_scene is not None:
            self._handle_nav_action(self.current_scene.update(dt))

    def render(self, surface: pygame.Surface) -> None:
        if self.current_scene is not None:
            self.current_scene.render(surface)
        self.transition.render(surface)

        is_cutscene = bool(
            (getattr(self.current_scene, "cutscene", None) and self.current_scene.cutscene.active)
            or (getattr(self.current_scene, "cg_overlay", None) and self.current_scene.cg_overlay.active)
        )
        if self._can_pause_now() and not self.pause_menu.active and not is_cutscene:
            top_off = 44 if self.overlay_visible else 14
            self.pause_btn_rect = pygame.Rect(884, top_off, 92, 32)
            pill = pygame.Surface((self.pause_btn_rect.width, self.pause_btn_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(pill, (16, 18, 28, 205), (0, 0, pill.get_width(), pill.get_height()), border_radius=8)
            hovered = self.pause_btn_rect.collidepoint(pygame.mouse.get_pos())
            border_col = (248, 174, 84, 240) if hovered else (180, 190, 210, 170)
            pygame.draw.rect(pill, border_col, (0, 0, pill.get_width(), pill.get_height()), 1, border_radius=8)
            surface.blit(pill, self.pause_btn_rect.topleft)
            bx = self.pause_btn_rect.left + 12
            by = self.pause_btn_rect.centery
            for dy in (-4, 0, 4):
                pygame.draw.line(surface, (248, 174, 84), (bx, by + dy), (bx + 11, by + dy), 2)
            lbl = get_ui_font(12, bold=True).render("ESC Menu", True, (240, 244, 248))
            surface.blit(lbl, (bx + 17, self.pause_btn_rect.centery - lbl.get_height() // 2))

        if self.pause_menu.active:
            self.pause_menu.render(surface)
        if self.overlay_visible:
            self._render_director_bar(surface)
        if self._toast_timer > 0 and self._toast_text:
            self._render_toast(surface)

    def _render_director_bar(self, surface: pygame.Surface) -> None:
        w, _ = surface.get_size()
        cfg = self.active_scenes[self.current_index]
        target_sec = float(cfg.get("target_minutes", 5.0)) * 60.0
        total_budget_sec = sum(float(s.get("target_minutes", 0.0)) for s in self.active_scenes) * 60.0

        bar = pygame.Surface((w, 34), pygame.SRCALPHA)
        pygame.draw.polygon(
            bar,
            (12, 12, 18, 215),
            [(0, 0), (w, 0), (w - 18, 34), (0, 34)],
        )
        pygame.draw.line(bar, (230, 52, 68), (0, 33), (w - 18, 33), 2)
        surface.blit(bar, (0, 0))

        font = get_ui_font(13, bold=True)
        real_n = len(self.ctx.assets.loaded_assets)
        draft_n = len(self.ctx.assets.fallback_assets)
        cutin_tag = "ON" if self.ctx.toggles["persona_cutin_fx"] else "OFF"
        sway_tag = "ON" if self.ctx.toggles["slow_cozy_sway"] else "OFF"

        left_txt = (
            f"[F1] {cfg['id']} ({_fmt_mmss(self.scene_elapsed)}/{_fmt_mmss(target_sec)}) "
            f"| Total {_fmt_mmss(self.total_elapsed)}/{_fmt_mmss(total_budget_sec)}"
        )
        right_txt = (
            f"[/] Scene | [F2] CutIn:{cutin_tag} | [F3] Sway:{sway_tag} "
            f"| [F5] Reload ({real_n}R/{draft_n}D) | [F9] Archive"
        )
        surface.blit(font.render(left_txt, True, (255, 224, 155)), (12, 9))
        r_surf = font.render(right_txt, True, (220, 225, 235))
        surface.blit(r_surf, (w - r_surf.get_width() - 26, 9))

    def _render_toast(self, surface: pygame.Surface) -> None:
        w, _ = surface.get_size()
        font = get_ui_font(15, bold=True)
        txt = font.render(self._toast_text, True, (255, 255, 255))
        box_w = txt.get_width() + 44
        x = (w - box_w) // 2
        y = 46
        pygame.draw.polygon(
            surface,
            (215, 32, 48),
            [(x + 10, y), (x + box_w, y), (x + box_w - 10, y + 32), (x, y + 32)],
        )
        pygame.draw.polygon(
            surface,
            (255, 220, 120),
            [(x + 10, y), (x + box_w, y), (x + box_w - 10, y + 32), (x, y + 32)],
            2,
        )
        surface.blit(txt, (x + 22, y + 7))

    def shutdown(self) -> None:
        if self.current_scene is not None:
            self.current_scene.on_exit()
        paths.write_save(self.ctx.save_data)
        self.ctx.assets.close()
