# Game Design Document (GDD)
## **Gerbong Terakhir ke Stasiun Senja (*Track 99: Resonance*)**

---

## 1. Identitas Game
* **Judul:** Gerbong Terakhir ke Stasiun Senja (*Track 99: Resonance*)
* **Genre:** 2D Pixel Art Narrative Puzzle & Interactive Audio-Visual Experience
* **Target Durasi:** ± 45 Menit (Single sitting, dirancang untuk dimainkan santai setelah pulang kerja/kuliah)
* **Platform & Bahasa Utama:** PC (Windows/Desktop) — Python (`pygame-ce` + `opencv-python` + `numpy` + `pillow`)
* **Gaya Visual & Referensi:**
  * **Pixel Art Lingkungan & Nuansa:** *A Space for the Unbound*, *Eastward*, *OMORI*
  * **Antarmuka (UI) & Gaya Kinetik:** *Persona 3 Reload* & *Persona 5* (poligon miring tajam, *slanted dialogue boxes*, *eye cut-in* dramatis, transisi geometris)
  * **Kedalaman Emosional & Pacing:** *To The Moon*, *When the Past Was Around*, *Before Your Eyes*
* **Konsep Inti (*High Concept*):**
  Kamu terbangun sendirian di dalam kereta komuter senja yang melaju di atas hamparan laut dangkal menuju stasiun yang tak pernah tiba. Berbekal sebuah **Walkman tua dengan 4 Kaset Emosi**, kamu harus memutar kaset untuk mengubah realitas, mendengarkan keluh kesah para penumpang, menyelaraskan frekuensi hati mereka, dan akhirnya menyadari siapa sebenarnya yang mengemudikan kereta menuju masa lalu tersebut.

---

## 2. Arsitektur Teknis Python (`Pygame-CE` + `OpenCV`)

Agar game 2D Python terasa sekelas game *indie* komersial dengan **"Efek WOW di menit pertama"** tanpa perlu menulis ribuan frame animasi manual, arsitektur teknis kita memadukan **Video Layering Real-Time** dan **Procedural Persona UI**:

### A. Layered Video-Behind-Window Pipeline (`cv2.VideoCapture` + `pygame-ce`)
Pemandangan luar jendela kereta tidak hanya gambar diam atau *scrolling* statis—melainkan **video looping ≤ 15 detik hasil generate Google Flow** yang diputar secara mulus di lapisan paling belakang!
1. **Layer 0 (Video Background — OpenCV):** `cv2.VideoCapture` membaca frame video `.mp4` (misal `vid_02_window_sunset_loop.mp4`), mengonversi ruang warna BGR → RGB, dan memproyeksikannya ke `pygame.Surface` secara asinkron/terjadwal sesuai FPS video.
2. **Layer 1 (Interior Gerbong — PNG Alpha Cutout):** Sprite interior gerbong kereta resolusi piksel di-render di atas Layer 0. Area kaca jendela pada gambar interior dibuat **transparan (alpha = 0)** atau memiliki *tint* kaca tipis, sehingga video laut senja/hujan neon dari Layer 0 terlihat meluncur hidup di luar jendela kereta!
3. **Layer 2 (Entitas, Karakter & Partikel):** Karakter utama (**Raka**), penumpang, barang memori, dan partikel debu cahaya/hujan yang dirender dengan kedalaman (*y-sorting* / parallax ringan).
4. **Layer 3 (Post-Processing & Shockwave Transition):** Efek perubahan realitas saat tombol *PLAY* Walkman ditekan (lingkaran/poligon *shockwave* yang menyapu layar dan mengganti palet warna serta video latar secara *real-time*).
5. **Layer 4 (Procedural Persona UI):** Kotak dialog poligon miring, indikator Walkman kinetik, gelombang frekuensi (*Waveform Tuner*), dan *Character Cut-In* yang dirender secara matematis menggunakan `pygame.draw.polygon`, *easing* (`lerp`), dan gelombang sinus (`math.sin`) agar super tajam di berbagai resolusi.

### B. Sistem Audio Dinamis (Crossfade & Synced BGM)
* Menggunakan `pygame.mixer.music` dan `pygame.mixer.Channel` terpisah agar saat pemain menekan tombol Walkman:
  * Terdengar suara mekanik tombol besi **`CLACK-CLICK`** dan dengung pita kaset (*tape hiss*) terlebih dahulu.
  * Musik berganti mengikuti kaset yang dipilih, sinkron dengan perubahan visual gerbong kereta.

---

## 3. Mekanik Utama (*Core Gameplay Loop*)

Game ini menghindari sistem *grinding* atau teka-teki rumit yang membuat pemain stres sepulang kerja/kuliah. Semua mekanik bersifat **taktil, memanjakan mata dan telinga, serta menjadi metafora psikologis cerita**:

### A. Walkman 4 Kaset Emosi (*Reality Shifting*)
Pemain menekan tombol (`1–4` atau klik UI Walkman di pojok layar) untuk mengganti kaset yang sedang diputar. Setiap kaset mengubah **Musik BGM**, **Video Jendela Luar**, **Warna Palet Interior**, dan **Perilaku Objek/Penumpang**:

1. **Side A: `SENJA` — *Nostalgia* (Palet: Jingga Keemasan / Amber)**
   * **Nuansa Musik:** City Pop / Lo-Fi hangat dengan Rhodes piano.
   * **Efek Realitas:** Menghidupkan kehangatan dan kenangan indah. Benda yang rusak tampak utuh seperti dulu; penumpang mau bercerita tentang hal-hal yang mereka rindukan.
2. **Side B: `HUJAN` — *Denial / Penyangkalan* (Palet: Biru Neon / Ungu Malam)**
   * **Nuansa Musik:** Synthwave melankolis dengan rintik hujan lembut.
   * **Efek Realitas:** Mengungkap beban pikiran, rasa bersalah, dan bayangan yang selama ini disembunyikan di balik senyuman. Teks rahasia, coretan dinding, atau aura emosi penumpang hanya tampak di frekuensi ini.
3. **Side C: `DETAK` — *Courage / Keberanian* (Palet: Merah Menyala / Hitam Kontras ala *Persona 5*)**
   * **Nuansa Musik:** Acid Jazz energik dengan *bassline* tegas dan ritme percaya diri.
   * **Efek Realitas:** Menghancurkan rantai keraguan, membekukan gangguan kecemasan, atau membuka pintu antargerbong yang terkunci oleh rasa takut.
4. **Side D: `FAJAR` — *Acceptance / Keikhlasan* (Palet: Hijau Teduh / Putih Cahaya Pagi)**
   * **Nuansa Musik:** Orkestra piano & strings emosional (*To The Moon* / *OMORI* vibe).
   * **Efek Realitas:** Hanya terbuka di babak akhir. Menyatukan seluruh lapisan masa lalu dan masa kini menjadi kedamaian yang utuh.

### B. Waveform Tuner (*Frekuensi Memori*)
Saat berinteraksi dengan penumpang yang hatinya "terkunci", muncul antarmuka **Waveform Tuner ala Persona**:
* Pemain melihat dua gelombang di layar: **Gelombang Emosi Penumpang** (berwarna acak/bergetar) dan **Gelombang Walkman Pemain**.
* Dengan memutar roda *tuner* (scroll mouse / tombol panah kiri-kanan) sambil memilih kaset yang tepat, pemain menyamakan amplitudo dan frekuensi hingga kedua garis bertumpuk sempurna dan bersinar emas → memicu **Memory Resonance** (*eye cut-in* + adegan kilas balik yang menyentuh).

### C. Momen "Duduk & Bernapas" (*Cozy Rest Spots*)
Di setiap gerbong ada kursi kosong dekat jendela di mana pemain boleh menekan tombol interaksi untuk sekadar **duduk, memandang video laut senja di luar jendela, dan mendengarkan musik** tanpa tekanan waktu—memberikan ruang relaksasi yang sangat dibutuhkan setelah hari yang melelahkan.

---

## 4. Struktur Cerita & Pacing 45 Menit (5 Gerbong)

Protagonis kita adalah **Raka**, seorang pemuda yang baru saja melewati fase berat dalam hidupnya dan tertidur di kereta terakhir sepulang aktivitas. Seluruh kereta *Track 99* adalah manifestasi dari perjalanan batinnya sebelum ia benar-benar siap melangkah ke babak baru.

| Fase & Durasi | Lokasi | Suasana & Pacing | Momen Kunci & Gameplay |
| :--- | :--- | :--- | :--- |
| **Menit 0–5**<br>*(Efek WOW Menit 1)* | **Gerbong 5:**<br>*Keheningan* | **Hening, Sketsa Hitam-Putih** | Game dibuka dengan video intro kereta melaju di atas laut (`vid_01`). Raka terbangun di gerbong sketsa pensil hitam-putih yang sunyi (hanya suara rel *klak-klak*). Di kursi sebelah tergeletak Walkman. Saat pemain menekan **PLAY (Kaset SENJA)**, **gelombang kejut warna jingga menyapu layar**, video laut senja menyala di balik jendela (`vid_02`), dan musik Lo-Fi hangat mulai mengalun. |
| **Menit 5–15**<br>*(Lambat & Cozy)* | **Gerbong 4:**<br>*Taman Bermain* | **Nostalgia, Hangat, Santai** | Raka berjalan pelan, bisa duduk menikmati pemandangan senja. Ia bertemu penumpang pertama: **Anak Kecil** yang terus mencari bagian mainan pesawat kertas/robotnya yang hilang. Dengan menukar kaset **SENJA** dan **HUJAN**, Raka menyadari bahwa mainan itu hilang bukan karena dibuang, melainkan karena takut rusak—cerminan masa kecil Raka sendiri yang belajar takut kehilangan. |
| **Menit 15–30**<br>*(Dalam & Relatable)* | **Gerbong 3 & 2:**<br>*Ruang Tunggu & Kampus/Kantor* | **Melankolis → Tegang/Berani** | Suasana menjadi lebih padat. Penumpang kedua adalah **Mahasiswi/Pekerja Kelelahan** yang tenggelam dalam tumpukan catatan dan jam dinding yang terus berputar mundur. Dengan kaset **HUJAN**, terlihat bayangan ekspektasi orang lain yang membebaninya. Pemain lalu membuka kaset **DETAK** (merah-hitam ala *Persona 5*) untuk melakukan *Break the Chain* dan menyadarkannya bahwa beristirahat bukanlah sebuah kegagalan. |
| **Menit 30–40**<br>*(Twist Emosional)* | **Gerbong 1:**<br>*Bayangan Masa Lalu* | **Intim, Penuh Kerinduan** | Di gerbong paling depan, hanya ada satu penumpang dengan wajah yang samar—seseorang dari masa lalu Raka (sahabat/sosok tersayang yang tak sempat ia temui lagi atau kalimat perpisahan yang tak terucap). Semua penumpang dari gerbong sebelumnya ternyata adalah potongan diri Raka di tiap fase hidupnya. Teka-teki membutuhkan kombinasi bergantian antara kaset **SENJA**, **HUJAN**, dan **DETAK**. |
| **Menit 40–45**<br>*(Klimaks & Puas)* | **Ruang Masinis → Stasiun Fajar** | **Katarsis, Hangat, Lega** | Pintu ruang masinis terbuka. Raka duduk di kursi masinis dan menggabungkan semua kaset ke dalam **Side D: FAJAR**. Musik mencapai klimaks emosional (`bgm_04`). Saat Raka menarik tuas rem dengan lembut, *All-Out Resonance* menyapu seluruh kereta dari Gerbong 5 hingga Gerbong 1. Kereta berhenti di peron tepi laut saat fajar menyingsing (`vid_05`). Pintu terbuka, dan Raka melangkah turun dengan senyum lega. |

---

## 5. Rencana Pengembangan Bertahap (*Roadmap*)

1. **Fase 1 — Dokumentasi & Asset Pipeline *(Sekarang)***: Menyiapkan GDD, daftar lengkap prompt video/audio/gambar, serta menguji 1 *sample* visual.
2. **Fase 2 — Prototipe "Menit Pertama WOW"**: Membangun *core engine* Python (`pygame-ce` + `opencv-python`) untuk Gerbong 5 (transisi sketsa → warna senja, video bergerak di balik jendela, UI Persona, dan Walkman player).
3. **Fase 3 — Sistem Dialog, Kaset & Waveform Tuner**: Mengimplementasikan *dialogue box* poligon miring, efek ketikan, *eye cut-in*, dan mini-game *Waveform Tuner*.
4. **Fase 4 — Produksi Konten 5 Gerbong**: Merangkai seluruh dialog, teka-teki tiap gerbong, transisi video *Mind-Dive*, dan *ending* Stasiun Fajar.
5. **Fase 5 — Polish & Feel (45-Minute Playtest)**: Menambahkan *screen shake* halus, *easing* animasi UI, efek suara rel/klik kaset, dan uji coba penuh agar pas di angka ~45 menit.
