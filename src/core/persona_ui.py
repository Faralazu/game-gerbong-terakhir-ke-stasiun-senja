"""Shared clean UI, typography, chroma-key asset slicers, filters, cutscenes, and transitions."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any

import numpy as np
import pygame

from src.core import paths


_FONT_CACHE: dict[tuple[int, bool, bool], pygame.font.Font] = {}
_UI_SURFACE_CACHE: dict[tuple[Any, ...], Any] = {}


def clear_ui_caches() -> None:
    """Clear processed surface caches (e.g., on F5 asset hot-reload)."""
    _UI_SURFACE_CACHE.clear()


def get_ui_font(size: int, bold: bool = False, serif: bool = False) -> pygame.font.Font:
    """Return a clean humanist sans-serif or literary serif font (replacing Consolas)."""
    key = (size, bold, serif)
    if key not in _FONT_CACHE:
        family = (
            "georgia,cambria,timesnewroman"
            if serif
            else "segoeui,trebuchetms,calibri,arial"
        )
        _FONT_CACHE[key] = pygame.font.SysFont(family, size, bold=bold)
    return _FONT_CACHE[key]


@dataclass(frozen=True)
class CassetteProfile:
    """Visual, audio, and emotional theme for a Walkman cassette."""

    slot: int
    code: str
    title: str
    emotion: str
    accent: tuple[int, int, int]
    tint_rgb: tuple[float, float, float]
    video_rel: str
    video_fallback: str
    bgm_rel: str


CASSETTES: dict[int, CassetteProfile] = {
    0: CassetteProfile(
        slot=0,
        code="---",
        title="Keheningan",
        emotion="Sunyi Sebelum Memutar Kaset",
        accent=(185, 185, 195),
        tint_rgb=(1.0, 1.0, 1.0),
        video_rel="videos/vid_02_window_sunset_loop.mp4",
        video_fallback="sketch",
        bgm_rel="audio/bgm/bgm_00_sketch_rails.mp3",
    ),
    1: CassetteProfile(
        slot=1,
        code="SIDE A",
        title="Senja — Nostalgia",
        emotion="Hangat & Menenangkan",
        accent=(248, 174, 84),
        tint_rgb=(1.04, 0.99, 0.93),
        video_rel="videos/vid_02_window_sunset_loop.mp4",
        video_fallback="sunset",
        bgm_rel="audio/bgm/bgm_01_nostalgia_sunset.mp3",
    ),
    2: CassetteProfile(
        slot=2,
        code="SIDE B",
        title="Hujan — Pengakuan",
        emotion="Biru Malam & Introspektif",
        accent=(102, 205, 255),
        tint_rgb=(0.68, 0.80, 1.12),
        video_rel="videos/vid_03_window_neon_rain_loop.mp4",
        video_fallback="rain",
        bgm_rel="audio/bgm/bgm_02_denial_rain.mp3",
    ),
    3: CassetteProfile(
        slot=3,
        code="SIDE C",
        title="Detak — Keberanian",
        emotion="Hangat & Mantap (Midnight Jazz)",
        accent=(232, 74, 88),
        tint_rgb=(1.10, 0.82, 0.84),
        video_rel="videos/vid_06_window_courage_loop.mp4",
        video_fallback="courage",
        bgm_rel="audio/bgm/bgm_03_courage_persona.mp3",
    ),
    4: CassetteProfile(
        slot=4,
        code="SIDE D",
        title="Fajar — Keikhlasan",
        emotion="Teduh & Utuh",
        accent=(145, 232, 195),
        tint_rgb=(0.94, 1.05, 1.07),
        video_rel="videos/vid_07_window_dawn_loop.mp4",
        video_fallback="dawn",
        bgm_rel="audio/bgm/bgm_04_acceptance_finale.mp3",
    ),
}


def resolve_cassette_video(assets: Any, cid: int) -> Any:
    """Load cassette window video, falling back to vid_02 if optional vid_06/07 isn't added yet."""
    prof = CASSETTES[cid]
    rel = prof.video_rel
    if not paths.asset_path(rel).exists() and cid in (0, 3, 4):
        rel = "videos/vid_02_window_sunset_loop.mp4"
    return assets.get_video(rel, fallback_style=prof.video_fallback)


def draw_contact_shadow(
    surface: pygame.Surface,
    center_x: int,
    feet_y: int,
    width: int = 104,
    height: int = 20,
) -> None:
    """Ground characters onto the wooden floor with a soft elliptical contact shadow."""
    shadow = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (8, 8, 14, 95), (0, 0, width, height))
    surface.blit(shadow, (center_x - width // 2, feet_y - height // 2))


def _key_green_window_surface(
    raw_surf: pygame.Surface,
    size: tuple[int, int],
    mask_override: np.ndarray | None = None,
    tint_rgb: tuple[float, float, float] | None = None,
    fill_non_override_paper: bool = False,
) -> tuple[pygame.Surface, np.ndarray]:
    """Scale carriage image, key out #00FF00 green windows, and despill edges."""
    w, h = size
    scaled = pygame.transform.smoothscale(raw_surf, (w, h))
    rgb = pygame.surfarray.pixels3d(scaled).transpose(1, 0, 2).astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]

    is_green = (g > 150) & ((g - np.maximum(r, b)) > 42)
    alpha = np.full((h, w), 255, dtype=np.uint8)

    if mask_override is not None:
        window_mask = mask_override
        if fill_non_override_paper:
            extra_green = is_green & (~mask_override)
            rgb[extra_green] = [235, 232, 224]
    else:
        window_mask = is_green

    alpha[window_mask] = 20
    fringe = (g - np.maximum(r, b)) > 20
    rgb[fringe, 1] = np.maximum(r[fringe], b[fringe]) + 8

    if tint_rgb is not None:
        tr, tg, tb = tint_rgb
        rgb[:, :, 0] = np.clip(rgb[:, :, 0] * tr, 0, 255)
        rgb[:, :, 1] = np.clip(rgb[:, :, 1] * tg, 0, 255)
        rgb[:, :, 2] = np.clip(rgb[:, :, 2] * tb, 0, 255)

    out = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.surfarray.pixels3d(out)[:] = np.clip(rgb, 0, 255).astype(np.uint8).transpose(1, 0, 2)
    pygame.surfarray.pixels_alpha(out)[:] = alpha.transpose(1, 0)
    return out.convert_alpha(), is_green


def load_carriage_backgrounds(assets: Any, size: tuple[int, int]) -> dict[int, pygame.Surface]:
    """Load default carriage backgrounds (sketch, sunset, rain, courage, dawn)."""
    ckey = ("carriage_bgs", id(assets), size)
    if ckey in _UI_SURFACE_CACHE:
        return _UI_SURFACE_CACHE[ckey]

    sunset_rel = (
        "images/backgrounds/bg_carriage_sunset.jpeg"
        if paths.asset_path("images/backgrounds/bg_carriage_sunset.jpeg").exists()
        else "images/backgrounds/preview_carriage_sunset.png"
    )
    sunset_raw = assets.get_image(sunset_rel, fallback_style="sunset")
    sunset_surf, sunset_mask = _key_green_window_surface(sunset_raw, size)

    sketch_raw = assets.get_image("images/backgrounds/bg_carriage_sketch.jpeg", fallback_style="sketch")
    sketch_surf, _ = _key_green_window_surface(
        sketch_raw, size, mask_override=sunset_mask, fill_non_override_paper=True
    )

    rain_raw = assets.get_image("images/backgrounds/bg_carriage_rain.jpeg", fallback_style="rain")
    rain_surf, _ = _key_green_window_surface(rain_raw, size)

    courage_raw = assets.get_image("images/backgrounds/bg_carriage_courage.jpeg", fallback_style="courage")
    courage_surf, _ = _key_green_window_surface(courage_raw, size)

    dawn_surf, _ = _key_green_window_surface(sunset_raw, size, tint_rgb=(0.94, 1.06, 1.08))

    res = {
        0: sketch_surf,
        1: sunset_surf,
        2: rain_surf,
        3: courage_surf,
        4: dawn_surf,
    }
    _UI_SURFACE_CACHE[ckey] = res
    return res


def load_custom_carriage_variants(
    assets: Any,
    bg_rel: str,
    size: tuple[int, int],
) -> dict[int, pygame.Surface]:
    """Load a unique carriage background (Gerbong 4/3/1) and derive tinted cassette layers."""
    if not paths.asset_path(bg_rel).exists():
        return load_carriage_backgrounds(assets, size)

    ckey = ("custom_carriage", id(assets), bg_rel, size)
    if ckey in _UI_SURFACE_CACHE:
        return _UI_SURFACE_CACHE[ckey]

    raw = assets.get_image(bg_rel, fallback_style="sunset")
    base_surf, base_mask = _key_green_window_surface(raw, size)
    variants: dict[int, pygame.Surface] = {1: base_surf}
    for cid in (0, 2, 3, 4):
        if cid == 0:
            variants[0] = base_surf
        else:
            surf, _ = _key_green_window_surface(
                raw,
                size,
                mask_override=base_mask,
                tint_rgb=CASSETTES[cid].tint_rgb,
            )
            variants[cid] = surf
    _UI_SURFACE_CACHE[ckey] = variants
    return variants


def load_raka_sitting_layers(assets: Any, size: tuple[int, int]) -> dict[int, pygame.Surface]:
    """Load full-carriage layers showing Raka seated in the left corner (Raka_sit1..3)."""
    ckey = ("raka_sitting", id(assets), size)
    if ckey in _UI_SURFACE_CACHE:
        return _UI_SURFACE_CACHE[ckey]

    sit1_raw = assets.get_image("images/sprites/Raka_sit1.jpeg", fallback_style="sunset")
    sit1_surf, _ = _key_green_window_surface(sit1_raw, size)

    sit2_raw = assets.get_image("images/sprites/Raka_sit2.jpeg", fallback_style="rain")
    sit2_surf, _ = _key_green_window_surface(sit2_raw, size)

    sit3_raw = assets.get_image("images/sprites/Raka_sit3.jpeg", fallback_style="courage")
    sit3_surf, _ = _key_green_window_surface(sit3_raw, size)

    sit4_surf, _ = _key_green_window_surface(sit1_raw, size, tint_rgb=(0.94, 1.06, 1.08))

    rgb0 = pygame.surfarray.pixels3d(sit1_surf).copy()
    alpha0 = pygame.surfarray.pixels_alpha(sit1_surf).copy()
    gray = (0.299 * rgb0[:, :, 0] + 0.587 * rgb0[:, :, 1] + 0.114 * rgb0[:, :, 2]).astype(np.uint8)
    sketch_sit = pygame.Surface(size, pygame.SRCALPHA)
    pygame.surfarray.pixels3d(sketch_sit)[:] = np.stack([gray, gray, gray], axis=2)
    pygame.surfarray.pixels_alpha(sketch_sit)[:] = alpha0

    res = {
        0: sketch_sit.convert_alpha(),
        1: sit1_surf,
        2: sit2_surf,
        3: sit3_surf,
        4: sit4_surf,
    }
    _UI_SURFACE_CACHE[ckey] = res
    return res


def _remove_magenta_surf(surf: pygame.Surface) -> pygame.Surface:
    """Convert #FF00FF magenta background to alpha=0 and despill JPEG edge halos."""
    w, h = surf.get_size()
    rgb = pygame.surfarray.pixels3d(surf).transpose(1, 0, 2).astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]

    excess = np.minimum(r, b) - g
    bg_mask = (r > 155) & (b > 155) & (excess > 45)
    alpha = np.full((h, w), 255, dtype=np.uint8)
    alpha[bg_mask] = 0

    fringe = (~bg_mask) & (r > 125) & (b > 125) & (excess > 16)
    cap = np.clip(g[fringe] + 18, 0, 255)
    rgb[fringe, 0] = np.minimum(r[fringe], cap)
    rgb[fringe, 2] = np.minimum(b[fringe], cap)
    alpha[fringe] = np.clip(255 - excess[fringe] * 2, 95, 255).astype(np.uint8)

    out = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.surfarray.pixels3d(out)[:] = np.clip(rgb, 0, 255).astype(np.uint8).transpose(1, 0, 2)
    pygame.surfarray.pixels_alpha(out)[:] = alpha.transpose(1, 0)
    return out.convert_alpha()


def _find_1d_spans(mask_1d: np.ndarray, min_len: int = 32) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    inside = False
    start = 0
    for idx, val in enumerate(mask_1d):
        if val and not inside:
            inside = True
            start = idx
        elif not val and inside:
            if idx - start >= min_len:
                spans.append((start, idx))
            inside = False
    if inside and len(mask_1d) - start >= min_len:
        spans.append((start, len(mask_1d)))
    return spans


def _slice_row_sprites(
    clean_surf: pygame.Surface,
    expected_count: int,
    target_max_height: int,
) -> list[pygame.Surface]:
    """Slice horizontally spaced sprites, preserving relative height ratios."""
    alpha = pygame.surfarray.pixels_alpha(clean_surf).transpose(1, 0)
    fg = alpha > 40
    col_spans = _find_1d_spans(fg.any(axis=0), min_len=36)

    if len(col_spans) != expected_count:
        xs = np.where(fg.any(axis=0))[0]
        if len(xs) == 0:
            return [clean_surf] * expected_count
        x_min, x_max = int(xs.min()), int(xs.max())
        step = max(1, (x_max - x_min) // expected_count)
        col_spans = [(x_min + i * step, min(clean_surf.get_width(), x_min + (i + 1) * step)) for i in range(expected_count)]

    raw_crops: list[pygame.Surface] = []
    heights: list[int] = []
    for x0, x1 in col_spans:
        ys = np.where(fg[:, x0:x1].any(axis=1))[0]
        if len(ys) == 0:
            raw_crops.append(pygame.Surface((64, 64), pygame.SRCALPHA))
            heights.append(64)
            continue
        y0, y1 = max(0, int(ys.min()) - 2), min(clean_surf.get_height(), int(ys.max()) + 3)
        sub = clean_surf.subsurface(pygame.Rect(x0, y0, x1 - x0, y1 - y0)).copy()
        raw_crops.append(sub)
        heights.append(sub.get_height())

    max_h = max(heights) if heights else 1
    scale_ratio = target_max_height / float(max_h)
    scaled_list: list[pygame.Surface] = []
    for sub in raw_crops:
        nw = max(16, int(round(sub.get_width() * scale_ratio)))
        nh = max(16, int(round(sub.get_height() * scale_ratio)))
        scaled_list.append(pygame.transform.smoothscale(sub, (nw, nh)).convert_alpha())
    return scaled_list


def load_raka_sprite_frames(assets: Any, target_height: int = 310) -> dict[str, list[pygame.Surface]]:
    """Load real Raka idle and walk sprite sheets with #FF00FF removal (cached)."""
    ckey = ("raka_frames", id(assets), target_height)
    if ckey in _UI_SURFACE_CACHE:
        return _UI_SURFACE_CACHE[ckey]

    idle_path = "images/sprites/Raka_idle.jpeg"
    walk_path = "images/sprites/Raka_walk.jpeg"

    if paths.asset_path(idle_path).exists() and paths.asset_path(walk_path).exists():
        idle_clean = _remove_magenta_surf(assets.get_image(idle_path))
        walk_clean = _remove_magenta_surf(assets.get_image(walk_path))
        idle_frames = _slice_row_sprites(idle_clean, expected_count=4, target_max_height=target_height)
        walk_frames = _slice_row_sprites(walk_clean, expected_count=4, target_max_height=target_height)
        res = {"idle": idle_frames, "walk": walk_frames}
        _UI_SURFACE_CACHE[ckey] = res
        return res

    fallback = create_pixel_raka_frames()
    res = {
        "idle": [pygame.transform.scale(fallback["idle"], (170, target_height))],
        "walk": [
            pygame.transform.scale(fallback["walk1"], (170, target_height)),
            pygame.transform.scale(fallback["walk2"], (170, target_height)),
        ],
    }
    _UI_SURFACE_CACHE[ckey] = res
    return res


def load_passenger_sprites(assets: Any, target_max_height: int = 315) -> dict[str, pygame.Surface]:
    """Load legacy single-frame passenger sprites facing left toward Raka."""
    rel = "images/sprites/spr_npc_passengers.png"
    keys = ("child", "student", "shadow", "senja")
    if paths.asset_path(rel).exists():
        clean = _remove_magenta_surf(assets.get_image(rel))
        sliced = _slice_row_sprites(clean, expected_count=4, target_max_height=target_max_height)
        return {
            key: pygame.transform.flip(sliced[idx], True, False).convert_alpha()
            for idx, key in enumerate(keys)
        }
    return {}


def _build_shadow_raka_frames(raka_idle: list[pygame.Surface]) -> list[pygame.Surface]:
    """Create 4-frame left-facing shadow silhouette frames derived directly from Raka."""
    frames: list[pygame.Surface] = []
    for base in raka_idle:
        flipped = pygame.transform.flip(base, True, False).convert_alpha()
        rgb = pygame.surfarray.pixels3d(flipped).copy()
        alpha = pygame.surfarray.pixels_alpha(flipped).copy()
        # Tint into deep midnight indigo while retaining internal outline shading
        dark_rgb = np.zeros_like(rgb)
        dark_rgb[:, :, 0] = (rgb[:, :, 0].astype(np.float32) * 0.16 + 12).clip(0, 255).astype(np.uint8)
        dark_rgb[:, :, 1] = (rgb[:, :, 1].astype(np.float32) * 0.18 + 15).clip(0, 255).astype(np.uint8)
        dark_rgb[:, :, 2] = (rgb[:, :, 2].astype(np.float32) * 0.34 + 34).clip(0, 255).astype(np.uint8)
        out = pygame.Surface(flipped.get_size(), pygame.SRCALPHA)
        pygame.surfarray.pixels3d(out)[:] = dark_rgb
        pygame.surfarray.pixels_alpha(out)[:] = (alpha.astype(np.float32) * 0.92).astype(np.uint8)
        frames.append(out.convert_alpha())
    return frames


def load_npc_idle_animations(assets: Any) -> dict[str, list[pygame.Surface]]:
    """Load cached 4-frame proportional idle sprite sheets for all story characters."""
    ckey = ("npc_anims", id(assets))
    if ckey in _UI_SURFACE_CACHE:
        return _UI_SURFACE_CACHE[ckey]

    specs: dict[str, tuple[str, int]] = {
        "child": ("images/sprites/spr_bima_idle.png", 225),
        "student": ("images/sprites/spr_nadia_idle.png", 296),
        "senja": ("images/sprites/spr_senja_idle.png", 294),
        "kondektur": ("images/sprites/spr_kondektur_idle.png", 312),
        "raka_kecil": ("images/sprites/spr_raka_kecil_idle.png", 220),
    }
    animations: dict[str, list[pygame.Surface]] = {}
    for style, (rel, target_h) in specs.items():
        if paths.asset_path(rel).exists():
            clean = _remove_magenta_surf(assets.get_image(rel))
            animations[style] = _slice_row_sprites(clean, expected_count=4, target_max_height=target_h)

    raka_frames = load_raka_sprite_frames(assets, target_height=310)
    if raka_frames.get("idle"):
        animations["shadow"] = _build_shadow_raka_frames(raka_frames["idle"])

    # Fall back gracefully to legacy single-frame sheet only if needed
    legacy = load_passenger_sprites(assets)
    for style, surf in legacy.items():
        if style not in animations:
            animations[style] = [surf]
    _UI_SURFACE_CACHE[ckey] = animations
    return animations


def _slice_2x2_prop_sheet(
    assets: Any,
    rel: str,
    quad_names: tuple[str, str, str, str],
) -> dict[str, dict[str, pygame.Surface]]:
    """Slice any 2x2 prop sprite sheet into normalized world (54px) & icon (84px) surfaces."""
    if not paths.asset_path(rel).exists():
        return {}
    raw = assets.get_image(rel, fallback_style="sunset")
    clean = _remove_magenta_surf(raw)
    alpha = pygame.surfarray.pixels_alpha(clean).transpose(1, 0)
    fg = alpha > 40
    h, w = fg.shape
    quads = {
        quad_names[0]: (0, h // 2, 0, w // 2),
        quad_names[1]: (0, h // 2, w // 2, w),
        quad_names[2]: (h // 2, h, 0, w // 2),
        quad_names[3]: (h // 2, h, w // 2, w),
    }
    result: dict[str, dict[str, pygame.Surface]] = {}
    for name, (y0, y1, x0, x1) in quads.items():
        sub_fg = fg[y0:y1, x0:x1]
        ys, xs = np.where(sub_fg)
        if len(xs) == 0 or len(ys) == 0:
            box = clean.subsurface(pygame.Rect(x0, y0, max(16, x1 - x0), max(16, y1 - y0))).copy()
        else:
            rect = pygame.Rect(
                x0 + int(xs.min()),
                y0 + int(ys.min()),
                max(8, int(xs.max() - xs.min() + 1)),
                max(8, int(ys.max() - ys.min() + 1)),
            )
            box = clean.subsurface(rect).copy()

        bw, bh = box.get_size()
        world_h = 54
        world_w = max(24, int(round(bw * (world_h / max(1, bh)))))
        icon_h = 84
        icon_w = max(32, int(round(bw * (icon_h / max(1, bh)))))
        result[name] = {
            "world": pygame.transform.smoothscale(box, (world_w, world_h)).convert_alpha(),
            "icon": pygame.transform.smoothscale(box, (icon_w, icon_h)).convert_alpha(),
        }
    return result


def load_prop_sprites(assets: Any) -> dict[str, dict[str, pygame.Surface]]:
    """Slice base Walkman/tea/ticket sheet plus all 3 narrative story item sheets (cached)."""
    ckey = ("prop_sprites", id(assets))
    if ckey in _UI_SURFACE_CACHE:
        return _UI_SURFACE_CACHE[ckey]

    sheets: list[tuple[str, tuple[str, str, str, str]]] = [
        ("images/sprites/spr_props_items.jpeg", ("walkman", "tea", "ticket_99", "pocket_watch")),
        ("images/sprites/spr_story_items_1.png", ("phone_cracked", "cassette_d_sealed", "comic_book", "hospital_paper_plane")),
        ("images/sprites/spr_story_items_2.png", ("lunchbox_ibu", "house_model", "helmet_cracked", "umbrella_rejection")),
        ("images/sprites/spr_story_items_3.png", ("manuscript_folder", "polaroid", "conductor_cap", "ticket_stub")),
    ]
    merged: dict[str, dict[str, pygame.Surface]] = {}
    for rel, names in sheets:
        merged.update(_slice_2x2_prop_sheet(assets, rel, names))
    ui_tapes = _slice_walkman_ui(assets)
    if "tape_2" in ui_tapes:
        t2 = ui_tapes["tape_2"]
        merged["cassette_b"] = {
            "world": pygame.transform.smoothscale(t2, (56, 36)).convert_alpha(),
            "icon": pygame.transform.smoothscale(t2, (96, 60)).convert_alpha(),
        }
    _UI_SURFACE_CACHE[ckey] = merged
    return merged


def _bust_portrait_from_sprite(
    sprite: pygame.Surface,
    bg_rgb: tuple[int, int, int],
    border_rgb: tuple[int, int, int],
    size: tuple[int, int],
) -> pygame.Surface:
    """Create a crisp circular-framed bust portrait from an NPC sprite frame."""
    alpha = pygame.surfarray.pixels_alpha(sprite).transpose(1, 0)
    ys, xs = np.where(alpha > 35)
    card = pygame.Surface(size, pygame.SRCALPHA)
    card.fill(bg_rgb)
    if len(xs) > 0 and len(ys) > 0:
        x0, x1 = int(xs.min()), int(xs.max())
        y0, y1 = int(ys.min()), int(ys.max())
        bust_h = max(24, int((y1 - y0) * 0.48))
        cx = (x0 + x1) // 2
        half_w = max(16, int(bust_h * 0.56))
        crop_x = max(0, cx - half_w)
        crop_w = min(sprite.get_width() - crop_x, half_w * 2)
        crop_y = max(0, y0 - 4)
        crop_h = min(sprite.get_height() - crop_y, bust_h + 6)
        bust = sprite.subsurface(pygame.Rect(crop_x, crop_y, max(8, crop_w), max(8, crop_h))).copy()
        scaled = pygame.transform.smoothscale(bust, (size[0] - 8, size[1] - 8))
        card.blit(scaled, (4, 6))
    pygame.draw.rect(card, border_rgb, (0, 0, size[0], size[1]), 2)
    return card.convert_alpha()


def load_extra_portraits(assets: Any, size: tuple[int, int] = (92, 92)) -> dict[str, pygame.Surface]:
    """Generate consistent dialogue portraits for Conductor, Kakek Harjo, Raka Kecil & Shadow (cached)."""
    ckey = ("extra_portraits", id(assets), size)
    if ckey in _UI_SURFACE_CACHE:
        return _UI_SURFACE_CACHE[ckey]

    extras: dict[str, pygame.Surface] = {}
    anims = load_npc_idle_animations(assets)
    if anims.get("kondektur"):
        extras["kondektur"] = _bust_portrait_from_sprite(
            anims["kondektur"][0], (26, 34, 54), (242, 198, 108), size
        )
    if anims.get("raka_kecil"):
        extras["raka_kecil"] = _bust_portrait_from_sprite(
            anims["raka_kecil"][0], (52, 40, 32), (248, 174, 84), size
        )
    cg_harjo_rel = "images/cg/cg_end_01_grandpa_conductor.png"
    if paths.asset_path(cg_harjo_rel).exists():
        cg_img = assets.get_image(cg_harjo_rel)
        cw, ch = cg_img.get_size()
        crop = cg_img.subsurface(
            pygame.Rect(int(cw * 0.54), int(ch * 0.06), int(cw * 0.16), int(ch * 0.28))
        ).copy()
        extras["kakek_harjo"] = pygame.transform.smoothscale(crop, size).convert_alpha()
    elif "kondektur" in extras:
        extras["kakek_harjo"] = extras["kondektur"]

    raka_ports = load_raka_expression_portraits(assets, size)
    shadow_p = raka_ports.get("sad", raka_ports["calm"]).copy()
    shadow_p.fill((118, 148, 215, 255), special_flags=pygame.BLEND_RGBA_MULT)
    extras["bayangan"] = shadow_p
    _UI_SURFACE_CACHE[ckey] = extras
    return extras


def load_raka_expression_portraits(assets: Any, size: tuple[int, int] = (92, 92)) -> dict[str, pygame.Surface]:
    """Slice 2x2 close-up expression portraits of Raka (calm, surprised, sad, smile)."""
    ckey = ("raka_portraits", id(assets), size)
    if ckey in _UI_SURFACE_CACHE:
        return _UI_SURFACE_CACHE[ckey]

    rel = "images/portraits/port_raka_expressions.png"
    if not paths.asset_path(rel).exists():
        cutin = assets.get_image("images/portraits/preview_raka_cutin.png", fallback_style="courage")
        base = crop_raka_portrait(cutin, size)
        res = {"calm": base, "surprised": base, "sad": base, "smile": base}
        _UI_SURFACE_CACHE[ckey] = res
        return res

    sheet = assets.get_image(rel)
    sw, sh = sheet.get_size()
    gx0, gx1 = int(sw * 0.258), int(sw * 0.746)
    gy0, gy1 = int(sh * 0.026), int(sh * 0.985)
    mid_x = (gx0 + gx1) // 2
    mid_y = (gy0 + gy1) // 2
    pad = int(sw * 0.008)

    boxes = {
        "calm": pygame.Rect(gx0 + pad, gy0 + pad, mid_x - gx0 - pad * 2, mid_y - gy0 - pad * 2),
        "surprised": pygame.Rect(mid_x + pad, gy0 + pad, gx1 - mid_x - pad * 2, mid_y - gy0 - pad * 2),
        "sad": pygame.Rect(gx0 + pad, mid_y + pad, mid_x - gx0 - pad * 2, gy1 - mid_y - pad * 2),
        "smile": pygame.Rect(mid_x + pad, mid_y + pad, gx1 - mid_x - pad * 2, gy1 - mid_y - pad * 2),
    }
    res = {
        expr: pygame.transform.smoothscale(sheet.subsurface(rect).copy(), size).convert_alpha()
        for expr, rect in boxes.items()
    }
    _UI_SURFACE_CACHE[ckey] = res
    return res


def _slice_walkman_ui(assets: Any) -> dict[str, pygame.Surface]:
    """Slice Walkman player and 4 cassette tape icons from ui_walkman_cassette.jpeg."""
    rel = "images/ui/ui_walkman_cassette.jpeg"
    if not paths.asset_path(rel).exists():
        return {}
    raw = assets.get_image(rel)
    sw, sh = raw.get_size()
    rgb = pygame.surfarray.pixels3d(raw).transpose(1, 0, 2).astype(np.int16)
    bg = rgb[10, 10]
    dist = np.abs(rgb - bg).sum(axis=2)
    alpha = np.where(dist > 28, 255, 0).astype(np.uint8)
    clean = pygame.Surface((sw, sh), pygame.SRCALPHA)
    pygame.surfarray.pixels3d(clean)[:] = rgb.astype(np.uint8).transpose(1, 0, 2)
    pygame.surfarray.pixels_alpha(clean)[:] = alpha.transpose(1, 0)

    def crop_pct(x0p: float, y0p: float, x1p: float, y1p: float, out_size: tuple[int, int]) -> pygame.Surface:
        r = pygame.Rect(
            int(sw * x0p),
            int(sh * y0p),
            int(sw * (x1p - x0p)),
            int(sh * (y1p - y0p)),
        )
        return pygame.transform.smoothscale(clean.subsurface(r).copy(), out_size).convert_alpha()

    return {
        "walkman": crop_pct(0.044, 0.150, 0.365, 0.858, (30, 38)),
        "tape_1": crop_pct(0.422, 0.158, 0.682, 0.470, (48, 30)),
        "tape_2": crop_pct(0.698, 0.158, 0.964, 0.470, (48, 30)),
        "tape_3": crop_pct(0.422, 0.530, 0.682, 0.842, (48, 30)),
        "tape_4": crop_pct(0.698, 0.530, 0.964, 0.842, (48, 30)),
    }


def create_pixel_raka_frames() -> dict[str, pygame.Surface]:
    """Build crisp procedural fallback pixel-art sprites for Raka."""
    frames: dict[str, pygame.Surface] = {}
    scale = 4
    pw, ph = 24, 40

    def draw_pose(pose: str) -> pygame.Surface:
        s = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(s, (26, 24, 34), (7, 2, 10, 5))
        pygame.draw.rect(s, (238, 188, 148), (8, 7, 8, 7))
        pygame.draw.rect(s, (34, 52, 92), (6, 15, 12, 12))
        if pose == "walk1":
            pygame.draw.rect(s, (28, 32, 46), (7, 27, 4, 10))
            pygame.draw.rect(s, (28, 32, 46), (13, 27, 4, 9))
        elif pose == "walk2":
            pygame.draw.rect(s, (28, 32, 46), (9, 27, 4, 9))
            pygame.draw.rect(s, (28, 32, 46), (11, 27, 4, 10))
        else:
            pygame.draw.rect(s, (28, 32, 46), (8, 27, 4, 10))
            pygame.draw.rect(s, (28, 32, 46), (12, 27, 4, 10))
        return pygame.transform.scale(s, (pw * scale, ph * scale)).convert_alpha()

    for pose_name in ("idle", "walk1", "walk2"):
        frames[pose_name] = draw_pose(pose_name)
    return frames


def crop_raka_portrait(full_cutin: pygame.Surface, size: tuple[int, int] = (92, 92)) -> pygame.Surface:
    """Extract Raka's bust portrait cleanly from the cut-in banner."""
    cw, ch = full_cutin.get_size()
    crop_rect = pygame.Rect(int(cw * 0.28), int(ch * 0.06), int(cw * 0.42), int(ch * 0.84))
    cropped = full_cutin.subsurface(crop_rect).copy()
    return pygame.transform.smoothscale(cropped, size)


def render_cassette_atmosphere_filter(surface: pygame.Surface, cassette_id: int, t: float) -> None:
    """Render subtle atmospheric screen filters per cassette without cluttering the view."""
    w, h = surface.get_size()
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)

    if cassette_id == 0:
        pygame.draw.rect(overlay, (30, 28, 24, 48), (0, 0, w, h), 10)
    elif cassette_id == 1:
        for idx in range(3):
            sx = 310 + idx * 240 + int(math.sin(t * 0.6 + idx) * 18)
            pts = [(sx, 150), (sx + 95, 150), (sx - 120, h - 100), (sx - 215, h - 100)]
            pygame.draw.polygon(overlay, (255, 200, 115, 20), pts)
    elif cassette_id == 2:
        pygame.draw.rect(overlay, (18, 36, 82, 32), (0, 0, w, h), 16)
        for i in range(16):
            rx = (i * 79 + int(t * 14)) % w
            ry = (i * 61 + int(t * 95)) % (h - 120)
            pygame.draw.line(overlay, (140, 215, 255, 50), (rx, ry), (rx - 4, ry + 11), 1)
    elif cassette_id == 3:
        pulse = int(4 + math.sin(t * 5.0) * 4)
        pygame.draw.polygon(overlay, (220, 48, 64, 48), [(0, 0), (96 + pulse, 0), (0, 84 + pulse)])
        pygame.draw.polygon(overlay, (220, 48, 64, 48), [(w, 0), (w - 96 - pulse, 0), (w, 84 + pulse)])
    elif cassette_id == 4:
        pygame.draw.polygon(overlay, (215, 255, 235, 22), [(260, 120), (1020, 120), (880, h - 90), (140, h - 90)])

    surface.blit(overlay, (0, 0))


class VideoCutsceneOverlay:
    """Plays full-screen Google Flow MP4 cutscenes with literary captions and skip prompt."""

    def __init__(self) -> None:
        self.active = False
        self.video: Any = None
        self.duration = 6.0
        self.timer = 0.0
        self.title = ""
        self.captions: tuple[str, ...] = ()
        self.accent: tuple[int, int, int] = (248, 174, 84)

    def start(
        self,
        video_player: Any,
        title: str,
        captions: tuple[str, ...] | list[str],
        duration: float = 6.0,
        accent: tuple[int, int, int] = (248, 174, 84),
    ) -> None:
        self.video = video_player
        self.title = title
        self.captions = tuple(captions)
        self.duration = max(1.0, duration)
        self.timer = 0.0
        self.accent = accent
        self.active = True

    def stop(self) -> None:
        self.active = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.active:
            return False
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
            self.stop()
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.stop()
            return True
        return False

    def update(self, dt: float) -> bool:
        if not self.active:
            return False
        self.timer += dt
        if self.video is not None:
            self.video.update(dt)
        if self.timer >= self.duration:
            self.stop()
            return True
        return False

    def render(self, surface: pygame.Surface) -> None:
        if not self.active:
            return
        w, h = surface.get_size()
        if self.video is not None:
            surface.blit(self.video.get_surface(), (0, 0))
        else:
            surface.fill((12, 14, 22))

        pygame.draw.rect(surface, (10, 10, 14), (0, 0, w, 58))
        pygame.draw.rect(surface, (10, 10, 14), (0, h - 116, w, 116))
        pygame.draw.line(surface, self.accent, (0, h - 116), (w, h - 116), 2)

        f_title = get_ui_font(15, bold=True)
        f_cap = get_ui_font(20, serif=True)
        f_skip = get_ui_font(13, bold=True)

        surface.blit(f_title.render(self.title, True, self.accent), (28, 22))
        if self.captions:
            idx = min(len(self.captions) - 1, int((self.timer / self.duration) * len(self.captions)))
            cap = f_cap.render(self.captions[idx], True, (245, 246, 250))
            surface.blit(cap, (w // 2 - cap.get_width() // 2, h - 80))

        skip = f_skip.render("[SPACE / Klik] Lanjut", True, (195, 204, 218))
        surface.blit(skip, (w - skip.get_width() - 28, h - 28))


class DiagonalWipeTransition:
    """Sharp Persona-style diagonal polygon curtain wipe between carriages."""

    def __init__(self, duration: float = 0.50) -> None:
        self.duration = max(0.1, duration)
        self.timer = 0.0
        self.active = False
        self.accent = (232, 74, 88)

    def trigger(self, accent: tuple[int, int, int] = (232, 74, 88)) -> None:
        self.accent = accent
        self.timer = self.duration
        self.active = True

    def update(self, dt: float) -> None:
        if not self.active:
            return
        self.timer = max(0.0, self.timer - dt)
        if self.timer <= 0.0:
            self.active = False

    def render(self, surface: pygame.Surface) -> None:
        if not self.active:
            return
        w, h = surface.get_size()
        p = self.timer / self.duration
        reach = int((w + 260) * p)
        pts = [(0, 0), (reach, 0), (max(0, reach - 220), h), (0, h)]
        pygame.draw.polygon(surface, (10, 10, 14), pts)
        pygame.draw.line(surface, self.accent, (reach, 0), (max(0, reach - 220), h), 6)


class AllOutResonanceBanner:
    """Dramatic Persona cut-in + shards when a passenger's heart harmonizes."""

    def __init__(self, duration: float = 1.30) -> None:
        self.duration = duration
        self.timer = 0.0
        self.active = False
        self.title = "ALL-OUT RESONANCE!"
        self.subtitle = "Frekuensi hati telah selaras."
        self.accent = (248, 174, 84)
        self.shards: list[list[float]] = []

    def trigger(
        self,
        title: str = "MEMORY RESONANCE!",
        subtitle: str = "Satu keping kenangan telah pulih.",
        accent: tuple[int, int, int] = (248, 174, 84),
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.accent = accent
        self.timer = self.duration
        self.active = True
        self.shards = [
            [
                640.0 + random.uniform(-120, 120),
                320.0 + random.uniform(-70, 70),
                random.uniform(-620, 620),
                random.uniform(-420, 420),
                random.uniform(14, 34),
            ]
            for _ in range(22)
        ]

    def update(self, dt: float) -> None:
        if not self.active:
            return
        self.timer = max(0.0, self.timer - dt)
        for s in self.shards:
            s[0] += s[2] * dt
            s[1] += s[3] * dt
        if self.timer <= 0.0:
            self.active = False

    def render(self, surface: pygame.Surface, cutin_banner: pygame.Surface | None = None) -> None:
        if not self.active:
            return
        w, h = surface.get_size()
        ratio = 1.0 - (self.timer / self.duration)
        slide = math.sin(min(1.0, ratio * 1.15) * math.pi)
        band_h = max(24, int(245 * max(0.25, slide)))
        cy = h // 2 - 20

        for sx, sy, _, _, size in self.shards:
            pts = [
                (int(sx), int(sy - size)),
                (int(sx + size * 0.8), int(sy)),
                (int(sx - size * 0.3), int(sy + size * 0.7)),
            ]
            pygame.draw.polygon(surface, self.accent, pts)

        band_pts = [
            (0, cy - band_h // 2 + 28),
            (w, cy - band_h // 2 - 28),
            (w, cy + band_h // 2 - 28),
            (0, cy + band_h // 2 + 28),
        ]
        pygame.draw.polygon(surface, (12, 12, 18), band_pts)
        pygame.draw.polygon(surface, self.accent, band_pts, 5)

        if cutin_banner is not None:
            scaled = pygame.transform.smoothscale(cutin_banner, (920, max(16, band_h - 18)))
            surface.blit(scaled, ((w - 920) // 2, cy - scaled.get_height() // 2))

        f_big = get_ui_font(32, bold=True)
        t_shd = f_big.render(self.title, True, (12, 14, 20))
        t_main = f_big.render(self.title, True, (255, 250, 240))
        strip_y = cy + band_h // 2 - 22
        pygame.draw.polygon(
            surface,
            self.accent,
            [(190, strip_y), (w - 140, strip_y - 16), (w - 170, strip_y + 42), (160, strip_y + 50)],
        )
        tx = w // 2 - t_main.get_width() // 2
        ty = strip_y + 6
        surface.blit(t_shd, (tx + 2, ty + 2))
        surface.blit(t_main, (tx, ty))


class PersonaDialogueBox:
    """Auto-hiding, clean semi-transparent Persona dialogue box with choices."""

    def __init__(self) -> None:
        self.visible = False
        self.speaker = "Raka"
        self.lines: list[str] = [""]
        self.line_speakers: list[str] = []
        self.line_portraits: list[pygame.Surface | None] = []
        self.index = 0
        self.type_chars = 0.0
        self._last_blip_char = 0
        self.portrait: pygame.Surface | None = None
        self.accent: tuple[int, int, int] = (248, 174, 84)
        self.choices: list[str] = []
        self.selected_choice = 0
        self.choice_hitboxes: list[tuple[int, pygame.Rect]] = []
        self.hint_override: str | None = None

    def set_dialogue(
        self,
        speaker: str,
        lines: list[str] | tuple[str, ...],
        portrait: pygame.Surface | None = None,
        accent: tuple[int, int, int] = (248, 174, 84),
        choices: list[str] | None = None,
        hint_override: str | None = None,
        line_portraits: list[pygame.Surface | None] | None = None,
        line_speakers: list[str] | None = None,
    ) -> None:
        self.visible = True
        self.speaker = speaker
        self.lines = list(lines) if lines else [""]
        self.line_speakers = list(line_speakers) if line_speakers else []
        self.line_portraits = list(line_portraits) if line_portraits else []
        self.index = 0
        self.type_chars = 0.0
        self._last_blip_char = 0
        self.portrait = portrait
        self.accent = accent
        self.choices = list(choices) if choices else []
        self.selected_choice = 0
        self.hint_override = hint_override

    def hide(self) -> None:
        """Dismiss dialogue so the bottom of the carriage is 100% clear."""
        self.visible = False
        self.choices = []

    def is_on_last_line_finished(self) -> bool:
        return self.index >= len(self.lines) - 1 and self.type_chars >= len(self.lines[self.index])

    def update(self, dt: float, assets: Any | None = None) -> None:
        if not self.visible:
            return
        target = len(self.lines[self.index])
        if self.type_chars < target:
            self.type_chars = min(float(target), self.type_chars + dt * 46.0)
            cur_int = int(self.type_chars)
            if assets is not None and cur_int - self._last_blip_char >= 4:
                self._last_blip_char = cur_int
                ch = self.lines[self.index][max(0, cur_int - 1)]
                if ch.isalnum():
                    assets.play_sfx("text_blip", volume=0.07)

    def handle_event(self, event: pygame.event.Event) -> str | int | None:
        """Handle input while dialogue is visible. Returns choice index, 'finished', or None."""
        if not self.visible:
            return None

        showing_choices = bool(self.choices) and self.is_on_last_line_finished()
        if showing_choices:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_choice = (self.selected_choice - 1) % len(self.choices)
                    return None
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_choice = (self.selected_choice + 1) % len(self.choices)
                    return None
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return self.selected_choice
                if pygame.K_1 <= event.key <= pygame.K_3:
                    idx = event.key - pygame.K_1
                    if idx < len(self.choices):
                        return idx
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for idx, rect in self.choice_hitboxes:
                    if rect.collidepoint(event.pos):
                        return idx
            return None

        advance = event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN)
        if not advance and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Clicking anywhere when dialogue is open advances smoothly
            if event.pos[1] > 70:
                advance = True

        if advance:
            full_len = len(self.lines[self.index])
            if self.type_chars < full_len:
                self.type_chars = float(full_len)
                return None
            if self.index < len(self.lines) - 1:
                self.index += 1
                self.type_chars = 0.0
                self._last_blip_char = 0
                return None
            self.hide()
            return "finished"
        return None

    def render(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        w, _ = surface.get_size()
        accent = self.accent

        # Compact sleek translucent glass dialogue bar (leaves ~82% of screen open)
        box_rect = pygame.Rect(108, 578, w - 216, 120)
        panel = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        pygame.draw.polygon(
            panel,
            (14, 16, 24, 224),
            [(14, 0), (box_rect.width, 0), (box_rect.width - 14, box_rect.height), (0, box_rect.height)],
        )
        pygame.draw.polygon(
            panel,
            (*accent, 210),
            [(14, 0), (box_rect.width, 0), (box_rect.width - 14, box_rect.height), (0, box_rect.height)],
            2,
        )
        surface.blit(panel, box_rect.topleft)

        active_speaker = (
            self.line_speakers[self.index]
            if self.index < len(self.line_speakers) and self.line_speakers[self.index]
            else self.speaker
        )
        f_name = get_ui_font(15, bold=True)
        name_surf = f_name.render(active_speaker, True, (14, 16, 22))
        badge_w = max(140, name_surf.get_width() + 30)
        badge_pts = [
            (box_rect.left + 20, box_rect.top - 16),
            (box_rect.left + 20 + badge_w, box_rect.top - 18),
            (box_rect.left + 10 + badge_w, box_rect.top + 10),
            (box_rect.left + 10, box_rect.top + 12),
        ]
        pygame.draw.polygon(surface, accent, badge_pts)
        surface.blit(name_surf, (box_rect.left + 26, box_rect.top - 14))

        active_portrait = (
            self.line_portraits[self.index]
            if self.index < len(self.line_portraits) and self.line_portraits[self.index] is not None
            else self.portrait
        )
        if active_portrait is not None:
            px, py = box_rect.left + 22, box_rect.top + 16
            surface.blit(active_portrait, (px, py))
            pygame.draw.rect(surface, accent, (px, py, active_portrait.get_width(), active_portrait.get_height()), 2, border_radius=4)
            text_x = px + active_portrait.get_width() + 20
        else:
            text_x = box_rect.left + 28

        max_text_w = box_rect.right - text_x - 42
        full_text = self.lines[self.index]
        is_thought = full_text.lstrip().startswith("(")
        f_body = get_ui_font(17, serif=is_thought)

        # Pre-wrap full line cleanly (splitting em-dash compounds if needed) before typewriter slice
        tokens: list[str] = []
        for raw_w in full_text.split(" "):
            if "—" in raw_w and f_body.size(raw_w)[0] > max_text_w * 0.45:
                parts = raw_w.split("—")
                for pi, part in enumerate(parts):
                    tokens.append((part + "—") if pi < len(parts) - 1 else part)
            else:
                tokens.append(raw_w)

        full_wrapped: list[str] = []
        cur = ""
        for token in tokens:
            test = f"{cur} {token}".strip()
            if f_body.size(test)[0] <= max_text_w:
                cur = test
            else:
                if cur:
                    full_wrapped.append(cur)
                cur = token
        if cur:
            full_wrapped.append(cur)

        text_col = (210, 222, 240) if is_thought else (244, 246, 250)
        rem_chars = int(self.type_chars)
        for idx, line in enumerate(full_wrapped[:3]):
            if rem_chars <= 0:
                break
            visible_line = line[:rem_chars]
            rem_chars = max(0, rem_chars - len(line) - 1)
            surface.blit(f_body.render(visible_line, True, text_col), (text_x, box_rect.top + 16 + idx * 26))

        f_hint = get_ui_font(12, bold=True)
        hint_msg = self.hint_override or "SPACE / Klik untuk lanjut"
        h_surf = f_hint.render(hint_msg, True, accent)
        surface.blit(h_surf, (box_rect.right - h_surf.get_width() - 28, box_rect.bottom - 22))

        self.choice_hitboxes.clear()
        if self.choices and self.is_on_last_line_finished():
            f_ch = get_ui_font(15, bold=True)
            base_y = box_rect.top - 18 - len(self.choices) * 44
            for idx, label in enumerate(self.choices):
                y = base_y + idx * 42
                is_sel = idx == self.selected_choice
                rect = pygame.Rect(box_rect.left + 132, y, 720, 36)
                self.choice_hitboxes.append((idx, rect))
                skew_pts = [
                    (rect.left + 10, rect.top),
                    (rect.right, rect.top - 3),
                    (rect.right - 12, rect.bottom),
                    (rect.left, rect.bottom + 1),
                ]
                fill = accent if is_sel else (18, 22, 32)
                fg = (14, 16, 22) if is_sel else (240, 244, 248)
                pygame.draw.polygon(surface, (6, 8, 12), [(x + 4, y0 + 4) for x, y0 in skew_pts])
                pygame.draw.polygon(surface, fill, skew_pts)
                pygame.draw.polygon(surface, accent, skew_pts, 2)
                prefix = "> " if is_sel else "  "
                surface.blit(f_ch.render(f"{prefix}[{idx + 1}] {label}", True, fg), (rect.left + 18, rect.top + 7))


class WalkmanHUD:
    """Collapsible top-right minimalist Walkman pill (never blocks bottom gameplay)."""

    def __init__(self, assets: Any | None = None) -> None:
        self.hitboxes: list[tuple[int, pygame.Rect]] = []
        self.pill_rect = pygame.Rect(986, 14, 276, 48)
        self.expanded = False
        self.expand_timer = 0.0
        self.t = 0.0
        self.unlocked_cassettes: set[int] = {0, 1, 2, 3, 4}
        self._ui_sprites: dict[str, pygame.Surface] = _slice_walkman_ui(assets) if assets is not None else {}

    def set_unlocked(self, unlocked: list[int] | set[int] | tuple[int, ...]) -> None:
        self.unlocked_cassettes = {0, *(int(c) for c in unlocked)}

    def reload_art(self, assets: Any) -> None:
        self._ui_sprites = _slice_walkman_ui(assets)

    def reveal_briefly(self, seconds: float = 3.5) -> None:
        self.expanded = True
        self.expand_timer = seconds

    def update(self, dt: float, is_playing: bool) -> None:
        self.t += dt * (1.0 if is_playing else 0.15)
        if self.expanded and self.expand_timer > 0.0:
            # Keep open while hovered
            if not pygame.Rect(986, 14, 276, 175).collidepoint(pygame.mouse.get_pos()):
                self.expand_timer = max(0.0, self.expand_timer - dt)
                if self.expand_timer <= 0.0:
                    self.expanded = False

    def handle_click(self, pos: tuple[int, int]) -> int | None:
        if self.expanded:
            for cid, rect in self.hitboxes:
                if rect.collidepoint(pos):
                    self.reveal_briefly(3.0)
                    if cid != 0 and cid not in self.unlocked_cassettes:
                        return -2
                    return cid
        if self.pill_rect.collidepoint(pos):
            self.expanded = not self.expanded
            self.expand_timer = 4.0 if self.expanded else 0.0
            return -1  # Consumed toggle click without switching cassette
        return None

    def render(
        self,
        surface: pygame.Surface,
        cassette_id: int,
        assets: Any,
        top_offset: int = 14,
        unlocked_cassettes: list[int] | set[int] | tuple[int, ...] | None = None,
    ) -> None:
        if unlocked_cassettes is not None:
            self.set_unlocked(unlocked_cassettes)
        if not self._ui_sprites:
            self._ui_sprites = _slice_walkman_ui(assets)

        prof = CASSETTES[cassette_id]
        accent = prof.accent
        self.pill_rect = pygame.Rect(986, top_offset, 276, 48)

        # Top-right compact glass pill
        pill = pygame.Surface((self.pill_rect.width, self.pill_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(pill, (16, 18, 28, 212), (0, 0, self.pill_rect.width, self.pill_rect.height), border_radius=10)
        pygame.draw.rect(pill, (*accent, 220), (0, 0, self.pill_rect.width, self.pill_rect.height), 2, border_radius=10)
        surface.blit(pill, self.pill_rect.topleft)

        if "walkman" in self._ui_sprites:
            surface.blit(self._ui_sprites["walkman"], (self.pill_rect.left + 8, self.pill_rect.top + 5))

        f_title = get_ui_font(13, bold=True)
        f_small = get_ui_font(11, bold=True)

        surface.blit(
            f_title.render(prof.title[:22], True, (244, 246, 250)),
            (self.pill_rect.left + 44, self.pill_rect.top + 7),
        )
        # Subtle 6-bar equalizer + toggle cue
        eq_x = self.pill_rect.left + 44
        eq_y = self.pill_rect.bottom - 8
        tempo = {0: 1.5, 1: 4.5, 2: 3.2, 3: 4.8, 4: 3.8}.get(cassette_id, 4.0)
        for bi in range(6):
            bh = 2 if cassette_id == 0 else 4 + int(abs(math.sin(self.t * tempo + bi * 0.8)) * 10)
            pygame.draw.rect(surface, accent, (eq_x + bi * 9, eq_y - bh, 6, bh), border_radius=1)

        hint_lbl = "Tutup" if self.expanded else "1-4 Kaset"
        h_surf = f_small.render(hint_lbl, True, accent)
        hx = self.pill_rect.right - h_surf.get_width() - 22
        hy = self.pill_rect.bottom - 20
        surface.blit(h_surf, (hx, hy))
        cx = self.pill_rect.right - 13
        cy = hy + h_surf.get_height() // 2
        if self.expanded:
            pygame.draw.polygon(surface, accent, [(cx - 4, cy + 2), (cx + 4, cy + 2), (cx, cy - 3)])
        else:
            pygame.draw.polygon(surface, accent, [(cx - 4, cy - 2), (cx + 4, cy - 2), (cx, cy + 3)])

        self.hitboxes.clear()
        if not self.expanded:
            return

        # Expanded drawer drops down cleanly from top-right
        drawer_rect = pygame.Rect(986, top_offset + 52, 276, 118)
        drawer = pygame.Surface((drawer_rect.width, drawer_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(drawer, (14, 16, 24, 232), (0, 0, drawer_rect.width, drawer_rect.height), border_radius=10)
        pygame.draw.rect(drawer, (*accent, 210), (0, 0, drawer_rect.width, drawer_rect.height), 2, border_radius=10)
        surface.blit(drawer, drawer_rect.topleft)

        tape_key = f"tape_{cassette_id}"
        if tape_key in self._ui_sprites:
            surface.blit(self._ui_sprites[tape_key], (drawer_rect.left + 12, drawer_rect.top + 10))

        surface.blit(
            f_small.render(f"Lagu: {assets.current_bgm_title[:25]}", True, (200, 210, 224)),
            (drawer_rect.left + 68, drawer_rect.top + 18),
        )

        labels = [(0, "0"), (1, "1:Snj"), (2, "2:Hjn"), (3, "3:Dtk"), (4, "4:Fjr")]
        bx = drawer_rect.left + 10
        by = drawer_rect.top + 56
        for cid, lbl in labels:
            bw = 34 if cid == 0 else 52
            rect = pygame.Rect(bx, by, bw, 46)
            self.hitboxes.append((cid, rect))
            is_unlocked = (cid == 0) or (cid in self.unlocked_cassettes)
            is_active = cid == cassette_id
            if not is_unlocked:
                fill = (24, 26, 34)
                border = (78, 84, 96)
                txt_col = (108, 116, 130)
                disp = f"{cid}:Knc"
            else:
                fill = CASSETTES[cid].accent if is_active else (34, 38, 52)
                border = CASSETTES[cid].accent
                txt_col = (14, 16, 22) if is_active else (228, 232, 240)
                disp = lbl
            pygame.draw.rect(surface, fill, rect, border_radius=6)
            pygame.draw.rect(surface, border, rect, 2, border_radius=6)
            t_surf = f_small.render(disp, True, txt_col)
            surface.blit(t_surf, (rect.centerx - t_surf.get_width() // 2, rect.centery - t_surf.get_height() // 2))
            bx += bw + 4
