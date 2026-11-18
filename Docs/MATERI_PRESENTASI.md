# Materi Presentasi Proyek
## Gerbong Terakhir ke Stasiun Senja (*Track 99: Resonance*)

---

## Slide 1 — Judul & Identitas Proyek

- **Judul Game:** Gerbong Terakhir ke Stasiun Senja (*Track 99: Resonance*)
- **Genre:** *2D Side-Scrolling Narrative Puzzle & Emotional Memory Adventure*
- **Platform:** Desktop PC Windows 10/11 (Python `3.10+`, dibuat & diuji pada Python `3.12`)
- **Target Durasi Permainan:** ~45 Menit (*Single Playthrough*)
- **Tagline:** *"Memaafkan diri sendiri bukan berarti melupakan kesalahan—melainkan berhenti menjadikan kesalahan itu tempat tinggal."*

---

## Slide 2 — Latar Belakang Masalah & Gagasan Utama

### Masalah yang Diangkat
- **Dari Sisi Tema (Psikologis Mahasiswa & Pekerja Kreatif Muda):**
  - Banyak mahasiswa dan pekerja muda mengalami kelelahan kreatif (*burnout*), takut gagal setelah menerima penolakan, serta menumpuk penyesalan lewat kata *"nanti ya"* hingga menjauh dari mimpi dan orang-orang terdekat.
  - Game lokal bertema refleksi emosional dan penerimaan diri (*self-forgiveness*) dengan bahasa dialog yang natural masih jarang ditemui pada proyek skala mahasiswa.
- **Dari Sisi Rekayasa Proyek Mahasiswa:**
  - Pengembangan game naratif sering gagal selesai akibat *scope creep* (misalnya dunia terlalu luas atau mekanik pertarungan yang terlalu kompleks bagi tim mahasiswa).

### Solusi Konsep Produk
- **Ruang Terbatas, Kedalaman Tinggi (*Narrow Space, Deep Narrative*):** Seluruh perjalanan berpusat di dalam **5 Gerbong Kereta + 1 Peron Stasiun Fajar** sehingga kualitas cerita, dialog bercabang, ilustrasi CG, dan audio dapat dimaksimalkan.
- **Konsep *First-Minute WOW*:** Pemain bangun di gerbong hitam-putih bergaya sketsa pensil yang sunyi, lalu ketika menekan **PLAY** pada Walkman perak peninggalan kakek, gelombang warna jingga senja meledak menyapu seluruh gerbong, suara musik lofi masuk, dan pemandangan laut senja di balik jendela mulai bergerak.

---

## Slide 3 — Target Pengguna & Tujuan Produk (Ringkasan PRD)

### Target Pengguna
1. **Mahasiswa & Pemain Game Naratif (18–25 tahun):** Penggemar game cerita reflektif dan gaya visual anime/pixel seperti *To the Moon*, *A Space for the Unbound*, *Wuthering Waves*, dan *Persona*.
2. **Dosen Pembimbing & Penguji Akademik:** Penilai kesesuaian antara spesifikasi kebutuhan (PRD), arsitektur sistem (SRD), kelengkapan fitur pengguna (*Save/Load*, Galeri), serta kestabilan aplikasi saat diuji.

### Ruang Lingkup Produk (*Scope Boundary*)
- **Termasuk di Dalam Proyek (*In-Scope*):**
  - 5 Gerbong cerita + Epilog Peron Stasiun Fajar berdurasi total ~45 menit.
  - Mekanik Walkman **4 Kaset Emosi** (*Senja*, *Hujan*, *Detak*, *Fajar*) yang mengubah video jendela, warna ruangan, musik BGM, dan dialog batin.
  - **25 Ilustrasi CG Cutscene** (*fade* hitam untuk kilas balik, *fade* putih untuk perpisahan & ending) + **5 Video MP4**.
  - **3 Variasi Mini-Game Relaks:** *Waveform Tuner*, *Pesawat Kertas Bima*, dan *Kintsugi Sketsa*.
  - Sistem **Pause Menu**, **10 Slot Save/Load** portabel, dan **Galeri Kenangan 25 CG**.
- **Di Luar Ruang Lingkup (*Out-of-Scope*):**
  - Tidak ada sistem *combat* / HP / *game over*, tidak ada fitur *online/multiplayer*, dan tidak menggunakan *full voice acting*.

---

## Slide 4 — Premis Cerita & *Dual-Layer Plot Twist*

### Premis Singkat
**Raka Adiwangsa (24)**, seorang desainer banner iklan yang lama berhenti menggambar setelah komik impiannya ditolak penerbit, terbangun di kereta tanpa warna pukul **23:59**. Ia mengira hanya ketiduran sepulang lembur. Dari Gerbong 5 hingga Gerbong 1, Raka membantu setiap penumpang menyelesaikan penyesalan mereka sambil dihantui potongan kilas balik masa lalunya sendiri.

### Kejutan Cerita Berlapis (*Dual-Layer Plot Twist*)

| Lapis | Dugaan Pemain Sepanjang Cerita | Kebenaran di Akhir Cerita (*Stasiun Fajar*) |
| :--- | :--- | :--- |
| **Twist 1: Senja** | Dialog yang sengaja ambigu membuat pemain mengira sahabat Raka, **Senja Kirana**, sudah meninggal dan Raka dihantui rasa bersalah. | **Senja masih hidup.** Satu tahun lalu ia hanya pindah ke Yogyakarta naik kereta pagi 06:00 dan akhirnya menerbitkan komik *TRACK 99* Vol. 1 memakai sketsa lama Raka. |
| **Twist 2: Raka & Kereta** | Pemain mengira kereta ini sekadar mimpi atau metafora psikologis orang yang kelelahan kerja. | **Raka dan para penumpang di kereta telah tiada.** Raka kelelahan dan tertidur di kereta terakhir pukul **23:59** malam sebelum keberangkatan Senja, dan tidak pernah bangun lagi. |

### Makna Perjalanan
Kereta *Track 99* adalah ruang persinggahan jiwa yang tidak akan berhenti sampai penumpangnya berdamai dengan diri sendiri. Pak Kondektur yang di akhir membuka topinya adalah **Kakek Harjo** (kakek Raka) yang menunggu hingga Raka siap untuk *"turun"*.

---

## Slide 5 — Karakter Utama & Simbolisme Penyesalan

| Karakter | Latar Singkat | Luka Batin / Cermin bagi Raka |
| :--- | :--- | :--- |
| **Raka Adiwangsa (24)** | Mantan ilustrator webcomic *TRACK 99* yang banting setir jadi desainer banner pasrah (*burnout*). | Membenci kegagalannya sendiri, merobek buku sketsa di bawah hujan, dan terus membalas pesan sahabat dengan kata *"nanti ya"*. |
| **Pak Kondektur / Kakek Harjo (~70)** | Pemandu kereta berseragam kondektur; mantan masinis *Senja Utama*. | Menolak melubangi tiket Raka di awal karena Raka belum siap memaafkan diri sendiri. Menyambut Raka di Stasiun Fajar dengan *"Waktunya turun, Le."* |
| **Bima Sakti Pratama (9)** | Anak penderita leukemia di Ruang Anggrek 3 berjas hujan kuning kebesaran. | Merasa sakitnya menghancurkan mimpi kakaknya (Mas Dimas) menggambar komik; takut menerbangkan pesawat kertas karena takut jatuh dan rusak. |
| **Nadia Larasati (26)** | Arsitek junior perantau dengan jam dinding berhenti di **01:14**. | Membentak ibunya di telepon saat lembur pada malam ulang tahun sang ibu sebelum mengalami kecelakaan fatal sepulang kerja. |
| **Bayangan Raka / Raka Kecil (8)** | Manifestasi suara kebencian diri di kaca Gerbong 2 yang luruh menjadi diri Raka masa kecil. | Mewakili penolakan dan hinaan Raka pada dirinya sendiri; berdamai lewat Kintsugi emas bersama anak 8 tahun pemegang krayon. |
| **Senja Kirana (24)** | Sahabat Raka & penulis *TRACK 99*; pembuat *mixtape* 4 kaset Walkman. | Hadir di Gerbong 1 sebagai cermin penerimaan di ingatan Raka, dan tampil hidup satu tahun kemudian di Peron 2 Stasiun Kotabaru pada *Ending*. |

---

## Slide 6 — Peta Perjalanan 5 Gerbong & Distribusi Durasi (45 Menit)

| Bab / Gerbong | Target Durasi | Tahap Batin | Kaset Aktif | Aktivitas, Mini-Game, & Cutscene |
| :--- | :---: | :--- | :--- | :--- |
| **Main Menu** | 0,5 mnt | Pembuka | `1: Senja` | Layar Raka duduk di kereta senja + akses Load/Galeri. |
| **Gerbong 5 (Keheningan)** | ~4,5 mnt | Penyangkalan | `0` $\rightarrow$ **`1: Senja`** | Video pembuka + `CG_00A–C`, **Shockwave Warna**, inspeksi 7 benda memori (Walkman, Tiket 23:59, Teh Melati, Jam Saku, Ponsel 99+, Kaset D Tersegel, Papan Rute), & dialog Kondektur. |
| **Gerbong 4 (Rak Buku)** | ~10 mnt | "Aku cuma beban" | **`1: Senja`** *(buka `2: Hujan`)* | Flashback `CG_FB1A–B`, 3 babak dialog Bima + 5 benda, Mini-game **Pesawat Kertas**, **Waveform Tuner**, Perpisahan `CG_BIMA`, & membuka **Kaset 3: Detak**. |
| **Gerbong 3 (Meja Kerja)** | ~10 mnt | Kata yang tak sempat | **`3: Detak`** | Flashback `CG_FB2A–B`, 3 babak dialog Nadia + 5 benda, pilihan dialog, **Waveform Tuner**, & Perpisahan `CG_NADIA`. |
| **Gerbong 2 (Cermin Hujan)** | ~10 mnt | Menerima diri | **`2: Hujan`** | Flashback `CG_FB3A–B`, refleksi kaca tertinggal `0.28 dtk`, Mini-game **Kintsugi Sketsa**, **Waveform Tuner**, Perpisahan `CG_BAYANGAN`, & segel **Kaset 4: Fajar** terbuka. |
| **Gerbong 1 & Stasiun Fajar** | ~10 mnt | Melepaskan & Pulang | **`4: Fajar`** | Flashback `CG_FB4A–B`, 3 babak dialog Senja, **Waveform Tuner**, `CG_SENJA`, Video Akhir, `CG_END_01–06` (*Twist Reveal*), & Epilog Stasiun Fajar. |

---

## Slide 7 — Fitur Gameplay & Inovasi Mekanik Utama

1. **Sistem Walkman 4 Kaset (`SENJA`, `HUJAN`, `DETAK`, `FAJAR`)**
   - Mengubah atmosfer visual (*tint* & partikel), video jendela luar kereta, lagu latar (*BGM*), dan memicu **Bisikan Hujan** saat Kaset 2 (*Hujan*) diputar.
   - Kaset terdistribusi bertahap dari Gerbong 5 hingga Gerbong 1 agar keempat musik mendapat porsi waktu dengar yang seimbang sepanjang 45 menit.
2. **Waveform Tuner + Efek Riak Tetesan Air**
   - Teka-teki menyelaraskan **Frekuensi** dan **Amplitudo** gelombang emosi Raka dengan gelombang hati penumpang, lengkap dengan efek riak air (*concentric water droplet ripples*) setiap kali kaset diganti dan fitur aksesibilitas `[TAB] Auto-Tune`.
3. **Dua Mini-Game Tematik Tambahan**
   - **Terbangkan Pesawat Kertas (Gerbong 4):** Memandu pesawat kertas komik milik Bima menangkap 5 cahaya kenangan.
   - **Kintsugi Sketsa (Gerbong 2):** Menyambung 4 keping buku sketsa yang robek menggunakan garis emas Kintsugi.
4. **Cutscene CG Gaya *Wuthering Waves* & Cut-In Gaya *Persona***
   - 25 ilustrasi CG penuh dengan efek gerak *Ken Burns zoom*, transisi tirai hitam/putih, subtitel puitis, dan banner selebrasi *"Bagian [Nama] Selesai!"* bergambar Raka tersenyum sambil mengacungkan jempol.
5. **10-Slot Save/Load & Galeri 25 CG**
   - Tersedia melalui Main Menu maupun Pause Menu (`ESC`), lengkap dengan *auto-unlock* CG ke Galeri Kenangan lintas penyimpanan.

---

## Slide 8 — Arsitektur Sistem & Tech Stack (Ringkasan SRD)

### Tech Stack yang Digunakan
- **Bahasa & Runtime:** Python `3.10+` (dibuat & diuji pada **Python `3.12`**, kompatibel hingga `3.13`/`3.14`, terisolasi dalam `.venv`).
- **Engine Render & Input:** `pygame-ce` (SDL2) pada resolusi kanvas `1280 x 720` di **60 FPS**.
- **Pemrosesan Video & Piksel:** `opencv-python` (`cv2`) untuk dekode MP4 *real-time* di jendela kereta + `numpy` untuk *chroma-key* dan manipulasi *surface*.
- **Packaging Portabel:** `PyInstaller` (`--onedir`) untuk distribusi desktop mandiri.

### Struktur Modular Kode (`src/`)
- **`main.py`:** Inisialisasi lingkungan portabel, game loop `60 FPS`, *crash logger*, dan mode verifikasi otomatis `--self-test`.
- **Lapisan Inti (`src/core/`):**
  - `paths.py`: Isolasi folder portabel (`TEMP`/`APPDATA` diarahkan ke `./userdata/`) & penulisan JSON atomik (`.tmp`).
  - `director.py`: Pengelola *playlist scene*, transisi *diagonal wipe*, *Pause Menu*, dan *Director HUD* (`F1` untuk pantau pacing 45 menit, `[`/`]` untuk lompat gerbong, `F5` *hot-reload*).
  - `persona_ui.py` & `cg_cutscene.py`: *Chroma-key* `#00FF00` & `#FF00FF`, pemotong sprite 4-frame otomatis, `_UI_SURFACE_CACHE`, HUD Walkman, kotak dialog anti-tumpang-tindih, dan pemutar 25 CG.
  - `waveform_tuner.py` & `minigames.py`: Logika puzzle gelombang sinus, riak tetesan air, Pesawat Kertas, dan Kintsugi.
  - `save_and_menus.py` & `narrative_script.py`: Manajemen 10 slot simpanan, Galeri 3 halaman, serta skrip narasi 3 babak tiap gerbong.
- **Lapisan Scene (`src/scenes/`):** `TitleScreenScene`, `Gerbong5IntroScene`, dan `CarriageStoryScene` (reusable/data-driven untuk Gerbong 4, 3, 2, 1, dan Stasiun Fajar).

---

## Slide 9 — Keunggulan Implementasi Teknis & Hasil Pengujian

### Solusi Teknis Kunci
1. **Chroma-Key Video Jendela & Auto-Slicing Sprite:** Kaca jendela berwarna `#00FF00` disaring dengan vektorisasi NumPy (*green despill*) sehingga video pemandangan MP4 dapat bergerak di balik sprite kereta, dan seluruh *sprite sheet* 4-frame dipotong proporsional secara otomatis.
2. **Surface & Zoom Caching (`_UI_SURFACE_CACHE` & `_zoom_cache`):** Menghilangkan jeda *lag* ~1 detik ketika berpindah gerbong, berganti kaset, atau memutar animasi *zoom* pada 25 CG.
3. **Interaksi Bebas Tumpang-Tindih & Raka Diam Saat Dialog:** Karakter otomatis berjalan ke posisi berdiri aman (`npc_talk_x` / `conductor_talk_x`) sambil menghadap NPC baik via keyboard `[E]` maupun klik mouse, dan pergerakan terkunci selama kotak dialog terbuka.
4. **Foreshadowing Teknis (Refleksi Tertinggal):** Di Kaset 2 (*Hujan*), histori posisi pemain (`_pos_history`) diambil `0.28` detik ke belakang untuk merender bayangan refleksi di kaca yang tertinggal dari tubuh Raka.
5. **Penyimpanan Portabel Anti-Korup:** Seluruh data (`slot_1..10.json`, `gallery_unlocked.json`, `settings.json`) disimpan atomik di `./userdata/saves/`.

### Hasil Verifikasi & Audit Sistem
- **Total Aset Aktif:** **74 aset nyata** terpakai (`7` BGM MP3, `10` WAV SFX akustik sintesis NumPy, `25` CG ilustrasi, `5` video MP4, `15` sprite sheet, `8` background, `3` portrait sheet, `1` UI Walkman).
- **Status Audit Aset (`build_portable.py --audit`):** **0** aset hilang (*missing/fallback*) dan **0** aset sisa tidak terpakai.
- **Status Self-Test Otomatis (`main.py --self-test`):** Seluruh 6 *scene*, 25 CG, 10 sekuens, 7 BGM, 10 SFX, 3 mini-game, dan *round-trip* Save/Load berhasil dieksekusi dengan status lolos (`exit code 0`).

---

## Slide 10 — Skenario Demo Game Langsung (*Live Demo Flow*)

Urutan fitur yang didemonstrasikan langsung di dalam aplikasi saat presentasi:
1. **Main Menu & Galeri Kenangan:** Menampilkan Raka duduk di samping video jendela senja, navigasi menu bersih, dan pratinjau Galeri 25 CG (termasuk fitur `F8` untuk membuka pratinjau bagi penguji).
2. **Prolog & Gerbong 5 (*First-Minute WOW*):** Menunjukkan perubahan dramatis dari dunia sketsa hitam-putih menjadi dunia berwarna senja saat tombol **PLAY** Walkman ditekan, inspeksi 7 benda memori, dan interaksi non-overlap dengan **Pak Kondektur**.
3. **Transisi Kilas Balik & Gerbong 4 (Bima):** Memperlihatkan pemutaran **CG Kilas Balik** (*fade* hitam), percakapan natural 3 babak dengan Bima (termasuk *auto-walk* menghadap NPC), mini-game **Pesawat Kertas**, **Waveform Tuner** lengkap dengan efek **riak tetesan air** saat ganti kaset, **CG Perpisahan**, serta cut-in **"Bagian Bima Selesai!"**.
4. **Demonstrasi Pacing & Lompat Gerbong (`F1` & `[`/`]`):** Menunjukkan fitur *Director Bar* (target 45 menit), efek pantulan kaca tertinggal di Gerbong 2 saat memutar Kaset *Hujan* + Mini-game **Kintsugi Sketsa**, serta sekilas *Ending* di **Peron Stasiun Fajar**.
5. **Pause Menu & Save/Load 10 Slot:** Menekan `ESC`, menyimpan progres ke salah satu dari 10 slot, lalu memuat ulang untuk membuktikan persistensi data portabel berjalan lancar.
