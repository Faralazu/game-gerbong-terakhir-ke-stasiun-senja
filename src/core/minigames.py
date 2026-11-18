"""Relaxing narrative mini-games for Gerbong 4 (Paper Plane) and Gerbong 2 (Kintsugi Sketchbook)."""

from __future__ import annotations

import math
import random
from typing import Any

import pygame

from src.core.persona_ui import CASSETTES, get_ui_font


class PaperPlaneGlideModal:
    """Cozy mini-game: guide Bima's paper airplane through 5 golden breeze memories."""

    def __init__(self) -> None:
        self.active = False
        self.t = 0.0
        self.plane_y = 330.0
        self.target_y = 330.0
        self.plane_vy = 0.0
        self.collected = 0
        self.goal = 5
        self.orbs: list[list[float]] = []
        self.trail: list[tuple[float, float]] = []

    def open(self) -> None:
        self.active = True
        self.t = 0.0
        self.plane_y = 330.0
        self.target_y = 330.0
        self.plane_vy = 0.0
        self.collected = 0
        self.trail.clear()
        self.orbs = [
            [920.0 + i * 210.0, float(random.randint(205, 445)), 1.0]
            for i in range(self.goal + 3)
        ]

    def close(self) -> None:
        self.active = False

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if not self.active:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return "cancel"
            if event.key == pygame.K_TAB:
                self.collected = self.goal
                self.close()
                return "solved"
        elif event.type == pygame.MOUSEMOTION:
            self.target_y = max(180.0, min(480.0, float(event.pos[1])))
        return None

    def update(self, dt: float) -> str | None:
        if not self.active:
            return None
        self.t += dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.target_y = max(180.0, self.target_y - 280.0 * dt)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.target_y = min(480.0, self.target_y + 280.0 * dt)

        self.plane_y += (self.target_y - self.plane_y) * min(1.0, dt * 6.5)
        plane_x = 340.0
        self.trail.append((plane_x - 18, self.plane_y))
        if len(self.trail) > 18:
            self.trail.pop(0)

        for idx, orb in enumerate(self.orbs):
            orb[0] -= 235.0 * dt
            orb[1] += math.sin(self.t * 3.0 + idx) * 28.0 * dt
            if orb[2] > 0.5 and math.hypot(orb[0] - plane_x, orb[1] - self.plane_y) < 38.0:
                orb[2] = 0.0
                self.collected += 1
                if self.collected >= self.goal:
                    self.close()
                    return "solved"
            if orb[0] < 150.0:
                orb[0] = 1100.0 + random.uniform(40, 180)
                orb[1] = float(random.randint(205, 445))
                orb[2] = 1.0
        return None

    def render(self, surface: pygame.Surface) -> None:
        if not self.active:
            return
        w, h = surface.get_size()
        dim = pygame.Surface((w, h), pygame.SRCALPHA)
        dim.fill((10, 12, 20, 195))
        surface.blit(dim, (0, 0))

        accent = CASSETTES[1].accent
        panel = pygame.Rect(140, 108, 1000, 460)
        pygame.draw.rect(surface, (24, 22, 32), panel, border_radius=12)
        pygame.draw.rect(surface, accent, panel, 3, border_radius=12)

        f_title = get_ui_font(22, bold=True)
        f_sub = get_ui_font(15)
        surface.blit(f_title.render("TERBANGKAN PESAWAT KERTAS BIMA", True, accent), (176, 130))
        surface.blit(
            f_sub.render(
                f"Gerakkan kursor / [W/S] untuk menangkap {self.collected}/{self.goal} cahaya kenangan   ([TAB] Lewati Santai)",
                True,
                (230, 234, 244),
            ),
            (176, 162),
        )

        sky = pygame.Rect(176, 196, 928, 300)
        pygame.draw.rect(surface, (46, 32, 48), sky, border_radius=8)
        pygame.draw.rect(surface, (248, 166, 72), sky, 2, border_radius=8)

        # Gentle breeze ribbon trail
        if len(self.trail) >= 2:
            pygame.draw.lines(surface, (255, 228, 170), False, [(int(x), int(y)) for x, y in self.trail], 2)

        # Memory orbs
        for ox, oy, alive in self.orbs:
            if alive > 0.5 and sky.left + 16 <= ox <= sky.right - 16:
                pygame.draw.circle(surface, (255, 220, 120), (int(ox), int(oy)), 12)
                pygame.draw.circle(surface, (255, 250, 225), (int(ox), int(oy)), 6)

        # Paper airplane sprite polygon
        px, py = 340, int(self.plane_y)
        plane_pts = [(px + 26, py), (px - 20, py - 14), (px - 10, py), (px - 20, py + 14)]
        pygame.draw.polygon(surface, (246, 248, 255), plane_pts)
        pygame.draw.polygon(surface, (185, 195, 215), plane_pts, 2)
        pygame.draw.line(surface, (165, 175, 195), (px - 10, py), (px + 26, py), 2)

        surface.blit(
            f_sub.render("Tip: Jangan takut jatuh—di sini anginnya selalu menopang.", True, (195, 205, 220)),
            (176, 518),
        )


class SketchbookKintsugiModal:
    """Cozy Kintsugi puzzle: mend 4 torn sketchbook fragments with golden lines."""

    def __init__(self) -> None:
        self.active = False
        self.t = 0.0
        self.placed = [False, False, False, False]
        self.selected_idx: int | None = None
        self.tray_rects: list[pygame.Rect] = []
        self.slot_rects: list[pygame.Rect] = []

    def open(self) -> None:
        self.active = True
        self.t = 0.0
        self.placed = [False, False, False, False]
        self.selected_idx = 0

    def close(self) -> None:
        self.active = False

    def _place_piece(self, idx: int) -> str | None:
        self.placed[idx] = True
        # Auto-select next unplaced piece
        self.selected_idx = next((i for i, p in enumerate(self.placed) if not p), None)
        if all(self.placed):
            self.close()
            return "solved"
        return None

    def handle_event(self, event: pygame.event.Event) -> tuple[str, Any] | None:
        if not self.active:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return ("cancel", None)
            if event.key == pygame.K_TAB:
                self.placed = [True, True, True, True]
                self.close()
                return ("solved", None)
            if pygame.K_1 <= event.key <= pygame.K_4:
                idx = event.key - pygame.K_1
                res = self._place_piece(idx)
                return ("solved", None) if res == "solved" else ("placed", idx)
            if event.key in (pygame.K_SPACE, pygame.K_RETURN) and self.selected_idx is not None:
                idx = self.selected_idx
                res = self._place_piece(idx)
                return ("solved", None) if res == "solved" else ("placed", idx)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, rect in enumerate(self.tray_rects):
                if rect.collidepoint(event.pos) and not self.placed[idx]:
                    self.selected_idx = idx
                    return ("select", idx)
            for idx, rect in enumerate(self.slot_rects):
                if rect.collidepoint(event.pos) and not self.placed[idx]:
                    res = self._place_piece(idx)
                    return ("solved", None) if res == "solved" else ("placed", idx)
        return None

    def update(self, dt: float) -> None:
        self.t += dt

    def render(self, surface: pygame.Surface) -> None:
        if not self.active:
            return
        w, h = surface.get_size()
        dim = pygame.Surface((w, h), pygame.SRCALPHA)
        dim.fill((10, 12, 20, 200))
        surface.blit(dim, (0, 0))

        accent = CASSETTES[2].accent
        gold = (248, 205, 102)
        panel = pygame.Rect(160, 96, 960, 480)
        pygame.draw.rect(surface, (20, 24, 34), panel, border_radius=12)
        pygame.draw.rect(surface, accent, panel, 3, border_radius=12)

        f_title = get_ui_font(22, bold=True)
        f_sub = get_ui_font(15)
        f_piece = get_ui_font(15, bold=True, serif=True)

        surface.blit(f_title.render("KINTSUGI SKETSA — MENYAMBUNG JATI DIRI", True, gold), (196, 118))
        done_n = sum(1 for p in self.placed if p)
        surface.blit(
            f_sub.render(
                f"Klik bagian sketsa yang kosong atau tekan [1-4] / [SPACE] untuk menyambungnya ({done_n}/4)  |  [TAB] Auto",
                True,
                (228, 234, 246),
            ),
            (196, 150),
        )

        # 2x2 torn sketchbook board on left
        self.slot_rects.clear()
        labels = [
            "1. Garis Peron Senja",
            "2. Dua Cangkir Teh",
            "3. Senyum Sahabat",
            "4. Tanda Tangan: Raka",
        ]
        board_x, board_y = 220, 198
        pw, ph = 205, 145
        for idx in range(4):
            col = idx % 2
            row = idx // 2
            rect = pygame.Rect(board_x + col * (pw + 12), board_y + row * (ph + 12), pw, ph)
            self.slot_rects.append(rect)
            if self.placed[idx]:
                pygame.draw.rect(surface, (238, 230, 214), rect, border_radius=4)
                pygame.draw.rect(surface, gold, rect, 3, border_radius=4)
                lbl = f_piece.render(labels[idx], True, (36, 32, 30))
                surface.blit(lbl, (rect.centerx - lbl.get_width() // 2, rect.centery - lbl.get_height() // 2))
            else:
                pygame.draw.rect(surface, (28, 32, 46), rect, border_radius=4)
                pygame.draw.rect(surface, accent, rect, 2, border_radius=4)
                lbl = f_sub.render(f"Klik Slot [{idx + 1}]", True, (150, 175, 210))
                surface.blit(lbl, (rect.centerx - lbl.get_width() // 2, rect.centery - lbl.get_height() // 2))

        # Golden Kintsugi seams when adjacent pieces connect
        if self.placed[0] and self.placed[1]:
            pygame.draw.line(surface, gold, (board_x + pw + 6, board_y + 12), (board_x + pw + 6, board_y + ph - 12), 4)
        if self.placed[2] and self.placed[3]:
            pygame.draw.line(surface, gold, (board_x + pw + 6, board_y + ph + 24), (board_x + pw + 6, board_y + ph * 2), 4)
        if self.placed[0] and self.placed[2]:
            pygame.draw.line(surface, gold, (board_x + 12, board_y + ph + 6), (board_x + pw - 12, board_y + ph + 6), 4)
        if self.placed[1] and self.placed[3]:
            pygame.draw.line(surface, gold, (board_x + pw + 24, board_y + ph + 6), (board_x + pw * 2, board_y + ph + 6), 4)

        # Fragment tray on right
        self.tray_rects.clear()
        tx = 695
        for idx, text in enumerate(labels):
            ty = 204 + idx * 76
            rect = pygame.Rect(tx, ty, 360, 62)
            self.tray_rects.append(rect)
            is_sel = idx == self.selected_idx and not self.placed[idx]
            fill = (52, 62, 82) if is_sel else ((36, 46, 42) if self.placed[idx] else (30, 34, 46))
            border = gold if (is_sel or self.placed[idx]) else accent
            pygame.draw.rect(surface, fill, rect, border_radius=6)
            pygame.draw.rect(surface, border, rect, 2, border_radius=6)
            status = "TERPASANG" if self.placed[idx] else f"[{idx + 1}] Pasang Potongan"
            surface.blit(f_piece.render(text, True, (242, 240, 234)), (rect.left + 16, rect.top + 10))
            surface.blit(f_sub.render(status, True, gold if self.placed[idx] else (165, 200, 235)), (rect.left + 16, rect.top + 34))
