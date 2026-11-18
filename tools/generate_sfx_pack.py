"""Synthesize 10 warm, studio-clean acoustic 44.1kHz stereo WAV sound effects into assets/audio/sfx/."""

from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[1]
SFX_DIR = ROOT_DIR / "assets" / "audio" / "sfx"
SAMPLE_RATE = 44100


def _save_wav(filename: str, samples: np.ndarray) -> Path:
    SFX_DIR.mkdir(parents=True, exist_ok=True)
    peak = float(np.max(np.abs(samples)))
    if peak > 0.92:
        samples = samples * (0.88 / peak)
    pcm = np.clip(samples * 32767.0, -32767.0, 32767.0).astype(np.int16)
    stereo = np.column_stack((pcm, pcm))
    out_path = SFX_DIR / filename
    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(stereo.tobytes())
    return out_path


def _lowpass_smooth(x: np.ndarray, passes: int = 2) -> np.ndarray:
    y = x.copy()
    kernel = np.array([0.25, 0.5, 0.25], dtype=np.float64)
    for _ in range(passes):
        y = np.convolve(y, kernel, mode="same")
    return y


def make_cassette_click() -> np.ndarray:
    """Warm retro tape deck mechanical latch + muted spring snap."""
    dur = 0.14
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    rng = np.random.default_rng(11)
    thud = np.sin(2 * np.pi * 145 * t) * np.exp(-65.0 * t)
    t2 = np.maximum(0.0, t - 0.042)
    latch = np.sin(2 * np.pi * 620 * t2) * np.exp(-95.0 * t2) * (t >= 0.042)
    noise = _lowpass_smooth(rng.normal(0, 0.16, len(t)), passes=3) * np.exp(-55.0 * t)
    return 0.55 * thud + 0.40 * latch + 0.25 * noise


def make_footstep_wood() -> np.ndarray:
    """Soft muffled shoe tap on vintage wooden train carriage planks."""
    dur = 0.11
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    rng = np.random.default_rng(22)
    wood_body = np.sin(2 * np.pi * (115 * np.exp(-12 * t)) * t) * np.exp(-42.0 * t)
    brush = _lowpass_smooth(rng.normal(0, 0.12, len(t)), passes=5) * np.exp(-48.0 * t)
    return 0.35 * wood_body + 0.18 * brush


def make_text_blip() -> np.ndarray:
    """Ultra-soft, warm felt piano/marimba dialogue tick."""
    dur = 0.048
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    attack = np.minimum(1.0, t / 0.004)
    decay = np.exp(-90.0 * t)
    tone = 0.65 * np.sin(2 * np.pi * 440.0 * t) + 0.25 * np.sin(2 * np.pi * 880.0 * t)
    return 0.22 * attack * decay * tone


def make_paper_rustle() -> np.ndarray:
    """Warm soft paper ticket / sketchbook flip."""
    dur = 0.22
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    rng = np.random.default_rng(33)
    raw = rng.normal(0, 1.0, len(t))
    smooth = _lowpass_smooth(raw, passes=2) - _lowpass_smooth(raw, passes=10)
    env = np.sin(np.pi * (t / dur)) ** 1.4
    return 0.28 * smooth * env


def make_door_slide() -> np.ndarray:
    """Gentle pneumatic whoosh + wooden latch of inter-carriage sliding door."""
    dur = 0.42
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    rng = np.random.default_rng(44)
    air = _lowpass_smooth(rng.normal(0, 0.24, len(t)), passes=6)
    env = np.sin(np.pi * (t / dur))
    clack = np.sin(2 * np.pi * 165 * t) * np.exp(-55.0 * t)
    return 0.35 * air * env + 0.32 * clack


def make_resonance_chime() -> np.ndarray:
    """Lush Fender Rhodes / celesta harmonic swell for Memory Resonance."""
    dur = 1.45
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    notes = (261.63, 329.63, 392.00, 493.88, 587.33)
    out = np.zeros_like(t)
    for idx, freq in enumerate(notes):
        onset = idx * 0.055
        dt_n = np.maximum(0.0, t - onset)
        active = (t >= onset).astype(np.float64)
        attack = np.minimum(1.0, dt_n / 0.015)
        decay = np.exp(-2.8 * dt_n)
        voice = 0.7 * np.sin(2 * np.pi * freq * dt_n) + 0.2 * np.sin(2 * np.pi * freq * 2.0 * dt_n) * np.exp(-6.0 * dt_n)
        out += active * attack * decay * voice
    return 0.24 * out


def make_ticket_punch() -> np.ndarray:
    """Crisp metallic brass conductor ticket punch click & card snip."""
    dur = 0.16
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    rng = np.random.default_rng(55)
    # Brass snap + crisp card perforation
    metal = (
        0.55 * np.sin(2 * np.pi * 1480.0 * t)
        + 0.35 * np.sin(2 * np.pi * 2320.0 * t)
    ) * np.exp(-75.0 * t)
    t_rel = np.maximum(0.0, t - 0.032)
    snip = np.sin(2 * np.pi * 880.0 * t_rel) * np.exp(-85.0 * t_rel) * (t >= 0.032)
    card = _lowpass_smooth(rng.normal(0, 0.15, len(t)), passes=2) * np.exp(-60.0 * t)
    return 0.45 * metal + 0.35 * snip + 0.20 * card


def make_phone_vibrate() -> np.ndarray:
    """Subtle smartphone double-buzz vibration for ending twist."""
    dur = 0.65
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    buzz1 = ((t >= 0.02) & (t <= 0.22)).astype(np.float64)
    buzz2 = ((t >= 0.32) & (t <= 0.56)).astype(np.float64)
    env = buzz1 * np.sin(np.pi * np.clip((t - 0.02) / 0.20, 0, 1)) + buzz2 * np.sin(np.pi * np.clip((t - 0.32) / 0.24, 0, 1))
    carrier = 0.65 * np.sin(2 * np.pi * 165.0 * t) + 0.25 * np.sin(2 * np.pi * 330.0 * t)
    return 0.30 * env * carrier


def make_wind_petals() -> np.ndarray:
    """Gentle coastal morning breeze & airy shimmer for farewells & ending."""
    dur = 1.85
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    rng = np.random.default_rng(66)
    raw = rng.normal(0, 1.0, len(t))
    breeze = _lowpass_smooth(raw, passes=18)
    env = np.sin(np.pi * (t / dur)) ** 1.1
    shimmer = 0.08 * np.sin(2 * np.pi * 659.25 * t) * np.exp(-1.8 * t)
    return 0.48 * breeze * env + shimmer


def make_memory_ache() -> np.ndarray:
    """Low warm heartbeat + distant music-box chime when entering a flashback."""
    dur = 1.20
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    beat1 = np.sin(2 * np.pi * 58.0 * t) * np.exp(-14.0 * t)
    t2 = np.maximum(0.0, t - 0.26)
    beat2 = np.sin(2 * np.pi * 54.0 * t2) * np.exp(-16.0 * t2) * (t >= 0.26)
    chime = (
        0.18 * np.sin(2 * np.pi * 783.99 * np.maximum(0.0, t - 0.10)) * np.exp(-4.0 * np.maximum(0.0, t - 0.10)) * (t >= 0.10)
        + 0.15 * np.sin(2 * np.pi * 659.25 * np.maximum(0.0, t - 0.35)) * np.exp(-3.5 * np.maximum(0.0, t - 0.35)) * (t >= 0.35)
    )
    return 0.45 * beat1 + 0.35 * beat2 + chime


def main() -> None:
    generators = {
        "sfx_cassette_click.wav": make_cassette_click,
        "sfx_footstep_wood.wav": make_footstep_wood,
        "sfx_text_blip.wav": make_text_blip,
        "sfx_paper_rustle.wav": make_paper_rustle,
        "sfx_door_slide.wav": make_door_slide,
        "sfx_resonance_chime.wav": make_resonance_chime,
        "sfx_ticket_punch.wav": make_ticket_punch,
        "sfx_phone_vibrate.wav": make_phone_vibrate,
        "sfx_wind_petals.wav": make_wind_petals,
        "sfx_memory_ache.wav": make_memory_ache,
    }
    for fname, fn in generators.items():
        path = _save_wav(fname, fn())
        print(f"Generated: {path}")


if __name__ == "__main__":
    main()
