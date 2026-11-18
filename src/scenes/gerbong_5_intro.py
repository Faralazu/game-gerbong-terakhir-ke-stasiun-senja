"""Gerbong 5: Keheningan, Efek WOW Menit Pertama & Pertemuan Pak Kondektur.

Alur sesuai STORY_BIBLE.md:
1. Video pembuka laut senja -> CG_00A..C (gaya Wuthering Waves, fade hitam halus).
2. Eksplorasi Sketsa B&W -> putar Walkman -> Efek WOW Shockwave Senja!
3. Periksa 7 benda bermakna di Gerbong 5 (min. 3 benda untuk membuka dialog Kondektur).
4. Pak Kondektur (4-frame idle) menolak melubangi Tiket 23:59 dan membuka pintu ke Gerbong 4.
5. Mendukung efek refleksi jendela tertinggal sepersekian detik saat Kaset B (HUJAN) diputar.
"""

from __future__ import annotations

import math
import random
from collections import deque
from typing import Any

import pygame

from src.core.cg_cutscene import WutheringWavesCGOverlay
from src.core.director import BaseScene, DirectorContext
from src.core.narrative_script import (
    GERBONG_5_CONDUCTOR_NEED_EXPLORE,
    GERBONG_5_CONDUCTOR_OPEN,
    GERBONG_5_PROPS,
    PropScript,
)
from src.core.persona_ui import (
    CASSETTES,
    PersonaDialogueBox,
    VideoCutsceneOverlay,
    WalkmanHUD,
    draw_contact_shadow,
    get_ui_font,
    load_carriage_backgrounds,
    load_extra_portraits,
    load_npc_idle_animations,
    load_prop_sprites,
    load_raka_expression_portraits,
    load_raka_sitting_layers,
    load_raka_sprite_frames,
    render_cassette_atmosphere_filter,
    resolve_cassette_video,
)


WAKEUP_LINES: tuple[tuple[str, str], ...] = (
    ("raka:calm", "Suara relnya pelan banget... Aku ketiduran di kereta komuter terakhir lagi ya?"),
    ("raka:surprised", "Tunggu—kenapa seisi gerbong ini terlihat seperti coretan pensil hitam-putih begini?"),
    ("raka:sad", "Kepalaku berat sekali... Ada Walkman perak berkedip pelan di bangku kiri. Coba kuputar dulu."),
)

SHIFT_REACTIONS: dict[int, tuple[tuple[str, str], ...]] = {
    1: (
        ("raka:surprised", "Whoa—warna senja langsung menyapu seluruh gerbong! Udara di sini terasa hangat sekali."),
        ("raka:calm", "Di bangku ada karcis 23:59, cangkir teh, jam saku, ponsel retak, dan kaset tersegel. Sebaiknya kuperiksa barang-barangku sebelum menghampiri kondektur."),
    ),
    2: (
        ("raka:sad", "Langitnya langsung berubah malam berhujan... Di frekuensi ini, pantulan diriku di kaca jendela terasa aneh sekali."),
    ),
    3: (
        ("raka:calm", "Irama bass yang tenang tapi tegas. Rasanya seperti ada keberanian pelan untuk tidak terus berlari."),
    ),
    4: (
        ("raka:smile", "Udara pagi yang lapang. Rasanya semua beban malam itu boleh ditaruh sebentar di sini."),
    ),
}


class Gerbong5IntroScene(BaseScene):
    """Interactive Minute-1 WOW scene with CG intro, 7 items, and Conductor gate."""

    def __init__(self, scene_cfg: dict[str, Any], ctx: DirectorContext) -> None:
        super().__init__(scene_cfg, ctx)
        self.w, self.h = ctx.screen_size
        self.cassette_id = int(ctx.save_data.get("active_cassette", 0))
        self.prev_cassette_id = self.cassette_id
        self.t = 0.0
        self._footstep_timer = 0.0

        self.player_x = 520.0
        self.feet_y = 632.0
        self.target_walk_x: float | None = None
        self.pending_action: tuple[str, Any] | None = None
        self.facing_right = False
        self.is_walking = False
        self.is_sitting = False
        self.left_bench_x = 295.0
        self.left_bench_zone = pygame.Rect(205, 390, 185, 190)

        self.conductor_x = 1035.0
        self.conductor_talk_x = self.conductor_x - 120.0
        self.conductor_hitbox = pygame.Rect(975, 310, 125, 325)
        self.right_door_zone = pygame.Rect(1135, 175, 130, 360)
        self.door_unlocked = bool(ctx.save_data.get("g5_door_unlocked", False))
        self._pending_unlock_door = False
        self._pending_prolog_cg = False

        # History for Window Reflection Lag under Cassette B (HUJAN)
        self._pos_history: deque[tuple[float, float, bool, bool]] = deque(maxlen=90)

        self.shockwave_active = False
        self.shockwave_progress = 1.0
        self.shockwave_origin = (int(self.player_x), int(self.feet_y - 160))
        self.cutin_timer = 0.0
        self.cutin_duration = 0.65

        self.dialogue = PersonaDialogueBox()
        self.walkman = WalkmanHUD(ctx.assets)
        self.cutscene = VideoCutsceneOverlay()
        self.cg_overlay = WutheringWavesCGOverlay(ctx.assets, (self.w, self.h))

        self.particles = [
            [random.uniform(0, self.w), random.uniform(70, self.h - 140), random.uniform(14, 38), random.randint(2, 4)]
            for _ in range(32)
        ]

        self.carriage_layers: dict[int, pygame.Surface] = {}
        self.sitting_layers: dict[int, pygame.Surface] = {}
        self.raka_sprites: dict[str, list[pygame.Surface]] = {}
        self.raka_portraits: dict[str, pygame.Surface] = {}
        self.extra_portraits: dict[str, pygame.Surface] = {}
        self.conductor_frames: list[pygame.Surface] = []
        self.props: dict[str, dict[str, pygame.Surface]] = {}
        self.cutin_banner: pygame.Surface | None = None
        self.videos: dict[int, Any] = {}
        self.intro_video: Any = None
        self.prop_hitboxes: list[tuple[PropScript, pygame.Rect]] = []

    def on_enter(self) -> None:
        self._load_visual_assets()
        self._activate_cassette(self.cassette_id, with_transition=False, show_dialogue=False)
        seen_cg = set(self.ctx.save_data.get("seen_cg", []))
        if self.cassette_id == 0 and "cg_00a_wakeup_window" not in seen_cg:
            self._pending_prolog_cg = True
            self.play_intro_cutscene()
        elif self.cassette_id == 0:
            self._show_lines("Raka", WAKEUP_LINES, accent=CASSETTES[0].accent)

    def play_intro_cutscene(self) -> None:
        """Start opening sea-train video, followed smoothly by CG_00A..C."""
        self.cutscene.start(
            self.intro_video,
            title="PROLOG — KERETA SENJA TRACK 99",
            captions=(
                "Pukul 23:59. Kereta terakhir melaju di atas laut senja...",
                "Suara rel berirama pelan membawa Raka masuk ke dalam gerbong kenangan.",
            ),
            duration=6.5,
            accent=CASSETTES[1].accent,
        )

    def _begin_prolog_cg(self) -> None:
        self._pending_prolog_cg = False
        started = self.cg_overlay.start_sequence("cg_seq_prolog", self.ctx.save_data)
        if not started and self.cassette_id == 0:
            self._show_lines("Raka", WAKEUP_LINES, accent=CASSETTES[0].accent)

    def on_hot_reload(self) -> None:
        self._load_visual_assets()
        self.walkman.reload_art(self.ctx.assets)

    def _load_visual_assets(self) -> None:
        self.carriage_layers = load_carriage_backgrounds(self.ctx.assets, (self.w, self.h))
        self.sitting_layers = load_raka_sitting_layers(self.ctx.assets, (self.w, self.h))
        self.raka_sprites = load_raka_sprite_frames(self.ctx.assets, target_height=310)
        self.raka_portraits = load_raka_expression_portraits(self.ctx.assets, (92, 92))
        self.extra_portraits = load_extra_portraits(self.ctx.assets, (92, 92))
        self.conductor_frames = load_npc_idle_animations(self.ctx.assets).get("kondektur", [])
        self.props = load_prop_sprites(self.ctx.assets)

        full_cutin = self.ctx.assets.get_image(
            "images/portraits/preview_raka_cutin.png",
            fallback_style="courage",
        )
        self.cutin_banner = pygame.transform.smoothscale(full_cutin, (960, 260))

        self.intro_video = self.ctx.assets.get_video(
            "videos/vid_01_intro_sea_train.mp4",
            fallback_style="sunset",
            size=(self.w, self.h),
        )
        for cid in CASSETTES:
            self.videos[cid] = resolve_cassette_video(self.ctx.assets, cid)

    def _count_inspected(self) -> int:
        inspected = list(self.ctx.save_data.get("inspected_props", []))
        return sum(1 for item in inspected if item.startswith("gerbong_5_intro:"))

    def _resolve_speaker_portrait(self, tag: str) -> tuple[str, pygame.Surface | None]:
        if tag.startswith("raka:"):
            expr = tag.split(":", 1)[1]
            return "Raka", self.raka_portraits.get(expr, self.raka_portraits.get("calm"))
        if tag == "kondektur":
            return "Pak Kondektur", self.extra_portraits.get("kondektur")
        return "Raka", self.raka_portraits.get("calm")

    def _show_lines(
        self,
        title: str,
        lines_pairs: tuple[tuple[str, str], ...],
        accent: tuple[int, int, int],
    ) -> None:
        texts: list[str] = []
        speakers: list[str] = []
        portraits: list[pygame.Surface | None] = []
        for tag, txt in lines_pairs:
            spk, port = self._resolve_speaker_portrait(tag)
            speakers.append(spk)
            portraits.append(port)
            texts.append(txt)
        self.is_walking = False
        self.target_walk_x = None
        self.pending_action = None
        self.dialogue.set_dialogue(
            title,
            texts,
            portrait=portraits[0] if portraits else None,
            accent=accent,
            line_speakers=speakers,
            line_portraits=portraits,
            hint_override="SPACE / Klik untuk lanjut",
        )

    def _unlocked_set(self) -> set[int]:
        raw = self.ctx.save_data.get("collected_cassettes", [1])
        return {0, *(int(c) for c in raw)}

    def _activate_cassette(
        self,
        new_id: int,
        with_transition: bool = True,
        show_dialogue: bool = True,
    ) -> None:
        if new_id not in CASSETTES:
            return
        if new_id != 0 and new_id not in self._unlocked_set():
            self.ctx.assets.play_sfx("click", volume=0.22)
            self._show_lines(
                "WALKMAN",
                (("raka:sad", f"Kaset [{new_id}] belum kutemukan atau segelnya masih rapat."),),
                accent=CASSETTES[self.cassette_id].accent,
            )
            return

        if with_transition and new_id != self.cassette_id:
            self.prev_cassette_id = self.cassette_id
            self.shockwave_active = True
            self.shockwave_progress = 0.0
            self.shockwave_origin = (int(self.player_x), int(self.feet_y - 165))
            if self.ctx.toggles.get("persona_cutin_fx", True) and new_id != 0:
                self.cutin_timer = self.cutin_duration
            self.ctx.assets.play_sfx("click", volume=0.35)
            if new_id != 0:
                self.ctx.assets.play_sfx("chime", volume=0.22)

        self.cassette_id = new_id
        self.ctx.save_data["active_cassette"] = new_id
        prof = CASSETTES[new_id]
        self.ctx.assets.play_bgm(prof.bgm_rel, track_title=f"{prof.code}: {prof.title}")
        if show_dialogue and new_id in SHIFT_REACTIONS:
            self._show_lines("Raka", SHIFT_REACTIONS[new_id], accent=prof.accent)

    def trigger_cassette(self, new_id: int) -> None:
        """Public helper for interactive clicks or headless verification."""
        self._activate_cassette(new_id, with_transition=True, show_dialogue=True)

    def inspect_prop(self, prop_key: str) -> None:
        """Inspect a memory prop or pick up the Walkman in Sketch mode."""
        if prop_key == "walkman" and self.cassette_id == 0:
            self._activate_cassette(1, with_transition=True, show_dialogue=True)
            return
        prop = GERBONG_5_PROPS.get(prop_key)
        if prop is not None:
            inspected = list(self.ctx.save_data.get("inspected_props", []))
            tag = f"gerbong_5_intro:{prop_key}"
            if tag not in inspected:
                inspected.append(tag)
                self.ctx.save_data["inspected_props"] = inspected
            self.ctx.assets.play_sfx("paper", volume=0.26)
            self._show_lines(prop.title, prop.lines, accent=CASSETTES[self.cassette_id].accent)

    def talk_to_conductor(self) -> None:
        """Converse with Pak Kondektur facing right cleanly without sprite overlap."""
        if self.cassette_id == 0:
            return
        self.is_sitting = False
        self.player_x = self.conductor_talk_x
        self.facing_right = True
        self.ctx.assets.play_sfx("paper", volume=0.22)
        if self._count_inspected() < 3 and not self.door_unlocked:
            self._show_lines("Pak Kondektur", GERBONG_5_CONDUCTOR_NEED_EXPLORE, accent=CASSETTES[1].accent)
        else:
            self._pending_unlock_door = True
            self._show_lines("Pak Kondektur", GERBONG_5_CONDUCTOR_OPEN, accent=CASSETTES[1].accent)

    def _run_pending_action(self, action: tuple[str, Any]) -> str | None:
        kind, payload = action
        if kind == "sit":
            self.is_sitting = True
            self.ctx.assets.play_sfx("click", volume=0.2)
        elif kind == "prop":
            self.inspect_prop(str(payload))
        elif kind == "conductor":
            self.talk_to_conductor()
        elif kind == "door_right":
            if self.door_unlocked:
                return "next_scene"
            self.talk_to_conductor()
        return None

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.cutscene.handle_event(event):
            if not self.cutscene.active and self._pending_prolog_cg:
                self._begin_prolog_cg()
            elif not self.cutscene.active and self.cassette_id == 0:
                self._show_lines("Raka", WAKEUP_LINES, accent=CASSETTES[0].accent)
            return None

        if self.cg_overlay.active:
            res = self.cg_overlay.handle_event(event)
            if res == "completed":
                prof = CASSETTES[self.cassette_id]
                self.ctx.assets.play_bgm(prof.bgm_rel, track_title=f"{prof.code}: {prof.title}")
                if self.cassette_id == 0:
                    self._show_lines("Raka", WAKEUP_LINES, accent=CASSETTES[0].accent)
            return None

        # Top-right Walkman pill / drawer always accessible
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.walkman.set_unlocked(self._unlocked_set())
            clicked_cid = self.walkman.handle_click(event.pos)
            if clicked_cid is not None:
                if clicked_cid == -2:
                    self._activate_cassette(max(2, len(self._unlocked_set())))  # Will cleanly show lock message
                elif clicked_cid >= 0:
                    self._activate_cassette(clicked_cid)
                return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.walkman.reveal_briefly(4.0)
                return None
            if pygame.K_0 <= event.key <= pygame.K_4 and not self.dialogue.choices:
                self.walkman.reveal_briefly(2.5)
                self._activate_cassette(event.key - pygame.K_0)
                return None

        # Raka freezes and dialogue consumes input while visible
        if self.dialogue.visible:
            dlg_res = self.dialogue.handle_event(event)
            if dlg_res == "finished" and self._pending_unlock_door:
                self._pending_unlock_door = False
                self.door_unlocked = True
                self.ctx.save_data["g5_door_unlocked"] = True
                self.ctx.assets.play_sfx("door", volume=0.28)
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.cassette_id == 0:
                self._activate_cassette(1)
                return None
            if event.key == pygame.K_RETURN and self.cassette_id != 0 and self.door_unlocked:
                return "next_scene"
            if event.key == pygame.K_e:
                if self.is_sitting:
                    self.is_sitting = False
                    return None
                if self.cassette_id == 0 and abs(self.player_x - self.left_bench_x) < 120:
                    self._activate_cassette(1)
                    return None
                if self.cassette_id != 0 and self.door_unlocked and self.player_x >= 1065:
                    return "next_scene"
                if self.cassette_id != 0 and abs(self.player_x - self.conductor_x) < 145:
                    if abs(self.player_x - self.conductor_talk_x) > 8.0:
                        self.target_walk_x = self.conductor_talk_x
                        self.pending_action = ("conductor", None)
                    else:
                        self.talk_to_conductor()
                    return None
                for prop, _ in self.prop_hitboxes:
                    if abs(self.player_x - prop.x) < 68:
                        self.inspect_prop(prop.prop_key)
                        return None
                if abs(self.player_x - self.left_bench_x) < 120:
                    self.player_x = self.left_bench_x
                    self.is_sitting = True
                    self.ctx.assets.play_sfx("click", volume=0.2)
                    return None

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for prop, rect in self.prop_hitboxes:
                if rect.collidepoint(event.pos):
                    self.is_sitting = False
                    self.target_walk_x = prop.x
                    self.pending_action = ("prop", prop.prop_key)
                    return None

            if self.cassette_id != 0 and self.conductor_hitbox.collidepoint(event.pos):
                self.is_sitting = False
                self.target_walk_x = self.conductor_talk_x
                self.pending_action = ("conductor", None)
                return None

            if self.right_door_zone.collidepoint(event.pos) and self.cassette_id != 0:
                self.is_sitting = False
                self.target_walk_x = 1120.0
                self.pending_action = ("door_right", None)
                return None

            if self.left_bench_zone.collidepoint(event.pos):
                if self.is_sitting:
                    self.is_sitting = False
                    return None
                self.target_walk_x = self.left_bench_x
                self.pending_action = ("sit", None)
                return None

            self.is_sitting = False
            self.pending_action = None
            self.target_walk_x = max(145.0, min(1135.0, float(event.pos[0])))
        return None

    def update(self, dt: float) -> str | None:
        self.t += dt
        if self.cutscene.active:
            if self.cutscene.update(dt):
                if self._pending_prolog_cg:
                    self._begin_prolog_cg()
                elif self.cassette_id == 0:
                    self._show_lines("Raka", WAKEUP_LINES, accent=CASSETTES[0].accent)
            return None

        if self.cg_overlay.active:
            if self.cg_overlay.update(dt) == "completed":
                prof = CASSETTES[self.cassette_id]
                self.ctx.assets.play_bgm(prof.bgm_rel, track_title=f"{prof.code}: {prof.title}")
                if self.cassette_id == 0:
                    self._show_lines("Raka", WAKEUP_LINES, accent=CASSETTES[0].accent)
            return None

        self.walkman.update(dt, is_playing=self.cassette_id != 0)
        self.dialogue.update(dt, assets=self.ctx.assets)

        if self.cassette_id in self.videos:
            self.videos[self.cassette_id].update(dt)
        if self.shockwave_active and self.prev_cassette_id in self.videos:
            self.videos[self.prev_cassette_id].update(dt)

        if self.shockwave_active:
            self.shockwave_progress = min(1.0, self.shockwave_progress + dt * 1.25)
            if self.shockwave_progress >= 1.0:
                self.shockwave_active = False
        if self.cutin_timer > 0.0:
            self.cutin_timer = max(0.0, self.cutin_timer - dt)

        # Keep Raka completely frozen whenever dialogue box is open
        if self.dialogue.visible:
            self.is_walking = False
            self.target_walk_x = None
            self.pending_action = None
        else:
            keys = pygame.key.get_pressed()
            move_dir = 0
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                move_dir -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                move_dir += 1

            if move_dir != 0:
                self.is_sitting = False
                self.target_walk_x = None
                self.pending_action = None
                self.is_walking = True
                self.facing_right = move_dir > 0
                self.player_x = max(145.0, min(1135.0, self.player_x + move_dir * 255.0 * dt))
            elif self.target_walk_x is not None and not self.is_sitting:
                dx = self.target_walk_x - self.player_x
                if abs(dx) <= 6.0:
                    self.player_x = self.target_walk_x
                    self.target_walk_x = None
                    self.is_walking = False
                    if self.pending_action is not None:
                        act = self.pending_action
                        self.pending_action = None
                        res = self._run_pending_action(act)
                        if res == "next_scene":
                            return res
                else:
                    self.is_walking = True
                    self.facing_right = dx > 0
                    step = min(abs(dx), 265.0 * dt)
                    self.player_x += step if dx > 0 else -step
            else:
                self.is_walking = False

        self._pos_history.append((self.t, self.player_x, self.facing_right, self.is_walking))

        if self.is_walking:
            self._footstep_timer += dt
            if self._footstep_timer >= 0.36:
                self._footstep_timer = 0.0
                self.ctx.assets.play_sfx("footstep", volume=0.14)
        else:
            self._footstep_timer = 0.2

        for p in self.particles:
            speed_mul = 4.2 if self.cassette_id == 2 else 1.0
            p[0] = (p[0] - p[2] * speed_mul * dt) % self.w
            if self.cassette_id == 2:
                p[1] = (p[1] + 190.0 * dt) % self.h
            else:
                p[1] = 85.0 + ((p[1] + math.sin(self.t + p[0] * 0.01) * 8.0 * dt) % (self.h - 230.0))
        return None

    def _render_window_reflection_lag(self, frame: pygame.Surface, sway_y: int) -> None:
        """Under Cassette B (HUJAN), render Raka's window reflection slightly delayed (~0.28s)."""
        if self.is_sitting or not self._pos_history:
            return
        target_t = self.t - 0.28
        chosen = self._pos_history[0]
        for entry in self._pos_history:
            if entry[0] <= target_t:
                chosen = entry
        _, lag_x, lag_facing, lag_walk = chosen
        frames = self.raka_sprites.get("walk" if lag_walk else "idle", [])
        if not frames:
            return
        spr = frames[int(self.t * (7.5 if lag_walk else 2.2)) % len(frames)].copy()
        if not lag_facing:
            spr = pygame.transform.flip(spr, True, False)
        spr.fill((110, 170, 235, 65), special_flags=pygame.BLEND_RGBA_MULT)
        sx = int(lag_x - spr.get_width() // 2)
        sy = int(self.feet_y - spr.get_height() + sway_y)
        frame.blit(spr, (sx, sy))

    def _render_world_for_cassette(self, cid: int, sway_y: int) -> pygame.Surface:
        frame = pygame.Surface((self.w, self.h))
        if cid in self.videos:
            frame.blit(self.videos[cid].get_surface(), (0, 0))

        # Subtle eerie lag reflection visible purely inside chroma-keyed window glass
        if cid == 2:
            self._render_window_reflection_lag(frame, sway_y)

        if self.is_sitting and cid in self.sitting_layers:
            frame.blit(self.sitting_layers[cid], (0, sway_y))
        elif cid in self.carriage_layers:
            frame.blit(self.carriage_layers[cid], (0, sway_y))

        self.prop_hitboxes.clear()
        if cid == 0:
            w_prop = GERBONG_5_PROPS["walkman"]
            if "walkman" in self.props:
                w_surf = self.props["walkman"]["world"]
                wx, wy = int(w_prop.x - w_surf.get_width() // 2), int(w_prop.y) + sway_y
                pulse = 180 + int(math.sin(self.t * 4.0) * 65)
                pygame.draw.circle(frame, (pulse, pulse, 255), (wx + w_surf.get_width() // 2, wy + w_surf.get_height() // 2), 34, 2)
                frame.blit(w_surf, (wx, wy))
                self.prop_hitboxes.append((w_prop, pygame.Rect(wx - 14, wy - 14, w_surf.get_width() + 28, w_surf.get_height() + 28)))
        else:
            for key, prop in GERBONG_5_PROPS.items():
                if key == "walkman":
                    continue
                skey = prop.sprite_key
                if skey and skey in self.props:
                    psurf = self.props[skey]["world"]
                    draw_x = int(prop.x - psurf.get_width() // 2)
                    draw_y = int(prop.y) + sway_y
                    frame.blit(psurf, (draw_x, draw_y))
                    self.prop_hitboxes.append(
                        (prop, pygame.Rect(draw_x - 10, draw_y - 10, psurf.get_width() + 20, psurf.get_height() + 20))
                    )
                else:
                    # Wall hotspot (Papan Rute Kereta)
                    hb = pygame.Rect(int(prop.x - 85), int(prop.y - 22) + sway_y, 170, 44)
                    self.prop_hitboxes.append((prop, hb))
                    if hb.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(frame, (*CASSETTES[cid].accent, 190), hb, 2, border_radius=6)

        if cid != 0:
            accent = CASSETTES[cid].accent
            for px, py, _, size in self.particles:
                if cid == 2:
                    pygame.draw.line(frame, accent, (int(px), int(py)), (int(px) - 3, int(py) + 9), 1)
                else:
                    pygame.draw.rect(frame, accent, (int(px), int(py) + sway_y, size, size))

            # Animated 4-frame Pak Kondektur waiting near right doorway
            if self.conductor_frames:
                c_spr = self.conductor_frames[int(self.t * 2.4) % len(self.conductor_frames)]
                draw_contact_shadow(frame, int(self.conductor_x), int(self.feet_y + sway_y), width=92, height=18)
                cx = int(self.conductor_x - c_spr.get_width() // 2)
                cy = int(self.feet_y - c_spr.get_height() + sway_y)
                frame.blit(c_spr, (cx, cy))
                self.conductor_hitbox = pygame.Rect(cx - 8, cy - 8, c_spr.get_width() + 16, c_spr.get_height() + 16)

            if self.door_unlocked:
                pulse = 180 + int(math.sin(self.t * 4.5) * 65)
                pygame.draw.rect(frame, (pulse, 225, 160), (1142, 190, 8, 290), 2)

        if self.target_walk_x is not None and not self.is_sitting:
            tx = int(self.target_walk_x)
            ty = 626 + sway_y
            pygame.draw.polygon(
                frame,
                CASSETTES[cid].accent,
                [(tx, ty - 7), (tx + 11, ty), (tx, ty + 7), (tx - 11, ty)],
                2,
            )

        if not self.is_sitting:
            draw_contact_shadow(frame, int(self.player_x), int(self.feet_y + sway_y))
            if self.is_walking and self.raka_sprites.get("walk"):
                walk_list = self.raka_sprites["walk"]
                sprite = walk_list[int(self.t * 7.5) % len(walk_list)]
            else:
                idle_list = self.raka_sprites.get("idle", [])
                sprite = idle_list[int(self.t * 2.2) % len(idle_list)] if idle_list else pygame.Surface((96, 200), pygame.SRCALPHA)

            if not self.facing_right:
                sprite = pygame.transform.flip(sprite, True, False)
            sx = int(self.player_x - sprite.get_width() // 2)
            sy = int(self.feet_y - sprite.get_height() + sway_y)
            frame.blit(sprite, (sx, sy))

        if not self.dialogue.visible:
            self._render_world_tooltip(frame, cid, sway_y)
        render_cassette_atmosphere_filter(frame, cid, self.t)
        return frame

    def _render_world_tooltip(self, frame: pygame.Surface, cid: int, sway_y: int) -> None:
        mpos = pygame.mouse.get_pos()
        label: str | None = None
        tx = int(self.player_x)
        ty = int(self.feet_y - 335 + sway_y)

        if cid != 0 and self.conductor_hitbox.collidepoint(mpos):
            done_n = self._count_inspected()
            if self.door_unlocked:
                label = "Klik: Bicara Pak Kondektur"
            else:
                label = f"Klik: Bicara Pak Kondektur (Periksa {min(done_n, 3)}/3 benda)"
            tx, ty = int(self.conductor_x), 292
        elif self.right_door_zone.collidepoint(mpos) and cid != 0 and self.door_unlocked:
            label = "Masuk ke Gerbong 4 →"
            tx, ty = 1150, 172
        elif self.left_bench_zone.collidepoint(mpos):
            label = "Berdiri" if self.is_sitting else "Duduk Santai"
            tx, ty = 295, 375
        else:
            for prop, prect in self.prop_hitboxes:
                if prect.collidepoint(mpos) or (not self.is_sitting and abs(self.player_x - prop.x) < 70 and abs(prop.y - 450) < 60):
                    label = "[E / Klik] Putar Walkman" if prop.prop_key == "walkman" else f"[E / Klik] {prop.title.title()}"
                    tx, ty = int(prop.x), int(prop.y) - 34
                    break

        if not label and cid != 0 and self.door_unlocked and self.player_x >= 1065 and not self.is_sitting:
            label = "[E] Masuk ke Gerbong 4 →"
        elif not label and cid != 0 and abs(self.player_x - self.conductor_x) < 145 and not self.is_sitting:
            label = "[E] Bicara Pak Kondektur"
        elif not label and not self.is_sitting and abs(self.player_x - self.left_bench_x) < 110 and cid != 0:
            label = "[E] Duduk di Kursi Pojok"
        elif not label and self.is_sitting:
            label = "[E / A / D] Berdiri"
            tx, ty = 295, 250

        if label:
            f_hint = get_ui_font(13, bold=True)
            tag = f_hint.render(label, True, (255, 244, 210))
            bx = max(18, min(self.w - tag.get_width() - 32, tx - tag.get_width() // 2))
            pill = pygame.Surface((tag.get_width() + 20, 26), pygame.SRCALPHA)
            pygame.draw.rect(pill, (16, 18, 28, 210), (0, 0, pill.get_width(), 26), border_radius=6)
            pygame.draw.rect(pill, (*CASSETTES[cid].accent, 210), (0, 0, pill.get_width(), 26), 1, border_radius=6)
            frame.blit(pill, (bx - 10, ty - 4))
            frame.blit(tag, (bx, ty))

    def render(self, surface: pygame.Surface) -> None:
        if self.cutscene.active:
            self.cutscene.render(surface)
            return
        if self.cg_overlay.active:
            self.cg_overlay.render(surface)
            return

        sway_y = int(round(math.sin(self.t * 7.5) * 1.6)) if self.ctx.toggles.get("slow_cozy_sway", True) else 0

        if self.shockwave_active:
            old_world = self._render_world_for_cassette(self.prev_cassette_id, sway_y)
            new_world = self._render_world_for_cassette(self.cassette_id, sway_y)
            eased = 1.0 - (1.0 - self.shockwave_progress) ** 3
            radius = max(12, int(eased * 1550))

            mask = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            mask.fill((0, 0, 0, 0))
            pygame.draw.circle(mask, (255, 255, 255, 255), self.shockwave_origin, radius)
            masked_new = new_world.convert_alpha()
            masked_new.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            surface.blit(old_world, (0, 0))
            surface.blit(masked_new, (0, 0))
            ring_col = CASSETTES[self.cassette_id].accent
            pygame.draw.circle(surface, ring_col, self.shockwave_origin, radius, 6)
            pygame.draw.circle(surface, (255, 255, 255), self.shockwave_origin, max(4, radius - 5), 2)
        else:
            surface.blit(self._render_world_for_cassette(self.cassette_id, sway_y), (0, 0))

        if self.cutin_timer > 0.0 and self.cutin_banner is not None:
            self._render_persona_cutin(surface)

        self.dialogue.render(surface)
        top_off = 44 if self.ctx.toggles.get("director_bar_visible") else 14
        self.walkman.render(
            surface,
            self.cassette_id,
            self.ctx.assets,
            top_offset=top_off,
            unlocked_cassettes=self._unlocked_set(),
        )

    def _render_persona_cutin(self, surface: pygame.Surface) -> None:
        ratio = 1.0 - (self.cutin_timer / self.cutin_duration)
        slide = math.sin(min(1.0, ratio) * math.pi)
        band_h = int(230 * slide)
        if band_h <= 10 or self.cutin_banner is None:
            return
        cy = self.h // 2 - 40
        pts = [
            (0, cy - band_h // 2 + 26),
            (self.w, cy - band_h // 2 - 26),
            (self.w, cy + band_h // 2 - 26),
            (0, cy + band_h // 2 + 26),
        ]
        pygame.draw.polygon(surface, (12, 12, 16), pts)
        pygame.draw.polygon(surface, CASSETTES[self.cassette_id].accent, pts, 5)
        scaled = pygame.transform.smoothscale(self.cutin_banner, (920, max(12, band_h - 14)))
        x_off = int((1.0 - slide) * 140) + (self.w - 920) // 2
        surface.blit(scaled, (x_off, cy - scaled.get_height() // 2))
