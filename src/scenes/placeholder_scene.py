"""Reusable placeholder scene for prototyping upcoming carriages before art is final."""

from __future__ import annotations

import pygame

from src.core.director import BaseScene
from src.core.persona_ui import get_ui_font


class PlaceholderCarriageScene(BaseScene):
    """Lightweight modular carriage template for testing pacing and narrative beats."""

    def __init__(self, scene_cfg: dict, ctx) -> None:
        super().__init__(scene_cfg, ctx)
        self.t = 0.0
        self.video = None

    def on_enter(self) -> None:
        self.video = self.ctx.assets.get_video(
            "videos/vid_02_window_sunset_loop.mp4",
            fallback_style="dawn" if "dawn" in self.cfg["id"] else "rain",
            size=self.ctx.screen_size,
        )
        self.ctx.assets.play_bgm(
            "audio/bgm/bgm_04_acceptance_finale.mp3"
            if "dawn" in self.cfg["id"]
            else "audio/bgm/bgm_02_denial_rain.mp3",
            track_title=self.cfg["title"],
        )

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return "next_scene"
        return None

    def update(self, dt: float) -> None:
        self.t += dt
        if self.video:
            self.video.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        if self.video:
            surface.blit(self.video.get_surface(), (0, 0))
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((12, 14, 22, 175))
        surface.blit(overlay, (0, 0))

        # Persona-style slanted title card
        pygame.draw.polygon(
            surface,
            (20, 20, 28),
            [(140, 210), (w - 110, 185), (w - 150, 440), (100, 465)],
        )
        pygame.draw.polygon(
            surface,
            (230, 52, 68),
            [(140, 210), (w - 110, 185), (w - 150, 440), (100, 465)],
            3,
        )

        f_big = get_ui_font(32, bold=True)
        f_mid = get_ui_font(18)
        f_small = get_ui_font(15)

        title = f_big.render(self.cfg["title"], True, (255, 232, 165))
        notes = f_mid.render(f"Fokus Pacing: {self.cfg.get('notes', '')}", True, (235, 240, 248))
        budget = f_mid.render(
            f"Target Durasi Babak Ini: {self.cfg.get('target_minutes', 10):.0f} menit",
            True,
            (130, 220, 255),
        )
        hint = f_small.render(
            "Tekan '[' untuk kembali ke Gerbong 5, ']' atau ENTER untuk lanjut.",
            True,
            (200, 200, 210),
        )
        surface.blit(title, (180, 245))
        surface.blit(notes, (180, 305))
        surface.blit(budget, (180, 342))
        surface.blit(hint, (180, 395))
