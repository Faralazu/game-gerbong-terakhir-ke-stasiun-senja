"""Smart asset manager with procedural fallbacks, hot-reload, and usage auditing.

Every requested image, video, or audio asset is tracked in a manifest saved to
userdata/logs/used_assets_manifest.json. If an asset is missing during rapid
prototyping, a procedural pixel-art / Persona-style fallback is synthesized so
gameplay iteration never crashes.
"""

from __future__ import annotations

import math
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pygame

from src.core import paths


def _normalize_asset_key(rel_path: str | Path, default_prefix: str) -> str:
    """Normalize an asset path relative to assets/ using forward slashes."""
    clean = Path(rel_path).as_posix().lstrip("./")
    if clean.startswith("assets/"):
        clean = clean[len("assets/") :]
    known_roots = ("images/", "videos/", "audio/")
    if not clean.startswith(known_roots):
        clean = f"{default_prefix.rstrip('/')}/{clean}"
    return clean


class VideoStreamPlayer:
    """Plays an MP4 loop via OpenCV or synthesizes an animated pixel-art window view."""

    def __init__(
        self,
        file_path: Path | None,
        fallback_style: str = "sunset",
        size: tuple[int, int] = (1280, 720),
    ) -> None:
        self.file_path = file_path
        self.fallback_style = fallback_style
        self.size = size
        self.cap: cv2.VideoCapture | None = None
        self.is_real_video = False
        self.fps = 24.0
        self._frame_timer = 0.0
        self._sim_time = 0.0
        self._current_surface: pygame.Surface | None = None
        self._open_capture()

    def _open_capture(self) -> None:
        self.close()
        if self.file_path and self.file_path.exists():
            cap = cv2.VideoCapture(str(self.file_path))
            if cap.isOpened():
                self.cap = cap
                self.is_real_video = True
                fps = cap.get(cv2.CAP_PROP_FPS)
                self.fps = fps if fps and 5.0 <= fps <= 120.0 else 24.0
                self._read_next_cv_frame()
                return
            cap.release()
        self.is_real_video = False
        self._current_surface = self._render_procedural_frame(0.0)

    def _read_next_cv_frame(self) -> None:
        if self.cap is None:
            return
        ok, frame = self.cap.read()
        if not ok:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = self.cap.read()
        if ok and frame is not None:
            target_w, target_h = self.size
            if frame.shape[1] != target_w or frame.shape[0] != target_h:
                frame = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_NEAREST)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            surf = pygame.image.frombuffer(rgb.tobytes(), (target_w, target_h), "RGB")
            self._current_surface = surf.convert()

    def _render_procedural_frame(self, t: float) -> pygame.Surface:
        """Render a cozy pixel-art animated exterior window scene as video fallback."""
        # Render at crisp low pixel resolution then scale cleanly with nearest-neighbor.
        pw, ph = 320, 180
        canvas = pygame.Surface((pw, ph))
        style = self.fallback_style

        if style == "sketch":
            canvas.fill((232, 229, 222))
            for y in range(95, ph, 6):
                pygame.draw.line(canvas, (195, 192, 184), (0, y), (pw, y), 1)
            pole_x = int(pw - ((t * 45) % (pw + 80)))
            pygame.draw.line(canvas, (110, 110, 110), (pole_x, 20), (pole_x, ph), 2)
        elif style == "rain":
            # Deep neon night sky + distant glowing city bokeh + rain streaks
            for y in range(0, 108, 4):
                ratio = y / 108.0
                r = int(16 + 26 * ratio)
                g = int(20 + 24 * ratio)
                b = int(52 + 65 * ratio)
                pygame.draw.rect(canvas, (r, g, b), (0, y, pw, 4))
            pygame.draw.rect(canvas, (14, 18, 42), (0, 108, pw, ph - 108))
            # Parallax neon city skyline
            scroll = int(t * 55)
            for idx in range(14):
                bx = (idx * 34 - scroll) % (pw + 48) - 32
                bh = 24 + (idx * 17) % 34
                pygame.draw.rect(canvas, (22, 26, 56), (bx, 108 - bh, 26, bh))
                win_col = (72, 215, 255) if idx % 2 == 0 else (200, 105, 255)
                for wy in range(108 - bh + 5, 104, 7):
                    pygame.draw.rect(canvas, win_col, (bx + 5, wy, 4, 3))
                    pygame.draw.rect(canvas, win_col, (bx + 15, wy, 4, 3))
            # Shimmering neon water reflections
            for i in range(28):
                ry = 112 + (i * 7) % 62
                rx = ((i * 53) - int(t * 70)) % pw
                col = (80, 200, 255) if i % 2 == 0 else (180, 95, 240)
                pygame.draw.rect(canvas, col, (rx, ry, 14 + (i % 8), 2))
            # Diagonal rain streaks
            for i in range(45):
                rx = (i * 29 + int(t * 210)) % pw
                ry = (i * 37 + int(t * 360)) % ph
                pygame.draw.line(canvas, (145, 210, 255), (rx, ry), (rx - 4, ry + 9), 1)
        elif style == "courage":
            # Stylish Persona crimson & gold speed-sky
            canvas.fill((22, 10, 16))
            for i in range(8):
                offset = ((i * 60) - int(t * 220)) % (pw + 120) - 60
                pts = [(offset, 0), (offset + 28, 0), (offset - 22, ph), (offset - 50, ph)]
                col = (210, 28, 45) if i % 2 == 0 else (245, 185, 55)
                pygame.draw.polygon(canvas, col, pts)
            pygame.draw.rect(canvas, (14, 12, 16), (0, 118, pw, ph - 118))
            for i in range(12):
                lx = (i * 40 - int(t * 320)) % pw
                pygame.draw.rect(canvas, (255, 230, 120), (lx, 130 + (i % 3) * 12, 22, 2))
        elif style == "dawn":
            # Soft serene morning pastel mint & golden horizon
            for y in range(0, 106, 4):
                ratio = y / 106.0
                r = int(125 + 120 * ratio)
                g = int(195 + 48 * ratio)
                b = int(205 + 25 * ratio)
                pygame.draw.rect(canvas, (r, g, b), (0, y, pw, 4))
            pygame.draw.circle(canvas, (255, 248, 210), (190, 94), 18)
            pygame.draw.rect(canvas, (82, 175, 175), (0, 106, pw, ph - 106))
            for i in range(24):
                rx = (i * 41 - int(t * 40)) % pw
                ry = 110 + (i * 9) % 60
                pygame.draw.rect(canvas, (255, 248, 220), (rx, ry, 14, 2))
        else:
            # Default: warm golden sunset over calm shimmering ocean + passing utility poles
            for y in range(0, 106, 4):
                ratio = y / 106.0
                r = int(78 + 175 * ratio)
                g = int(58 + 115 * ratio)
                b = int(105 - 25 * ratio)
                pygame.draw.rect(canvas, (r, g, b), (0, y, pw, 4))
            # Soft drifting pixel clouds
            for c_idx in range(4):
                cx = int((c_idx * 95 - t * 14) % (pw + 70)) - 35
                cy = 28 + (c_idx % 2) * 20
                pygame.draw.rect(canvas, (255, 198, 132), (cx, cy, 48, 10))
                pygame.draw.rect(canvas, (255, 222, 165), (cx + 8, cy - 5, 28, 6))
            # Glowing sunset sun
            pygame.draw.circle(canvas, (255, 232, 148), (160, 98), 20)
            # Calm shimmering sea
            pygame.draw.rect(canvas, (215, 112, 72), (0, 106, pw, ph - 106))
            for i in range(30):
                rx = (115 + (i % 7) * 14 + int(math.sin(t * 2 + i) * 6))
                ry = 109 + i * 2
                if ry < ph:
                    w = max(4, 26 - i // 2)
                    pygame.draw.rect(canvas, (255, 232, 150), (rx - w // 2, ry, w, 2))
            # Passing coastal utility poles & drooping wire
            pole_spacing = 180
            pole_x = int(pw - ((t * 145) % pole_spacing))
            for px in (pole_x, pole_x - pole_spacing):
                pygame.draw.rect(canvas, (45, 22, 26), (px, 10, 4, ph - 10))
                pygame.draw.rect(canvas, (45, 22, 26), (px - 7, 24, 18, 2))
            pygame.draw.line(canvas, (55, 28, 32), (0, 28), (pw, 32), 1)

        return pygame.transform.scale(canvas, self.size).convert()

    def update(self, dt: float) -> None:
        self._sim_time += dt
        if self.is_real_video:
            self._frame_timer += dt
            interval = 1.0 / self.fps
            if self._frame_timer >= interval:
                self._frame_timer %= interval
                self._read_next_cv_frame()
        else:
            self._current_surface = self._render_procedural_frame(self._sim_time)

    def get_surface(self) -> pygame.Surface:
        if self._current_surface is None:
            self._current_surface = self._render_procedural_frame(self._sim_time)
        return self._current_surface

    def reload(self) -> None:
        self._open_capture()

    def close(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None


class AssetManager:
    """Centralized portable asset loader with fallbacks, hot-reload, and audit logging."""

    def __init__(self) -> None:
        self._image_cache: dict[tuple[str, tuple[int, int] | None], pygame.Surface] = {}
        self._video_cache: dict[str, VideoStreamPlayer] = {}
        self._sfx_cache: dict[str, pygame.mixer.Sound] = {}
        self.used_assets: set[str] = set()
        self.loaded_assets: set[str] = set()
        self.fallback_assets: set[str] = set()
        self.current_bgm_key: str = ""
        self.current_bgm_title: str = "Silent Rails"
        self.current_bgm_is_fallback: bool = True

    def _record_usage(self, norm_key: str, is_real: bool) -> None:
        self.used_assets.add(norm_key)
        if is_real:
            self.loaded_assets.add(norm_key)
            self.fallback_assets.discard(norm_key)
        else:
            self.fallback_assets.add(norm_key)

    def get_image(
        self,
        rel_path: str,
        size: tuple[int, int] | None = None,
        fallback_style: str = "sunset",
    ) -> pygame.Surface:
        norm_key = _normalize_asset_key(rel_path, "images")
        cache_key = (norm_key, size)
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]

        full_path = paths.asset_path(norm_key)
        if full_path.exists():
            surf = pygame.image.load(str(full_path)).convert_alpha()
            if size is not None and surf.get_size() != size:
                surf = pygame.transform.smoothscale(surf, size)
            self._record_usage(norm_key, is_real=True)
        else:
            surf = self._build_fallback_image(norm_key, size or (640, 360), fallback_style)
            self._record_usage(norm_key, is_real=False)

        self._image_cache[cache_key] = surf
        return surf

    def _build_fallback_image(
        self,
        label: str,
        size: tuple[int, int],
        style: str,
    ) -> pygame.Surface:
        """Synthesize a clean Persona / Pixel-Art placeholder when art doesn't exist yet."""
        w, h = size
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        palette = {
            "sunset": ((38, 22, 34), (242, 138, 68)),
            "rain": ((18, 24, 48), (90, 200, 255)),
            "courage": ((20, 12, 16), (225, 32, 48)),
            "dawn": ((28, 48, 52), (160, 235, 205)),
        }.get(style, ((30, 30, 38), (220, 220, 220)))

        bg_col, accent = palette
        surf.fill((*bg_col, 235))
        pygame.draw.polygon(
            surf,
            (*accent, 75),
            [(0, int(h * 0.72)), (w, int(h * 0.45)), (w, h), (0, h)],
        )
        pygame.draw.rect(surf, accent, (4, 4, w - 8, h - 8), 2)
        font = pygame.font.SysFont("segoeui,calibri,arial", max(14, min(22, h // 14)), bold=True)
        txt = font.render(f"[DRAFT ASSET] {Path(label).name}", True, (245, 245, 245))
        surf.blit(txt, (16, max(12, h // 2 - txt.get_height() // 2)))
        return surf

    def get_video(
        self,
        rel_path: str,
        fallback_style: str = "sunset",
        size: tuple[int, int] = (1280, 720),
    ) -> VideoStreamPlayer:
        norm_key = _normalize_asset_key(rel_path, "videos")
        if norm_key in self._video_cache:
            player = self._video_cache[norm_key]
            player.fallback_style = fallback_style
            return player

        full_path = paths.asset_path(norm_key)
        player = VideoStreamPlayer(
            full_path if full_path.exists() else None,
            fallback_style=fallback_style,
            size=size,
        )
        self._record_usage(norm_key, is_real=player.is_real_video)
        self._video_cache[norm_key] = player
        return player

    def play_bgm(
        self,
        rel_path: str,
        track_title: str = "",
        loops: int = -1,
        fade_ms: int = 800,
    ) -> bool:
        norm_key = _normalize_asset_key(rel_path, "audio/bgm")
        full_path = paths.asset_path(norm_key)
        already_playing = (
            self.current_bgm_key == norm_key
            and not self.current_bgm_is_fallback
            and pygame.mixer.get_init() is not None
            and pygame.mixer.music.get_busy()
        )
        self.current_bgm_key = norm_key
        self.current_bgm_title = track_title or Path(norm_key).stem
        if already_playing:
            return True

        if full_path.exists() and pygame.mixer.get_init() is not None:
            self._record_usage(norm_key, is_real=True)
            self.current_bgm_is_fallback = False
            try:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.fadeout(320)
                pygame.mixer.music.load(str(full_path))
                pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
                return True
            except pygame.error:
                self.current_bgm_is_fallback = True
                return False

        self._record_usage(norm_key, is_real=full_path.exists())
        self.current_bgm_is_fallback = True
        if pygame.mixer.get_init() is not None:
            pygame.mixer.music.fadeout(min(300, fade_ms))
        return False

    def play_sfx(self, kind: str = "click", volume: float = 0.25) -> None:
        """Play a real WAV SFX from assets/audio/sfx/, with in-memory fallback."""
        alias_map = {
            "click": "sfx_cassette_click.wav",
            "cassette_click": "sfx_cassette_click.wav",
            "chime": "sfx_resonance_chime.wav",
            "resonance_chime": "sfx_resonance_chime.wav",
            "footstep": "sfx_footstep_wood.wav",
            "footstep_wood": "sfx_footstep_wood.wav",
            "text_blip": "sfx_text_blip.wav",
            "paper": "sfx_paper_rustle.wav",
            "paper_rustle": "sfx_paper_rustle.wav",
            "door": "sfx_door_slide.wav",
            "door_slide": "sfx_door_slide.wav",
            "ticket_punch": "sfx_ticket_punch.wav",
            "phone_vibrate": "sfx_phone_vibrate.wav",
            "wind_petals": "sfx_wind_petals.wav",
            "memory_ache": "sfx_memory_ache.wav",
        }
        filename = alias_map.get(kind, f"sfx_{kind}.wav")
        norm_key = _normalize_asset_key(filename, "audio/sfx")
        full_path = paths.asset_path(norm_key)
        if pygame.mixer.get_init() is None:
            return

        if full_path.exists():
            self._record_usage(norm_key, is_real=True)
            if norm_key not in self._sfx_cache:
                self._sfx_cache[norm_key] = pygame.mixer.Sound(str(full_path))
            snd = self._sfx_cache[norm_key]
            snd.set_volume(volume)
            snd.play()
            return

        cache_key = f"__synth_{kind}"
        if cache_key not in self._sfx_cache:
            self._sfx_cache[cache_key] = self._generate_synth_sound(kind)
        snd = self._sfx_cache[cache_key]
        snd.set_volume(volume)
        snd.play()

    def play_synth_sfx(self, kind: str = "click", volume: float = 0.25) -> None:
        """Backward-compatible wrapper delegating to play_sfx."""
        self.play_sfx(kind=kind, volume=volume)

    def _generate_synth_sound(self, kind: str) -> pygame.mixer.Sound:
        sample_rate = 22050
        if kind == "chime":
            dur = 0.35
            t = np.linspace(0, dur, int(sample_rate * dur), endpoint=False)
            wave = (
                0.5 * np.sin(2 * np.pi * 523.25 * t)
                + 0.4 * np.sin(2 * np.pi * 659.25 * t)
                + 0.3 * np.sin(2 * np.pi * 783.99 * t)
            ) * np.exp(-6.0 * t)
        else:
            # Mechanical Walkman CLACK-CLICK
            dur = 0.08
            t = np.linspace(0, dur, int(sample_rate * dur), endpoint=False)
            click = np.sin(2 * np.pi * 180 * t) * np.exp(-55.0 * t)
            snap = np.sin(2 * np.pi * 920 * np.maximum(0.0, t - 0.025)) * np.exp(-85.0 * np.maximum(0.0, t - 0.025))
            wave = 0.7 * click + 0.45 * snap

        pcm = np.clip(wave * 32767, -32767, 32767).astype(np.int16)
        stereo = np.column_stack((pcm, pcm))
        return pygame.sndarray.make_sound(stereo)

    def reload_all(self) -> dict[str, int]:
        """Hot-reload all cached images & video streams from disk (F5)."""
        self._image_cache.clear()
        self.loaded_assets.clear()
        self.fallback_assets.clear()
        for key, player in self._video_cache.items():
            full = paths.asset_path(key)
            player.file_path = full if full.exists() else None
            player.reload()
            self._record_usage(key, is_real=player.is_real_video)
        return {
            "real_count": len(self.loaded_assets),
            "fallback_count": len(self.fallback_assets),
        }

    def save_manifest(self) -> Path:
        """Persist used/missing asset tracking to userdata/logs/used_assets_manifest.json."""
        manifest_path = paths.LOGS_DIR / "used_assets_manifest.json"
        payload = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "used_assets": sorted(self.used_assets),
            "loaded_real_assets": sorted(self.loaded_assets),
            "missing_fallback_assets": sorted(self.fallback_assets),
        }
        return paths.write_json(manifest_path, payload)

    def scan_unused_assets(self, include_manifest: bool = True) -> dict[str, list[str]]:
        """Compare all files inside assets/ against active used_assets."""
        used = set(self.used_assets)
        if include_manifest:
            manifest = paths.read_json(paths.LOGS_DIR / "used_assets_manifest.json", default={})
            for item in manifest.get("used_assets", []):
                used.add(item)

        disk_files: list[str] = []
        if paths.ASSETS_DIR.exists():
            for p in sorted(paths.ASSETS_DIR.rglob("*")):
                if p.is_file():
                    disk_files.append(p.relative_to(paths.ASSETS_DIR).as_posix())

        active = [f for f in disk_files if f in used]
        unused = [f for f in disk_files if f not in used]
        return {
            "disk_files": disk_files,
            "active_used": active,
            "unused_on_disk": unused,
            "referenced_total": sorted(used),
        }

    def archive_unused_assets(self) -> list[str]:
        """Safely move unused files from assets/ to _asset_vault/unused_archive/."""
        report = self.scan_unused_assets(include_manifest=True)
        moved: list[str] = []
        stamp = time.strftime("%Y%m%d_%H%M%S")
        for rel in report["unused_on_disk"]:
            src = paths.ASSETS_DIR / rel
            dst = paths.UNUSED_ARCHIVE_DIR / rel
            if dst.exists():
                dst = dst.with_name(f"{dst.stem}_{stamp}{dst.suffix}")
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            moved.append(rel)
        return moved

    def close(self) -> None:
        for player in self._video_cache.values():
            player.close()
        self.save_manifest()
