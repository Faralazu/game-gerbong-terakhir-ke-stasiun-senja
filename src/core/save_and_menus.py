"""10-slot Save/Load manager, Pause Menu, and 25-CG Gallery modal."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pygame

from src.core import paths
from src.core.cg_cutscene import (
    ALL_CG_SLIDES,
    WutheringWavesCGOverlay,
    load_unlocked_gallery,
    unlock_all_cgs_in_gallery,
)
from src.core.persona_ui import CASSETTES, get_ui_font


SCENE_LABELS: dict[str, str] = {
    "gerbong_5_intro": "Gerbong 5 — Keheningan",
    "gerbong_4_childhood": "Gerbong 4 — Bima & Pesawat",
    "gerbong_3_burnout": "Gerbong 3 — Nadia & Waktu",
    "gerbong_2_crossroads": "Gerbong 2 — Bayangan Diri",
    "gerbong_1_dawn": "Gerbong 1 — Senja & Fajar",
}


def get_save_slot_info(slot_idx: int) -> dict[str, Any] | None:
    """Return metadata dict for slot_1..slot_10, or None if empty."""
    slot_file = paths.SAVES_DIR / f"slot_{slot_idx}.json"
    if not slot_file.exists():
        return None
    data = paths.read_json(slot_file, default={})
    if not isinstance(data, dict) or not data.get("saved_at"):
        # Legacy default slot without explicit player save timestamp
        if slot_idx == 1 and float(data.get("elapsed_total_seconds", 0.0)) > 1.0:
            return data
        return None
    return data


def save_game_to_slot(slot_idx: int, save_data: dict[str, Any]) -> dict[str, Any]:
    """Persist current playable progress into slot_<idx>.json inside userdata/saves/."""
    payload = dict(save_data)
    scene_id = str(payload.get("resume_scene") or payload.get("current_scene") or "gerbong_5_intro")
    if scene_id == "title_screen":
        scene_id = "gerbong_5_intro"
    payload["slot"] = f"slot_{slot_idx}"
    payload["current_scene"] = scene_id
    payload["resume_scene"] = scene_id
    payload["carriage_title"] = SCENE_LABELS.get(scene_id, scene_id)
    payload["saved_at"] = datetime.now().strftime("%d %b %Y, %H:%M")
    paths.write_save(payload, slot=f"slot_{slot_idx}")
    return payload


def load_game_from_slot(slot_idx: int) -> dict[str, Any] | None:
    """Load saved progress from slot_<idx>.json if populated."""
    info = get_save_slot_info(slot_idx)
    if info is None:
        return None
    return dict(info)


class SaveLoadModal:
    """Clean 10-slot Save / Load grid modal."""

    def __init__(self, assets: Any) -> None:
        self.assets = assets
        self.active = False
        self.mode = "load"  # "save" or "load"
        self.slot_rects: list[tuple[int, pygame.Rect]] = []
        self.close_rect = pygame.Rect(1040, 86, 120, 38)
        self._slots_cache: dict[int, dict[str, Any] | None] = {}

    def open(self, mode: str = "load") -> None:
        self.mode = mode
        self.active = True
        self.refresh()

    def refresh(self) -> None:
        self._slots_cache = {idx: get_save_slot_info(idx) for idx in range(1, 11)}

    def close(self) -> None:
        self.active = False

    def handle_event(
        self,
        event: pygame.event.Event,
        current_save_data: dict[str, Any] | None = None,
    ) -> tuple[str, Any] | None:
        """Return ('saved', slot_idx), ('loaded', dict), ('closed', None), or None."""
        if not self.active:
            return None

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.close()
            return ("closed", None)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.close_rect.collidepoint(event.pos):
                self.assets.play_sfx("click", volume=0.22)
                self.close()
                return ("closed", None)

            for slot_idx, rect in self.slot_rects:
                if rect.collidepoint(event.pos):
                    if self.mode == "save" and current_save_data is not None:
                        saved = save_game_to_slot(slot_idx, current_save_data)
                        self.assets.play_sfx("chime", volume=0.26)
                        self.refresh()
                        return ("saved", (slot_idx, saved))
                    if self.mode == "load":
                        loaded = load_game_from_slot(slot_idx)
                        if loaded is not None:
                            self.assets.play_sfx("click", volume=0.30)
                            self.close()
                            return ("loaded", loaded)
        return None

    def render(self, surface: pygame.Surface) -> None:
        if not self.active:
            return
        w, h = surface.get_size()
        dim = pygame.Surface((w, h), pygame.SRCALPHA)
        dim.fill((8, 10, 16, 212))
        surface.blit(dim, (0, 0))

        accent = CASSETTES[1].accent if self.mode == "save" else CASSETTES[2].accent
        panel = pygame.Rect(92, 66, w - 184, h - 132)
        pygame.draw.rect(surface, (18, 21, 32), panel, border_radius=14)
        pygame.draw.rect(surface, accent, panel, 2, border_radius=14)

        f_title = get_ui_font(24, bold=True)
        f_slot = get_ui_font(15, bold=True)
        f_sub = get_ui_font(13)

        hdr = "SIMPAN PERJALANAN (10 SLOT)" if self.mode == "save" else "LANJUTKAN CERITA (10 SLOT)"
        surface.blit(f_title.render(hdr, True, accent), (126, 88))

        self.close_rect = pygame.Rect(panel.right - 140, 86, 110, 36)
        pygame.draw.rect(surface, (42, 46, 62), self.close_rect, border_radius=8)
        pygame.draw.rect(surface, accent, self.close_rect, 1, border_radius=8)
        c_lbl = f_sub.render("ESC / Tutup", True, (238, 242, 248))
        surface.blit(c_lbl, (self.close_rect.centerx - c_lbl.get_width() // 2, self.close_rect.centery - c_lbl.get_height() // 2))

        self.slot_rects.clear()
        col_w, row_h = 505, 86
        start_x, start_y = 126, 146
        mpos = pygame.mouse.get_pos()

        for idx in range(1, 11):
            col = (idx - 1) // 5
            row = (idx - 1) % 5
            rx = start_x + col * (col_w + 20)
            ry = start_y + row * (row_h + 10)
            rect = pygame.Rect(rx, ry, col_w, row_h)
            self.slot_rects.append((idx, rect))

            info = self._slots_cache.get(idx)
            hovered = rect.collidepoint(mpos)
            fill = (32, 38, 54) if hovered else (24, 28, 40)
            border = accent if hovered else (62, 68, 92)
            pygame.draw.rect(surface, fill, rect, border_radius=10)
            pygame.draw.rect(surface, border, rect, 2 if hovered else 1, border_radius=10)

            badge = pygame.Rect(rx + 12, ry + 14, 58, 58)
            pygame.draw.rect(surface, accent if info else (42, 46, 62), badge, border_radius=8)
            num_surf = f_title.render(f"{idx:02d}", True, (14, 16, 22) if info else (180, 188, 204))
            surface.blit(num_surf, (badge.centerx - num_surf.get_width() // 2, badge.centery - num_surf.get_height() // 2))

            if info is None:
                surface.blit(f_slot.render("Slot Kosong", True, (150, 160, 178)), (rx + 84, ry + 20))
                hint_txt = "Klik untuk menyimpan progres di sini" if self.mode == "save" else "Belum ada data tersimpan"
                surface.blit(f_sub.render(hint_txt, True, (115, 124, 142)), (rx + 84, ry + 46))
            else:
                title = str(info.get("carriage_title", SCENE_LABELS.get(info.get("current_scene", ""), "Perjalanan")))
                secs = float(info.get("elapsed_total_seconds", 0.0))
                mins_str = f"{int(secs // 60):02d}:{int(secs % 60):02d}"
                stubs = len(info.get("harmonized_carriages", []))
                cassettes = len(info.get("collected_cassettes", [1]))
                saved_at = str(info.get("saved_at", "-"))
                surface.blit(f_slot.render(title, True, (244, 246, 252)), (rx + 84, ry + 14))
                surface.blit(
                    f_sub.render(f"Tiket: {stubs}/4  |  Kaset: {cassettes}/4  |  Durasi: {mins_str}", True, (175, 212, 240)),
                    (rx + 84, ry + 38),
                )
                surface.blit(f_sub.render(f"Disimpan: {saved_at}", True, (155, 165, 182)), (rx + 84, ry + 58))


class CGGalleryModal:
    """Paginated 25-CG Memory Gallery modal with preview playback."""

    PER_PAGE = 9  # 3x3 clean grid across 3 pages

    def __init__(self, assets: Any, screen_size: tuple[int, int] = (1280, 720)) -> None:
        self.assets = assets
        self.w, self.h = screen_size
        self.active = False
        self.page = 0
        self.unlocked: set[str] = set()
        self.thumb_cache: dict[str, pygame.Surface] = {}
        self.card_rects: list[tuple[str, pygame.Rect]] = []
        self.prev_rect = pygame.Rect(0, 0, 0, 0)
        self.next_rect = pygame.Rect(0, 0, 0, 0)
        self.close_rect = pygame.Rect(0, 0, 0, 0)
        self.unlock_all_rect = pygame.Rect(0, 0, 0, 0)
        self.viewer = WutheringWavesCGOverlay(assets, screen_size)

    def open(self) -> None:
        self.active = True
        self.page = 0
        self.unlocked = load_unlocked_gallery()

    def close(self) -> None:
        self.active = False
        self.viewer.active = False

    def _get_thumb(self, cg_id: str, rel_path: str) -> pygame.Surface:
        if cg_id not in self.thumb_cache:
            img = self.assets.get_image(rel_path, size=(280, 158), fallback_style="sunset")
            self.thumb_cache[cg_id] = img
        return self.thumb_cache[cg_id]

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.active:
            return False

        if self.viewer.active:
            self.viewer.handle_event(event)
            return True

        total_pages = max(1, (len(ALL_CG_SLIDES) + self.PER_PAGE - 1) // self.PER_PAGE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return True
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.page = (self.page - 1) % total_pages
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.page = (self.page + 1) % total_pages
            elif event.key == pygame.K_F8:
                unlock_all_cgs_in_gallery()
                self.unlocked = load_unlocked_gallery()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.close_rect.collidepoint(event.pos):
                self.assets.play_sfx("click", volume=0.22)
                self.close()
                return True
            if self.prev_rect.collidepoint(event.pos):
                self.page = (self.page - 1) % total_pages
                self.assets.play_sfx("click", volume=0.18)
                return True
            if self.next_rect.collidepoint(event.pos):
                self.page = (self.page + 1) % total_pages
                self.assets.play_sfx("click", volume=0.18)
                return True
            if self.unlock_all_rect.collidepoint(event.pos):
                unlock_all_cgs_in_gallery()
                self.unlocked = load_unlocked_gallery()
                self.assets.play_sfx("chime", volume=0.24)
                return True

            for cg_id, rect in self.card_rects:
                if rect.collidepoint(event.pos) and cg_id in self.unlocked:
                    self.assets.play_sfx("click", volume=0.25)
                    self.viewer.start_single_cg(cg_id)
                    return True
        return True

    def update(self, dt: float) -> None:
        if self.active and self.viewer.active:
            self.viewer.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        if not self.active:
            return
        if self.viewer.active:
            self.viewer.render(surface)
            return

        w, h = surface.get_size()
        dim = pygame.Surface((w, h), pygame.SRCALPHA)
        dim.fill((8, 10, 16, 218))
        surface.blit(dim, (0, 0))

        accent = CASSETTES[1].accent
        panel = pygame.Rect(68, 42, w - 136, h - 84)
        pygame.draw.rect(surface, (18, 21, 32), panel, border_radius=14)
        pygame.draw.rect(surface, accent, panel, 2, border_radius=14)

        f_title = get_ui_font(22, bold=True)
        f_sub = get_ui_font(13, bold=True)
        f_cap = get_ui_font(13)

        unlocked_n = len(self.unlocked)
        surface.blit(
            f_title.render(f"GALERI KENANGAN ({unlocked_n}/{len(ALL_CG_SLIDES)} CG Terbuka)", True, accent),
            (102, 62),
        )

        self.unlock_all_rect = pygame.Rect(panel.right - 318, 60, 184, 34)
        pygame.draw.rect(surface, (36, 48, 56), self.unlock_all_rect, border_radius=8)
        pygame.draw.rect(surface, (145, 232, 195), self.unlock_all_rect, 1, border_radius=8)
        u_lbl = f_sub.render("Buka Semua Preview", True, (220, 255, 240))
        surface.blit(u_lbl, (self.unlock_all_rect.centerx - u_lbl.get_width() // 2, self.unlock_all_rect.centery - u_lbl.get_height() // 2))

        self.close_rect = pygame.Rect(panel.right - 122, 60, 96, 34)
        pygame.draw.rect(surface, (42, 46, 62), self.close_rect, border_radius=8)
        pygame.draw.rect(surface, accent, self.close_rect, 1, border_radius=8)
        c_lbl = f_sub.render("Tutup", True, (238, 242, 248))
        surface.blit(c_lbl, (self.close_rect.centerx - c_lbl.get_width() // 2, self.close_rect.centery - c_lbl.get_height() // 2))

        start = self.page * self.PER_PAGE
        page_slides = ALL_CG_SLIDES[start : start + self.PER_PAGE]
        self.card_rects.clear()
        mpos = pygame.mouse.get_pos()

        cw, ch = 330, 154
        gx0, gy0 = 112, 114
        for idx, slide in enumerate(page_slides):
            col = idx % 3
            row = idx // 3
            rx = gx0 + col * (cw + 32)
            ry = gy0 + row * (ch + 20)
            rect = pygame.Rect(rx, ry, cw, ch)
            self.card_rects.append((slide.cg_id, rect))

            is_open = slide.cg_id in self.unlocked
            hovered = rect.collidepoint(mpos)
            pygame.draw.rect(surface, (28, 32, 46) if hovered else (22, 26, 38), rect, border_radius=8)
            pygame.draw.rect(surface, accent if (is_open and hovered) else (60, 66, 88), rect, 2 if hovered else 1, border_radius=8)

            if is_open:
                thumb = self._get_thumb(slide.cg_id, slide.rel_path)
                scaled = pygame.transform.smoothscale(thumb, (cw - 16, 114))
                surface.blit(scaled, (rx + 8, ry + 8))
                surface.blit(f_cap.render(f"[{slide.category}] {slide.title}", True, (242, 245, 250)), (rx + 10, ry + 128))
            else:
                pygame.draw.rect(surface, (14, 16, 24), (rx + 8, ry + 8, cw - 16, 114), border_radius=6)
                lock_txt = f_sub.render("??? (Belum Ditemukan)", True, (115, 124, 144))
                surface.blit(lock_txt, (rx + cw // 2 - lock_txt.get_width() // 2, ry + 56))
                surface.blit(f_cap.render(f"[{slide.category}] Terkunci", True, (115, 124, 144)), (rx + 10, ry + 128))

        total_pages = max(1, (len(ALL_CG_SLIDES) + self.PER_PAGE - 1) // self.PER_PAGE)
        self.prev_rect = pygame.Rect(w // 2 - 170, panel.bottom - 48, 100, 34)
        self.next_rect = pygame.Rect(w // 2 + 70, panel.bottom - 48, 100, 34)
        for btn, lbl in ((self.prev_rect, "< Sebelumnya"), (self.next_rect, "Berikutnya >")):
            pygame.draw.rect(surface, (36, 40, 54), btn, border_radius=8)
            pygame.draw.rect(surface, accent, btn, 1, border_radius=8)
            t = f_cap.render(lbl, True, (236, 240, 248))
            surface.blit(t, (btn.centerx - t.get_width() // 2, btn.centery - t.get_height() // 2))

        pg_txt = f_sub.render(f"Hal {self.page + 1}/{total_pages}", True, (220, 226, 238))
        surface.blit(pg_txt, (w // 2 - pg_txt.get_width() // 2, panel.bottom - 40))


class PauseMenuModal:
    """In-game ESC Pause Menu with Save (10 slots), Load (10 slots), Gallery, and Main Menu."""

    def __init__(self, assets: Any, screen_size: tuple[int, int] = (1280, 720)) -> None:
        self.assets = assets
        self.active = False
        self.selected = 0
        self.items = [
            ("resume", "Lanjutkan Permainan"),
            ("save", "Simpan Permainan (10 Slot)"),
            ("load", "Muat Permainan (10 Slot)"),
            ("gallery", "Galeri Kenangan (25 CG)"),
            ("main_menu", "Kembali ke Menu Utama"),
        ]
        self.hitboxes: list[tuple[int, pygame.Rect]] = []
        self.save_load = SaveLoadModal(assets)
        self.gallery = CGGalleryModal(assets, screen_size)

    def open(self) -> None:
        self.active = True
        self.selected = 0

    def close(self) -> None:
        self.active = False
        self.save_load.close()
        self.gallery.close()

    def handle_event(
        self,
        event: pygame.event.Event,
        current_save_data: dict[str, Any],
    ) -> tuple[str, Any] | None:
        if not self.active:
            return None

        if self.gallery.active:
            self.gallery.handle_event(event)
            return None

        if self.save_load.active:
            res = self.save_load.handle_event(event, current_save_data=current_save_data)
            if res is not None and res[0] == "loaded":
                self.close()
                return res
            if res is not None and res[0] == "saved":
                return res
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return ("resume", None)
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.items)
                self.assets.play_sfx("click", volume=0.14)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.items)
                self.assets.play_sfx("click", volume=0.14)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self._trigger_item(self.selected)
        elif event.type == pygame.MOUSEMOTION:
            for idx, rect in self.hitboxes:
                if rect.collidepoint(event.pos):
                    self.selected = idx
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, rect in self.hitboxes:
                if rect.collidepoint(event.pos):
                    return self._trigger_item(idx)
        return None

    def _trigger_item(self, idx: int) -> tuple[str, Any] | None:
        key, _ = self.items[idx]
        self.assets.play_sfx("click", volume=0.22)
        if key == "resume":
            self.close()
            return ("resume", None)
        if key == "save":
            self.save_load.open("save")
            return None
        if key == "load":
            self.save_load.open("load")
            return None
        if key == "gallery":
            self.gallery.open()
            return None
        if key == "main_menu":
            self.close()
            return ("main_menu", None)
        return None

    def update(self, dt: float) -> None:
        if self.active and self.gallery.active:
            self.gallery.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        if not self.active:
            return
        if self.gallery.active:
            self.gallery.render(surface)
            return
        if self.save_load.active:
            self.save_load.render(surface)
            return

        w, h = surface.get_size()
        dim = pygame.Surface((w, h), pygame.SRCALPHA)
        dim.fill((8, 10, 16, 195))
        surface.blit(dim, (0, 0))

        accent = CASSETTES[1].accent
        panel = pygame.Rect(w // 2 - 220, 148, 440, 412)
        pygame.draw.rect(surface, (18, 22, 32), panel, border_radius=14)
        pygame.draw.rect(surface, accent, panel, 2, border_radius=14)

        f_hdr = get_ui_font(24, bold=True)
        f_btn = get_ui_font(16, bold=True)
        hdr = f_hdr.render("JEDA PERJALANAN", True, accent)
        surface.blit(hdr, (panel.centerx - hdr.get_width() // 2, panel.top + 26))

        self.hitboxes.clear()
        for idx, (_, label) in enumerate(self.items):
            rect = pygame.Rect(panel.left + 36, panel.top + 82 + idx * 60, panel.width - 72, 46)
            self.hitboxes.append((idx, rect))
            is_sel = idx == self.selected
            fill = accent if is_sel else (28, 33, 48)
            fg = (14, 16, 22) if is_sel else (238, 242, 248)
            pygame.draw.rect(surface, fill, rect, border_radius=8)
            pygame.draw.rect(surface, accent, rect, 2 if is_sel else 1, border_radius=8)
            txt = f_btn.render(label, True, fg)
            surface.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))
