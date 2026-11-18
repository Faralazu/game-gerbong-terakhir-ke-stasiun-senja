# Gerbong Terakhir ke Stasiun Senja (_Track 99: Resonance_)

Link Gameplay : https://youtu.be/4db7HCXq-X0?si=tbYdJ3XJn1ToIuLl

> _"Memaafkan diri sendiri bukan berarti melupakan kesalahan—melainkan berhenti menjadikan kesalahan itu tempat tinggal."_

**Gerbong Terakhir ke Stasiun Senja** adalah game naratif 2D _side-scrolling_ berbahasa Indonesia bergenre _Emotional Memory Adventure & Narrative Puzzle_ (~45 menit permainan). Anda berperan sebagai **Raka Adiwangsa (24)**, seorang desainer yang kelelahan (_burnout_) dan terbangun di dalam kereta tanpa warna pukul **23:59**. Dengan memutar **Walkman perak** peninggalan kakeknya, warna senja kembali menyapu gerbong—mengantar Raka menolong para penumpang dari Gerbong 5 hingga Gerbong 1 sambil menyingkap misteri kereta menuju **Stasiun Fajar**.

---

## Fitur Utama

- **Efek _First-Minute WOW_:** Dunia sketsa hitam-putih berubah menjadi warna jingga senja melalui efek gelombang kejut (_shockwave_) saat Walkman pertama kali diputar.
- **Sistem Walkman 4 Kaset Emosi:** Putar **Senja**, **Hujan**, **Detak**, dan **Fajar** untuk mengubah pemandangan video di balik jendela kereta, palet pencahayaan gerbong, lagu latar (_BGM_), serta membuka bisikan rahasia (_Rain Whisper_) dan refleksi kaca tertinggal pada frekuensi hujan.
- **3 Variasi Mini-Game Relaks:**
  - _Waveform Tuner_ (penyelarasan frekuensi & amplitudo emosi lengkap dengan efek riak tetesan air dan mode bantuan `[TAB] Auto-Tune`).
  - _Terbangkan Pesawat Kertas Bima_ (Gerbong 4).
  - _Kintsugi Sketsa_ (Gerbong 2).
- **25 _Illustrated CG Cutscene_ & 5 Video MP4:** Transisi kilas balik (_fade_ hitam) dan perpisahan/ending (_fade_ putih) bergaya _Wuthering Waves_ lengkap dengan _Galeri Kenangan_.
- **Pause Menu & 10-Slot Save/Load Portabel:** Seluruh data simpanan tersimpan rapi di dalam folder `./userdata/saves/` tanpa mengotori folder Windows pengguna.

---

## Mengapa Distribusi Ini Menggunakan `main.py` & Script (Tanpa File `.exe`)?

Agar **satu folder proyek ini bisa langsung dibagikan lewat GitHub (umum) maupun Google Drive (internal mahasiswa & dosen)** dengan aman:

1. **100% Bebas Blokir _Windows Smart App Control_ & Antivirus:** File `.exe` buatan mahasiswa yang tidak memiliki _Code Signing Certificate_ berbayar hampir selalu diblokir oleh Windows 11 (_Smart App Control_). Menjalankan langsung kode Python sumber (`main.py`) melewati masalah tersebut sepenuhnya.
2. **Gratis & Transparan (_Open-Source_):** Dosen penguji, mahasiswa, dan pengguna umum dapat membaca langsung seluruh kode sumber di `src/` serta daftar dependensi resmi di `requirements.txt` (`pygame-ce`, `opencv-python`, `numpy`, `pillow`).
3. **Ringan untuk GitHub & Drive:** Seluruh library diunduh resmi langsung dari PyPI ke virtual environment lokal (`.venv`) di perangkat masing-masing melalui script satu-klik.

---

## Panduan Instalasi & Menjalankan Game (Windows)

### Prasyarat (Cukup Sekali Saja)

Pastikan komputer memiliki **Python 3.10 atau lebih baru** (mendukung versi terbaru seperti **Python 3.13 / 3.14**; game ini dibuat dan diuji menggunakan **Python 3.12**):

- Cek lewat Command Prompt / PowerShell dengan mengetik:
  ```cmd
  python --version
  ```
- Jika Python belum terpasang, unduh gratis dari situs resmi **[python.org/downloads](https://www.python.org/downloads/)** (disarankan Python `3.12` atau versi terbaru di atasnya).
- **PENTING:** Saat menjalankan installer Python, wajib centang kotak **`[x] Add python.exe to PATH`** di bagian bawah sebelum menekan _Install Now_. _(Alternatif cepat lewat PowerShell: `winget install Python.Python.3.12`)_

---

### Cara 1: Paling Mudah — Lewat Klik 2x (Rekomendasi untuk Mahasiswa & Dosen)

Cocok jika Anda mengunduh folder game dari **Google Drive** (`.zip`) maupun **GitHub**:

1. Ekstrak folder proyek jika berbentuk `.zip`.
2. **Instalasi Library (hanya sekali di awal, butuh internet ~150 MB):**
   - Klik 2x file **`INSTALL_LIBRARIES.bat`**.
   - Tunggu hingga proses membuat `.venv` lokal dan mengunduh 4 library resmi dari `requirements.txt` selesai bertuliskan **`Instalasi SELESAI!`**.
3. **Memainkan Game:**
   - Klik 2x file **`RUN_GAME.bat`** kapan saja untuk membuka game (tidak perlu internet saat bermain).
   - _(Tips: Jika langsung klik 2x `RUN_GAME.bat` pada perangkat baru pun, script otomatis akan mengecek dan menjalankan instalasi library bila belum terpasang.)_

> **Catatan Pengguna Google Drive:** Jika folder yang Anda unduh kebetulan masih membawa folder `.venv` dari komputer lain, `INSTALL_LIBRARIES.bat` otomatis mendeteksi dan membangun ulang `.venv` lokal yang sesuai dengan laptop Anda.

---

### Cara 2: Via Terminal / Command Prompt / VS Code (Rekomendasi Pengguna GitHub)

1. Clone repositori atau masuk ke folder proyek:
   ```bash
   git clone <url-repo-github-anda>
   cd "<nama-folder-proyek>"
   ```
2. Buat virtual environment (disarankan) lalu instal library resmi:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Jalankan game:
   ```bash
   python main.py
   ```
4. _(Opsional) Verifikasi otomatis & audit 74 aset:_
   ```bash
   python main.py --self-test
   python tools/build_portable.py --audit
   ```

---

## Kontrol Bermain & Shortcut Penguji (Dosen / Presenter)

### Kontrol Standar Pemain

| Tombol / Input                                         | Fungsi                                                                                                            |
| :----------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| **`A` / `D`**, **`←` / `→`**, atau **Klik Kiri**       | Menggerakkan Raka ke kiri / kanan di dalam gerbong                                                                |
| **`E`** atau **Klik Objek / Karakter**                 | Berinteraksi dengan benda memori, berbicara dengan NPC, duduk di kursi kiri, atau pindah gerbong                  |
| **`SPACE`** / **`ENTER`** / **Klik Kiri**              | Melanjutkan dialog, memilih opsi jawaban, atau melewati baris ketik                                               |
| **`1` – `4`** atau **Klik HUD Kanan Atas**             | Mengganti kaset Walkman yang sudah terbuka (`TAB` untuk memunculkan/menyembunyikan laci HUD)                      |
| **`W` / `S` / `A` / `D`** / **Mouse** _(di Mini-Game)_ | Mengendalikan _Waveform Tuner_, _Pesawat Kertas_, dan _Kintsugi Sketsa_ (`TAB` untuk _Auto-Tune / Lewati Santai_) |
| **`ESC`**                                              | Membuka **Pause Menu** (Lanjut, Simpan 10 Slot, Muat 10 Slot, Galeri 25 CG, Kembali ke Menu Utama)                |

### Shortcut Khusus Pengujian & Demo Presentasi Dosen

| Shortcut                             | Fungsi                                                                               |
| :----------------------------------- | :----------------------------------------------------------------------------------- |
| **`F1`**                             | Menampilkan/menyembunyikan **Director Pacing Bar** (pantauan waktu target 45 menit)  |
| **`[`** dan **`]`**                  | Melompat langsung ke gerbong sebelumnya / gerbong berikutnya secara instan saat demo |
| **`F8`** _(saat di Galeri Kenangan)_ | Membuka pratinjau seluruh **25 Ilustrasi CG** sekaligus untuk evaluasi visual        |
| **`F5`**                             | _Hot-Reload_ seluruh aset gambar, video, dan audio tanpa menutup aplikasi            |

---

## Struktur Folder Final

```text
.
├── main.py                      # Entry point utama aplikasi & CLI --self-test
├── requirements.txt             # Daftar library Python resmi (pygame-ce, opencv-python, numpy, pillow)
├── INSTALL_LIBRARIES.bat        # Script satu-klik instalasi library ke .venv lokal
├── RUN_GAME.bat                 # Launcher pintar satu-klik untuk menjalankan game
├── README.md                    # Panduan distribusi, instalasi, & kontrol bermain
├── .gitignore                   # Aturan pengecualian file sementara/.venv untuk GitHub
├── assets/                      # 74 aset multimedia aktif (BGM MP3, WAV SFX, CG, Sprite, Video MP4)
├── src/
│   ├── core/                    # Engine inti (paths, director, asset_manager, UI, CG, tuner, minigames, saves)
│   └── scenes/                  # Modul scene (Title Screen, Gerbong 5 Intro, Gerbong 4-1 & Stasiun Fajar)
├── tools/                       # Utilitas pengembang (generate_sfx_pack.py & build_portable.py --audit)
├── userdata/                    # Penyimpanan lokal portabel (saves 10 slot, gallery, settings, playlist, logs)
└── Docs/                        # Seluruh dokumentasi akademik, cerita, & prompt aset:
    ├── PRD.md                   # Product Requirements Document
    ├── SRD.md                   # System Requirements Document
    ├── MATERI_PRESENTASI.md     # Substansi materi presentasi tim (siap kemas ke PPT)
    ├── GAME_DESIGN_DOCUMENT.md  # Dokumen desain game awal
    ├── story/                   # Dokumen narasi inti (STORY_BIBLE.md & NOVEL_TRACK99.md)
    └── prompts/                 # Arsip prompt aset & CG (DAFTAR_ASSET_DAN_PROMPT, PROMPT_CG_NARASI, dll.)
```

---

## Daftar Pustaka Dokumentasi Proyek

- **Product Requirements Document:** [`Docs/PRD.md`](Docs/PRD.md)
- **System Requirements Document:** [`Docs/SRD.md`](Docs/SRD.md)
- **Materi Presentasi Tim:** [`Docs/MATERI_PRESENTASI.md`](Docs/MATERI_PRESENTASI.md)
- **Game Design Document:** [`Docs/GAME_DESIGN_DOCUMENT.md`](Docs/GAME_DESIGN_DOCUMENT.md)
- **Story Bible & Novel Lengkap:** [`Docs/story/STORY_BIBLE.md`](Docs/story/STORY_BIBLE.md) & [`Docs/story/NOVEL_TRACK99.md`](Docs/story/NOVEL_TRACK99.md)
- **Daftar Prompt Aset & CG:** [`Docs/prompts/`](Docs/prompts/)
