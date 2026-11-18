"""Playable narrative story carriages (Gerbong 4, 3, 2, and 1 + Stasiun Fajar).

Implements the complete STORY_BIBLE.md loop:
- 1x Wuthering Waves-style Flashback CG upon entering each carriage (+ Raka memory shock).
- 4-frame proportional idle sprites for Bima, Nadia, Bayangan Raka, Raka Kecil & Senja.
- All 16 interactive story items + wall hotspots, with mandatory exploration gate before Babak 2.
- Key-locked Cassette progression (A -> B in Gerbong 4 -> C from Bima -> D unsealed in Gerbong 2).
- Subtle window-reflection lag foreshadowing under Cassette B (HUJAN).
- Mini-games + Waveform Tuner -> Farewell CG ("Terima kasih, Raka") -> Passenger fades out,
  leaving star-punched ticket stub on an empty bench.
- Gerbong 1 finale chains CG_SENJA -> vid_05 -> CG_END_01..06 + Stasiun Fajar Epilogue.
"""

from __future__ import annotations

import math
import random
from collections import deque
from typing import Any

import pygame

from src.core.cg_cutscene import WutheringWavesCGOverlay
from src.core.director import BaseScene, DirectorContext
from src.core.minigames import PaperPlaneGlideModal, SketchbookKintsugiModal
from src.core.narrative_script import CarriageNarrative, PropScript, get_carriage_narrative
from src.core.persona_ui import (
    CASSETTES,
    AllOutResonanceBanner,
    PersonaDialogueBox,
    VideoCutsceneOverlay,
    WalkmanHUD,
    draw_contact_shadow,
    get_ui_font,
    load_custom_carriage_variants,
    load_extra_portraits,
    load_npc_idle_animations,
    load_prop_sprites,
    load_raka_expression_portraits,
    load_raka_sitting_layers,
    load_raka_sprite_frames,
    render_cassette_atmosphere_filter,
    resolve_cassette_video,
)
from src.core.waveform_tuner import WaveformTunerModal


def _create_fallback_passenger_sprite(style: str) -> pygame.Surface:
    pw, ph = 24, 40
    scale = 7
    s = pygame.Surface((pw, ph), pygame.SRCALPHA)
    col = {
        "child": (245, 198, 52),
        "student": (85, 130, 175),
        "shadow": (28, 28, 44),
        "senja": (235, 225, 210),
    }.get(style, (220, 220, 220))
    pygame.draw.rect(s, col, (6, 8, 12, 22))
    pygame.draw.rect(s, (240, 195, 165), (8, 2, 8, 6))
    pygame.draw.rect(s, (30, 34, 46), (8, 30, 3, 9))
    pygame.draw.rect(s, (30, 34, 46), (13, 30, 3, 9))
    return pygame.transform.scale(s, (pw * scale, ph * scale)).convert_alpha()


def _slice_passenger_portrait(sheet: pygame.Surface, panel_idx: int, size: tuple[int, int] = (92, 92)) -> pygame.Surface:
    sw, sh = sheet.get_size()
    panel_w = sw // 3
    inset_x = 18
    x0 = panel_idx * panel_w + inset_x
    cw = max(32, panel_w - inset_x * 2)
    ch = min(sh - 32, cw)
    crop_rect = pygame.Rect(x0, 22, cw, ch)
    return pygame.transform.smoothscale(sheet.subsurface(crop_rect).copy(), size)


class CarriageStoryScene(BaseScene):
    """Deep multi-chapter story carriage with CG cutscenes, mini-games, and clean UI."""

    def __init__(self, scene_cfg: dict[str, Any], ctx: DirectorContext) -> None:
        super().__init__(scene_cfg, ctx)
        self.w, self.h = ctx.screen_size
        self.story: CarriageNarrative = get_carriage_narrative(scene_cfg["id"])
        self.t = 0.0
        self._footstep_timer = 0.0
        self._shake_timer = 0.0

        harmonized_list = list(ctx.save_data.get("harmonized_carriages", []))
        completed_mg = list(ctx.save_data.get("completed_minigames", []))
        self.harmonized = self.story.scene_id in harmonized_list
        self.minigame_done = (
            self.story.minigame_type == "none"
            or self.story.scene_id in completed_mg
            or self.harmonized
        )
        self.chapter_idx = len(self.story.chapters) - 1 if self.harmonized else 0
        self._dialogue_mode = "idle"
        self.show_dawn_station = self.story.is_finale and self.harmonized and bool(ctx.save_data.get("ending_reached", False))

        # Balance all 4 cassettes across carriages: auto-unlock & select carriage theme on entry
        self._unlock_cassette(self.story.default_cassette)
        self.cassette_id = self.story.default_cassette if not self.harmonized else int(
            ctx.save_data.get("active_cassette", self.story.default_cassette)
        )
        if self.cassette_id == 0 or self.cassette_id not in self._unlocked_set():
            self.cassette_id = self.story.default_cassette

        self.player_x = 220.0
        self.feet_y = 632.0
        self.target_walk_x: float | None = None
        self.pending_action: tuple[str, Any] | None = None
        self.facing_right = True
        self.is_walking = False
        self.is_sitting = False
        self.left_bench_x = 295.0
        self.left_bench_zone = pygame.Rect(205, 390, 185, 190)
        self.left_door_zone = pygame.Rect(25, 175, 145, 360)
        self.right_door_zone = pygame.Rect(1110, 175, 145, 360)
        self.npc_x = 855.0
        self.npc_talk_x = self.npc_x - 125.0
        self.npc_hitbox = pygame.Rect(780, 310, 150, 325)
        self.stub_hitbox = pygame.Rect(830, 448, 64, 52)

        self._pos_history: deque[tuple[float, float, bool, bool]] = deque(maxlen=90)

        self.particles = [
            [random.uniform(0, self.w), random.uniform(70, self.h - 140), random.uniform(16, 42), random.randint(2, 4)]
            for _ in range(32)
        ]

        self.dialogue = PersonaDialogueBox()
        self.walkman = WalkmanHUD(ctx.assets)
        self.tuner = WaveformTunerModal()
        self.plane_game = PaperPlaneGlideModal()
        self.kintsugi_game = SketchbookKintsugiModal()
        self.resonance_banner = AllOutResonanceBanner()
        self.cutscene = VideoCutsceneOverlay()
        self.cg_overlay = WutheringWavesCGOverlay(ctx.assets, (self.w, self.h))
        self._cg_context = ""      # "entry" | "harmony" | "ending"
        self._video_context = ""   # "mind_dive" | "ending"
        self._pending_post_cutscene_banner = False

        self.carriage_layers: dict[int, pygame.Surface] = {}
        self.sitting_layers: dict[int, pygame.Surface] = {}
        self.raka_sprites: dict[str, list[pygame.Surface]] = {}
        self.raka_portraits: dict[str, pygame.Surface] = {}
        self.extra_portraits: dict[str, pygame.Surface] = {}
        self.props: dict[str, dict[str, pygame.Surface]] = {}
        self.npc_frames: list[pygame.Surface] = []
        self.raka_kecil_frames: list[pygame.Surface] = []
        self.videos: dict[int, Any] = {}
        self.mind_dive_video: Any = None
        self.ending_video: Any = None
        self.station_dawn_bg: pygame.Surface | None = None
        self.cutin_banner: pygame.Surface | None = None
        self.npc_portrait: pygame.Surface | None = None
        self.prop_hitboxes: list[tuple[PropScript, pygame.Rect]] = []

    def _unlocked_set(self) -> set[int]:
        raw = self.ctx.save_data.get("collected_cassettes", [1])
        return {0, *(int(c) for c in raw)}

    def _unlock_cassette(self, cid: int) -> bool:
        if cid not in (1, 2, 3, 4):
            return False
        cur = sorted({1, *(int(c) for c in self.ctx.save_data.get("collected_cassettes", [1]))})
        if cid not in cur:
            cur.append(cid)
            cur.sort()
            self.ctx.save_data["collected_cassettes"] = cur
            self.ctx.save_data["cassette_unlocked"] = list(cur)
            self.walkman.set_unlocked(cur)
            self.walkman.reveal_briefly(4.0)
            return True
        return False

    def _count_carriage_props_inspected(self) -> int:
        inspected = list(self.ctx.save_data.get("inspected_props", []))
        prefix = f"{self.story.scene_id}:"
        return sum(1 for item in inspected if item.startswith(prefix))

    def on_enter(self) -> None:
        self._load_assets()
        self._apply_cassette(self.cassette_id, play_sfx=False, whisper_on_rain=False)

        if self.story.entry_cg_seq and not self.harmonized:
            started = self.cg_overlay.start_sequence(self.story.entry_cg_seq, self.ctx.save_data, force=False)
            if started:
                self._cg_context = "entry"
                return

        if self.show_dawn_station:
            lines = self.story.finale_station_lines or self.story.epilogue_lines
            self._show_script_lines(
                "Stasiun Fajar",
                lines,
                accent=CASSETTES[4].accent,
                mode="epilogue",
            )

    def on_hot_reload(self) -> None:
        self.story = get_carriage_narrative(self.cfg["id"])
        self._load_assets()
        self.walkman.reload_art(self.ctx.assets)

    def _load_assets(self) -> None:
        self.carriage_layers = load_custom_carriage_variants(
            self.ctx.assets, self.story.bg_image_rel, (self.w, self.h)
        )
        self.sitting_layers = load_raka_sitting_layers(self.ctx.assets, (self.w, self.h))
        self.raka_sprites = load_raka_sprite_frames(self.ctx.assets, target_height=310)
        self.raka_portraits = load_raka_expression_portraits(self.ctx.assets, (92, 92))
        self.extra_portraits = load_extra_portraits(self.ctx.assets, (92, 92))
        self.props = load_prop_sprites(self.ctx.assets)

        anims = load_npc_idle_animations(self.ctx.assets)
        self.npc_frames = anims.get(self.story.sprite_style) or [_create_fallback_passenger_sprite(self.story.sprite_style)]
        self.raka_kecil_frames = anims.get("raka_kecil", [])

        self.station_dawn_bg = self.ctx.assets.get_image(
            "images/backgrounds/bg_station_dawn.png",
            size=(self.w, self.h),
            fallback_style="dawn",
        )
        cutin_full = self.ctx.assets.get_image(
            "images/portraits/preview_raka_cutin.png",
            fallback_style="courage",
        )
        self.cutin_banner = pygame.transform.smoothscale(cutin_full, (960, 260))

        sheet = self.ctx.assets.get_image(
            "images/portraits/passengers_portraits.png",
            fallback_style="sunset",
        )
        if self.story.portrait_slot >= 0:
            self.npc_portrait = _slice_passenger_portrait(sheet, self.story.portrait_slot, (92, 92))
        else:
            self.npc_portrait = self.extra_portraits.get("bayangan") or self.raka_portraits.get("sad")

        for cid in CASSETTES:
            self.videos[cid] = resolve_cassette_video(self.ctx.assets, cid)

        self.mind_dive_video = self.ctx.assets.get_video(
            "videos/vid_04_mind_dive_transition.mp4",
            fallback_style="courage",
            size=(self.w, self.h),
        )
        self.ending_video = self.ctx.assets.get_video(
            "videos/vid_05_ending_dawn_station.mp4",
            fallback_style="dawn",
            size=(self.w, self.h),
        )

    def _resolve_speaker_and_portrait(self, tag: str) -> tuple[str, pygame.Surface | None]:
        if tag.startswith("raka:"):
            expr = tag.split(":", 1)[1]
            return "Raka", self.raka_portraits.get(expr, self.raka_portraits.get("calm"))
        if tag == "kondektur":
            return "Pak Kondektur", self.extra_portraits.get("kondektur")
        if tag == "kakek_harjo":
            return "Kakek Harjo", self.extra_portraits.get("kakek_harjo")
        if tag == "raka_kecil":
            return "Raka Kecil", self.extra_portraits.get("raka_kecil")
        if tag == "bayangan":
            return "Bayangan Raka", self.extra_portraits.get("bayangan")
        return self.story.passenger_name, self.npc_portrait

    def _show_script_lines(
        self,
        default_title: str,
        pairs: tuple[tuple[str, str], ...],
        accent: tuple[int, int, int],
        mode: str,
        choices: tuple[str, ...] = (),
        choice_prompt: str = "",
    ) -> None:
        self._dialogue_mode = mode
        texts: list[str] = []
        speakers: list[str] = []
        portraits: list[pygame.Surface | None] = []
        for tag, txt in pairs:
            spk, port = self._resolve_speaker_and_portrait(tag)
            speakers.append(spk)
            portraits.append(port)
            texts.append(txt)
        if choices and choice_prompt:
            texts.append(choice_prompt)
            speakers.append("Raka")
            portraits.append(self.raka_portraits.get("calm"))

        self.is_walking = False
        self.target_walk_x = None
        self.pending_action = None
        self.dialogue.set_dialogue(
            default_title,
            texts,
            portrait=portraits[0] if portraits else None,
            accent=accent,
            choices=list(choices) if choices else None,
            line_portraits=portraits,
            line_speakers=speakers,
        )

    def _apply_cassette(
        self,
        new_id: int,
        play_sfx: bool = True,
        whisper_on_rain: bool = True,
    ) -> None:
        if new_id not in CASSETTES or new_id == 0:
            return
        if new_id not in self._unlocked_set():
            if play_sfx:
                self.ctx.assets.play_sfx("click", volume=0.20)
                self._show_script_lines(
                    "WALKMAN",
                    (("raka:sad", f"Kaset [{new_id}] belum ditemukan atau masih tersegel."),),
                    accent=CASSETTES[self.cassette_id].accent,
                    mode="prop",
                )
            return

        if play_sfx and new_id != self.cassette_id:
            self.ctx.assets.play_sfx("click", volume=0.32)
        self.cassette_id = new_id
        self.ctx.save_data["active_cassette"] = new_id
        prof = CASSETTES[new_id]
        self.ctx.assets.play_bgm(prof.bgm_rel, track_title=f"{prof.code}: {prof.title}")

        if (
            whisper_on_rain
            and new_id == 2
            and not self.harmonized
            and not self.dialogue.visible
            and not self.tuner.active
            and not self.cg_overlay.active
        ):
            self._show_script_lines(
                f"{self.story.passenger_name} (Frekuensi Hujan)",
                (("npc", self.story.rain_whisper),),
                accent=CASSETTES[2].accent,
                mode="prop",
            )

    def start_passenger_conversation(self) -> None:
        """Position Raka cleanly facing passenger (no overlap) and open dialogue."""
        if not self.harmonized:
            self.is_sitting = False
            self.player_x = self.npc_talk_x
            self.facing_right = True
        else:
            self.is_sitting = False
            self.facing_right = self.player_x <= self.npc_x
            self._show_script_lines(
                "Kenangan Tersisa",
                self.story.epilogue_lines,
                accent=CASSETTES[self.cassette_id].accent,
                mode="epilogue",
            )
            return

        ch = self.story.chapters[min(self.chapter_idx, len(self.story.chapters) - 1)]
        self._show_script_lines(
            f"{self.story.passenger_name} — {ch.title}",
            ch.lines,
            accent=CASSETTES[self.cassette_id].accent,
            mode="chapter",
            choices=ch.choices,
            choice_prompt=ch.choice_prompt,
        )

    def inspect_prop(self, prop_story: PropScript) -> None:
        """Inspect one of the carriage memory objects or environmental hotspots."""
        inspected = list(self.ctx.save_data.get("inspected_props", []))
        tag = f"{self.story.scene_id}:{prop_story.prop_key}"
        if tag not in inspected:
            inspected.append(tag)
            self.ctx.save_data["inspected_props"] = inspected
        if prop_story.unlocks_cassette > 0:
            if self._unlock_cassette(prop_story.unlocks_cassette):
                self.ctx.assets.play_sfx("chime", volume=0.28)
        self.ctx.assets.play_sfx("paper", volume=0.25)
        self._show_script_lines(
            prop_story.title,
            prop_story.lines,
            accent=CASSETTES[self.cassette_id].accent,
            mode="prop",
        )

    def _launch_next_challenge_or_tuner(self) -> None:
        if self.harmonized:
            return
        if not self.minigame_done:
            if self.story.minigame_type == "paper_plane":
                self.plane_game.open()
                return
            if self.story.minigame_type == "kintsugi":
                self.kintsugi_game.open()
                return
        self.open_tuner()

    def open_tuner(self) -> None:
        if self.harmonized:
            return
        # Ensure required cassette is usable inside tuner if script already reached Babak 3
        self._unlock_cassette(self.story.required_cassette)
        self.tuner.open(
            passenger_name=self.story.passenger_name,
            required_cassette=self.story.required_cassette,
            target_freq=self.story.target_freq,
            target_amp=self.story.target_amp,
            cassette_hint=self.story.cassette_hint,
        )

    def _trigger_dawn_station_ending(self) -> None:
        """Play final arrival video + Ending CGs once player steps out of Gerbong 1."""
        self._video_context = "ending"
        self.cutscene.start(
            self.ending_video,
            title="MENUJU PERON — STASIUN FAJAR",
            captions=(
                "Pintu lokomotif terbuka lebar menyambut udara pagi laut yang tenang...",
                "Untuk pertama kalinya, jam di saku Raka terasa hangat kembali.",
            ),
            duration=5.5,
            accent=CASSETTES[4].accent,
        )

    def complete_harmonization(self, with_cutscene: bool = True) -> None:
        self.harmonized = True
        self.minigame_done = True
        harmonized_list = list(self.ctx.save_data.get("harmonized_carriages", []))
        if self.story.scene_id not in harmonized_list:
            harmonized_list.append(self.story.scene_id)
            self.ctx.save_data["harmonized_carriages"] = harmonized_list
            self.ctx.save_data["ticket_stubs"] = int(self.ctx.save_data.get("ticket_stubs", 0)) + 1

        if self.story.unlocks_cassette_on_harmony > 0:
            self._unlock_cassette(self.story.unlocks_cassette_on_harmony)

        self._apply_cassette(self.story.required_cassette, play_sfx=False, whisper_on_rain=False)
        self.ctx.assets.play_sfx("chime", volume=0.36)

        if with_cutscene:
            if self.story.is_finale:
                # Finale: Farewell Senja CG -> return to empty Gerbong 1 with Kaset 4 Fajar playing
                started = self.cg_overlay.start_sequence(
                    self.story.harmony_cg_seq, self.ctx.save_data, force=True
                )
                if started:
                    self._cg_context = "harmony"
                    return
            else:
                self._video_context = "mind_dive"
                self.cutscene.start(
                    self.mind_dive_video,
                    title=self.story.resonance_title,
                    captions=self.story.mind_dive_captions,
                    duration=4.2,
                    accent=CASSETTES[self.story.required_cassette].accent,
                )
                self._pending_post_cutscene_banner = True
                return

        self._trigger_resonance_banner()
        self._show_script_lines(
            "Kenangan Pulih",
            self.story.epilogue_lines,
            accent=CASSETTES[self.story.required_cassette].accent,
            mode="epilogue",
        )

    def _advance_post_cutscene_chain(self) -> None:
        if self._video_context == "mind_dive":
            self._video_context = ""
            if self.story.harmony_cg_seq:
                started = self.cg_overlay.start_sequence(
                    self.story.harmony_cg_seq, self.ctx.save_data, force=True
                )
                if started:
                    self._cg_context = "harmony"
                    return
            self._finish_harmony_sequence()
        elif self._video_context == "ending":
            self._video_context = ""
            started = self.cg_overlay.start_sequence("cg_seq_ending", self.ctx.save_data, force=True)
            if started:
                self._cg_context = "ending"
                return
            self._finish_ending_sequence()

    def _advance_post_cg_chain(self) -> None:
        ctx_kind = self._cg_context
        self._cg_context = ""
        prof = CASSETTES[self.cassette_id]

        if ctx_kind == "entry":
            self.ctx.assets.play_bgm(prof.bgm_rel, track_title=f"{prof.code}: {prof.title}")
            self._shake_timer = 0.25
            if self.story.entry_reaction_lines:
                self._show_script_lines(
                    "Raka (Kilas Balik)",
                    self.story.entry_reaction_lines,
                    accent=prof.accent,
                    mode="prop",
                )
        elif ctx_kind == "harmony":
            self.ctx.assets.play_bgm(prof.bgm_rel, track_title=f"{prof.code}: {prof.title}")
            self._finish_harmony_sequence()
        elif ctx_kind == "ending":
            self._finish_ending_sequence()

    def _finish_harmony_sequence(self) -> None:
        self._pending_post_cutscene_banner = False
        self._trigger_resonance_banner()
        self._show_script_lines(
            "Kenangan Pulih",
            self.story.epilogue_lines,
            accent=CASSETTES[self.story.required_cassette].accent,
            mode="epilogue",
        )

    def _finish_ending_sequence(self) -> None:
        self.show_dawn_station = True
        self.ctx.save_data["ending_reached"] = True
        self.ctx.assets.play_bgm("audio/bgm/bgm_06_ending_wind.mp3", track_title="ENDING: Selamat Pulang, Raka")
        lines = self.story.finale_station_lines or self.story.epilogue_lines
        self._show_script_lines(
            "Stasiun Fajar",
            lines,
            accent=CASSETTES[4].accent,
            mode="epilogue",
        )

    def _trigger_resonance_banner(self) -> None:
        if self.ctx.toggles.get("persona_cutin_fx", True):
            self.resonance_banner.trigger(
                title=self.story.resonance_title,
                subtitle=self.story.resonance_subtitle,
                accent=CASSETTES[self.story.required_cassette].accent,
            )

    def _run_pending_action(self, action: tuple[str, Any]) -> str | None:
        kind, payload = action
        if kind == "sit":
            self.is_sitting = True
            self.ctx.assets.play_sfx("click", volume=0.2)
        elif kind == "prop":
            self.inspect_prop(payload)
        elif kind == "npc":
            self.start_passenger_conversation()
        elif kind == "door_left":
            return "prev_scene"
        elif kind == "door_right" and self.harmonized:
            if self.story.is_finale:
                if not self.show_dawn_station:
                    self._trigger_dawn_station_ending()
                return None
            return "next_scene"
        return None

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.cutscene.handle_event(event):
            if not self.cutscene.active:
                if self._video_context in ("mind_dive", "ending"):
                    self._advance_post_cutscene_chain()
                elif self._pending_post_cutscene_banner:
                    self._finish_harmony_sequence()
            return None

        if self.cg_overlay.active:
            res = self.cg_overlay.handle_event(event)
            if res == "completed":
                self._advance_post_cg_chain()
            return None

        if self.plane_game.active:
            res = self.plane_game.handle_event(event)
            if res == "solved":
                self._mark_minigame_done()
            return None

        if self.kintsugi_game.active:
            res = self.kintsugi_game.handle_event(event)
            if res is not None:
                kind, _ = res
                if kind == "placed":
                    self.ctx.assets.play_sfx("paper", volume=0.25)
                elif kind == "solved":
                    self._mark_minigame_done()
            return None

        if self.tuner.active:
            res = self.tuner.handle_event(event)
            if res is not None:
                kind, val = res
                if kind == "cassette":
                    self._apply_cassette(int(val), whisper_on_rain=False)
            return None

        # Top-right Walkman pill click / TAB toggle
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.walkman.set_unlocked(self._unlocked_set())
            clicked_cid = self.walkman.handle_click(event.pos)
            if clicked_cid is not None:
                if clicked_cid == -2:
                    self._apply_cassette(max(2, len(self._unlocked_set())), play_sfx=True)
                elif clicked_cid > 0:
                    self._apply_cassette(clicked_cid)
                return None

        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self.walkman.reveal_briefly(4.0)
            return None

        if self.dialogue.visible:
            dlg_res = self.dialogue.handle_event(event)
            if isinstance(dlg_res, int):
                ch = self.story.chapters[min(self.chapter_idx, len(self.story.chapters) - 1)]
                reply_lines = ch.choice_replies[dlg_res] if dlg_res < len(ch.choice_replies) else ()
                self.chapter_idx = min(len(self.story.chapters) - 1, self.chapter_idx + 1)
                if reply_lines:
                    self._show_script_lines(
                        self.story.passenger_name,
                        reply_lines,
                        accent=CASSETTES[self.cassette_id].accent,
                        mode="choice_reply",
                    )
                else:
                    self.dialogue.hide()
                return None
            if dlg_res == "finished":
                if self._dialogue_mode == "epilogue" and self.story.is_finale and self.show_dawn_station:
                    return "goto:title_screen"
                if self._dialogue_mode == "chapter":
                    if self.chapter_idx == 0:
                        done_props = self._count_carriage_props_inspected()
                        if done_props >= self.story.required_props_for_ch2:
                            self.chapter_idx = 1
                        else:
                            self._dialogue_mode = "idle"
                            self._show_script_lines(
                                "Raka",
                                (
                                    (
                                        "raka:calm",
                                        f"(Sebaiknya kuperiksa dulu benda-benda di gerbong ini [{done_props}/{self.story.required_props_for_ch2}] sebelum melanjutkan obrolan.)",
                                    ),
                                ),
                                accent=CASSETTES[self.cassette_id].accent,
                                mode="prop",
                            )
                            return None
                    elif self.chapter_idx < len(self.story.chapters) - 1:
                        self.chapter_idx += 1
                    else:
                        self._launch_next_challenge_or_tuner()
                self._dialogue_mode = "idle"
                return None
            return None

        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_4:
                self.walkman.reveal_briefly(2.5)
                self._apply_cassette(event.key - pygame.K_0)
                return None
            if event.key == pygame.K_t and not self.harmonized:
                self._launch_next_challenge_or_tuner()
                return None
            if event.key == pygame.K_RETURN and self.harmonized:
                if self.story.is_finale:
                    if not self.show_dawn_station:
                        self._trigger_dawn_station_ending()
                    return None
                return "next_scene"
            if event.key == pygame.K_e:
                if self.is_sitting:
                    self.is_sitting = False
                    return None
                if self.harmonized and self.player_x >= 990:
                    if self.story.is_finale:
                        if not self.show_dawn_station:
                            self._trigger_dawn_station_ending()
                        return None
                    return "next_scene"
                if self.player_x <= 185:
                    return "prev_scene"
                if abs(self.player_x - self.npc_x) < 150:
                    if not self.harmonized and abs(self.player_x - self.npc_talk_x) > 8.0:
                        self.target_walk_x = self.npc_talk_x
                        self.pending_action = ("npc", None)
                    else:
                        self.start_passenger_conversation()
                    return None
                for prop_story, _ in self.prop_hitboxes:
                    if abs(self.player_x - prop_story.x) < 68 and abs(prop_story.y - 450) < 90:
                        self.inspect_prop(prop_story)
                        return None
                if abs(self.player_x - self.left_bench_x) < 110:
                    self.player_x = self.left_bench_x
                    self.is_sitting = True
                    self.ctx.assets.play_sfx("click", volume=0.2)
                    return None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.show_dawn_station:
                lines = self.story.finale_station_lines or self.story.epilogue_lines
                self._show_script_lines(
                    "Stasiun Fajar",
                    lines,
                    accent=CASSETTES[4].accent,
                    mode="epilogue",
                )
                return None

            for prop_story, rect in self.prop_hitboxes:
                if rect.collidepoint(event.pos):
                    self.is_sitting = False
                    self.target_walk_x = prop_story.x
                    self.pending_action = ("prop", prop_story)
                    return None

            if not self.harmonized and self.npc_hitbox.collidepoint(event.pos):
                self.is_sitting = False
                self.target_walk_x = self.npc_talk_x
                self.pending_action = ("npc", None)
                return None

            if self.harmonized and self.stub_hitbox.collidepoint(event.pos):
                self.is_sitting = False
                self.target_walk_x = self.npc_x - 105.0
                self.pending_action = ("npc", None)
                return None

            if self.right_door_zone.collidepoint(event.pos) and self.harmonized:
                self.is_sitting = False
                self.target_walk_x = 1095.0
                self.pending_action = ("door_right", None)
                return None

            if self.left_door_zone.collidepoint(event.pos):
                self.is_sitting = False
                self.target_walk_x = 155.0
                self.pending_action = ("door_left", None)
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

    def _mark_minigame_done(self) -> None:
        self.minigame_done = True
        done = list(self.ctx.save_data.get("completed_minigames", []))
        if self.story.scene_id not in done:
            done.append(self.story.scene_id)
            self.ctx.save_data["completed_minigames"] = done
        self.ctx.assets.play_sfx("chime", volume=0.28)
        self.open_tuner()

    def update(self, dt: float) -> str | None:
        self.t += dt
        if self._shake_timer > 0.0:
            self._shake_timer = max(0.0, self._shake_timer - dt)

        if self.cutscene.active:
            if self.cutscene.update(dt):
                if self._video_context in ("mind_dive", "ending"):
                    self._advance_post_cutscene_chain()
                elif self._pending_post_cutscene_banner:
                    self._finish_harmony_sequence()
            return None

        if self.cg_overlay.active:
            if self.cg_overlay.update(dt) == "completed":
                self._advance_post_cg_chain()
            return None

        self.walkman.update(dt, is_playing=True)
        self.dialogue.update(dt, assets=self.ctx.assets)
        self.resonance_banner.update(dt)

        if self.cassette_id in self.videos:
            self.videos[self.cassette_id].update(dt)

        if self.plane_game.active:
            if self.plane_game.update(dt) == "solved":
                self._mark_minigame_done()
            return None

        if self.kintsugi_game.active:
            self.kintsugi_game.update(dt)
            return None

        if self.tuner.active:
            if self.tuner.update(dt, self.cassette_id) == "solved":
                self.complete_harmonization(with_cutscene=True)
            return None

        if self.dialogue.visible or self.show_dawn_station:
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
                        return self._run_pending_action(act)
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
            speed_mul = 4.0 if self.cassette_id == 2 else 1.0
            p[0] = (p[0] - p[2] * speed_mul * dt) % self.w
            if self.cassette_id == 2:
                p[1] = (p[1] + 185.0 * dt) % self.h
            else:
                p[1] = 85.0 + ((p[1] + math.sin(self.t + p[0] * 0.01) * 9.0 * dt) % (self.h - 230.0))
        return None

    def _render_window_reflection_lag(self, surface: pygame.Surface, sway_y: int) -> None:
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
        surface.blit(spr, (sx, sy))

    def render(self, surface: pygame.Surface) -> None:
        if self.cutscene.active:
            self.cutscene.render(surface)
            return
        if self.cg_overlay.active:
            self.cg_overlay.render(surface)
            return

        shake_x = int(math.sin(self.t * 48.0) * 4) if self._shake_timer > 0.0 else 0
        sway_y = (
            int(round(math.sin(self.t * 7.5) * 1.6))
            if (self.ctx.toggles.get("slow_cozy_sway", True) and not self.show_dawn_station)
            else 0
        )

        if self.show_dawn_station and self.station_dawn_bg is not None:
            surface.blit(self.station_dawn_bg, (0, 0))
            for px, py, _, size in self.particles:
                pygame.draw.circle(surface, (255, 226, 232), (int(px), int(py)), max(2, size))
            render_cassette_atmosphere_filter(surface, 4, self.t)
            self._render_finale_card(surface)
        else:
            if self.cassette_id in self.videos:
                surface.blit(self.videos[self.cassette_id].get_surface(), (0, 0))

            if self.cassette_id == 2:
                self._render_window_reflection_lag(surface, sway_y)

            if self.is_sitting and self.cassette_id in self.sitting_layers:
                surface.blit(self.sitting_layers[self.cassette_id], (shake_x, sway_y))
            elif self.cassette_id in self.carriage_layers:
                surface.blit(self.carriage_layers[self.cassette_id], (shake_x, sway_y))

            self.prop_hitboxes.clear()
            for p_story in self.story.props:
                skey = p_story.sprite_key
                if skey and skey in self.props:
                    psurf = self.props[skey]["world"]
                    px = int(p_story.x - psurf.get_width() // 2) + shake_x
                    py = int(p_story.y) + sway_y
                    surface.blit(psurf, (px, py))
                    self.prop_hitboxes.append(
                        (p_story, pygame.Rect(px - 10, py - 10, psurf.get_width() + 20, psurf.get_height() + 20))
                    )
                else:
                    hb = pygame.Rect(int(p_story.x - 80) + shake_x, int(p_story.y - 24) + sway_y, 160, 48)
                    self.prop_hitboxes.append((p_story, hb))
                    if hb.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(surface, (*CASSETTES[self.cassette_id].accent, 190), hb, 2, border_radius=6)

            accent = CASSETTES[self.cassette_id].accent
            for px, py, _, size in self.particles:
                if self.cassette_id == 2:
                    pygame.draw.line(surface, accent, (int(px), int(py)), (int(px) - 3, int(py) + 9), 1)
                else:
                    pygame.draw.rect(surface, accent, (int(px), int(py) + sway_y, size, size))

            if not self.harmonized and self.npc_frames:
                use_frames = (
                    self.raka_kecil_frames
                    if (self.story.scene_id == "gerbong_2_crossroads" and self.minigame_done and self.raka_kecil_frames)
                    else self.npc_frames
                )
                spr_npc = use_frames[int(self.t * 2.5) % len(use_frames)]
                draw_contact_shadow(surface, int(self.npc_x) + shake_x, int(self.feet_y + sway_y), width=96, height=18)
                nx = int(self.npc_x - spr_npc.get_width() // 2) + shake_x
                ny = int(self.feet_y - spr_npc.get_height() + sway_y)
                for i in range(4):
                    ang = self.t * 1.8 + i * (math.pi / 2.0)
                    ox = int(self.npc_x + math.cos(ang) * 56) + shake_x
                    oy = int(ny + spr_npc.get_height() * 0.45 + math.sin(ang * 1.3) * 44)
                    pts = [(ox, oy - 8), (ox + 8, oy), (ox, oy + 8), (ox - 8, oy)]
                    pygame.draw.polygon(surface, CASSETTES[self.story.required_cassette].accent, pts, 2)
                surface.blit(spr_npc, (nx, ny))
                self.npc_hitbox = pygame.Rect(nx - 10, ny - 10, spr_npc.get_width() + 20, spr_npc.get_height() + 20)
            elif self.harmonized and "ticket_stub" in self.props:
                stub = self.props["ticket_stub"]["world"]
                sx_s = int(self.npc_x - stub.get_width() // 2) + shake_x
                sy_s = int(462) + sway_y
                surface.blit(stub, (sx_s, sy_s))
                self.stub_hitbox = pygame.Rect(sx_s - 12, sy_s - 12, stub.get_width() + 24, stub.get_height() + 24)

            if self.target_walk_x is not None and not self.is_sitting:
                tx = int(self.target_walk_x)
                ty = 626 + sway_y
                pygame.draw.polygon(surface, accent, [(tx, ty - 7), (tx + 11, ty), (tx, ty + 7), (tx - 11, ty)], 2)

            if not self.is_sitting:
                draw_contact_shadow(surface, int(self.player_x) + shake_x, int(self.feet_y + sway_y))
                if self.is_walking and self.raka_sprites.get("walk"):
                    walk_list = self.raka_sprites["walk"]
                    sprite = walk_list[int(self.t * 7.5) % len(walk_list)]
                else:
                    idle_list = self.raka_sprites.get("idle", [])
                    sprite = idle_list[int(self.t * 2.2) % len(idle_list)] if idle_list else pygame.Surface((96, 200), pygame.SRCALPHA)

                if not self.facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                sx = int(self.player_x - sprite.get_width() // 2) + shake_x
                sy = int(self.feet_y - sprite.get_height() + sway_y)
                surface.blit(sprite, (sx, sy))

            if not self.dialogue.visible:
                self._render_world_prompts(surface, sway_y)
            render_cassette_atmosphere_filter(surface, self.cassette_id, self.t)

        top_hdr_y = 46 if self.ctx.toggles.get("director_bar_visible") else 16
        self._render_carriage_header(surface, top_hdr_y)

        self.dialogue.render(surface)
        top_off = 44 if self.ctx.toggles.get("director_bar_visible") else 14
        self.walkman.render(
            surface,
            self.cassette_id,
            self.ctx.assets,
            top_offset=top_off,
            unlocked_cassettes=self._unlocked_set(),
        )

        self.plane_game.render(surface)
        self.kintsugi_game.render(surface)
        self.tuner.render(surface, self.cassette_id)
        if self.resonance_banner.active:
            self.resonance_banner.render(surface, self.cutin_banner)

    def _render_world_prompts(self, surface: pygame.Surface, sway_y: int) -> None:
        mpos = pygame.mouse.get_pos()
        f_hint = get_ui_font(13, bold=True)
        prompt: str | None = None
        tx = int(self.player_x)
        ty = int(self.feet_y - 335 + sway_y)

        if not self.harmonized and self.npc_hitbox.collidepoint(mpos):
            ch_lbl = f"Babak {self.chapter_idx + 1}/3"
            prompt = f"Klik: Bicara {self.story.passenger_name.split(' ')[0]} ({ch_lbl})"
            tx, ty = int(self.npc_x), 292
        elif self.harmonized and self.stub_hitbox.collidepoint(mpos):
            prompt = "Klik: Potongan Tiket Bintang & Kenangan"
            tx, ty = int(self.npc_x), 426
        elif self.right_door_zone.collidepoint(mpos) and self.harmonized:
            prompt = "Keluar ke Peron Stasiun Fajar ->" if self.story.is_finale else "Gerbong Berikutnya ->"
            tx, ty = 1140, 172
        elif self.left_door_zone.collidepoint(mpos):
            prompt = "<- Gerbong Sebelumnya"
            tx, ty = 135, 172
        elif self.left_bench_zone.collidepoint(mpos):
            prompt = "Berdiri" if self.is_sitting else "Duduk Santai"
            tx, ty = 295, 375
        else:
            if not self.is_sitting and abs(self.player_x - self.npc_x) < 150:
                if self.harmonized:
                    prompt = f"[E] Lihat Kenangan {self.story.passenger_name.split(' ')[0]}"
                else:
                    prompt = f"[E] Bicara (Babak {self.chapter_idx + 1}/3)"
            else:
                for p_story, prect in self.prop_hitboxes:
                    if prect.collidepoint(mpos) or (not self.is_sitting and abs(self.player_x - p_story.x) < 65 and abs(p_story.y - 450) < 90):
                        prompt = f"[E / Klik] {p_story.title.title()}"
                        tx, ty = int(p_story.x), int(p_story.y) - 34
                        break

        if not prompt and self.harmonized and self.player_x >= 990 and not self.is_sitting:
            prompt = "[E] Keluar ke Peron Stasiun Fajar ->" if self.story.is_finale else "[E] Masuk ke Gerbong Berikutnya ->"
        elif not prompt and self.player_x <= 185 and not self.is_sitting:
            prompt = "[E] <- Kembali ke Gerbong Sebelumnya"
        elif not prompt and not self.is_sitting and abs(self.player_x - self.left_bench_x) < 110:
            prompt = "[E] Duduk di Kursi Pojok"
        elif not prompt and self.is_sitting:
            prompt = "[E / A / D] Berdiri"
            tx, ty = 295, 250

        if prompt:
            tag = f_hint.render(prompt, True, (255, 244, 210))
            bx = max(18, min(self.w - tag.get_width() - 32, tx - tag.get_width() // 2))
            pill = pygame.Surface((tag.get_width() + 20, 26), pygame.SRCALPHA)
            pygame.draw.rect(pill, (16, 18, 28, 210), (0, 0, pill.get_width(), 26), border_radius=6)
            pygame.draw.rect(pill, (*CASSETTES[self.cassette_id].accent, 210), (0, 0, pill.get_width(), 26), 1, border_radius=6)
            surface.blit(pill, (bx - 10, ty - 4))
            surface.blit(tag, (bx, ty))

        if self.harmonized:
            pulse = 180 + int(math.sin(self.t * 4.5) * 65)
            pygame.draw.rect(surface, (pulse, 235, 180), (1128, 190, 8, 290), 2)

    def _render_carriage_header(self, surface: pygame.Surface, top_y: int) -> None:
        accent = CASSETTES[self.cassette_id].accent
        f_hdr = get_ui_font(13, bold=True)
        lbl = "PERON — STASIUN FAJAR" if self.show_dawn_station else self.story.carriage_label
        txt = f_hdr.render(lbl, True, (242, 244, 248))
        pill = pygame.Surface((txt.get_width() + 26, 30), pygame.SRCALPHA)
        pygame.draw.rect(pill, (16, 18, 28, 190), (0, 0, pill.get_width(), 30), border_radius=8)
        pygame.draw.rect(pill, (*accent, 195), (0, 0, pill.get_width(), 30), 1, border_radius=8)
        surface.blit(pill, (18, top_y))
        surface.blit(txt, (31, top_y + 6))

    def _render_finale_card(self, surface: pygame.Surface) -> None:
        """Render serene poetic title over Stasiun Fajar without an arcade scoreboard."""
        f_big = pygame.font.SysFont("georgia,palatino linotype,book antiqua,garamond", 36, bold=True)
        f_sub = get_ui_font(16, serif=True)
        title = "Stasiun Fajar"
        sub = "Kereta telah tiba di pagi yang tenang. Terima kasih sudah berjuang, Raka."

        t_shd = f_big.render(title, True, (18, 24, 34))
        t_main = f_big.render(title, True, (255, 246, 224))
        s_shd = f_sub.render(sub, True, (18, 24, 34))
        s_main = f_sub.render(sub, True, (238, 246, 244))

        cx = 795
        surface.blit(t_shd, (cx - t_main.get_width() // 2 + 2, 108))
        surface.blit(t_main, (cx - t_main.get_width() // 2, 106))
        surface.blit(s_shd, (cx - s_main.get_width() // 2 + 1, 155))
        surface.blit(s_main, (cx - s_main.get_width() // 2, 154))
