# Daftar Lengkap Asset & Prompt Generator
## **Gerbong Terakhir ke Stasiun Senja (*Track 99: Resonance*)**

Dokumen ini adalah panduan produksi aset lengkap agar visual, video latar, dan musik game konsisten.
Setiap aset sudah diberi **nama file target yang wajib digunakan** agar nanti langsung terbaca otomatis oleh kode Python kita.

> **Tips Konsistensi Gaya Pixel Art:**
> Semua aset gambar dan video mengusung gaya **High-Detail 16-bit / 32-bit Modern Anime Pixel Art** (mirip *A Space for the Unbound* & *Eastward*), pencahayaan atmosferik ala Makoto Shinkai, dan aksen UI geometris tajam ala *Persona*.

---

## BAGIAN 1: Video Google Flow (Maksimal 15 Detik, `.mp4`, Rasio 16:9)
*Bagian ini dikerjakan oleh **Kamu di Google Flow**. Catatan: Pastikan tidak ada teks atau watermark di video, dan untuk loop pemandangan jendela usahakan kamera bergerak horizontal mulus (side-scrolling).*

### 1. `assets/videos/vid_01_intro_sea_train.mp4`
* **Fungsi:** Video pembuka (Cutscene Intro) saat game baru dimulai.
* **Durasi ideal:** 10–15 detik.
* **Prompt Google Flow (Copy-Paste):**
  > `High-detail 2D pixel art anime animation, wide establishing shot of a vintage Japanese commuter train gliding smoothly across railway tracks submerged in shallow glowing ocean water at golden sunset, warm amber and coral sky reflections on gentle water ripples, distant silhouette of a coastal city, Makoto Shinkai lighting aesthetic, cozy nostalgic atmosphere, smooth cinematic camera glide, 16-bit modern indie game cutscene style like A Space for the Unbound, no text, no UI.`

### 2. `assets/videos/vid_02_window_sunset_loop.mp4`
* **Fungsi:** Video *looping* pemandangan di balik kaca jendela gerbong saat memutar **Kaset A (SENJA / Nostalgia)**.
* **Durasi ideal:** 8–15 detik (seamless side-scrolling).
* **Prompt Google Flow (Copy-Paste):**
  > `2D pixel art side-scrolling background animation seen directly through a train window, continuous smooth horizontal parallax motion from right to left, glowing golden hour sunset sky over a calm sparkling sea, silhouette of utility poles and power lines rhythmically passing by in the foreground, fluffy orange and pink clouds drifting slowly, warm nostalgic atmosphere, Eastward and A Space for the Unbound pixel art style, seamless loop, flat 2D side view, no train interior frame, no text.`

### 3. `assets/videos/vid_03_window_neon_rain_loop.mp4`
* **Fungsi:** Video *looping* pemandangan di balik kaca jendela gerbong saat memutar **Kaset B (HUJAN / Penyangkalan)**.
* **Durasi ideal:** 8–15 detik (seamless side-scrolling).
* **Prompt Google Flow (Copy-Paste):**
  > `2D pixel art side-scrolling background animation seen from a moving train, continuous smooth horizontal motion from right to left, moody rainy night cityscape with blurred neon blue and violet lights reflecting on wet streets, diagonal rain streaks falling outside, distant glowing apartment windows passing by, melancholic lo-fi atmosphere, high-detail modern pixel art, seamless loop, flat 2D side view, no train interior, no text.`

### 4. `assets/videos/vid_04_mind_dive_transition.mp4`
* **Fungsi:** Video transisi dramatis (5–8 detik) saat pemain berhasil menyelaraskan *Waveform Tuner* dan masuk ke memori terdalam penumpang (*Space Dive* ala *A Space for the Unbound* + gaya geometris *Persona*).
* **Durasi ideal:** 5–8 detik.
* **Prompt Google Flow (Copy-Paste):**
  > `Stylish 2D anime pixel art transition animation, a glowing retro cassette tape spinning rapidly in the center and bursting into swirling crimson red, gold, and black geometric star polygons and light ribbons, zooming forward through a surreal memory tunnel filled with floating golden clock hands and shattered photo frames, Persona 5 inspired dynamic motion graphics blended with pixel art, dramatic energy, no text.`

### 5. `assets/videos/vid_05_ending_dawn_station.mp4`
* **Fungsi:** Video penutup (*Ending Cutscene*) saat kereta berhenti di Stasiun Senja/Fajar dan pintu kereta terbuka.
* **Durasi ideal:** 12–15 detik.
* **Prompt Google Flow (Copy-Paste):**
  > `High-detail 2D pixel art anime animation, interior point-of-view looking out through sliding train doors that slowly open onto a serene seaside train station platform at early dawn, soft warm morning sunlight and sea breeze blowing pale sakura petals across the platform, calm turquoise ocean and pastel sky in the background, deeply peaceful and emotional finale atmosphere like To The Moon and Makoto Shinkai films, gentle camera drift, no text.`

### 6. `assets/videos/vid_06_window_courage_loop.mp4` *(Baru — Untuk Kaset C: DETAK)*
* **Fungsi:** Video *looping* pemandangan luar jendela gerbong saat memutar **Kaset C (DETAK / Keberanian)** bergaya *Persona 5* yang penuh energi.
* **Durasi ideal:** 8–15 detik (seamless side-scrolling).
* **Prompt Google Flow (Copy-Paste):**
  > `2D pixel art side-scrolling background animation seen through a moving train window, continuous fast horizontal motion from right to left, stylized Persona 5 inspired surreal metropolis at night with bold crimson red, gold, and obsidian black geometric skyscrapers, dynamic diagonal speed lines and floating glowing star shards passing by, energetic rebellious atmosphere, crisp modern 16-bit pixel art, seamless loop, flat 2D side view, no train interior frame, no text.`

### 7. `assets/videos/vid_07_window_dawn_loop.mp4` *(Baru — Untuk Kaset D: FAJAR)*
* **Fungsi:** Video *looping* pemandangan luar jendela gerbong saat memutar **Kaset D (FAJAR / Keikhlasan)** menuju matahari terbit yang teduh.
* **Durasi ideal:** 8–15 detik (seamless side-scrolling).
* **Prompt Google Flow (Copy-Paste):**
  > `2D pixel art side-scrolling background animation seen through a moving train window, continuous gentle horizontal motion from right to left, serene early morning sunrise over a calm turquoise and pastel gold ocean, soft morning sunbeams breaking through pale pink clouds, delicate sakura petals drifting in the breeze, peaceful cathartic finale atmosphere like Makoto Shinkai and A Space for the Unbound, seamless loop, flat 2D side view, no train interior frame, no text.`

---

## Status Aset Saat Ini *(Checklist Otomatis Terbaca Engine)*
* **Sudah Lengkap & Aktif:**
  * Video: `vid_01_intro_sea_train.mp4`, `vid_02_window_sunset_loop.mp4`, `vid_03_window_neon_rain_loop.mp4`, `vid_04_mind_dive_transition.mp4`, `vid_05_ending_dawn_station.mp4`
  * BGM Audio: `bgm_00_sketch_rails.mp3` s.d. `bgm_04_acceptance_finale.mp3`
  * Background Gerbong & Stasiun: `bg_carriage_sketch.jpeg`, `bg_carriage_sunset.jpeg`, `bg_carriage_rain.jpeg`, `bg_carriage_courage.jpeg`, `bg_station_dawn.png`
  * Sprite & UI: `Raka_idle.jpeg`, `Raka_walk.jpeg`, `Raka_sit1..3.jpeg`, `spr_props_items.jpeg`, `ui_walkman_cassette.jpeg`, `spr_npc_passengers.png`
  * Potret: `preview_raka_cutin.png`, `passengers_portraits.png`, `port_raka_expressions.png`
* **Opsional / Dapat Ditambahkan Kapan Saja (Lalu Tekan `F5`):**
  * Video Kaset C & D (`vid_06_window_courage_loop.mp4`, `vid_07_window_dawn_loop.mp4`) — sebelum dibuat, game otomatis memakai `vid_02` + filter atmosferik Persona merah / Fajar pastel.
  * SFX pendek (`sfx_cassette_click.wav`, `sfx_ui_whoosh.wav`, `sfx_resonance_chime.wav`) — saat ini dibuat otomatis secara prosedural dengan Python.

---

## BAGIAN 2: Musik & BGM Gemini Web / Lyria (`.mp3` atau `.wav`)
*Bagian ini dikerjakan oleh **Kamu di Gemini Web (Music Generation)**. Setelah selesai di-download, ubah namanya sesuai path di bawah ini.*

### 1. `assets/audio/bgm/bgm_00_sketch_rails.mp3`
* **Fungsi:** Suasana awal gerbong sketsa hitam-putih sebelum Walkman dinyalakan (Menit 0–2).
* **Prompt Gemini Web:**
  > `Minimalist ambient soundscape featuring the rhythmic gentle clack-clack of a slow commuter train on old railway tracks, subtle warm vinyl record crackle, distant muffled wind, and one sparse echoing felt piano chord every few bars. Quiet, lonely, contemplative, loopable.`

### 2. `assets/audio/bgm/bgm_01_nostalgia_sunset.mp3`
* **Fungsi:** Musik **Kaset A (SENJA / Nostalgia)** — Lagu utama yang membuat pemain rileks sepulang kuliah/kerja.
* **Prompt Gemini Web:**
  > `Warm nostalgic Japanese City Pop meets cozy Lo-Fi Hip Hop instrumental, smooth Fender Rhodes electric piano chords, mellow melodic bassline, soft brushed lo-fi drum groove at 82 BPM, warm analog tape saturation, shimmering sunset synth pad. Deeply relaxing, comforting, and emotional after a long day, no vocals, seamless loop.`

### 3. `assets/audio/bgm/bgm_02_denial_rain.mp3`
* **Fungsi:** Musik **Kaset B (HUJAN / Penyangkalan)** — Suasana introspektif saat malam hujan.
* **Prompt Gemini Web:**
  > `Melancholic ambient synthwave and soft lo-fi piano instrumental at 74 BPM, delicate emotional upright piano melody, gentle rain texture in the background, warm muted cello pad, bittersweet and introspective mood inspired by OMORI and To The Moon, no vocals, loopable.`

### 4. `assets/audio/bgm/bgm_03_courage_persona.mp3`
* **Fungsi:** Musik **Kaset C (DETAK / Keberanian)** — Tetap hangat, lembut, dan sinkron dengan ketiga kaset lainnya (vibe *Persona 5 "Beneath the Mask"* di malam hujan/kafe, bukan musik keras yang mengagetkan).
* **Prompt Gemini Web (Diperbarui agar selaras):**
  > `Warm comforting Japanese Jazz-Hop and Neo-Soul Lo-Fi instrumental inspired by Persona 5 "Beneath the Mask" instrumental, gentle 84 BPM groove, velvet Fender Rhodes electric piano chords, warm mellow upright bassline, soft brushed snare drum, soulful muted acoustic guitar and gentle warm saxophone melody. Cozy, calm, quietly determined, soothing to listen to after work or study, no harsh brass, no jarring drops, no vocals, seamless loop.`

### 5. `assets/audio/bgm/bgm_04_acceptance_finale.mp3`
* **Fungsi:** Musik **Kaset D (FAJAR / Keikhlasan)** — Klimaks menyentuh hati di Gerbong 1 hingga Stasiun Fajar.
* **Prompt Gemini Web:**
  > `Emotional cinematic anime soundtrack instrumental inspired by To The Moon and Makoto Shinkai films, starts with an intimate delicate solo piano, slowly swells with warm string quartet, acoustic guitar arpeggios, and gentle uplifting percussion into a heartfelt hopeful crescendo. Moving, cathartic, peaceful resolution, no vocals.`

### *(Opsional)* Efek Suara Tambahan (`assets/audio/sfx/`)
Untuk SFX pendek seperti suara tombol Walkman *CLACK*, bunyi *statis radio*, dan *UI swoosh*, bisa dibuat secara prosedural langsung lewat script Python atau dicari dari SFX bebas royalti (*freesound.org*) lalu disimpan sebagai:
* `assets/audio/sfx/sfx_cassette_click.wav`
* `assets/audio/sfx/sfx_ui_whoosh.wav`
* `assets/audio/sfx/sfx_resonance_chime.wav`

---

## BAGIAN 3: Gambar Pixel Art (`.png`)
*Kabar baik: Daftar gambar di bawah ini **bisa langsung saya generate dari sini** secara bertahap, ATAU kalau kamu ingin ikut eksperimen di Gemini Web, kamu juga bisa pakai prompt di bawah ini!*

### A. Background Interior Gerbong Kereta (1280×720 atau 16:9, Flat Side-View)
> **Penting:** Bagian kaca jendela pada gambar interior nanti akan dibuat **transparan oleh script Python** (atau diedit alpha-nya) agar video dari Google Flow di Bagian 1 terlihat bergerak di luarnya!

1. `assets/images/backgrounds/bg_carriage_sketch.png`
   * **Prompt:** `2D pixel art game background, flat side-view cross-section interior of an empty vintage commuter train carriage, drawn purely in monochrome black and white ink sketch lines on paper texture, clean large rectangular train windows filled with solid bright green #00FF00 chroma key color, wooden floor planks, hanging hand straps, side bench seats, no characters, no perspective distortion, indie game asset.`
2. `assets/images/backgrounds/bg_carriage_sunset.png`
   * **Prompt:** `2D pixel art game background, flat side-view cross-section interior of a cozy vintage Japanese commuter train carriage, warm golden sunset lighting casting long soft shadows on polished wooden floor and plush velvet bench seats, overhead luggage racks, hanging commuter hand straps, clean large rectangular train windows filled with solid flat bright green #00FF00 chroma key for background replacement, A Space for the Unbound and Eastward pixel art style, no characters, crisp pixels.`
3. `assets/images/backgrounds/bg_carriage_rain.png`
   * **Prompt:** `2D pixel art game background, flat side-view cross-section interior of a vintage commuter train carriage at night, moody cool cyan-blue and soft violet ambient interior lighting, subtle glowing overhead fluorescent strip lights, wet umbrella leaning near the door, clean large rectangular train windows filled with solid flat bright green #00FF00 chroma key, detailed modern 2D indie game pixel art, no characters.`
4. `assets/images/backgrounds/bg_carriage_courage.png`
   * **Prompt:** `2D pixel art game background, flat side-view cross-section interior of a stylized commuter train carriage inspired by Persona 5 aesthetic, dramatic crimson red, obsidian black, and stark gold high-contrast lighting, bold geometric shadow patterns across the floor and seats, glowing red emergency brake lever at the front, clean large rectangular train windows filled with solid flat bright green #00FF00 chroma key, crisp 2D pixel art, no characters.`

### B. Sprite Karakter & Objek Interaktif (Background Polos/Transparan)
1. `assets/images/sprites/spr_raka_sheet.png` (Protagonis — Pemuda berjaket hoodie santai dengan headphone di leher)
   * **Prompt:** `2D pixel art character sprite sheet for a side-scrolling indie game, young Indonesian/Asian man named Raka wearing a relaxed oversized navy jacket, white t-shirt, dark jeans, and retro silver headphones around his neck, 4 poses side-by-side in a clean row: standing idle facing right, walking step 1, walking step 2, and sitting calmly looking at window. Consistent proportions, 64x64 pixel art style like Eastward, isolated on solid flat magenta #FF00FF background, no overlap.`
2. `assets/images/sprites/spr_npc_child.png` (Penumpang Gerbong 4 — Anak kecil dengan mainan pesawat rusak)
   * **Prompt:** `2D pixel art character sprite, side-view of a young child wearing a yellow raincoat and shorts sitting on a train bench holding a broken paper/wooden toy airplane, looking sad yet curious, 64x64 pixel art style matching A Space for the Unbound, isolated on solid flat magenta #FF00FF background.`
3. `assets/images/sprites/spr_npc_student.png` (Penumpang Gerbong 3/2 — Mahasiswi/pekerja kelelahan dengan tas dan buku catatan)
   * **Prompt:** `2D pixel art character sprite, side-view of a tired young woman in casual college cardigan sitting slightly slumped with a tote bag, laptop sleeve, and floating faint dark clock icons around her, 64x64 pixel art style matching A Space for the Unbound, isolated on solid flat magenta #FF00FF background.`
4. `assets/images/sprites/spr_npc_memory.png` (Penumpang Gerbong 1 — Sosok kenangan masa lalu yang bercahaya lembut)
   * **Prompt:** `2D pixel art character sprite, side-view of a serene young woman/friend standing near the front train door wearing a light scarf, edges subtly dissolving into warm golden starlight pixels, gentle smile, 64x64 pixel art style, isolated on solid flat magenta #FF00FF background.`
5. `assets/images/sprites/spr_props_items.png` (Kumpulan objek interaktif: Walkman di kursi, cangkir kopi hangat, tiket kereta Track 99, jam saku retak)
   * **Prompt:** `2D pixel art game prop icon set arranged neatly in a 2x2 grid with wide spacing: 1) retro silver cassette Walkman with orange foam headphones, 2) steaming ceramic cup of warm tea, 3) vintage paper train ticket stamped 99, 4) glowing cracked pocket watch. Crisp 32x32 pixel art style, isolated on solid flat magenta #FF00FF background.`

### C. Potret Dialog & Cut-In Ala *Persona* (High-Detail Pixel Portrait)
1. `assets/images/portraits/port_raka_expressions.png` (4 ekspresi Raka: Tenang, Terkejut, Sedih/Terharu, Tersenyum Lega)
   * **Prompt:** `2D anime pixel art character bust portrait grid (2x2), close-up of Raka, a young man with slightly messy dark hair and retro silver headphones around his neck, expressive anime eyes, showing 4 expressions: calm tired, surprised, deeply moved/teary, and gentle relieved smile. Dynamic shading with warm sunset rim light, sharp Persona-style silhouette, isolated on solid dark navy background.`
2. `assets/images/portraits/cutin_raka_persona.png` (Cut-in mata menyala ala *Persona* saat *All-Out Resonance* / ganti kaset penting)
   * **Prompt:** `Persona 5 inspired horizontal diagonal eye cut-in banner rendered in crisp high-detail anime pixel art, dramatic close-up of a young man's determined glowing amber eye reflecting a sunset train track, surrounded by sharp crimson, gold, and black angular graphic shards and speed lines, ultra-stylish 2D game UI art, wide 16:4 banner composition.`
3. `assets/images/portraits/port_passengers.png` (Potret ekspresi untuk Anak Kecil, Mahasiswi/Pekerja, dan Sosok Kenangan)
   * **Prompt:** `2D anime pixel art character bust portraits side by side (3 portraits): 1) innocent child in yellow hoodie with curious eyes, 2) exhausted college woman with glasses and messy bun, 3) warm nostalgic friend with soft golden backlighting and gentle eyes. High-detail expressive anime pixel art, isolated on solid dark navy background.`

### D. UI Walkman & 4 Kaset Fisik (Untuk Overlay Interaktif)
1. `assets/images/ui/ui_walkman_cassette.png` (Ilustrasi Walkman & 4 kaset berwarna berbeda)
   * **Prompt:** `2D pixel art UI asset set on solid dark background, top-down front view of a stylish retro metallic silver portable cassette player (Walkman) with transparent tape window and glowing red LED indicator, next to 4 distinct colorful retro cassette tapes: glowing sunset orange tape labeled A, rainy neon blue tape labeled B, Persona crimson-black striped tape labeled C, and radiant pastel mint-gold tape labeled D. Crisp clean pixel art, no overlapping.`

---

## Ringkasan Pembagian Kerja (Supaya Cepat Jadi!)
1. **Tugas Kamu (di Google Flow & Gemini Web):**
   * Mulai dengan 2 file dulu biar bisa langsung kita tes di prototipe Menit Pertama:
     1. Video `vid_02_window_sunset_loop.mp4` (Google Flow)
     2. Musik `bgm_01_nostalgia_sunset.mp3` (Gemini Web)
   * Sisanya menyusul bertahap sambil kita ngoding!
2. **Tugas Saya (di sini):**
   * Langsung membuatkan *preview* aset Pixel Art awal (sekarang sedang diproses!).
   * Setelah kamu oke dengan arah visualnya, kita langsung coding **Prototipe Menit Pertama** dalam Python (`pygame-ce` + `opencv-python`) sehingga kamu bisa langsung jalan-jalan di gerbong sketsa, menekan tombol Walkman, dan melihat efek WOW-nya langsung di layar!
