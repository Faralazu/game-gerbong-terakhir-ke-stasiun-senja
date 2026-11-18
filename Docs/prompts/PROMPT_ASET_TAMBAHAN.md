# PROMPT ASET TAMBAHAN (Benda Cerita Baru, Karakter Baru, & BGM Tambahan)
### Melengkapi kebutuhan aset dari `STORY_BIBLE.md` agar siap diintegrasikan ke Python

> [!TIP]
> Semua sprite di dokumen ini mengikuti format sheet **2×2 (latar `#FF00FF`)** atau baris horizontal supaya otomatis terpotong rapi oleh slicer Python kita tanpa perlu mengatur koordinat satu per satu.
> Kamu bisa membuat aset gambar ini di **Gemini Web**, atau meminta saya langsung meng-generate-nya di sesi implementasi berikutnya.

---

## BAGIAN 1: 3 Sheet Benda Interaktif Baru (2×2 Grid, Background `#FF00FF`)

### 1. `assets/images/sprites/spr_story_items_1.png` *(Gerbong 5 & 4)*
* **Isi 2×2:**
  * Kiri-Atas: **Ponsel Retak** layar gelap menyala redup dengan ikon notifikasi merah kecil (tanpa huruf terbaca).
  * Kanan-Atas: **Kaset D Tersegel** berwarna hijau-mint pucat terikat pita kertas krem kecil bertuliskan `FAJAR`.
  * Kiri-Bawah: **Buku Komik Buatan Tangan** dijilid benang merah dengan gambar lokomotif di sampulnya.
  * Kanan-Bawah: **Gelang Pasien Rumah Sakit Putih** berdampingan dengan **Pesawat Kertas Komik** lipatan pensil.
* **Prompt Gemini Web / Image Generator:**
  > `2D pixel art game prop icon sheet arranged cleanly in a balanced 2x2 grid with wide spacing on a solid flat bright magenta #FF00FF chroma key background: Top-Left: cracked black smartphone with a soft dim screen glow and tiny red notification dot; Top-Right: pastel mint-gold retro cassette tape wrapped with a tiny cream paper seal band; Bottom-Left: thin handmade spiral/stitched comic notebook showing a cute train drawing on the cover; Bottom-Right: white hospital patient wristband beside a folded paper airplane made from sketch paper. Crisp 32-bit indie pixel art matching Eastward and A Space for the Unbound, clean dark outlines, no text, no drop shadows.`

### 2. `assets/images/sprites/spr_story_items_2.png` *(Gerbong 3 & 2)*
* **Isi 2×2:**
  * Kiri-Atas: **Kotak Bekal dari Ibu** terbungkus kain batik/kotak-kotak tradisional hangat.
  * Kanan-Atas: **Maket Kertas Miniatur Rumah Kayu** di atas alas kardus kecil.
  * Kiri-Bawah: **Helm Motor Putih** dengan satu garis retak tipis di bagian samping.
  * Kanan-Bawah: **Payung Transparan Basah** terlipat meneteskan air, dan **Amplop Surat Penolakan** krem kusut.
* **Prompt Gemini Web / Image Generator:**
  > `2D pixel art game prop icon sheet arranged cleanly in a balanced 2x2 grid with wide spacing on a solid flat bright magenta #FF00FF chroma key background: Top-Left: cozy homemade lunch box wrapped in a traditional patterned cloth bundle; Top-Right: delicate small white paper architectural scale model of a wooden coastal house on a small board; Bottom-Left: classic white scooter motorcycle helmet with a subtle thin hairline crack on the side; Bottom-Right: folded clear wet umbrella beside a crumpled cream envelope letter. Crisp modern 32-bit indie pixel art, clean outlines, no text, no drop shadows.`

### 3. `assets/images/sprites/spr_story_items_3.png` *(Gerbong 1 & Koleksi Tiket)*
* **Isi 2×2:**
  * Kiri-Atas: **Map Biru Tua Naskah "TRACK 99"** sedikit lusuh berisi lembaran sketsa.
  * Kanan-Atas: **Foto Polaroid** kecil bergambar dua teman tersenyum di atap saat senja.
  * Kiri-Bawah: **Topi Masinis Klasik** berwarna biru tua dengan lencana sayap emas.
  * Kanan-Bawah: **Potongan Tiket Kereta Berlubang Bintang** dengan stempel emas hangat.
* **Prompt Gemini Web / Image Generator:**
  > `2D pixel art game prop icon sheet arranged cleanly in a balanced 2x2 grid with wide spacing on a solid flat bright magenta #FF00FF chroma key background: Top-Left: worn navy blue manuscript folder filled with loose sketch pages; Top-Right: small vintage instant polaroid photograph showing two smiling silhouettes at sunset; Bottom-Left: classic navy railway conductor peaked cap with a small gold emblem; Bottom-Right: small vintage train ticket stub punched with a clean star-shaped hole. Crisp modern 32-bit indie pixel art, clean outlines, no text, no drop shadows.`

---

## BAGIAN 2: Karakter Baru (Pak Kondektur / Kakek Harjo & Raka Kecil)

### 1. `assets/images/sprites/spr_conductor_and_young_raka.png` *(Sprite Berdiri)*
* **Fungsi:** Sprite berdiri Pak Kondektur (lentera kuningan + pelubang tiket) dan Raka Kecil 8 tahun (kaos garis merah-putih + krayon & buku gambar) agar bisa muncul langsung di gerbong.
* **Prompt Gemini Web / Image Generator:**
  > `2D pixel art character sprite sheet for a side-scrolling indie game, 2 full-body characters arranged side-by-side in a horizontal row with wide empty spacing on a solid flat bright magenta #FF00FF chroma key background: Left: an elderly Indonesian railway conductor around 70 years old with neat white mustache, wearing an old-fashioned navy conductor uniform with brass buttons and a peaked cap shadowing his eyes, holding a warm glowing brass lantern, facing left; Right: a small 8-year-old Indonesian boy with messy dark-brown hair and cowlick, wearing an oversized red-and-white striped t-shirt and shorts, holding a crayon and small sketchbook, facing left. Crisp pixel art matching Eastward and A Space for the Unbound, no text, no ground shadows.`

### 2. `assets/images/portraits/port_conductor_and_young_raka.png` *(Potret Dialog)*
* **Fungsi:** 3 panel potret dialog sejajar: 1) Pak Kondektur bertopi miring misterius, 2) Kakek Harjo tersenyum tanpa topi untuk adegan ending, 3) Raka Kecil tersenyum ceria.
* **Prompt Gemini Web / Image Generator:**
  > `2D anime pixel art character bust portrait sheet arranged cleanly in 3 equal vertical panels side-by-side on a solid flat dark navy #101420 background: Left panel: mysterious kindly elderly Indonesian railway conductor with white mustache wearing a navy peaked cap that shadows his eyes slightly; Center panel: the same kindly elderly Indonesian man without his cap, revealing warm wrinkled eyes and gentle grandfatherly smile in golden dawn light; Right panel: cheerful 8-year-old Indonesian boy with messy dark hair, cowlick, red-and-white striped shirt, and gap-toothed smile holding a crayon. High-detail expressive pixel art matching A Space for the Unbound, no text, no letters.`

---

## BAGIAN 3: Audio BGM Tambahan (Gemini Web / Lyria)

### 1. `assets/audio/bgm/bgm_05_flashback_musicbox.mp3`
* **Fungsi:** Lagu khusus ketika **4 adegan Kilas Balik (`CG_FB1` – `CG_FB4`)** muncul saat Raka melangkah ke gerbong baru.
* **Prompt Gemini Web:**
  > `Nostalgic antique music box melody accompanied by warm muted felt piano and faint distant train rail rhythm, bittersweet intimate mood, gentle 72 BPM waltz feel inspired by To The Moon and OMORI, delicate and emotional, no vocals, seamless loop.`

### 2. `assets/audio/bgm/bgm_06_ending_wind.mp3`
* **Fungsi:** Lagu penutup emosional saat **Epilog Stasiun Fajar** (ketika Raka membaca ponselnya, bertemu Senja di Peron 2, dan tubuhnya tertiup angin pagi) hingga daftar kredit berakhir.
* **Prompt Gemini Web:**
  > `Deeply moving acoustic piano solo slowly joined by warm solo cello, delicate acoustic guitar fingerpicking, and soft coastal morning breeze texture, bittersweet yet peaceful hopeful catharsis inspired by To The Moon and Makoto Shinkai endings, 68 BPM, emotional crescendo then gentle quiet resolution, no vocals.`

---

## Catatan untuk Aset Lama (`bg_gerbong*` & `bgm_03`)
1. **`bgm_03_courage_persona.mp3`:** Prompt barunya (*Midnight Jazz-Hop / "Beneath the Mask"*) tetap berlaku seperti di [DAFTAR_ASSET_DAN_PROMPT.md](../DAFTAR_ASSET_DAN_PROMPT.md).
2. **`cg_*.png` (25 Gambar Narasi):** Seluruh prompt-nya ada di [PROMPT_CG_NARASI.md](PROMPT_CG_NARASI.md) — dan di Python nanti, jika sebagian gambar CG belum selesai digenerate, game otomatis tetap berjalan memakai latar gerbong yang di-*blur* + efek gradasi *Wuthering Waves* sehingga kamu bisa menguji ceritanya dulu sambil melengkapi CG bertahap!
