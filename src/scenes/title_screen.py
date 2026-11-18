"""Persona-styled Main Menu showcasing sitting Raka, 10-slot Load, and 25-CG Gallery."""

from __future__ import annotations

import math
import random
from typing import Any

import pygame

from src.core.director import BaseScene, DirectorContext
from src.core.persona_ui import (
    CASSETTES,
    get_ui_font,
    load_raka_sitting_layers,
    render_cassette_atmosphere_filter,
    resolve_cassette_video,
)
from src.core.save_and_menus import CGGalleryModal, SaveLoadModal


class TitleScreenScene(BaseScene):
    """Animated sunset ocean carriage with Raka seated on the left & sleek Persona menu."""

    def __init__(self, scene_cfg: dict[str, Any], ctx: DirectorContext) -> None:
        super().__init__(scene_cfg, ctx)
        self.w, self.h = ctx.screen_size
        self.t = 0.0
        self.selected = 0
        self.video = None
        self.sitting_overlay: pygame.Surface | None = None
        self.hitboxes: list[tuple[int, pygame.Rect]] = []
        self.save_modal = SaveLoadModal(ctx.assets)
        self.gallery_modal = CGGalleryModal(ctx.assets, (self.w, self.h))
        self._right_scrim: pygame.Surface | None = None
        self.particles = [
            [random.uniform(0, self.w * 0.65), random.uniform(80, self.h - 140), random.uniform(14, 34), random.randint(2, 4)]
            for _ in range(24)
        ]
        self.menu_items = [
            ("start_new", "Mulai Cerita Baru"),
            ("load_game", "Lanjutkan Cerita"),
            ("gallery", "Galeri Kenangan"),
            ("quit", "Keluar"),
        ]

    def on_enter(self) -> None:
        self._load_assets()
        self.ctx.assets.play_bgm(
            CASSETTES[1].bgm_rel,
            track_title="SIDE A: Senja — Main Menu",
        )

    def on_hot_reload(self) -> None:
        self._load_assets()

    def _load_assets(self) -> None:
        self.video = resolve_cassette_video(self.ctx.assets, 1)
        self.sitting_overlay = load_raka_sitting_layers(self.ctx.assets, (self.w, self.h))[1]
        scrim = pygame.Surface((620, self.h), pygame.SRCALPHA)
        for x in range(620):
            alpha = int(min(218, max(0, (x / 220.0) * 195)))
            pygame.draw.line(scrim, (10, 12, 20, alpha), (x, 0), (x, self.h))
        self._right_scrim = scrim

    def _activate_item(self, idx: int) -> str | None:
        action_id, _ = self.menu_items[idx]
        self.ctx.assets.play_sfx("click", volume=0.28)
        if action_id == "start_new":
            return "new_game"
        if action_id == "load_game":
            self.save_modal.open("load")
            return None
        if action_id == "gallery":
            self.gallery_modal.open()
            return None
        if action_id == "quit":
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        return None

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.gallery_modal.active:
            self.gallery_modal.handle_event(event)
            return None

        if self.save_modal.active:
            res = self.save_modal.handle_event(event, current_save_data=self.ctx.save_data)
            if res is not None and res[0] == "loaded":
                self.ctx.save_data.clear()
                self.ctx.save_data.update(res[1])
                return "reload_save"
            return None

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.menu_items)
                self.ctx.assets.play_sfx("click", volume=0.14)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.menu_items)
                self.ctx.assets.play_sfx("click", volume=0.14)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self._activate_item(self.selected)
        elif event.type == pygame.MOUSEMOTION:
            for idx, rect in self.hitboxes:
                if rect.collidepoint(event.pos):
                    self.selected = idx
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, rect in self.hitboxes:
                if rect.collidepoint(event.pos):
                    return self._activate_item(idx)
        return None

    def update(self, dt: float) -> str | None:
        self.t += dt
        if self.video is not None:
            self.video.update(dt)
        if self.gallery_modal.active:
            self.gallery_modal.update(dt)
        for p in self.particles:
            p[0] = (p[0] - p[2] * dt) % self.w
            p[1] = 80.0 + ((p[1] + math.sin(self.t + p[0] * 0.01) * 7.0 * dt) % (self.h - 220.0))
        return None

    def render(self, surface: pygame.Surface) -> None:
        if self.video is not None:
            surface.blit(self.video.get_surface(), (0, 0))
        else:
            surface.fill((24, 18, 28))

        sway_y = int(round(math.sin(self.t * 4.2) * 1.4)) if self.ctx.toggles.get("slow_cozy_sway", True) else 0
        if self.sitting_overlay is not None:
            surface.blit(self.sitting_overlay, (0, sway_y))

        accent = CASSETTES[1].accent
        for px, py, _, sz in self.particles:
            pygame.draw.rect(surface, accent, (int(px), int(py) + sway_y, sz, sz))

        render_cassette_atmosphere_filter(surface, 1, self.t)

        # Clean translucent backdrop strictly on the right menu column (leaves sitting Raka unobstructed)
        if self._right_scrim is not None:
            surface.blit(self._right_scrim, (self.w - 620, 0))

        # Stylized Persona header (clean serif display, no Track 99 // tag)
        f_title = pygame.font.SysFont("georgia,palatino linotype,book antiqua,garamond", 46, bold=True)
        f_sub = pygame.font.SysFont("georgia,palatino linotype,book antiqua,garamond", 22, bold=True)
        f_btn = get_ui_font(18, bold=True)
        f_hint = get_ui_font(13)

        menu_x = 696
        title_y = 88

        t_str = "GERBONG TERAKHIR"
        surface.blit(f_title.render(t_str, True, (8, 10, 16)), (menu_x + 3, title_y + 3))
        surface.blit(f_title.render(t_str, True, (254, 246, 232)), (menu_x, title_y))

        s_str = "KE STASIUN SENJA"
        surface.blit(f_sub.render(s_str, True, (8, 10, 16)), (menu_x + 3, title_y + 60))
        surface.blit(f_sub.render(s_str, True, accent), (menu_x, title_y + 58))

        # Clean golden-crimson ornamental rule with center diamond
        line_y = title_y + 98
        pygame.draw.polygon(
            surface,
            (232, 74, 88),
            [(menu_x, line_y), (menu_x + 480, line_y - 5), (menu_x + 472, line_y + 1), (menu_x - 6, line_y + 6)],
        )
        cx_orn = menu_x + 236
        pygame.draw.polygon(
            surface,
            accent,
            [(cx_orn, line_y - 6), (cx_orn + 8, line_y + 1), (cx_orn, line_y + 8), (cx_orn - 8, line_y + 1)],
        )

        self.hitboxes.clear()
        btn_y0 = 236
        btn_w = 500
        btn_h = 58
        for idx, (_aid, label) in enumerate(self.menu_items):
            y = btn_y0 + idx * 74
            is_sel = idx == self.selected
            x_shift = -14 if is_sel else 0
            rect = pygame.Rect(menu_x + x_shift, y, btn_w, btn_h)
            self.hitboxes.append((idx, rect))

            pts = [
                (rect.left + 16, rect.top),
                (rect.right, rect.top - 4),
                (rect.right - 16, rect.bottom),
                (rect.left, rect.bottom + 4),
            ]
            pygame.draw.polygon(surface, (8, 10, 16), [(px + 5, py + 5) for px, py in pts])
            fill = accent if is_sel else (20, 24, 34)
            border = (255, 244, 210) if is_sel else (112, 122, 148)
            txt_col = (14, 16, 22) if is_sel else (238, 242, 248)
            pygame.draw.polygon(surface, fill, pts)
            pygame.draw.polygon(surface, border, pts, 2)

            if is_sel:
                dx_m = rect.left + 32
                dy_m = rect.centery
                pygame.draw.polygon(
                    surface,
                    (18, 20, 28),
                    [(dx_m - 6, dy_m - 6), (dx_m + 6, dy_m), (dx_m - 6, dy_m + 6)],
                )

            t_surf = f_btn.render(label, True, txt_col)
            surface.blit(t_surf, (rect.left + 52, rect.centery - t_surf.get_height() // 2))

        hint = f_hint.render("↑ / ↓ atau Mouse: Pilih   |   SPACE / Klik: Konfirmasi", True, (206, 214, 228))
        surface.blit(hint, (self.w - hint.get_width() - 42, self.h - 46))

        if self.save_modal.active:
            self.save_modal.render(surface)
        elif self.gallery_modal.active:
            self.gallery_modal.render(surface)
