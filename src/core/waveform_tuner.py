"""Interactive Persona-styled Waveform Tuner mini-game for harmonizing passenger hearts."""

from __future__ import annotations

import math
from typing import Any

import pygame

from src.core.persona_ui import CASSETTES, get_ui_font


class WaveformTunerModal:
    """Modal puzzle where the player aligns cassette, frequency, and amplitude to resonate."""

    def __init__(self) -> None:
        self.active = False
        self.passenger_name = ""
        self.target_freq = 2.4
        self.target_amp = 48.0
        self.required_cassette = 1
        self.cassette_hint = ""

        self.player_freq = 1.2
        self.player_amp = 24.0
        self.resonance_gauge = 0.0
        self.t = 0.0
        self.auto_tuning = False
        self.cassette_buttons: list[tuple[int, pygame.Rect]] = []
        self.autotune_rect = pygame.Rect(0, 0, 0, 0)

        # Water droplet ripple animation state on cassette switch
        self.ripples: list[dict[str, Any]] = []
        self.wave_disturb_t: float = 0.0
        self.wave_disturb_col: tuple[int, int, int] = (248, 174, 84)

    def open(
        self,
        passenger_name: str,
        required_cassette: int,
        target_freq: float,
        target_amp: float,
        cassette_hint: str,
    ) -> None:
        self.active = True
        self.passenger_name = passenger_name
        self.required_cassette = required_cassette
        self.target_freq = target_freq
        self.target_amp = target_amp
        self.cassette_hint = cassette_hint
        self.player_freq = 1.1 if target_freq > 2.0 else 3.8
        self.player_amp = 22.0 if target_amp > 42.0 else 72.0
        self.resonance_gauge = 0.0
        self.auto_tuning = False
        self.ripples.clear()
        self.wave_disturb_t = 0.0

    def close(self) -> None:
        self.active = False
        self.auto_tuning = False
        self.ripples.clear()
        self.wave_disturb_t = 0.0

    def trigger_ripple(self, cid: int, pos: tuple[int, int] | None = None) -> None:
        """Spawn concentric water-droplet rings and perturb the oscilloscope wave."""
        prof = CASSETTES.get(cid, CASSETTES[1])
        col = prof.accent
        btn_pos = pos
        if btn_pos is None:
            for b_cid, rect in self.cassette_buttons:
                if b_cid == cid:
                    btn_pos = rect.center
                    break
        if btn_pos is not None:
            self.ripples.append({"x": btn_pos[0], "y": btn_pos[1], "age": 0.0, "dur": 0.72, "max_r": 96.0, "col": col})
        # Large calm droplet ripple inside the center of the oscilloscope pool
        self.ripples.append({"x": 638, "y": 279, "age": 0.0, "dur": 0.92, "max_r": 210.0, "col": col})
        self.wave_disturb_t = 1.0
        self.wave_disturb_col = col

    def compute_sync_ratio(self, current_cassette: int) -> float:
        """Compute instantaneous 0.0..1.0 alignment between player and passenger waves."""
        freq_score = max(0.0, 1.0 - abs(self.player_freq - self.target_freq) / 2.2)
        amp_score = max(0.0, 1.0 - abs(self.player_amp - self.target_amp) / 48.0)
        cassette_score = 1.0 if current_cassette == self.required_cassette else 0.25
        return max(
            0.0,
            min(1.0, (0.45 * freq_score + 0.45 * amp_score) * cassette_score + (0.10 if current_cassette == self.required_cassette else 0.0)),
        )

    def handle_event(self, event: pygame.event.Event) -> tuple[str, Any] | None:
        """Handle modal input. Returns ('cassette', cid), ('cancel', None), or None."""
        if not self.active:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return ("cancel", None)
            if event.key == pygame.K_TAB:
                self.auto_tuning = True
                self.trigger_ripple(self.required_cassette)
                return ("cassette", self.required_cassette)
            if pygame.K_1 <= event.key <= pygame.K_4:
                cid = event.key - pygame.K_0
                self.trigger_ripple(cid)
                return ("cassette", cid)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.autotune_rect.collidepoint(event.pos):
                self.auto_tuning = True
                self.trigger_ripple(self.required_cassette, event.pos)
                return ("cassette", self.required_cassette)
            for cid, rect in self.cassette_buttons:
                if rect.collidepoint(event.pos):
                    self.trigger_ripple(cid, rect.center)
                    return ("cassette", cid)
        return None

    def update(self, dt: float, current_cassette: int) -> str | None:
        """Advance tuner state. Returns 'solved' once gauge hits 100%."""
        if not self.active:
            return None
        self.t += dt
        if self.wave_disturb_t > 0.0:
            self.wave_disturb_t = max(0.0, self.wave_disturb_t - dt * 1.10)
        if self.ripples:
            for r in self.ripples:
                r["age"] += dt
            self.ripples = [r for r in self.ripples if r["age"] < r["dur"]]

        if self.auto_tuning:
            self.player_freq += (self.target_freq - self.player_freq) * min(1.0, dt * 4.5)
            self.player_amp += (self.target_amp - self.player_amp) * min(1.0, dt * 4.5)
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player_freq = max(0.8, self.player_freq - 1.65 * dt)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player_freq = min(4.8, self.player_freq + 1.65 * dt)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player_amp = max(14.0, self.player_amp - 42.0 * dt)
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player_amp = min(82.0, self.player_amp + 42.0 * dt)

        sync = self.compute_sync_ratio(current_cassette)
        if current_cassette == self.required_cassette and sync >= 0.88:
            self.resonance_gauge = min(1.0, self.resonance_gauge + dt * 1.15)
            if self.resonance_gauge >= 1.0:
                self.close()
                return "solved"
        else:
            self.resonance_gauge = max(0.0, self.resonance_gauge - dt * 0.45)
        return None

    def _render_ripples(self, surface: pygame.Surface, scope_rect: pygame.Rect) -> None:
        if not self.ripples:
            return
        w, h = surface.get_size()
        layer = pygame.Surface((w, h), pygame.SRCALPHA)
        for r in self.ripples:
            p = min(1.0, r["age"] / max(0.05, r["dur"]))
            eased = 1.0 - (1.0 - p) ** 2.4
            col = r["col"]
            # Render 3 cascading concentric droplet rings
            for ring_i in range(3):
                sub_p = p - ring_i * 0.14
                if sub_p <= 0.0:
                    continue
                rad = max(4, int(eased * r["max_r"] * (1.0 - ring_i * 0.22)))
                alpha = int(max(0, 195 * (1.0 - sub_p) * (1.0 - ring_i * 0.22)))
                if alpha <= 0:
                    continue
                width = max(1, int(3 - ring_i))
                if r["y"] == scope_rect.centery:
                    # Clip subtly inside scope rect vertically via horizontal oval ripple
                    ov = pygame.Rect(r["x"] - rad, r["y"] - int(rad * 0.44), rad * 2, int(rad * 0.88))
                    if scope_rect.colliderect(ov):
                        pygame.draw.ellipse(layer, (*col, alpha), ov, width)
                else:
                    pygame.draw.circle(layer, (*col, alpha), (r["x"], r["y"]), rad, width)
            # Small radial water droplet flecks
            if p < 0.75:
                d_alpha = int(210 * (1.0 - p / 0.75))
                for di in range(8):
                    ang = di * (math.pi / 4.0) + r["age"] * 0.6
                    dist = 8.0 + eased * min(64.0, r["max_r"] * 0.42)
                    dx = int(r["x"] + math.cos(ang) * dist)
                    dy = int(r["y"] + math.sin(ang) * dist * (0.45 if r["y"] == scope_rect.centery else 0.75))
                    pygame.draw.circle(layer, (*col, d_alpha), (dx, dy), 2)
        surface.blit(layer, (0, 0))

    def render(self, surface: pygame.Surface, current_cassette: int) -> None:
        if not self.active:
            return
        w, h = surface.get_size()
        dim = pygame.Surface((w, h), pygame.SRCALPHA)
        dim.fill((8, 10, 16, 200))
        surface.blit(dim, (0, 0))

        accent = CASSETTES[current_cassette].accent
        req_accent = CASSETTES[self.required_cassette].accent
        panel_pts = [(140, 86), (1152, 72), (1126, 560), (116, 570)]
        pygame.draw.polygon(surface, (6, 6, 10), [(x + 10, y + 10) for x, y in panel_pts])
        pygame.draw.polygon(surface, (18, 20, 28), panel_pts)
        pygame.draw.polygon(surface, accent, panel_pts, 4)

        f_big = get_ui_font(24, bold=True)
        f_mid = get_ui_font(16, bold=True)
        f_small = get_ui_font(13, bold=True)

        surface.blit(
            f_big.render(f"WAVEFORM TUNER — {self.passenger_name.upper()}", True, accent),
            (172, 104),
        )
        surface.blit(
            f_small.render(f"Petunjuk Emosi: {self.cassette_hint}", True, (225, 232, 244)),
            (172, 140),
        )

        # Oscilloscope window
        scope = pygame.Rect(172, 174, 932, 210)
        pygame.draw.rect(surface, (10, 12, 18), scope)
        pygame.draw.rect(surface, (52, 58, 76), scope, 2)
        pygame.draw.line(surface, (40, 46, 62), (scope.left, scope.centery), (scope.right, scope.centery), 1)

        # Target wave (passenger emotion) and Player wave (with droplet ripple perturbation on cassette swap)
        target_pts: list[tuple[int, int]] = []
        player_pts: list[tuple[int, int]] = []
        steps = 110
        for i in range(steps + 1):
            frac = i / steps
            px = int(scope.left + frac * scope.width)
            py_target = int(
                scope.centery
                + math.sin(frac * math.pi * 2.0 * self.target_freq - self.t * 3.0) * self.target_amp
            )
            ripple_dy = 0.0
            if self.wave_disturb_t > 0.0:
                dist_c = abs(frac - 0.5)
                ripple_dy = (
                    math.sin(dist_c * 30.0 - self.t * 16.0)
                    * math.exp(-dist_c * 4.5)
                    * 16.0
                    * self.wave_disturb_t
                )
            py_player = int(
                max(
                    scope.top + 8,
                    min(
                        scope.bottom - 8,
                        scope.centery
                        + math.sin(frac * math.pi * 2.0 * self.player_freq - self.t * 3.0) * self.player_amp
                        + ripple_dy,
                    ),
                )
            )
            target_pts.append((px, py_target))
            player_pts.append((px, py_player))

        pygame.draw.lines(surface, req_accent, False, target_pts, 3)
        sync = self.compute_sync_ratio(current_cassette)
        player_col = (255, 240, 130) if (current_cassette == self.required_cassette and sync >= 0.88) else (245, 248, 255)
        pygame.draw.lines(surface, player_col, False, player_pts, 4)

        # Cassette quick selector inside modal
        self.cassette_buttons.clear()
        bx = 172
        by = 404
        for cid in (1, 2, 3, 4):
            prof = CASSETTES[cid]
            rect = pygame.Rect(bx, by, 156, 38)
            self.cassette_buttons.append((cid, rect))
            is_cur = cid == current_cassette
            fill = prof.accent if is_cur else (32, 34, 46)
            fg = (14, 14, 18) if is_cur else (232, 236, 244)
            pygame.draw.rect(surface, fill, rect, border_radius=4)
            pygame.draw.rect(surface, prof.accent, rect, 2, border_radius=4)
            lbl = f_small.render(f"[{cid}] {prof.title.split(' ')[0]}", True, fg)
            surface.blit(lbl, (rect.centerx - lbl.get_width() // 2, rect.centery - lbl.get_height() // 2))
            bx += 168

        # Render cascading water droplet ripples above oscilloscope & buttons
        self._render_ripples(surface, scope)

        # Auto-Tune Assist button for relaxed play
        self.autotune_rect = pygame.Rect(872, 404, 232, 38)
        pygame.draw.rect(surface, (42, 68, 72), self.autotune_rect, border_radius=4)
        pygame.draw.rect(surface, (145, 232, 195), self.autotune_rect, 2, border_radius=4)
        auto_lbl = f_small.render("[TAB] AUTO-TUNE SANTAI", True, (220, 255, 240))
        surface.blit(
            auto_lbl,
            (self.autotune_rect.centerx - auto_lbl.get_width() // 2, self.autotune_rect.centery - auto_lbl.get_height() // 2),
        )

        # Sync & Resonance Gauge
        sync_pct = int(sync * 100)
        gauge_pct = int(self.resonance_gauge * 100)
        surface.blit(
            f_mid.render(
                f"SYNC: {sync_pct:3d}%  |  RESONANCE LOCK: {gauge_pct:3d}%",
                True,
                (255, 236, 150) if sync >= 0.88 else (235, 240, 248),
            ),
            (172, 462),
        )
        bar_bg = pygame.Rect(172, 492, 932, 22)
        pygame.draw.rect(surface, (28, 30, 42), bar_bg)
        fill_w = int(bar_bg.width * self.resonance_gauge)
        if fill_w > 0:
            pygame.draw.rect(surface, req_accent, (bar_bg.left, bar_bg.top, fill_w, bar_bg.height))
        pygame.draw.rect(surface, accent, bar_bg, 2)

        controls_txt = "[A/D] Frekuensi   [W/S] Amplitudo   [1-4] Pilih Kaset   [TAB] Auto-Tune   [ESC] Tutup"
        surface.blit(f_small.render(controls_txt, True, (195, 204, 218)), (172, 526))
