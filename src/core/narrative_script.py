"""Final narrative scripts aligned with STORY_BIBLE.md & NOVEL_TRACK99.md.

Supports optional player/writer overrides from userdata/custom_dialogues.json.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.core import paths


@dataclass(frozen=True)
class PropScript:
    """Interactive carriage object or environmental hotspot with reflection & optional unlock."""

    prop_key: str
    title: str
    x: float
    y: float
    lines: tuple[tuple[str, str], ...]
    sprite_key: str | None = None
    unlocks_cassette: int = 0


@dataclass(frozen=True)
class ChapterScript:
    """One conversational beat in a multi-chapter passenger story."""

    title: str
    lines: tuple[tuple[str, str], ...]
    choice_prompt: str = ""
    choices: tuple[str, ...] = ()
    choice_replies: tuple[tuple[tuple[str, str], ...], ...] = ()


@dataclass(frozen=True)
class CarriageNarrative:
    """Complete multi-chapter story data for one carriage."""

    scene_id: str
    carriage_label: str
    bg_image_rel: str
    default_cassette: int
    passenger_name: str
    portrait_slot: int
    sprite_style: str
    required_cassette: int
    target_freq: float
    target_amp: float
    cassette_hint: str
    minigame_type: str  # "none", "paper_plane", "kintsugi"
    props: tuple[PropScript, ...]
    chapters: tuple[ChapterScript, ...]
    rain_whisper: str
    mind_dive_captions: tuple[str, ...]
    resonance_title: str
    resonance_subtitle: str
    epilogue_lines: tuple[tuple[str, str], ...]
    is_finale: bool = False
    finale_station_lines: tuple[tuple[str, str], ...] = ()
    entry_cg_seq: str = ""
    entry_reaction_lines: tuple[tuple[str, str], ...] = ()
    harmony_cg_seq: str = ""
    unlocks_cassette_on_harmony: int = 0
    required_props_for_ch2: int = 2


# ---------------------------------------------------------------------------
# GERBONG 5 — KEHENINGAN (PROLOG & KONDEKTUR)
# ---------------------------------------------------------------------------

GERBONG_5_PROPS: dict[str, PropScript] = {
    "walkman": PropScript(
        prop_key="walkman",
        title="WALKMAN PERAK KAKEK HARJO",
        x=295.0,
        y=455.0,
        sprite_key="walkman",
        lines=(
            ("raka:calm", "Walkman perak tua peninggalan Kakek Harjo masih tergeletak di bangku... Lampu merahnya berkedip pelan."),
            ("raka:sad", "Kaset A di dalamnya bertuliskan tangan Senja dengan spidol luntur: 'buat pulang kantor yang capek'."),
            ("raka:smile", "Entah kenapa, baru memegangnya saja sudah membuat suara gemuruh rel terasa sedikit lebih ramah."),
        ),
    ),
    "ticket_99": PropScript(
        prop_key="ticket_99",
        title="TIKET KERTAS — TRACK 99 (23:59)",
        x=445.0,
        y=466.0,
        sprite_key="ticket_99",
        lines=(
            ("raka:surprised", "Karcis ini tercetak pukul 23:59. Kolom tujuannya pudar seperti tersiram air hujan, cuma terbaca samar 'STASIUN...'"),
            ("raka:calm", "Belum ada lubang kondektur di pinggirnya. Padahal seingatku tadi aku naik kereta komuter terakhir sepulang lembur."),
        ),
    ),
    "tea": PropScript(
        prop_key="tea",
        title="TEH MELATI HANGAT",
        x=555.0,
        y=455.0,
        sprite_key="tea",
        lines=(
            ("raka:calm", "Secangkir teh melati yang uapnya masih mengepul tipis. Manisnya pas, persis seduhan Ibu waktu aku masih kuliah."),
            ("raka:sad", "Terakhir kali Ibu nyodorin teh hangat sambil bilang 'istirahat dulu, Le', aku malah sibuk memandangi laptop sambil mengiyakan."),
        ),
    ),
    "pocket_watch": PropScript(
        prop_key="pocket_watch",
        title="JAM SAKU RETAK (23:59)",
        x=655.0,
        y=466.0,
        sprite_key="pocket_watch",
        lines=(
            ("raka:surprised", "Jarum jam saku kuningan ini berhenti di angka 23:59, persis seperti jam di tiketku tadi."),
            ("raka:calm", "Kacanya ada retak rambut tipis. Entah baterai mati atau memang waktu di luar jendela sengaja berjalan lambat malam ini."),
        ),
    ),
    "phone_cracked": PropScript(
        prop_key="phone_cracked",
        title="PONSEL RETAK (99+ NOTIFIKASI)",
        x=750.0,
        y=466.0,
        sprite_key="phone_cracked",
        lines=(
            ("raka:sad", "Layarnya retak di sudut atas. Tertulis 'Tidak Ada Sinyal', tapi lambang pesan masuknya penuh di angka 99+."),
            ("raka:calm", "Jempolku membeku di atas layar. Aku nggak berani membukanya sekarang... takut membaca marah atau kecewa dari orang-orang yang kutelantarkan."),
        ),
    ),
    "cassette_d_sealed": PropScript(
        prop_key="cassette_d_sealed",
        title="KASET D TERSEGEL ('FAJAR — S')",
        x=835.0,
        y=462.0,
        sprite_key="cassette_d_sealed",
        lines=(
            ("raka:calm", "Kaset keempat terikat rapi dengan selotip kertas. Tulisan tangan Senja tertera di label mint-nya:"),
            ("raka:sad", "'FAJAR — dengerin pas kamu udah siap. — S'. Sudah setahun penuh segelnya tidak pernah kusentuh."),
        ),
    ),
    "hotspot:route_board": PropScript(
        prop_key="hotspot:route_board",
        title="PAPAN RUTE KERETA SENJA",
        x=545.0,
        y=225.0,
        sprite_key=None,
        lines=(
            ("raka:calm", "Pelat besi di atas jendela menuliskan urutan perhentian yang aneh:"),
            ("raka:surprised", "'STASIUN RUMAH  →  KAMPUS  →  HUJAN  →  FAJAR'. Kenapa rasanya seperti membaca peta hidupku sendiri...?"),
        ),
    ),
}

GERBONG_5_CONDUCTOR_NEED_EXPLORE: tuple[tuple[str, str], ...] = (
    ("kondektur", "Selamat malam, Mas. Mau periksa tiketnya dulu? Tapi sepertinya masih ada barang-barang Mas di bangku yang belum Mas lihat lagi."),
    ("raka:calm", "Oh, iya Pak... Sebentar saya bereskan dan periksa dulu barang-barang saya di kursi kiri."),
)

GERBONG_5_CONDUCTOR_OPEN: tuple[tuple[str, str], ...] = (
    ("kondektur", "Permisi, Mas Raka. Boleh Bapak lihat tiket 23:59-nya sebentar?"),
    ("raka:calm", "Eh—Bapak tahu nama saya? Ini tiketnya, Pak. Ngomong-ngomong, kereta ini nanti berhenti di Stasiun Kotabaru?"),
    ("kondektur", "Saya hanya mengantar sampai stasiun akhir, Mas. Tapi lihat ini... tiket Mas belum bisa dilubangi sekarang."),
    ("raka:surprised", "Belum bisa? Memangnya kenapa, Pak? Saya bayar penuh kok tadi—atau salah gerbong?"),
    ("kondektur", "Bukan salah bayar. Pelubang tiket saya hanya bisa menembus kertas kalau penumpangnya sendiri sudah siap turun."),
    ("raka:sad", "...Siap turun? Bapak ngomongin apa sih. Aku kan cuma ketiduran sepulang kerja."),
    ("kondektur", "Silakan jalan pelan-pelan ke gerbong depan ya, Mas. Kalau ketemu penumpang lain, dengarkan saja cerita mereka sebentar."),
    ("raka:calm", "Baik, Pak... Pintu ke Gerbong 4 sudah terbuka sekarang."),
)


# ---------------------------------------------------------------------------
# GERBONG 4 -> GERBONG 1 (NARRATIVE MASTER SCRIPTS)
# ---------------------------------------------------------------------------

RAW_SCRIPTS: dict[str, CarriageNarrative] = {
    "gerbong_4_childhood": CarriageNarrative(
        scene_id="gerbong_4_childhood",
        carriage_label="GERBONG 4 — RAK BUKU & LANGIT SORE",
        bg_image_rel="images/backgrounds/bg_gerbong4_childhood.png",
        default_cassette=1,
        passenger_name="Bima Sakti Pratama",
        portrait_slot=0,
        sprite_style="child",
        required_cassette=1,
        target_freq=2.3,
        target_amp=46.0,
        cassette_hint="Gunakan Kaset [1] SENJA lalu sejajarkan frekuensi tenang untuk Bima.",
        minigame_type="paper_plane",
        entry_cg_seq="cg_seq_fb1",
        entry_reaction_lines=(
            ("raka:surprised", "...Hah?! Kepalaku berdenyut kencang sekali. Tadi itu... Kakek Harjo di peron zaman aku masih SD?"),
            ("raka:sad", "Aku bahkan nggak ingat kapan terakhir kali memikirkan sore itu. Kenapa ingatannya tiba-tiba muncul di gerbong ini...?"),
        ),
        harmony_cg_seq="cg_seq_bima",
        unlocks_cassette_on_harmony=3,
        required_props_for_ch2=2,
        props=(
            PropScript(
                prop_key="cassette_b_hujan",
                title="KASET B — 'HUJAN' DI RAK BUKU",
                x=365.0,
                y=424.0,
                sprite_key="cassette_b",
                unlocks_cassette=2,
                lines=(
                    ("raka:surprised", "Terselip di antara buku cerita anak—ada satu kaset biru bening yang hilang dari tas Walkman-ku!"),
                    ("raka:calm", "Tulisan tangan Senja berbunyi: 'HUJAN — kalau pengen nangis tapi gengsi'. [Kaset [2] HUJAN terbuka!]"),
                ),
            ),
            PropScript(
                prop_key="comic_book",
                title="KOMIK 'KERETA KE LAUT' KARYA MAS DIMAS",
                x=485.0,
                y=458.0,
                sprite_key="comic_book",
                lines=(
                    ("raka:calm", "Buku tulis bergaris yang penuh coretan pensil tentang kereta biru yang melaju di atas ombak. Gambarnya rapi banget..."),
                    ("raka:sad", "Sampul belakangnya ada catatan kecil: 'Buat Bima, tunggu Mas Dimas selesai kerja ya'. Rasanya aku kenal rasa rindu menggambar seperti ini."),
                ),
            ),
            PropScript(
                prop_key="hospital_paper_plane",
                title="GELANG PASIEN & PESAWAT KERTAS",
                x=615.0,
                y=464.0,
                sprite_key="hospital_paper_plane",
                lines=(
                    ("raka:surprised", "Gelang plastik putih bertuliskan 'RUANG ANGGREK 3 — BIMA S.' tergeletak di sebelah lipatan pesawat dari kertas komik."),
                    ("raka:sad", "Bima... dirawat di rumah sakit? Tapi kenapa dia naik kereta sendirian memakai jas hujan kebesaran begini?"),
                ),
            ),
            PropScript(
                prop_key="lunchbox_ibu",
                title="BEKAL ROTI & KAIN BATIK",
                x=685.0,
                y=454.0,
                sprite_key="lunchbox_ibu",
                lines=(
                    ("raka:calm", "Kotak bekal dibungkus kain batik yang disiapkan sebelum berangkat. Sentuhan kecil orang rumah sebelum pergi jauh."),
                ),
            ),
            PropScript(
                prop_key="hotspot:chalkboard_99",
                title="PAPAN KAPUR HITUNGAN TIANG LISTRIK",
                x=545.0,
                y=225.0,
                sprite_key=None,
                lines=(
                    ("raka:calm", "Garis-garis kapur putih di dinding mencatat angka: '97... 98... 99...' lalu berhenti di situ."),
                    ("raka:sad", "Kata Bima, kalau sampai seratus, lautnya bakal kelihatan."),
                ),
            ),
        ),
        chapters=(
            ChapterScript(
                title="Babak 1: Menghitung Tiang Listrik",
                lines=(
                    ("npc", "Sembilan puluh tujuh... sembilan puluh delapan... sembilan puluh sembilan. Eh—yah, ketutup awan lagi."),
                    ("raka:calm", "Ngitungin tiang listrik di luar jendela, Dik? Kok tahu-tahu berhenti di sembilan puluh sembilan?"),
                    ("npc", "Soalnya kata Mas Dimas, kalau Bima sabar ngitung sampai seratus, nanti lautnya langsung kelihatan di balik kaca!"),
                    ("raka:smile", "Wah, janji kakak yang keren banget. Ngomong-ngomong, jas hujan kuningmu kebesaran banget tuh, padahal di luar lagi senja cerah."),
                    ("npc", "Hehe, ini dibeliin Mas Dimas pas musim hujan kemarin. Katanya, 'Biar nanti pas kita ke pantai nggak kehujanan'."),
                    ("npc", "Eh, Mas juga naik kereta ini, berarti Mas juga..."),
                    ("raka:surprised", "(Suara sambungan rel berderak keras tepat memotong kalimatnya.) Hah? Berarti aku kenapa, Bim?"),
                    ("npc", "Eh—enggak, Mas! Itu... maksud Bima, Mas juga suka dengerin lagu di Walkman sambil ngelamun kayak Mas Dimas ya? (Coba lihat-lihat dulu buku & benda di meja gerbong ini ya, Mas.)"),
                ),
            ),
            ChapterScript(
                title="Babak 2: Takut Kertasnya Robek",
                lines=(
                    ("raka:calm", "Bim... aku barusan lihat buku komik 'Kereta ke Laut' di bangku sana. Gambar kakakmu bagus sekali. Sekarang Mas Dimas kerja di mana?"),
                    ("npc", "Mas Dimas berhenti ikut les gambar tahun lalu, Mas. Katanya cat warna mahal, jadi dia kerja bantu di bengkel sama jaga toko."),
                    ("npc", "Padahal Bima tahu, dia berhenti gara-gara uang tabungannya kepakai buat bayarin kamar Anggrek 3 terus..."),
                    ("raka:sad", "...Bim. Jangan ngomong gitu."),
                    ("npc", "Bima cuma pengen cepet sembuh biar nggak ngerepotin Ibu sama Mas Dimas terus. Kemarin waktu Ibu jual motornya, Bima cuma pura-pura tidur."),
                    ("raka:sad", "(Tenggorokanku tercekat. Aku teringat buku tabungan lusuh milik Ibu saat aku memutuskan berhenti menggambar karena malu gagal...)"),
                    ("npc", "Mas... kalau kertas ini Bima terbangkan keluar jendela, nanti kalau jatuh kena angin dan robek gimana? Mas Dimas capek gambarnya lho."),
                    ("npc", "Eh, Mas Raka juga lagi nyimpen sesuatu yang nggak berani dikeluarin ya? Tangannya dari tadi ngegosok jari terus kayak orang mau megang pensil."),
                ),
                choice_prompt="Bima menatap pesawat kertas terakhir di tangannya. Bagaimana Raka menjawab?",
                choices=(
                    "\"Orang yang sayang sama kamu nggak pernah ngitung kamu sebagai beban, Bim.\"",
                    "\"Pesawat kertas dibikin justru buat terbang, bukan disimpen di saku takut robek.\"",
                ),
                choice_replies=(
                    (
                        ("raka:calm", "Orang yang benar-benar sayang sama kita nggak pernah menaruh kalkulator di rasa capeknya, Bim. Mas Dimas pengen kamu bahagia, itu aja."),
                        ("npc", "Beneran ya, Mas...? Jadi Bima nggak merusak mimpi Mas Dimas?"),
                    ),
                    (
                        ("raka:smile", "Kertas itu baru beneran hidup kalau kita berani ngebiarin dia kena angin. Sama kayak gambar kakakmu—dan mungkin gambarku juga."),
                        ("npc", "Hehe... Mas Raka ngomongnya kayak kakak beneran!"),
                    ),
                ),
            ),
            ChapterScript(
                title="Babak 3: Pesawat Kertas ke Laut",
                lines=(
                    ("npc", "Ayo, Mas! Bantu Bima lipat sayapnya biar lurus, terus kita samakan lagu hangat Kaset [1] SENJA buat nganter pesawat ini ke tiang ke-100!"),
                    ("raka:smile", "Siap. Kita terbangkan sama-sama."),
                ),
            ),
        ),
        rain_whisper="[Bisikan Kaset HUJAN]: 'Kalau Bima pulang duluan... Mas Dimas jangan pernah berhenti gambar lagi, ya.'",
        mind_dive_captions=(
            "Jendela gerbong terbuka lebar membiarkan angin laut senja masuk ke dalam ruangan...",
            "Pesawat kertas meluncur ke angkasa bersama pesan untuk Mas Dimas.",
        ),
        resonance_title="Bagian Bima Selesai!",
        resonance_subtitle="Tiang listrik ke-100 terlewati. Kaset [3] DETAK ditinggalkan di atas bangku.",
        epilogue_lines=(
            ("raka:calm", "Kursi Bima kini kosong... hanya tertinggal selembar potongan tiket berlubang bintang dan sebuah kaset bertulisan tangan Senja."),
            ("raka:smile", "Kaset [3] DETAK: 'buat hari-hari yang butuh nekat dikit'. Dia sudah turun duluan ke laut yang cerah, ya."),
        ),
    ),
    "gerbong_3_burnout": CarriageNarrative(
        scene_id="gerbong_3_burnout",
        carriage_label="GERBONG 3 — MEJA KERJA & JAM DINDING 01:14",
        bg_image_rel="images/backgrounds/bg_gerbong3_work.png",
        default_cassette=3,
        passenger_name="Nadia Larasati",
        portrait_slot=1,
        sprite_style="student",
        required_cassette=3,
        target_freq=3.4,
        target_amp=64.0,
        cassette_hint="Putar Kaset [3] DETAK — Keberanian (dari Bima) lalu sejajarkan gelombang Nadia.",
        minigame_type="none",
        entry_cg_seq="cg_seq_fb2",
        entry_reaction_lines=(
            ("raka:surprised", "Ugh... Bayangan atap gedung kampus sore itu muncul lagi—waktu aku dan Senja pertama kali merancang TRACK 99."),
            ("raka:sad", "Dulu, bahkan sebelum ditolak penerbit, aku percaya banget gambar-gambar kami bisa bikin orang merasa tidak sendirian. Kapan tepatnya aku berubah?"),
        ),
        harmony_cg_seq="cg_seq_nadia",
        required_props_for_ch2=2,
        props=(
            PropScript(
                prop_key="phone_nadia",
                title="PONSEL NADIA (14 MISSED CALLS: IBU)",
                x=460.0,
                y=466.0,
                sprite_key="phone_cracked",
                lines=(
                    ("raka:sad", "Log panggilannya membeku di jam 01:14 dini hari: 14 panggilan tak terjawab dari kontak bernama 'Ibu'."),
                    ("raka:sad", "Pesan terakhir yang tertulis di atasnya singkat banget: 'Nad, makan malam ulang tahun Ibu sudah dingin nih. Pulang hati-hati ya.'"),
                ),
            ),
            PropScript(
                prop_key="lunchbox_nadia",
                title="KOTAK BEKAL KAIN DARI IBU",
                x=590.0,
                y=454.0,
                sprite_key="lunchbox_ibu",
                lines=(
                    ("raka:calm", "Kotak bekal dibungkus kain rapi di sudut meja lipat. Di tutupnya masih tertempel sticky note: 'Jangan telat makan, Sayang'."),
                    ("raka:sad", "Segel kotaknya bahkan belum sempat dibuka sejak malam itu."),
                ),
            ),
            PropScript(
                prop_key="house_model",
                title="SKETSA 'RUMAH IBU DI TEPI LAUT'",
                x=680.0,
                y=450.0,
                sprite_key="house_model",
                lines=(
                    ("raka:calm", "Di balik tumpukan gambar revisi proyek komersial, Nadia menyelipkan maket rumah mungil bertuliskan 'Rumah Pensiun Ibu — Menghadap Laut'."),
                    ("raka:sad", "Mirip banget sama caraku dulu menyembunyikan halaman komikku di balik file banner iklan kantor."),
                ),
            ),
            PropScript(
                prop_key="helmet_cracked",
                title="HELM PUTIH RETAK",
                x=985.0,
                y=462.0,
                sprite_key="helmet_cracked",
                lines=(
                    ("raka:surprised", "Helm retro putih diletakkan rapi di bangku ujung, dengan retak halus panjang di pelipis kirinya."),
                    ("raka:sad", "Aku... memilih tidak menanyakan bagaimana helm itu bisa retak begitu."),
                ),
            ),
            PropScript(
                prop_key="hotspot:wall_clock_0114",
                title="JAM DINDING GERBONG (01:14)",
                x=645.0,
                y=212.0,
                sprite_key=None,
                lines=(
                    ("raka:surprised", "Jam bulat di dinding ini pun mati... tapi berhentinya di angka 01:14, bukan 23:59 seperti jam sakuku."),
                ),
            ),
        ),
        chapters=(
            ChapterScript(
                title="Babak 1: Kopi yang Telanjur Dingin",
                lines=(
                    ("npc", "Aduh, maaf Mas... Meja depannya jadi sempit sama gulungan gambar proyek saya. Mas mau lewat atau mau duduk?"),
                    ("raka:calm", "Santai aja, Mbak. Aku cuma jalan lihat-lihat. Ngomong-ngomong, gambar denahnya rapi banget—arsitek ya?"),
                    ("npc", "Arsitek junior merangkap tukang revisi tengah malam sih tepatnya, haha. Ini desain kesekian buat klien yang pengen 'terlihat mewah tapi murah'."),
                    ("npc", "Sebentar ya... mata Mas kelihatan kayak orang yang sudah lupa rasanya tidur siang tanpa alarm. Sama-sama anak agensi lembur juga ya?"),
                    ("raka:smile", "Kelihatan jelas banget ya? Biasa, desainer 'nanti logo digedein sedikit'."),
                    ("npc", "(Nadia tersenyum tipis lalu menatap jam dinding di atas kepalanya. Kamu bisa memeriksa meja kerjanya & bekal sebelum ngobrol lagi.)"),
                ),
            ),
            ChapterScript(
                title="Babak 2: Di Balik 'Nanti Aja'",
                lines=(
                    ("raka:sad", "Mbak Nadia... aku nggak sengaja lihat kotak bekal sama catatan 14 panggilan tak terjawab di meja sana. Maaf kalau lancang."),
                    ("npc", "Nggak apa-apa. Malah anehnya lebih lega ada yang tahu sekarang... Malam itu ulang tahun Ibu. Beliau telepon berkali-kali ngajak makan malam."),
                    ("npc", "Tapi deadline proyek lagi dikejar revisi jam satu malam. Di telepon kesekian, aku keburu meledak: 'Bu, aku lagi kerja! Jangan telepon terus!'"),
                    ("npc", "Aku nutup teleponnya, terus bilang dalam hati 'nanti pas udah nyampe rumah tinggal minta maaf'. Ternyata kata 'nanti' nggak selalu punya besok, Mas."),
                    ("raka:sad", "...Aku juga melakukan hal yang sama."),
                    ("npc", "Maksud Mas?"),
                    ("raka:sad", "Satu tahun terakhir ini... setiap sahabatku—namanya Senja—mengirim chat ngajak ketemu atau nanyain kabar, aku selalu bilang 'nanti ya kalau kerjaanku beres'. Sampai akhirnya pesan terakhirnya pun nggak kukirim balasan."),
                    ("npc", "Jadi Mas ngerti banget rasa dinginnya layar ponsel yang nggak berani kita buka lagi..."),
                ),
                choice_prompt="Nadia meremas ujung cardigan-nya sambil menatap maket rumah kecil yang belum selesai dirakit.",
                choices=(
                    "\"Kata maaf yang telat diucapkan bukan berarti nggak nyampe. Yuk selesaikan maket Ibu.\"",
                    "\"Ibu pasti tahu kamu kerja keras juga karena pengen bikin beliau bangga, Nad.\"",
                ),
                choice_replies=(
                    (
                        ("raka:calm", "Kita mungkin nggak bisa mengulang jam 01:14 itu. Tapi kamu masih bisa ngucapin kalimat yang tertinggal di sini dengan jujur."),
                        ("npc", "Terima kasih, Raka... Kamu bener. Aku nggak mau bawa penyesalan ini terus."),
                    ),
                    (
                        ("raka:smile", "Seorang ibu nggak pernah marah lama-lama cuma karena anaknya capek, Nad. Beliau justru pengen kamu berhenti menyiksa diri sendiri."),
                        ("npc", "(Nadia menyeka sudut kacamatanya pelan dan mengangguk kecil.)"),
                    ),
                ),
            ),
            ChapterScript(
                title="Babak 3: Keberanian Mengucap Maaf",
                lines=(
                    ("npc", "Mas bawa kaset dari anak kecil tadi? Boleh kita putar Kaset [3] DETAK dan samakan frekuensinya? Aku perlu keberanian buat ngomong ke Ibu."),
                    ("raka:calm", "Tentu. Mari kita selesaikan maket rumah tepi laut itu sama-sama."),
                ),
            ),
        ),
        rain_whisper="[Bisikan Kaset HUJAN]: 'Maaf ya, Bu... rumah tepi lautnya pasti jadi, kok.'",
        mind_dive_captions=(
            "Maket kayu kecil 'Rumah Ibu di Tepi Laut' selesai disusun di atas meja lipat...",
            "Melalui rekaman kaset, Nadia akhirnya berbisik lembut: 'Selamat ulang tahun, Bu.'",
        ),
        resonance_title="Bagian Nadia Selesai!",
        resonance_subtitle="Pesan suara untuk Ibu terekam dengan tenang bersama udara fajar.",
        epilogue_lines=(
            ("raka:calm", "Nadia melangkah masuk ke dalam cahaya biru yang hangat. Di atas meja tertinggal maket Rumah Ibu dan potongan tiket berlubang bintang."),
            ("raka:sad", "'Kamu juga... jangan bilang nanti lagi, ya.' Kalimatnya masih terngiang keras di telingaku."),
        ),
    ),
    "gerbong_2_crossroads": CarriageNarrative(
        scene_id="gerbong_2_crossroads",
        carriage_label="GERBONG 2 — CERMIN HUJAN & RETAS TINTA",
        bg_image_rel="images/backgrounds/bg_gerbong2_rain_crossroads.png",
        default_cassette=2,
        passenger_name="Bayangan Raka",
        portrait_slot=-1,
        sprite_style="shadow",
        required_cassette=2,
        target_freq=1.9,
        target_amp=34.0,
        cassette_hint="Putar Kaset [2] HUJAN (dari rak buku Gerbong 4) untuk meredam badai di dalam cermin.",
        minigame_type="kintsugi",
        entry_cg_seq="cg_seq_fb3",
        entry_reaction_lines=(
            ("raka:surprised", "Nggak! Jangan munculin ingatan malam hujan itu—malam waktu aku merobek buku sketsaku sendiri dan membentak Senja..."),
            ("raka:sad", "Aku masih ingat matanya membesar di balik payung transparan waktu kubentak: 'Mimpi kita ketinggian, Ja!'"),
        ),
        harmony_cg_seq="cg_seq_bayangan",
        unlocks_cassette_on_harmony=4,
        required_props_for_ch2=2,
        props=(
            PropScript(
                prop_key="manuscript_draft",
                title="EMPAT SOBEKAN SKETSA KINTSUGI",
                x=465.0,
                y=456.0,
                sprite_key="manuscript_folder",
                lines=(
                    ("raka:sad", "Kertas gambar yang dulu kusobek berkeping-keping di pinggir jalan kini basah oleh hujan dan berserakan di kursi."),
                    ("raka:calm", "Anehnya, tiap garis pensilnya masih terlihat utuh... menunggu disambung kembali."),
                ),
            ),
            PropScript(
                prop_key="umbrella_rejection",
                title="PAYUNG SENJA & SURAT PENOLAKAN PENERBIT",
                x=600.0,
                y=462.0,
                sprite_key="umbrella_rejection",
                lines=(
                    ("raka:sad", "Tiga amplop balasan penerbit: 'Konsep cerita terlalu lambat, visual kurang komersial untuk pasar saat ini.'"),
                    ("raka:sad", "Di sampingnya tergeletak payung transparan yang Senja pinjamkan waktu aku berlari pergi seperti orang bodoh."),
                ),
            ),
            PropScript(
                prop_key="poster_track99",
                title="DRAF AWAL 'TRACK 99'",
                x=680.0,
                y=458.0,
                sprite_key="comic_book",
                lines=(
                    ("raka:smile", "Sketsa cover komik zaman kuliah—kereta senja berlatar laut oranye. Tulisan judulnya masih kami warnai pakai krayon sama spidol murah."),
                ),
            ),
            PropScript(
                prop_key="hotspot:rain_mirror",
                title="KACA JENDELA YANG BERBAYANG",
                x=555.0,
                y=250.0,
                sprite_key=None,
                lines=(
                    ("raka:surprised", "Pantulanku di kaca jendela tadi... menatap lurus dengan mata kuning redup, sama sekali tidak menirukan gerakan tanganku!"),
                ),
            ),
        ),
        chapters=(
            ChapterScript(
                title="Babak 1: Orang Asing Bernama Diriku",
                lines=(
                    ("npc", "Lihat kaca di sebelahmu, Raka. Bagus ya gambarnya? Oh, lupa—kau kan sudah membunuh bakatmu sendiri setahun lalu."),
                    ("raka:surprised", "Siapa di situ?! Suara itu persis suaraku sendiri..."),
                    ("npc", "Aku bagian dirimu yang tidak pernah bisa dibungkam oleh jadwal lembur dan teh melati. Yang paling tahu kalau kau pengecut."),
                    ("npc", "Berapa kali kau menolak telepon Senja cuma karena gengsi mengakui kalau gambarmu dikatain sampah di internet?"),
                    ("raka:sad", "Diam...! Aku cuma mencoba realistis! Ibu butuh uang hidup, bukan impian komik murahan!"),
                    ("npc", "Alasan murahan. Dengarkan dirimu baik-baik: kamu sudah lama berhenti hidup, Raka. Sejak jauh sebelum kereta ini jalan."),
                    ("raka:sad", "(Periksa dulu robekan kertas dan payung Senja di bangku gerbong ini sebelum menghadapi bayangan diriku sendiri...)"),
                ),
            ),
            ChapterScript(
                title="Babak 2: Retakan yang Tidak Harus Disembunyikan",
                lines=(
                    ("raka:sad", "Kau tahu? Memang salahku semua. Aku berhenti gambar, aku mengecewakan Senja, dan aku nggak pernah sempat bilang terima kasih ke Ibu."),
                    ("npc", "Akhirnya ngaku juga. Terus sekarang maumu apa? Mau nyobek sisa kertas di kursimu lagi?"),
                    ("raka:calm", "Enggak. Di budaya Kintsugi, cangkir yang retak nggak dibuang. Garis retaknya disambung pakai emas biar kelihatan kalau ia pernah berjuang."),
                    ("raka:smile", "Mungkin gambaranku nggak sempurna. Mungkin aku pernah lari ketakutan. Tapi bukan berarti anak kecil yang dulu suka kereta itu harus kuhapus."),
                ),
                choice_prompt="Bayangan di depan kaca mulai bergetar hebat saat Raka tidak lagi bersembunyi.",
                choices=(
                    "\"Kemarilah. Bagian diriku yang gagal juga berhak aku maafin.\"",
                    "\"Ayo kita sambung lagi halaman TRACK 99 yang sempat kubuang.\"",
                ),
                choice_replies=(
                    (
                        ("raka:calm", "Aku berhenti menyalahkanmu terus-terusan. Sekarang giliranku memeluk rasa sakitku sendiri."),
                        ("npc", "...Kenapa suaramu terdengar jauh lebih hangat dari suaraku?"),
                    ),
                    (
                        ("raka:smile", "Biar retak, kita sambung pakai emas. Itu cerita kita."),
                        ("npc", "(Tinta gelap di tepi bayangan perlahan menyusut...)"),
                    ),
                ),
            ),
            ChapterScript(
                title="Babak 3: Tinta yang Mengering Pelan",
                lines=(
                    ("raka:calm", "Saatnya menyambung halaman sketsa lewat Kintsugi, lalu menyelaraskan Kaset [2] HUJAN agar badai ini tenang."),
                ),
            ),
        ),
        rain_whisper="[Bisikan Kaset HUJAN]: 'Kalau gambarnya jelek, ya belajar lagi bareng aku, Rak. Nggak usah lari.' — Senja",
        mind_dive_captions=(
            "Tinta hitam di kaca menyusut menjadi sesosok anak kecil berbaju garis merah putih...",
            "Raka dewasa dan Raka kecil berlutut menggambar kereta yang sama dengan garis Kintsugi emas.",
        ),
        resonance_title="Bagian Raka Kecil Selesai!",
        resonance_subtitle="Segel Kaset [4] FAJAR terlepas sendiri. Hujan di kaca perlahan mereda.",
        epilogue_lines=(
            ("raka_kecil", "Terima kasih sudah ingat aku lagi, Kak Raka! Krayon merahku masih awet kok!"),
            ("raka:smile", "Raka kecil larut menjadi kunang-kunang keemasan... dan di dalam sakuku, selotip segel Kaset [4] FAJAR terlepas dengan sendirinya."),
        ),
    ),
    "gerbong_1_dawn": CarriageNarrative(
        scene_id="gerbong_1_dawn",
        carriage_label="GERBONG 1 — RUANG MASINIS & STASIUN FAJAR",
        bg_image_rel="images/backgrounds/bg_gerbong1_cockpit.png",
        default_cassette=4,
        passenger_name="Senja Kirana",
        portrait_slot=2,
        sprite_style="senja",
        required_cassette=4,
        target_freq=4.1,
        target_amp=78.0,
        cassette_hint="Putar Kaset [4] FAJAR yang telah terlepas segelnya, lalu satukan dengan panel masinis.",
        minigame_type="none",
        entry_cg_seq="cg_seq_fb4",
        entry_reaction_lines=(
            ("raka:surprised", "Malam itu pukul 23:41... Aku mengetik balasan untuk Senja, tapi terpotong karena mengejar kereta jam 23:59?!"),
            ("raka:sad", "Jadi ini beneran kereta komuter terakhir itu? Tapi... kenapa Senja sudah menunggu di gerbong masinis di depan sana?"),
        ),
        harmony_cg_seq="cg_seq_senja",
        is_finale=True,
        required_props_for_ch2=2,
        props=(
            PropScript(
                prop_key="manuscript_folder",
                title="NASKAH BAB TERAKHIR 'TRACK 99'",
                x=465.0,
                y=454.0,
                sprite_key="manuscript_folder",
                lines=(
                    ("raka:smile", "Map biru lusuh yang selalu dipeluk Senja ke mana-mana. Tulisan tangannya penuh revisi dialog yang ditulis penuh semangat."),
                    ("raka:calm", "Di halaman paling belakang tertulis: 'Jangan bikin ending di mana karakter utamanya sendirian terus ya, Rak.'"),
                ),
            ),
            PropScript(
                prop_key="polaroid",
                title="POLAROID SENJA & RAKA DI KAMPUS",
                x=595.0,
                y=462.0,
                sprite_key="polaroid",
                lines=(
                    ("raka:smile", "Foto kami waktu berhasil menyelesaikan bab pertama di halte kampus senja. Senja tertawa sampai matanya merem."),
                    ("raka:sad", "Kapan ya aku terakhir ketawa seperti orang di foto ini tanpa mikir beban esok hari?"),
                ),
            ),
            PropScript(
                prop_key="conductor_cap",
                title="TOPI MASINIS KAKEK HARJO",
                x=685.0,
                y=452.0,
                sprite_key="conductor_cap",
                lines=(
                    ("raka:surprised", "Topi pet biru dengan emblem sayap emas tergantung rapi di dinding lokomotif depan... Persis topi yang dipakai Pak Kondektur tadi?"),
                ),
            ),
            PropScript(
                prop_key="ticket_final",
                title="POTONGAN TIKET BERBINTANG PENUMPANG",
                x=965.0,
                y=468.0,
                sprite_key="ticket_stub",
                lines=(
                    ("raka:calm", "Kumpulan bekas tiket berlubang bintang milik Bima, Nadia, dan diriku kecil—tinggal milikku sendiri yang belum selesai."),
                ),
            ),
            PropScript(
                prop_key="hotspot:control_panel",
                title="TUAS REM KUNINGAN STASIUN FAJAR",
                x=1095.0,
                y=360.0,
                sprite_key=None,
                lines=(
                    ("raka:calm", "Layar panel kemudi memantulkan cahaya langit biru-emas di cakrawala depan. Stasiun berikutnya sudah terlihat."),
                ),
            ),
        ),
        chapters=(
            ChapterScript(
                title="Babak 1: Seperti Sore Biasa di Peron",
                lines=(
                    ("npc", "Lama banget sih jalannya dari gerbong belakang, Rak. Keburu ayam goreng kantin depan ludes tuh kalau jalanmu selambat tadi."),
                    ("raka:surprised", "Senja...? Beneran kamu?! Kukira... aku nggak bakal sempat nemuin kamu lagi."),
                    ("npc", "Hahaha, mukamu kayak habis dikejar deadline sepuluh halaman deh. Sini duduk bentar, lihat langit depannya mulai terang."),
                    ("raka:smile", "Masih aja pake jepit mustard yang sama ya, Ja. Ngomong-ngomong... lagu di kaset-kaset yang kamu bikinin ini beberapa norak banget tahu."),
                    ("npc", "HEH! Enak aja! Aku milihin itu sambil begadang di warung kopi lho! Eh—ngomong-ngomong... coba lihat barang-barang di meja dulu sana."),
                ),
            ),
            ChapterScript(
                title="Babak 2: Stasiunku Bukan di Sini",
                lines=(
                    ("npc", "Aku sudah nulis bab terakhir TRACK 99, Rak. Di bab paling akhir, tokoh utamanya akhirnya berani menoleh ke masa lalu, terus pintu keretanya terbuka di Stasiun Fajar."),
                    ("raka:sad", "Bagus banget... Nanti kita terbitin bareng ya, Ja? Kali ini aku janji nggak bakal lari atau merobek gambar lagi."),
                    ("npc", "(Senja terdiam sejenak sambil memeluk map birunya erat. Matanya tersenyum teduh, tapi suaranya terdengar sangat pelan.)"),
                    ("npc", "Raka... aku nggak bisa turun bareng kamu dari kereta ini."),
                    ("raka:surprised", "Hah? Maksud kamu apa, Ja? Aku baru aja sampai di gerbong satu buat nyusul kamu!"),
                    ("npc", "Stasiunku bukan di sini, Rak. Sekarang coba dengerin kaset keempat yang akhirnya lepas segelnya itu. Pesan pertamaku masih ada di awal pitanya."),
                ),
                choice_prompt="Senja menunjuk Kaset [4] FAJAR di Walkman Raka saat cahaya pagi mulai menyapu kaca depan.",
                choices=(
                    "\"Baik... Mari kita putar Kaset FAJAR dan hentikan kereta ini sama-sama.\"",
                    "\"Aku siap mendengarkan pesanmu yang setahun kutunda, Senja.\"",
                ),
                choice_replies=(
                    (
                        ("npc", "[Rekaman Kaset D — Suara Senja]: 'Rak, kalau kamu dengerin ini, berarti kamu udah siap. Aku nggak marah. Aku cuma kangen gambar keretamu.'"),
                        ("raka:smile", "(Air mataku akhirnya jatuh tenang, tanpa rasa sesak.) Terima kasih sudah nungguin aku, Ja."),
                    ),
                    (
                        ("npc", "[Rekaman Kaset D — Suara Senja]: 'Nggak usah terburu-buru jadi dewasa kalau bikin kamu lupa cara bernapas. Sampai ketemu di pagi yang cerah ya.'"),
                        ("raka:smile", "Aku sudah mendengarnya dengan utuh sekarang, Senja."),
                    ),
                ),
            ),
            ChapterScript(
                title="Babak 3: Simfoni Stasiun Fajar",
                lines=(
                    ("npc", "Putar Kaset [4] FAJAR di Waveform Tuner masinis, dan samakan gelombang hatimu sebelum pintu peron terbuka."),
                    ("raka:calm", "Semuanya sudah lengkap: Senja, Hujan, Detak, dan Fajar. Ayo kita akhiri perjalanan ini."),
                ),
            ),
        ),
        rain_whisper="[Bisikan Kaset HUJAN]: 'Jangan pernah berhenti merasa cukup dengan dirimu sendiri, Raka.'",
        mind_dive_captions=(
            "Semua frekuensi kaset bergetar serempak menerangi seluruh rel laut di depan lokomotif...",
            "Tuas rem kuningan ditarik pelan. Kereta Track 99 tiba di peron Stasiun Fajar.",
        ),
        resonance_title="Bagian Senja Selesai!",
        resonance_subtitle="Pintu kereta akhirnya terbuka ke peron yang sesungguhnya.",
        epilogue_lines=(
            ("raka:smile", "Kursi ruang masinis kini sunyi dan hangat... di dekat tuas rem kuningan hanya tertinggal potongan tiket berbintang."),
            ("raka:calm", "Pintu gerbong paling depan di sisi kanan terbuka ke arah laut pagi. Saatnya melangkah turun ke Stasiun Fajar."),
        ),
        finale_station_lines=(
            ("kakek_harjo", "Waktunya turun, Le. Semua orang yang kamu sayangi tidak pernah meninggalkanmu—terima kasih sudah bertahan sebaik itu."),
            ("raka:smile", "Maaf aku telat, Senja. Terima kasih sudah menunggu... Sekarang, selamat tinggal semuanya. (SPACE / Klik untuk kembali ke Menu Utama)"),
        ),
    ),
}


def get_carriage_narrative(scene_id: str) -> CarriageNarrative:
    """Return narrative script for a carriage, merging userdata/custom_dialogues.json if present."""
    base = RAW_SCRIPTS.get(scene_id, RAW_SCRIPTS["gerbong_4_childhood"])
    custom_path = paths.userdata_path("custom_dialogues.json")
    custom = paths.read_json(custom_path, default={})
    if not isinstance(custom, dict) or scene_id not in custom:
        return base

    override = custom[scene_id]
    if not isinstance(override, dict):
        return base

    custom_chapters = override.get("chapters")
    if isinstance(custom_chapters, list) and custom_chapters:
        parsed_chapters: list[ChapterScript] = []
        for idx, ch in enumerate(custom_chapters):
            fallback_ch = base.chapters[min(idx, len(base.chapters) - 1)]
            lines_raw = ch.get("lines", fallback_ch.lines)
            lines = tuple((str(pair[0]), str(pair[1])) for pair in lines_raw if len(pair) >= 2)
            parsed_chapters.append(
                ChapterScript(
                    title=str(ch.get("title", fallback_ch.title)),
                    lines=lines or fallback_ch.lines,
                    choice_prompt=str(ch.get("choice_prompt", fallback_ch.choice_prompt)),
                    choices=tuple(str(c) for c in ch.get("choices", fallback_ch.choices)),
                    choice_replies=fallback_ch.choice_replies,
                )
            )
        return CarriageNarrative(
            scene_id=base.scene_id,
            carriage_label=base.carriage_label,
            bg_image_rel=base.bg_image_rel,
            default_cassette=base.default_cassette,
            passenger_name=base.passenger_name,
            portrait_slot=base.portrait_slot,
            sprite_style=base.sprite_style,
            required_cassette=base.required_cassette,
            target_freq=base.target_freq,
            target_amp=base.target_amp,
            cassette_hint=base.cassette_hint,
            minigame_type=base.minigame_type,
            props=base.props,
            chapters=tuple(parsed_chapters),
            rain_whisper=str(override.get("rain_whisper", base.rain_whisper)),
            mind_dive_captions=base.mind_dive_captions,
            resonance_title=base.resonance_title,
            resonance_subtitle=base.resonance_subtitle,
            epilogue_lines=base.epilogue_lines,
            is_finale=base.is_finale,
            finale_station_lines=base.finale_station_lines,
            entry_cg_seq=base.entry_cg_seq,
            entry_reaction_lines=base.entry_reaction_lines,
            harmony_cg_seq=base.harmony_cg_seq,
            unlocks_cassette_on_harmony=base.unlocks_cassette_on_harmony,
            required_props_for_ch2=base.required_props_for_ch2,
        )
    return base
