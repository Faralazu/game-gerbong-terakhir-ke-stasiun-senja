"""Wuthering Waves-style 25-CG narrative cutscene engine, transitions, and gallery tracker."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any

import pygame

from src.core import paths
from src.core.persona_ui import get_ui_font


@dataclass(frozen=True)
class CGSlide:
    """One full-screen static illustration slide with multi-line Wuthering Waves subtitles."""

    cg_id: str
    rel_path: str
    title: str
    category: str
    lines: tuple[tuple[str, str], ...]  # (speaker, text) — "" means italic inner thought
    sfx_on_enter: str = ""
    bgm_override: str = ""
    particles: str = "none"  # "none", "dust", "gold", "petals"


@dataclass(frozen=True)
class CGSequence:
    """Ordered sequence of CG slides with black or white fade transitions."""

    seq_id: str
    fade_color: tuple[int, int, int]  # (0,0,0) for flashbacks, (250,248,242) for farewell/ending
    slides: tuple[CGSlide, ...]
    bgm_rel: str = ""
    shake_on_enter: bool = False


ALL_CG_SLIDES: tuple[CGSlide, ...] = (
    # --- PROLOG (3) ---
    CGSlide(
        cg_id="cg_00a_wakeup_window",
        rel_path="images/cg/cg_00a_wakeup_window.png",
        title="Terbangun di Dunia Kelabu",
        category="Prolog",
        bgm_override="audio/bgm/bgm_00_sketch_rails.mp3",
        particles="dust",
        lines=(
            ("", "Deru besi di atas rel tidak pernah benar-benar hilang, bahkan di dalam tidur yang paling berat."),
            ("", "Saat mataku terbuka, seluruh isi gerbong tampak pucat tanpa warna—seperti digambar dengan pensil di atas kertas buram."),
            ("Raka", "Aku... ketiduran lagi di kereta sepulang kantor ya? Tapi kenapa di luar cuma ada hamparan laut...?"),
        ),
    ),
    CGSlide(
        cg_id="cg_00b_ticket_hands",
        rel_path="images/cg/cg_00b_ticket_hands.png",
        title="Tiket Pukul 23:59",
        category="Prolog",
        sfx_on_enter="paper",
        lines=(
            ("", "Di antara jari-jariku terselip secarik tiket kereta yang sudah sedikit kusut."),
            ("Raka", "Jam keberangkatannya tercetak tepat pukul 23:59... dan nama stasiun tujuannya terhapus seperti terkena air."),
            ("", "Ibu jari kananku refleks menggesek telunjuk—kebiasaan lama, seolah aku masih menjepit pensil yang sudah setahun tidak pernah kupegang lagi."),
        ),
    ),
    CGSlide(
        cg_id="cg_00c_walkman_bench",
        rel_path="images/cg/cg_00c_walkman_bench.png",
        title="Walkman Perak Kakek",
        category="Prolog",
        particles="dust",
        lines=(
            ("", "Di bangku kosong seberang, hanya satu benda yang masih menyimpan sedikit warna di tengah ruangan yang bisu."),
            ("Raka", "Walkman perak peninggalan Kakek... dan di dalamnya sudah terpasang satu kaset bertuliskan tulisan tangan Senja."),
            ("", "Entah mengapa, sesuatu di dalam dadaku bilang aku harus menekan tombol PLAY itu sekarang."),
        ),
    ),
    # --- KILAS BALIK 1: GERBONG 4 (2) ---
    CGSlide(
        cg_id="cg_fb1a_grandpa_shoulders",
        rel_path="images/cg/cg_fb1a_grandpa_shoulders.png",
        title="Pundak Kakek Harjo",
        category="Kilas Balik",
        sfx_on_enter="memory_ache",
        bgm_override="audio/bgm/bgm_05_flashback_musicbox.mp3",
        particles="dust",
        lines=(
            ("", "Begitu melewati pintu Gerbong 4, pelipisku berdenyut tajam. Suara rel berubah menjadi dengung kotak musik tua."),
            ("Kakek Harjo", "Lihat, Le. Kereta itu selalu tahu ke mana harus pulang, sejauh apa pun dia jalan."),
            ("", "Tahun 2008. Pundak Kakek selalu hangat, dan lokomotif jingga Senja Utama melintas membelah sore Surabaya."),
        ),
    ),
    CGSlide(
        cg_id="cg_fb1b_first_sketchbook",
        rel_path="images/cg/cg_fb1b_first_sketchbook.png",
        title="Buku Sketsa Pertama",
        category="Kilas Balik",
        lines=(
            ("Kakek Harjo", "Kalau capek lihat jalanan yang lurus terus, gambar aja pemandangan yang pengen kamu tuju, Rak."),
            ("", "Tangan keriput Kakek meletakkan buku gambar kosong dan Walkman perak itu di pangkuanku."),
            ("", "Kenangan itu muncul begitu saja, membuat kepalaku terasa berat... sebelum perlahan memudar kembali."),
        ),
    ),
    # --- PERPISAHAN BIMA (2) ---
    CGSlide(
        cg_id="cg_bima_a_paper_plane_window",
        rel_path="images/cg/cg_bima_a_paper_plane_window.png",
        title="Pesawat Kertas di Atas Laut",
        category="Perpisahan",
        sfx_on_enter="wind_petals",
        particles="gold",
        lines=(
            ("", "Jendela besar di tengah gerbong terbuka selebar satu lengan, membiarkan angin laut senja masuk menyapu rambut kami."),
            ("Raka", "Ayo, Bim. Pegang ujung sayapnya pelan-pelan—biar kita lihat seberapa jauh kertas ini bisa terbang."),
            ("Bima", "Satu... dua... tiga! Terbang, pesawat! Kejar tiang keseratus!"),
        ),
    ),
    CGSlide(
        cg_id="cg_bima_b_thank_you_fade",
        rel_path="images/cg/cg_bima_b_thank_you_fade.png",
        title="Terima Kasih, Mas Raka",
        category="Perpisahan",
        sfx_on_enter="wind_petals",
        particles="gold",
        lines=(
            ("", "Pesawat kertas bertuliskan 'Mas Dimas, gambar lagi ya' meluncur tinggi di atas laut keemasan tanpa pernah jatuh."),
            ("Bima", "Mas lihat kan? Ternyata aku bukan beban... dan pesawatnya sampai!"),
            ("Bima", "Terima kasih, Mas Raka!"),
            ("", "Senyum anak itu bersinar sangat terang, sebelum jas hujan kuningnya perlahan larut menjadi butiran cahaya hangat."),
        ),
    ),
    # --- KILAS BALIK 2: GERBONG 3 (2) ---
    CGSlide(
        cg_id="cg_fb2a_bus_stop_meet",
        rel_path="images/cg/cg_fb2a_bus_stop_meet.png",
        title="Halte Kampus Saat Senja",
        category="Kilas Balik",
        sfx_on_enter="memory_ache",
        bgm_override="audio/bgm/bgm_05_flashback_musicbox.mp3",
        lines=(
            ("", "Saat membuka pintu Gerbong 3, aroma hujan sore tujuh tahun lalu tiba-tiba menusuk ingatanku."),
            ("Senja", "Keretamu kelihatan kayak lagi kangen sesuatu. Aku Senja. Kamu yang gambar, aku yang nulis ceritanya, mau nggak?"),
            ("", "Jepit rambut kuning mustardnya berkilat di balik gerimis halte kampus. Saat itu aku bahkan terlalu kikuk untuk mengangguk."),
        ),
    ),
    CGSlide(
        cg_id="cg_fb2b_rooftop_drawing",
        rel_path="images/cg/cg_fb2b_rooftop_drawing.png",
        title="Atap Gedung & TRACK 99",
        category="Kilas Balik",
        particles="dust",
        lines=(
            ("Senja", "Ini mixtape buatan aku! Empat kaset buat empat mood kamu kalau lagi buntu gambar komik kita!"),
            ("", "Atap gedung kampus, es teh yang mencair, dan lembaran sketsa proyek kecil kami yang kami beri judul TRACK 99."),
            ("", "Kenapa... dada rasanya sesak sekali setiap kali suara tawanya terputar di kepalaku malam ini?"),
        ),
    ),
    # --- PERPISAHAN NADIA (2) ---
    CGSlide(
        cg_id="cg_nadia_a_paper_house_model",
        rel_path="images/cg/cg_nadia_a_paper_house_model.png",
        title="Maket Rumah Tepi Laut",
        category="Perpisahan",
        sfx_on_enter="paper",
        particles="dust",
        lines=(
            ("", "Di bawah cahaya hangat lampu meja, kami merapikan potongan karton kecil dari blueprint yang selama ini tersembunyi."),
            ("Raka", "Atap terasnya sudah pas menghadap laut. Kelihatannya hangat sekali, Nad."),
            ("Nadia", "Bu... maaf kemarin malam aku kasar. Rumahnya udah jadi ya, Bu. Tungguin aku pulang."),
        ),
    ),
    CGSlide(
        cg_id="cg_nadia_b_thank_you_fade",
        rel_path="images/cg/cg_nadia_b_thank_you_fade.png",
        title="Jangan Bilang 'Nanti' Lagi",
        category="Perpisahan",
        sfx_on_enter="wind_petals",
        particles="gold",
        lines=(
            ("", "Setelah menyimpan pesan suara itu, bahu Nadia yang sejak tadi menegang akhirnya turun sepenuhnya."),
            ("Nadia", "Ternyata berdiri sebentar dan mengaku capek nggak bikin aku jadi anak yang gagal ya, Mas."),
            ("Nadia", "Terima kasih, Raka. Kamu juga... jangan bilang 'nanti' lagi, ya."),
            ("", "Cahaya biru lembut menyelimutinya, dan beberapa detik kemudian hanya maket rumah kertas yang tersisa di meja."),
        ),
    ),
    # --- KILAS BALIK 3: GERBONG 2 (2) ---
    CGSlide(
        cg_id="cg_fb3a_rain_torn_sketch",
        rel_path="images/cg/cg_fb3a_rain_torn_sketch.png",
        title="Malam Penolakan & Hujan",
        category="Kilas Balik",
        sfx_on_enter="memory_ache",
        bgm_override="audio/bgm/bgm_05_flashback_musicbox.mp3",
        lines=(
            ("", "Langkahku ke Gerbong 2 langsung ditampar ingatan paling dingin yang selama ini kupaksa kubur."),
            ("", "Tiga surat penolakan penerbit basah di aspal gang kos. Komentar kejam di layar ponsel masih terngiang."),
            ("", "Tanganku sendiri yang mencabik buku sketsa TRACK 99 itu di bawah hujan, membenci diriku yang pernah berani bermimpi."),
        ),
    ),
    CGSlide(
        cg_id="cg_fb3b_umbrella_turnaway",
        rel_path="images/cg/cg_fb3b_umbrella_turnaway.png",
        title="Di Bawah Payung yang Sama",
        category="Kilas Balik",
        lines=(
            ("", "Senja berlari menyusul dengan napas terengah, mengangkat payung bening tepat di atas kepalaku yang basah."),
            ("Raka", "Udah, Ja. Mimpi kita ketinggian. Aku cuma bikin kamu ikut buang-buang waktu."),
            ("", "Aku memalingkan wajah dengan dingin—padahal yang paling aku benci malam itu adalah diriku sendiri."),
        ),
    ),
    # --- PERPISAHAN BAYANGAN / RAKA KECIL (2) ---
    CGSlide(
        cg_id="cg_bayangan_a_drawing_together",
        rel_path="images/cg/cg_bayangan_a_drawing_together.png",
        title="Garis Emas Kintsugi",
        category="Perpisahan",
        sfx_on_enter="chime",
        particles="gold",
        lines=(
            ("", "Sosok bayangan gelap itu luruh—krayon dan senyum ompong masa kecilku kembali hadir di lantai gerbong."),
            ("Raka Kecil", "Lihat deh, Kak! Halaman yang tadi robek disambung pakai garis emas malah kelihatan lebih bagus, ya?"),
            ("Raka", "Iya... Untuk pertama kalinya setelah setahun, tanganku nggak gemetar lagi waktu pegang pensil."),
        ),
    ),
    CGSlide(
        cg_id="cg_bayangan_b_hug_fade",
        rel_path="images/cg/cg_bayangan_b_hug_fade.png",
        title="Memeluk Diri Sendiri",
        category="Perpisahan",
        sfx_on_enter="wind_petals",
        particles="gold",
        lines=(
            ("", "Aku berlutut dan memeluk anak delapan tahun yang selama ini kutitipkan sendirian di sudut gelap ingatanku."),
            ("Raka Kecil", "Terima kasih udah inget aku lagi, Raka."),
            ("", "Hangat sinar matahari meresap tepat ke dalam dadaku, dan hujan deras di luar jendela perlahan berhenti."),
        ),
    ),
    # --- KILAS BALIK 4: GERBONG 1 (2) ---
    CGSlide(
        cg_id="cg_fb4a_office_last_text",
        rel_path="images/cg/cg_fb4a_office_last_text.png",
        title="Pesan Pukul 23:41",
        category="Kilas Balik",
        sfx_on_enter="memory_ache",
        bgm_override="audio/bgm/bgm_05_flashback_musicbox.mp3",
        lines=(
            ("", "Kantor agensi iklan yang sepi. Pukul 23:41. Layar ponselku menyala dengan pesan dari Senja."),
            ("Senja", "'Rak, besok jam 06.00 pagi aku berangkat ke Jogja dari Peron 2 Stasiun Kotabaru. Aku bawa bab terakhir TRACK 99. Kalau sempat, aku tunggu ya.'"),
            ("", "Aku mengetik 'Aku dateng, Ja', lalu menghapusnya. Mengetiknya lagi... lalu berlari mengejar kereta terakhir."),
        ),
    ),
    CGSlide(
        cg_id="cg_fb4b_last_train_2359",
        rel_path="images/cg/cg_fb4b_last_train_2359.png",
        title="Kereta Terakhir 23:59",
        category="Kilas Balik",
        lines=(
            ("", "Di pojok kursi kereta komuter malam yang kosong, kupasang headphone Walkman Kakek untuk meredam pening yang berat."),
            ("", "Jam peron di luar kaca melintas tepat di angka 23:59 ketika kelopak mataku menutup perlahan."),
            ("", "Tentu saja... dari malam itulah aku tertidur dan terbawa sampai ke gerbong ini."),
        ),
    ),
    # --- PERPISAHAN SENJA (2) ---
    CGSlide(
        cg_id="cg_senja_a_cockpit_sunrise",
        rel_path="images/cg/cg_senja_a_cockpit_sunrise.png",
        title="Fajar di Kaca Masinis",
        category="Perpisahan",
        sfx_on_enter="wind_petals",
        particles="gold",
        lines=(
            ("", "Keempat kaset—Senja, Hujan, Detak, dan Fajar—menyatu menjadi satu harmoni saat tuas rem kuningan ditarik perlahan."),
            ("Senja", "Lihat ke depan, Rak. Kereta nggak pernah bisa jalan mundur—tapi pemandangan di depan nggak kalah indah kok."),
            ("Raka", "Maaf aku butuh waktu lama banget buat sampai di gerbong paling depan ini, Ja."),
        ),
    ),
    CGSlide(
        cg_id="cg_senja_b_thank_you_fade",
        rel_path="images/cg/cg_senja_b_thank_you_fade.png",
        title="Giliran Kamu yang Pulang",
        category="Perpisahan",
        sfx_on_enter="wind_petals",
        particles="petals",
        lines=(
            ("", "Senja menyerahkan halaman terakhir naskah TRACK 99—sebuah gambar dua sahabat di peron di bawah langit pagi."),
            ("Senja", "Aku nggak pernah marah, Rak. Aku cuma pengen kamu berhenti menyalahkan dirimu sendiri."),
            ("Senja", "Terima kasih, Raka. Sekarang giliran kamu yang pulang."),
            ("", "Cahaya fajar keemasan memeluk sosoknya hingga seluruh ruang kokpit dipenuhi sinar pagi yang tenang."),
        ),
    ),
    # --- ENDING STASIUN FAJAR (6) ---
    CGSlide(
        cg_id="cg_end_01_grandpa_conductor",
        rel_path="images/cg/cg_end_01_grandpa_conductor.png",
        title="Waktunya Turun, Le",
        category="Ending",
        sfx_on_enter="ticket_punch",
        bgm_override="audio/bgm/bgm_06_ending_wind.mp3",
        particles="petals",
        lines=(
            ("", "Di samping pintu kereta yang terbuka ke peron pagi, Pak Kondektur akhirnya melubangi Tiket 23:59 milikku dengan bentuk bintang."),
            ("", "Lalu ia melepas topi pet birunya perlahan. Rambut putih dan senyum keriput yang sangat kukenal itu tampak jelas di cahaya fajar."),
            ("Kakek Harjo", "Waktunya turun, Le."),
        ),
    ),
    CGSlide(
        cg_id="cg_end_02_translucent_hand_phone",
        rel_path="images/cg/cg_end_02_translucent_hand_phone.png",
        title="Kebenaran di Telapak Tangan",
        category="Ending",
        sfx_on_enter="phone_vibrate",
        particles="petals",
        lines=(
            ("", "Begitu kakiku menginjak peron batu yang basah, sehelai kelopak bunga melayang... dan menembus telapak tanganku yang tembus cahaya."),
            ("", "Di saat yang sama, ponsel retak di sakuku bergetar. Layarnya menyala menampilkan tanggal satu tahun setelah malam 23:59 itu."),
            ("Senja (Pesan Tersimpan)", "'Rak... Ibu telepon aku. Katanya kamu ketiduran di kereta terakhir semalam dan nggak bangun lagi. Aku nggak nyangka...'"),
            ("Raka", "...Oh. Jadi bukan Senja yang pergi. Aku yang tidak pernah sampai ke peron malam itu."),
        ),
    ),
    CGSlide(
        cg_id="cg_end_03_senja_bench_comic",
        rel_path="images/cg/cg_end_03_senja_bench_comic.png",
        title="Peron 2 Stasiun Kotabaru, 06.00",
        category="Ending",
        particles="petals",
        lines=(
            ("", "Stasiun Fajar menyatu dengan Peron 2 Stasiun Kotabaru satu tahun kemudian. Di bangku kayu, Senja yang hidup duduk memeluk buku komik cetak dan Walkman perakku."),
            ("", "Aku berdiri tepat di belakangnya, nyaris sepenuhnya menyatu dengan cahaya pagi—namun tidak ada lagi sesak di dadaku."),
            ("Raka", "Maaf aku telat, Ja. Terima kasih udah nungguin aku sampai siap."),
        ),
    ),
    CGSlide(
        cg_id="cg_end_04_raka_dissolve_wind",
        rel_path="images/cg/cg_end_04_raka_dissolve_wind.png",
        title="Tertiup Angin Fajar",
        category="Ending",
        sfx_on_enter="wind_petals",
        particles="petals",
        lines=(
            ("", "Angin laut pagi berembus lembut menyapu peron. Dari ujung jari dan bahuku, tubuhku terurai menjadi titik-titik cahaya dan kelopak bunga."),
            ("", "Angin yang sama mengangkat ujung syal putih Senja, membuat ia mendongak ke arah sinar matahari dengan mata berkaca-kaca namun tersenyum hangat."),
            ("Senja", "...Kamu dateng juga ya, Rak."),
        ),
    ),
    CGSlide(
        cg_id="cg_end_05_comic_dedication",
        rel_path="images/cg/cg_end_05_comic_dedication.png",
        title="Gambarmu Selalu Sampai",
        category="Ending",
        particles="petals",
        lines=(
            ("", "Di pangkuan Senja, halaman persembahan komik TRACK 99 Volume 1 terbuka di bawah sinar pagi:"),
            ("", "'Untuk Raka — gambarmu selalu sampai.'"),
            ("", "Sehelai kelopak bunga mendarat pelan di atas gambar kereta senja yang melaju di atas laut."),
        ),
    ),
    CGSlide(
        cg_id="cg_end_06_empty_train_horizon",
        rel_path="images/cg/cg_end_06_empty_train_horizon.png",
        title="Track 99 Menuju Horizon",
        category="Ending",
        particles="dust",
        lines=(
            ("", "Kereta Track 99 yang kini kosong melaju tenang di atas permukaan laut pagi menuju horizon."),
            ("", "Di salah satu bangkunya, pemutar kaset tua masih berputar pelan—menemani siapa saja yang kelak perlu belajar memaafkan dirinya sendiri."),
        ),
    ),
)

CG_BY_ID: dict[str, CGSlide] = {slide.cg_id: slide for slide in ALL_CG_SLIDES}


def _make_seq(
    seq_id: str,
    fade_color: tuple[int, int, int],
    cg_ids: tuple[str, ...],
    bgm_rel: str = "",
    shake_on_enter: bool = False,
) -> CGSequence:
    return CGSequence(
        seq_id=seq_id,
        fade_color=fade_color,
        slides=tuple(CG_BY_ID[cid] for cid in cg_ids),
        bgm_rel=bgm_rel,
        shake_on_enter=shake_on_enter,
    )


BLACK = (8, 8, 12)
WHITE = (248, 246, 240)

CG_SEQUENCES: dict[str, CGSequence] = {
    "cg_seq_prolog": _make_seq(
        "cg_seq_prolog",
        BLACK,
        ("cg_00a_wakeup_window", "cg_00b_ticket_hands", "cg_00c_walkman_bench"),
        bgm_rel="audio/bgm/bgm_00_sketch_rails.mp3",
    ),
    "cg_seq_fb1": _make_seq(
        "cg_seq_fb1",
        BLACK,
        ("cg_fb1a_grandpa_shoulders", "cg_fb1b_first_sketchbook"),
        bgm_rel="audio/bgm/bgm_05_flashback_musicbox.mp3",
        shake_on_enter=True,
    ),
    "cg_seq_bima": _make_seq(
        "cg_seq_bima",
        WHITE,
        ("cg_bima_a_paper_plane_window", "cg_bima_b_thank_you_fade"),
    ),
    "cg_seq_fb2": _make_seq(
        "cg_seq_fb2",
        BLACK,
        ("cg_fb2a_bus_stop_meet", "cg_fb2b_rooftop_drawing"),
        bgm_rel="audio/bgm/bgm_05_flashback_musicbox.mp3",
        shake_on_enter=True,
    ),
    "cg_seq_nadia": _make_seq(
        "cg_seq_nadia",
        WHITE,
        ("cg_nadia_a_paper_house_model", "cg_nadia_b_thank_you_fade"),
    ),
    "cg_seq_fb3": _make_seq(
        "cg_seq_fb3",
        BLACK,
        ("cg_fb3a_rain_torn_sketch", "cg_fb3b_umbrella_turnaway"),
        bgm_rel="audio/bgm/bgm_05_flashback_musicbox.mp3",
        shake_on_enter=True,
    ),
    "cg_seq_bayangan": _make_seq(
        "cg_seq_bayangan",
        WHITE,
        ("cg_bayangan_a_drawing_together", "cg_bayangan_b_hug_fade"),
    ),
    "cg_seq_fb4": _make_seq(
        "cg_seq_fb4",
        BLACK,
        ("cg_fb4a_office_last_text", "cg_fb4b_last_train_2359"),
        bgm_rel="audio/bgm/bgm_05_flashback_musicbox.mp3",
        shake_on_enter=True,
    ),
    "cg_seq_senja": _make_seq(
        "cg_seq_senja",
        WHITE,
        ("cg_senja_a_cockpit_sunrise", "cg_senja_b_thank_you_fade"),
    ),
    "cg_seq_ending": _make_seq(
        "cg_seq_ending",
        WHITE,
        (
            "cg_end_01_grandpa_conductor",
            "cg_end_02_translucent_hand_phone",
            "cg_end_03_senja_bench_comic",
            "cg_end_04_raka_dissolve_wind",
            "cg_end_05_comic_dedication",
            "cg_end_06_empty_train_horizon",
        ),
        bgm_rel="audio/bgm/bgm_06_ending_wind.mp3",
    ),
}


def load_unlocked_gallery() -> set[str]:
    """Load permanently unlocked CG IDs from userdata/saves/gallery_unlocked.json."""
    gpath = paths.SAVES_DIR / "gallery_unlocked.json"
    data = paths.read_json(gpath, default={"unlocked": []})
    items = data.get("unlocked", []) if isinstance(data, dict) else []
    return {str(i) for i in items}


def unlock_cg_in_gallery(cg_id: str) -> None:
    """Persist unlocked CG ID across all save slots."""
    gpath = paths.SAVES_DIR / "gallery_unlocked.json"
    unlocked = load_unlocked_gallery()
    if cg_id not in unlocked:
        unlocked.add(cg_id)
        paths.write_json(gpath, {"unlocked": sorted(unlocked)})


def unlock_all_cgs_in_gallery() -> None:
    """Unlock all 25 CGs (useful for Gallery preview mode)."""
    gpath = paths.SAVES_DIR / "gallery_unlocked.json"
    paths.write_json(gpath, {"unlocked": sorted(CG_BY_ID.keys())})


class WutheringWavesCGOverlay:
    """Full-screen static CG player with Ken Burns motion, smooth fades, and gradient subtitles."""

    def __init__(self, assets: Any, screen_size: tuple[int, int] = (1280, 720)) -> None:
        self.assets = assets
        self.w, self.h = screen_size
        self.active = False
        self.seq: CGSequence | None = None
        self.slide_idx = 0
        self.line_idx = 0
        self.type_chars = 0.0
        self._last_blip = 0

        self.phase = "idle"  # "fade_in", "playing", "crossfade", "fade_out"
        self.phase_timer = 0.0
        self.phase_dur = 0.75
        self.slide_elapsed = 0.0
        self.shake_timer = 0.0

        self._cur_surf: pygame.Surface | None = None
        self._prev_surf: pygame.Surface | None = None
        self._zoom_cache: dict[tuple[int, int, int], pygame.Surface] = {}
        self._skip_rect = pygame.Rect(20, 18, 118, 34)
        self._scrim_surf = self._build_bottom_scrim()
        self._particles = [
            [random.uniform(0, self.w), random.uniform(0, self.h), random.uniform(14, 38), random.randint(2, 5)]
            for _ in range(28)
        ]

    def _build_bottom_scrim(self) -> pygame.Surface:
        scrim_h = 210
        surf = pygame.Surface((self.w, scrim_h), pygame.SRCALPHA)
        for y in range(scrim_h):
            alpha = int(205 * ((y / float(scrim_h)) ** 1.35))
            pygame.draw.line(surf, (6, 8, 14, alpha), (0, y), (self.w, y))
        return surf

    def _load_slide_surface(self, slide: CGSlide) -> pygame.Surface:
        # Load at slightly oversized 1360x765 so Ken Burns 1.05x zoom stays razor sharp
        return self.assets.get_image(slide.rel_path, size=(1360, 765), fallback_style="sunset")

    def start_sequence(
        self,
        seq_id: str,
        save_data: dict[str, Any] | None = None,
        force: bool = False,
    ) -> bool:
        """Start a CG sequence if not yet seen (or if force=True for Gallery)."""
        if seq_id not in CG_SEQUENCES:
            return False
        if save_data is not None and not force:
            seen = list(save_data.get("seen_cg", []))
            if seq_id in seen:
                return False
            seen.append(seq_id)
            save_data["seen_cg"] = seen

        self.seq = CG_SEQUENCES[seq_id]
        self.slide_idx = 0
        self.line_idx = 0
        self.type_chars = 0.0
        self._last_blip = 0
        self.slide_elapsed = 0.0
        self.phase = "fade_in"
        self.phase_timer = 0.0
        self.phase_dur = 0.75
        self.shake_timer = 0.35 if self.seq.shake_on_enter else 0.0
        self.active = True

        first = self.seq.slides[0]
        self._zoom_cache.clear()
        self._cur_surf = self._load_slide_surface(first)
        self._prev_surf = None
        unlock_cg_in_gallery(first.cg_id)

        if first.bgm_override:
            self.assets.play_bgm(first.bgm_override, track_title=first.title)
        elif self.seq.bgm_rel:
            self.assets.play_bgm(self.seq.bgm_rel, track_title=first.title)
        if first.sfx_on_enter:
            self.assets.play_sfx(first.sfx_on_enter, volume=0.30)
        return True

    def start_single_cg(self, cg_id: str) -> bool:
        """Play a single CG slide from the Gallery."""
        if cg_id not in CG_BY_ID:
            return False
        slide = CG_BY_ID[cg_id]
        temp_seq = CGSequence(
            seq_id=f"gallery_{cg_id}",
            fade_color=BLACK,
            slides=(slide,),
        )
        self.seq = temp_seq
        self.slide_idx = 0
        self.line_idx = 0
        self.type_chars = 0.0
        self._last_blip = 0
        self.slide_elapsed = 0.0
        self.phase = "fade_in"
        self.phase_timer = 0.0
        self.phase_dur = 0.55
        self.shake_timer = 0.0
        self.active = True
        self._cur_surf = self._load_slide_surface(slide)
        self._prev_surf = None
        return True

    def _begin_next_slide_or_end(self) -> None:
        if self.seq is None:
            self.active = False
            return
        if self.slide_idx + 1 < len(self.seq.slides):
            self._prev_surf = self._cur_surf
            self.slide_idx += 1
            nxt = self.seq.slides[self.slide_idx]
            self._cur_surf = self._load_slide_surface(nxt)
            unlock_cg_in_gallery(nxt.cg_id)
            self.line_idx = 0
            self.type_chars = 0.0
            self._last_blip = 0
            self.slide_elapsed = 0.0
            self.phase = "crossfade"
            self.phase_timer = 0.0
            self.phase_dur = 0.85 if self.seq.fade_color == WHITE else 0.70
            if nxt.bgm_override:
                self.assets.play_bgm(nxt.bgm_override, track_title=nxt.title)
            if nxt.sfx_on_enter:
                self.assets.play_sfx(nxt.sfx_on_enter, volume=0.30)
        else:
            self.phase = "fade_out"
            self.phase_timer = 0.0
            self.phase_dur = 1.05 if self.seq.fade_color == WHITE else 0.75

    def skip(self) -> None:
        """Unlock remaining slides in sequence and fade out cleanly."""
        if self.seq is not None:
            for s in self.seq.slides:
                unlock_cg_in_gallery(s.cg_id)
        self.phase = "fade_out"
        self.phase_timer = 0.0
        self.phase_dur = 0.45

    def stop(self) -> None:
        """Immediately stop CG playback."""
        self.active = False
        self.seq = None

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if not self.active or self.seq is None:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._skip_rect.collidepoint(event.pos):
                self.assets.play_sfx("click", volume=0.22)
                self.skip()
                return None

        if self.phase in ("fade_in", "crossfade"):
            return None

        advance = event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN)
        if not advance and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            advance = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.skip()
            return None

        if advance and self.phase == "playing":
            slide = self.seq.slides[self.slide_idx]
            _, cur_txt = slide.lines[self.line_idx]
            if self.type_chars < len(cur_txt):
                self.type_chars = float(len(cur_txt))
                return None
            if self.line_idx + 1 < len(slide.lines):
                self.line_idx += 1
                self.type_chars = 0.0
                self._last_blip = 0
                return None
            self._begin_next_slide_or_end()
        return None

    def update(self, dt: float) -> str | None:
        """Advance CG player. Returns 'completed' when sequence finishes fading out."""
        if not self.active or self.seq is None:
            return None

        self.slide_elapsed += dt
        if self.shake_timer > 0.0:
            self.shake_timer = max(0.0, self.shake_timer - dt)

        slide = self.seq.slides[self.slide_idx]
        if slide.particles != "none":
            for p in self._particles:
                if slide.particles == "petals":
                    p[0] = (p[0] + p[2] * 1.4 * dt) % self.w
                    p[1] = (p[1] + 42.0 * dt) % self.h
                else:
                    p[0] = (p[0] - p[2] * 0.5 * dt) % self.w
                    p[1] = (p[1] - 24.0 * dt) % self.h

        if self.phase == "fade_in":
            self.phase_timer += dt
            if self.phase_timer >= self.phase_dur:
                self.phase = "playing"
            return None

        if self.phase == "crossfade":
            self.phase_timer += dt
            if self.phase_timer >= self.phase_dur:
                self.phase = "playing"
            return None

        if self.phase == "fade_out":
            self.phase_timer += dt
            if self.phase_timer >= self.phase_dur:
                self.active = False
                self.phase = "idle"
                return "completed"
            return None

        # Typing current subtitle line
        _, cur_txt = slide.lines[self.line_idx]
        if self.type_chars < len(cur_txt):
            self.type_chars = min(float(len(cur_txt)), self.type_chars + dt * 44.0)
            cur_int = int(self.type_chars)
            if cur_int - self._last_blip >= 4:
                self._last_blip = cur_int
                ch = cur_txt[max(0, cur_int - 1)]
                if ch.isalnum():
                    self.assets.play_sfx("text_blip", volume=0.06)
        return None

    def _blit_ken_burns(self, target: pygame.Surface, img: pygame.Surface, alpha: int = 255) -> None:
        zoom = 1.0 + min(0.05, self.slide_elapsed * 0.0065)
        cw = int(self.w * zoom)
        ch = int(self.h * zoom)
        cache_key = (id(img), cw, ch)
        scaled = self._zoom_cache.get(cache_key)
        if scaled is None:
            if len(self._zoom_cache) > 8:
                self._zoom_cache.clear()
            scaled = pygame.transform.smoothscale(img, (cw, ch))
            self._zoom_cache[cache_key] = scaled
        ox = int((self.w - cw) * 0.5 - math.sin(self.slide_elapsed * 0.25) * 8)
        oy = int((self.h - ch) * 0.5)
        if self.shake_timer > 0.0:
            ox += random.randint(-5, 5)
            oy += random.randint(-4, 4)
        scaled.set_alpha(alpha if alpha < 255 else None)
        target.blit(scaled, (ox, oy))

    def render(self, surface: pygame.Surface) -> None:
        if not self.active or self.seq is None or self._cur_surf is None:
            return

        slide = self.seq.slides[self.slide_idx]
        if self.phase == "crossfade" and self._prev_surf is not None:
            prog = min(1.0, self.phase_timer / self.phase_dur)
            self._blit_ken_burns(surface, self._prev_surf, 255)
            self._blit_ken_burns(surface, self._cur_surf, int(255 * prog))
        else:
            self._blit_ken_burns(surface, self._cur_surf, 255)

        # Floating atmosphere particles (gold motes / sakura petals)
        if slide.particles == "petals":
            for px, py, _, sz in self._particles:
                pygame.draw.ellipse(surface, (255, 222, 232), (int(px), int(py), sz + 4, sz + 1))
        elif slide.particles == "gold":
            for px, py, _, sz in self._particles:
                pygame.draw.circle(surface, (255, 234, 165), (int(px), int(py)), max(2, sz // 2))
        elif slide.particles == "dust":
            for px, py, _, sz in self._particles:
                pygame.draw.circle(surface, (220, 225, 235), (int(px), int(py)), max(1, sz // 2))

        # Bottom Wuthering Waves gradient scrim + centered speaker & white subtitle text
        surface.blit(self._scrim_surf, (0, self.h - self._scrim_surf.get_height()))

        speaker, full_txt = slide.lines[self.line_idx]
        shown = full_txt[: int(self.type_chars)]
        is_thought = speaker == ""

        if speaker:
            f_spk = get_ui_font(18, bold=True)
            s_surf = f_spk.render(speaker, True, (248, 198, 102))
            s_shd = f_spk.render(speaker, True, (10, 10, 14))
            sx = self.w // 2 - s_surf.get_width() // 2
            surface.blit(s_shd, (sx + 2, 558))
            surface.blit(s_surf, (sx, 556))

        f_body = get_ui_font(20, serif=is_thought)
        words = shown.split(" ")
        wrapped: list[str] = []
        cur = ""
        for word in words:
            test = f"{cur} {word}".strip()
            if f_body.size(test)[0] <= 900:
                cur = test
            else:
                wrapped.append(cur)
                cur = word
        if cur:
            wrapped.append(cur)

        text_col = (228, 234, 246) if is_thought else (248, 249, 252)
        base_y = 586 if speaker else 576
        for idx, line in enumerate(wrapped[:3]):
            l_surf = f_body.render(line, True, text_col)
            l_shd = f_body.render(line, True, (8, 10, 14))
            lx = self.w // 2 - l_surf.get_width() // 2
            surface.blit(l_shd, (lx + 2, base_y + idx * 30 + 2))
            surface.blit(l_surf, (lx, base_y + idx * 30))

        # Pulsing diamond prompt when line finished typing
        if self.phase == "playing" and self.type_chars >= len(full_txt):
            pulse_y = 688 + int(math.sin(self.slide_elapsed * 5.0) * 3)
            cx = self.w // 2
            pygame.draw.polygon(
                surface,
                (248, 198, 102),
                [(cx, pulse_y - 6), (cx + 7, pulse_y), (cx, pulse_y + 6), (cx - 7, pulse_y)],
            )

        # Clean top-left SKIP button with crisp vector fast-forward triangles (no missing-glyph box)
        skip_pill = pygame.Surface((self._skip_rect.width, self._skip_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(skip_pill, (12, 14, 22, 165), (0, 0, self._skip_rect.width, self._skip_rect.height), border_radius=16)
        pygame.draw.rect(skip_pill, (235, 240, 248, 160), (0, 0, self._skip_rect.width, self._skip_rect.height), 1, border_radius=16)
        surface.blit(skip_pill, self._skip_rect.topleft)
        f_skip = get_ui_font(13, bold=True)
        sk_txt = f_skip.render("LEWATI", True, (242, 245, 250))
        surface.blit(
            sk_txt,
            (self._skip_rect.left + 18, self._skip_rect.centery - sk_txt.get_height() // 2),
        )
        tri_x = self._skip_rect.left + 78
        tri_y = self._skip_rect.centery
        for offset in (0, 8):
            pygame.draw.polygon(
                surface,
                (248, 198, 102),
                [(tri_x + offset, tri_y - 5), (tri_x + offset + 6, tri_y), (tri_x + offset, tri_y + 5)],
            )

        # Smooth Black / White Fade Curtains
        if self.phase == "fade_in":
            alpha = int(255 * max(0.0, 1.0 - self.phase_timer / self.phase_dur))
            curtain = pygame.Surface((self.w, self.h))
            curtain.fill(self.seq.fade_color)
            curtain.set_alpha(alpha)
            surface.blit(curtain, (0, 0))
        elif self.phase == "fade_out":
            alpha = int(255 * min(1.0, self.phase_timer / self.phase_dur))
            curtain = pygame.Surface((self.w, self.h))
            curtain.fill(self.seq.fade_color)
            curtain.set_alpha(alpha)
            surface.blit(curtain, (0, 0))
