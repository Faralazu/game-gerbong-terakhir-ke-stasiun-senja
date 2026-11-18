# PANDUAN & PROMPT CG NARASI (*Wuthering Waves* Cutscene Style)
### Dokumen prompt untuk seluruh 25 Gambar Cutscene Statis di `assets/images/cg/`

---

## 1. Gaya Visual, Komposisi, & Aturan Transisi

### A. Gaya Ilustrasi (Mengacu pada Referensi *Wuthering Waves* yang Kamu Berikan)
* **Visual:** Ilustrasi anime sinematik *painterly* beresolusi tinggi (16:9, target simpan `1920×1080` atau `1280×720`), pencahayaan *rim light* dramatis, efek *bloom* lembut, partikel debu cahaya/kelopak bunga, dan komposisi sinematik yang ekspresif.
* **PENTING untuk Legibilitas Subtitle:** Jaga **22% bagian bawah gambar tetap bersih / tidak terlalu ramai detail penting**, karena di dalam game bagian bawah layar akan diberi gradasi gelap halus dan teks dialog bergaya *Wuthering Waves* (nama pembicara berwarna emas di atas teks putih bersih, tanpa kotak dialog).
* **Larangan Prompt:** Selalu sertakan `no text, no UI, no subtitles, no watermark` agar gambar murni bersih untuk digerakkan kamera *Ken Burns* oleh Python.

### B. Jangkar Visual Karakter (*Wajib Copy-Paste Utuh agar Konsisten*)
> Gunakan deskripsi karakter persis di bawah ini di dalam prompt mana pun yang memunculkan karakter tersebut:

* **RAKA (24 thn):** `young Indonesian man, 24, warm tan skin, messy dark-brown hair with a cowlick, tired gentle dark-brown eyes, navy blue bomber jacket over white t-shirt, dark jeans, black sneakers, retro silver headphones with orange foam pads around neck, small silver cassette Walkman clipped on belt`
* **SENJA (Dewasa/Ingatan, 24 thn):** `young Indonesian woman, 24, shoulder-length dark-brown hair with a small mustard-yellow hair clip on the left side, bright warm mischievous eyes, beige long coat over a cream knit sweater, soft white knit scarf, holding a worn blue manuscript folder`
* **SENJA (Kampus/Flashback):** `young Indonesian woman, 21, shoulder-length dark-brown hair with a small mustard-yellow hair clip on the left side, mustard knit cardigan over white blouse, tote bag full of books`
* **BIMA (9 thn):** `small Indonesian boy, 9, short messy black hair, big curious dark eyes, oversized bright-yellow raincoat with hood down, dark shorts, white hospital wristband peeking from sleeve, holding a paper airplane folded from a comic page`
* **NADIA (26 thn):** `Indonesian woman, 26, round thin-framed glasses, dark hair in a messy low bun with loose strands, tired kind eyes, blue-gray oversized knit cardigan over cream blouse, office ID lanyard`
* **RAKA KECIL (8 thn):** `small Indonesian boy, 8, messy dark-brown hair with cowlick, oversized red-and-white striped t-shirt, shorts, holding a crayon and worn sketchbook`
* **KAKEK HARJO / KONDEKTUR (~70 thn):** `elderly Indonesian man, around 70, kind wrinkled face, neat white mustache, old-fashioned navy railway conductor uniform with brass buttons, peaked conductor cap, holding a warm brass lantern`

---

## 2. Daftar Lengkap 25 CG & Prompt Siap Copy-Paste

### BAGIAN A — PROLOG (Setelah Video Intro `vid_01`)
*Transisi masuk: Video intro → pudar **putih** 0,8 dtk → CG_00A → crossfade 0,7 dtk → CG_00B → crossfade 0,7 dtk → CG_00C → pudar **hitam** 0,8 dtk → Gameplay Gerbong 5 (Sketsa).*

#### 1. `assets/images/cg/cg_00a_wakeup_window.png`
* **Teks di layar (Monolog Raka, *italic*):** *"Suara relnya pelan banget... Aku ketiduran di kereta sepulang kerja lagi ya? Tapi kenapa... di luar cuma ada laut, dan semuanya pucat seperti sketsa pensil?"*
* **Prompt Generator:**
  > `Cinematic anime cutscene illustration in Wuthering Waves and Makoto Shinkai painterly style, 16:9 widescreen, interior of an empty vintage commuter train carriage rendered in desaturated monochrome pencil-sketch silver and slate tones, young Indonesian man, 24, warm tan skin, messy dark-brown hair with a cowlick, tired gentle dark-brown eyes, navy blue bomber jacket over white t-shirt, retro silver headphones with orange foam pads around neck, slowly waking up with head resting lightly against a large train window overlooking an endless pale silver ocean, soft ethereal light beams, uncluttered calm lower 25% framing for subtitles, no text, no UI, no watermark.`

#### 2. `assets/images/cg/cg_00b_ticket_hands.png`
* **Teks di layar (Monolog Raka, *italic*):** *"Di sela jari-jariku ada tiket bertuliskan pukul 23:59... dan nama stasiun tujuannya terhapus seperti terkena air."*
* **Prompt Generator:**
  > `Cinematic anime cutscene illustration in Wuthering Waves painterly style, 16:9 widescreen, dramatic close-up POV looking down at a young man's tan hands holding a crumpled vintage paper train ticket stamped with subtle clock digits 23:59 and a smudged blank destination line, muted monochrome slate carriage background slightly out of focus, soft silver light rim around the fingers, melancholic mysterious mood, clean darker lower edge, no UI, no watermark.`

#### 3. `assets/images/cg/cg_00c_walkman_bench.png`
* **Teks di layar (Monolog Raka, *italic*):** *"Di bangku seberang yang pucat, cuma satu benda ini yang masih punya warna... Walkman perak peninggalan Kakek."*
* **Prompt Generator:**
  > `Cinematic anime cutscene illustration in Wuthering Waves painterly style, 16:9 widescreen, atmospheric medium shot inside a desaturated monochrome black-and-white sketched train carriage, on an empty bench sits a retro silver cassette Walkman with orange foam headphones glowing with faint warm golden color amidst the colorless world, delicate floating dust motes catching a single warm sunbeam, dramatic contrast, clean uncluttered bottom area, no text, no UI.`

---

### BAGIAN B — KILAS BALIK MASUK GERBONG (Terpicu 1× Saat Masuk Gerbong Baru)
*Transisi masuk: Getar layar halus 0,3 dtk → pudar **hitam** 0,6 dtk → CG_FBA → crossfade 0,7 dtk → CG_FBB → pudar **hitam** 0,8 dtk → Raka memegangi kepala ("Kenapa aku ingat ini sekarang...?"). Filter: Sepia/nostalgia redup & suara `bgm_05_flashback_musicbox.mp3`.*

#### 4. `assets/images/cg/cg_fb1a_grandpa_shoulders.png` *(Masuk Gerbong 4)*
* **Teks di layar (*italic*):** *"Suara mesin kereta sore... Tiba-tiba kepalaku teringat tahun 2008. 'Lihat, Le. Kereta itu selalu tahu ke mana harus pulang.'"*
* **Prompt Generator:**
  > `Cinematic anime flashback illustration in Wuthering Waves and Makoto Shinkai painterly style, warm nostalgic golden-sepia tint, 16:9 widescreen, at a small vintage Indonesian railway crossing at sunset, an elderly Indonesian man, around 70, kind wrinkled face, neat white mustache, old-fashioned navy railway conductor uniform with brass buttons, carrying a small Indonesian boy, 8, messy dark-brown hair with cowlick, oversized red-and-white striped t-shirt, on his shoulders as they watch a classic orange-cream passenger train pass by in glowing golden dust, soft film grain, uncluttered lower foreground, no text, no UI.`

#### 5. `assets/images/cg/cg_fb1b_first_sketchbook.png` *(Masuk Gerbong 4)*
* **Teks di layar (*italic*):** *"'Kalau capek lihat jalan yang lurus terus, gambar aja pemandangan yang pengen kamu tuju, Rak.'"*
* **Prompt Generator:**
  > `Cinematic anime flashback illustration in Wuthering Waves painterly style, warm nostalgic amber-sepia memory filter, 16:9 widescreen, cozy wooden porch of an old Indonesian house at twilight, warm close shot of an elderly retired train driver's wrinkled hands gently placing a blank sketchbook and a retro silver cassette Walkman with orange foam pads onto the lap of a small 8-year-old Indonesian boy in a striped shirt smiling with gap-toothed wonder, warm lantern glow, gentle bokeh, uncluttered bottom area, no text, no UI.`

#### 6. `assets/images/cg/cg_fb2a_bus_stop_meet.png` *(Masuk Gerbong 3)*
* **Teks di layar (Senja, *emas*):** *"'Keretamu kelihatan kayak lagi kangen sesuatu. Aku Senja. Kamu yang gambar, aku yang nulis ceritanya, mau nggak?'"*
* **Prompt Generator:**
  > `Cinematic anime flashback illustration in Wuthering Waves painterly style, soft rainy twilight nostalgia palette, 16:9 widescreen, quiet university bus stop shelter during gentle late-afternoon rain, a young Indonesian man, 21, messy dark-brown hair, navy jacket, sitting holding an open sketchbook of trains, looking up in surprise at a young Indonesian woman, 21, shoulder-length dark-brown hair with a small mustard-yellow hair clip on the left side, mustard knit cardigan over white blouse, tote bag full of books, leaning forward curiously with a bright playful smile while rain sparkles outside, clean lower pavement margin, no text, no UI.`

#### 7. `assets/images/cg/cg_fb2b_rooftop_drawing.png` *(Masuk Gerbong 3)*
* **Teks di layar (*italic*):** *"Atap kampus, dua gelas es teh, dan komik kecil bernama TRACK 99. Kenapa... dada rasanya sesak sekali waktu ingat sore itu?"*
* **Prompt Generator:**
  > `Cinematic anime flashback illustration in Wuthering Waves painterly style, vibrant golden-hour campus rooftop, 16:9 widescreen, two Indonesian college friends sitting cross-legged on a concrete university rooftop overlooking a warm glowing city skyline at sunset: a young man, 21, in navy jacket sketching intently on paper sheets scattered around, next to a young woman, 21, shoulder-length hair with mustard-yellow hair clip, mustard cardigan, laughing while holding up four colorful cassette tapes and notebook manuscripts, warm wind blowing loose sketch pages, clean lower rooftop floor for subtitles, no text, no UI.`

#### 8. `assets/images/cg/cg_fb3a_rain_torn_sketch.png` *(Masuk Gerbong 2)*
* **Teks di layar (*italic*):** *"Malam hujan setelah penolakan ketiga... Aku merobek buku gambarku sendiri di depan kamar kos, berharap semuanya tidak pernah kumulai."*
* **Prompt Generator:**
  > `Cinematic anime flashback illustration in Wuthering Waves painterly style, moody cold blue-indigo stormy night, 16:9 widescreen, wet narrow alley under heavy pouring rain lit by one dim streetlamp, young Indonesian man, 23, warm tan skin, messy soaked dark-brown hair, navy blue bomber jacket, on his knees looking down with heartbreak as torn sketchbook pages and crumpled publisher rejection letters float in dark rain puddles reflecting neon streetlight, intense emotion, clean dark wet asphalt in bottom 25%, no text, no UI.`

#### 9. `assets/images/cg/cg_fb3b_umbrella_turnaway.png` *(Masuk Gerbong 2)*
* **Teks di layar (*italic*):** *"Senja datang membawakan payung... dan aku justru menoleh pergi. 'Udah, Ja. Mimpi kita ketinggian.'"*
* **Prompt Generator:**
  > `Cinematic anime flashback illustration in Wuthering Waves painterly style, emotional rainy night composition, 16:9 widescreen, young Indonesian woman, 23, shoulder-length hair with mustard-yellow hair clip, beige coat, holding a clear wet umbrella over a young Indonesian man, 23, messy wet dark-brown hair, navy bomber jacket, who turns his back and looks away coldly in self-loathing while rain streams down the clear umbrella, soft tragic rim light, uncluttered dark lower ground, no text, no UI.`

#### 10. `assets/images/cg/cg_fb4a_office_last_text.png` *(Masuk Gerbong 1)*
* **Teks di layar (*italic*):** *"Pukul 23:41. Aku mengetik 'Aku dateng, Ja', lalu menghapusnya lagi... dan langsung berlari mengejar kereta terakhir."*
* **Prompt Generator:**
  > `Cinematic anime flashback illustration in Wuthering Waves painterly style, sterile late-night office lighting vs warm phone screen, 16:9 widescreen, over-the-shoulder shot of an exhausted young Indonesian man, 24, messy dark hair, navy bomber jacket, sitting alone in a dark empty design agency office bathed in pale monitor blue light at 23:41, looking down at a cracked smartphone screen glowing warmly in his hands with an unsent message draft, coffee cups and messy desk, uncluttered bottom space, no readable text, no UI.`

#### 11. `assets/images/cg/cg_fb4b_last_train_2359.png` *(Masuk Gerbong 1)*
* **Teks di layar (*italic*):** *"Aku memejamkan mata sebentar di kereta malam itu... tepat saat jam peron di luar menunjukkan pukul 23:59."*
* **Prompt Generator:**
  > `Cinematic anime flashback illustration in Wuthering Waves painterly style, quiet midnight commuter train interior, 16:9 widescreen, young Indonesian man, 24, warm tan skin, messy dark-brown hair, navy blue bomber jacket, wearing retro silver headphones with orange foam pads over his ears, sitting slouched in the left corner seat of an empty late-night city train with eyes gently closed in deep exhaustion, outside the dark window blurs a glowing distant station platform clock at midnight, peaceful melancholic silence, clean lower floor area, no UI, no watermark.`

---

### BAGIAN C — MOMEN BERSAMA & PERPISAHAN PENUMPANG (Setelah Waveform Tuner)
*Transisi masuk: All-Out Resonance → pudar **putih** 1,0 dtk → CG_A → crossfade putih 0,9 dtk → CG_B → pudar **putih** 1,2 dtk → kembali ke gerbong (kursi kosong + potongan tiket).*

#### 12. `assets/images/cg/cg_bima_a_paper_plane_window.png` *(Gerbong 4 — Bima)*
* **Teks di layar (Raka):** *"Ayo, Bim. Biar kita berdua lihat seberapa jauh pesawat kertas ini bisa terbang di atas laut senja."*
* **Prompt Generator:**
  > `Cinematic anime cutscene illustration in Wuthering Waves and Makoto Shinkai luminous painterly style, 16:9 widescreen, dynamic warm golden-hour perspective inside a vintage train carriage with an open side window, young Indonesian man, 24, navy blue bomber jacket, silver headphones around neck, kneeling warmly behind a small Indonesian boy, 9, oversized bright-yellow raincoat, white hospital wristband peeking from sleeve, guiding the boy's hand to launch a paper airplane made from a comic page straight out over a vast sparkling amber sunset ocean, sunlit dust motes and wind blowing hair, clean lower foreground, no text, no UI.`

#### 13. `assets/images/cg/cg_bima_b_thank_you_fade.png` *(Gerbong 4 — Bima)*
* **Teks di layar (Bima, *emas*):** **"Terima kasih, Mas Raka!"** *(Di sayap pesawat yang menjauh tertulis samar pesan untuk Mas Dimas, dan Bima tersenyum sebelum larut menjadi cahaya hangat.)*
* **Prompt Generator:**
  > `Cinematic anime farewell illustration in Wuthering Waves painterly style with soft luminous bloom, 16:9 widescreen, emotional medium shot by a sunlit train window overlooking golden ocean clouds, small Indonesian boy, 9, messy black hair, oversized bright-yellow raincoat, turning back toward the viewer with a radiant joyful smile and waving goodbye as his edges gently dissolve into glowing golden light motes and sparkling dust drifting toward the sunset window, paper airplane soaring far in the bright sky behind him, uncluttered bottom margin, no text, no UI.`

#### 14. `assets/images/cg/cg_nadia_a_paper_house_model.png` *(Gerbong 3 — Nadia)*
* **Teks di layar (Nadia, *emas*):** *"'Bu... maaf kemarin malam aku kasar. Rumah tepi lautnya udah jadi ya, Bu. Tungguin aku pulang.'"*
* **Prompt Generator:**
  > `Cinematic anime cutscene illustration in Wuthering Waves painterly style, cozy late-night warm lamp vs cool rain window contrast, 16:9 widescreen, intimate shot across a small train folding table bathed in warm amber table-lamp glow while blue rain streaks down the window behind, Indonesian woman, 26, round thin-framed glasses, messy low bun, blue-gray cardigan, and young Indonesian man, 24, navy bomber jacket, sitting together carefully finishing a delicate miniature paper architectural model of a cozy seaside wooden house beside two steaming tea cups, peaceful relieved expressions, clean bottom table/shadow edge, no text, no UI.`

#### 15. `assets/images/cg/cg_nadia_b_thank_you_fade.png` *(Gerbong 3 — Nadia)*
* **Teks di layar (Nadia, *emas*):** **"Terima kasih, Raka. Kamu juga... jangan bilang 'nanti' lagi, ya."**
* **Prompt Generator:**
  > `Cinematic anime farewell illustration in Wuthering Waves painterly style, soft cyan and warm golden light bloom, 16:9 widescreen, Indonesian woman, 26, round thin-framed glasses, messy low bun, blue-gray knit cardigan, sitting peacefully beside a miniature paper house on a train table, smiling warmly with gentle tears of relief as her silhouette gracefully dissolves into soft serene sky-blue light ribbons and glowing particles drifting upward, soft rain clearing outside the window, uncluttered lower area, no text, no UI.`

#### 16. `assets/images/cg/cg_bayangan_a_drawing_together.png` *(Gerbong 2 — Raka Kecil)*
* **Teks di layar (Raka Kecil, *emas*):** *"'Lihat deh, Kak. Halaman yang robek disambung pakai garis emas malah kelihatan lebih bagus, ya?'"*
* **Prompt Generator:**
  > `Cinematic anime cutscene illustration in Wuthering Waves painterly style, magical warm golden light inside a quiet train carriage after rain, 16:9 widescreen, young Indonesian man, 24, warm tan skin, navy blue bomber jacket, silver headphones around neck, sitting cross-legged on the wooden train floor beside a small 8-year-old version of himself, messy hair with cowlick, oversized red-and-white striped t-shirt, holding a crayon, both leaning happily over an open sketchbook whose torn pages are mended with glowing golden Kintsugi seams as they draw a train together, clean lower floor edge, no text, no UI.`

#### 17. `assets/images/cg/cg_bayangan_b_hug_fade.png` *(Gerbong 2 — Raka Kecil)*
* **Teks di layar (Raka Kecil, *emas*):** **"Terima kasih udah inget aku lagi, Raka."**
* **Prompt Generator:**
  > `Cinematic anime emotional embrace illustration in Wuthering Waves painterly style, luminous warm gold bloom, 16:9 widescreen, young Indonesian man, 24, navy bomber jacket, kneeling with eyes gently closed as he hugs his 8-year-old child self in a red-and-white striped t-shirt, the child dissolving peacefully into warm swirling ribbons of golden ink and starlight melting right into Raka's chest while rain clears to soft blue dawn light outside the train windows, uncluttered bottom space, no text, no UI.`

#### 18. `assets/images/cg/cg_senja_a_cockpit_sunrise.png` *(Gerbong 1 — Senja)*
* **Teks di layar (Senja, *emas*):** *"'Lihat ke depan, Rak. Kereta nggak pernah bisa jalan mundur—tapi pemandangan di depan nggak kalah indah kok.'"*
* **Prompt Generator:**
  > `Cinematic anime cutscene illustration in Wuthering Waves and Makoto Shinkai breathtaking painterly style, 16:9 widescreen, wide view from inside a vintage train driver cockpit looking out the large front windshield at early golden sunrise over a vast calm turquoise ocean with glowing pastel clouds, young Indonesian man, 24, navy bomber jacket, headphones around neck, resting his hand gently on a brass brake lever beside a young Indonesian woman, 24, shoulder-length hair with mustard-yellow hair clip, beige long coat, soft white knit scarf, looking serenely toward the sunrise with a warm nostalgic smile, clean lower console silhouette, no text, no UI.`

#### 19. `assets/images/cg/cg_senja_b_thank_you_fade.png` *(Gerbong 1 — Senja)*
* **Teks di layar (Senja, *emas*):** **"Terima kasih, Raka. Sekarang giliran kamu yang pulang."**
* **Prompt Generator:**
  > `Cinematic anime farewell illustration in Wuthering Waves painterly style, radiant golden dawn bloom, 16:9 widescreen, inside a sunlit train cockpit bathed in bright morning sunbeams, young Indonesian woman, 24, shoulder-length dark-brown hair with mustard-yellow hair clip, beige coat, white knit scarf, holding out a worn blue manuscript folder with a tender tearful smile as golden morning light and soft petals dissolve her figure gently into shimmering dawn rays, dramatic lens flare, uncluttered bottom margin, no text, no UI.`

---

### BAGIAN D — ENDING: STASIUN FAJAR & KEBENARAN (Twist Terungkap)
*Transisi: Video `vid_05_ending_dawn_station.mp4` → pudar putih → CG_END_01 → crossfade lambat 1,2 dtk antar-CG → pudar putih panjang menuju kredit.*

#### 20. `assets/images/cg/cg_end_01_grandpa_conductor.png`
* **Teks di layar (Kakek Harjo, *emas*):** **"Waktunya turun, Le."**
* **Prompt Generator:**
  > `Cinematic anime illustration in Wuthering Waves painterly style, 16:9 widescreen, standing beside the open sliding door of a vintage train at a serene seaside dawn platform, an elderly Indonesian man, around 70, kind wrinkled face, neat white mustache, navy railway conductor uniform with brass buttons, removing his peaked conductor cap and holding it to his chest while smiling with deep grandfatherly warmth, holding a glowing brass lantern and a star-punched train ticket, warm sunrise glow behind him, uncluttered lower steps, no text, no UI.`

#### 21. `assets/images/cg/cg_end_02_translucent_hand_phone.png` *(TWIST TERUNGKAP)*
* **Teks di layar (*italic*):** *"Kelopak bunga menembus telapak tanganku... dan layar ponsel akhirnya menyala: setahun sudah berlalu sejak malam 23:59 itu. '...Oh. Jadi begitu.'"*
* **Prompt Generator:**
  > `Cinematic anime emotional twist illustration in Wuthering Waves painterly style, 16:9 widescreen, close-up over-the-shoulder shot on a misty seaside dawn train platform, a young Indonesian man's translucent glowing hand held out in shock as a pale pink cherry-blossom petal passes cleanly straight through his semi-transparent palm, while his other hand holds a cracked smartphone glowing softly with unread notifications, ethereal morning sunlight piercing through his fading silhouette, clean darker stone platform at bottom, no readable text, no UI.`

#### 22. `assets/images/cg/cg_end_03_senja_bench_comic.png`
* **Teks di layar (Raka, *italic*):** *"Peron 2 Stasiun Kotabaru, pukul enam pagi. 'Maaf aku telat, Ja. Terima kasih sudah nungguin aku.'"*
* **Prompt Generator:**
  > `Cinematic anime illustration in Wuthering Waves and Makoto Shinkai style, 16:9 widescreen, quiet realistic Japanese/Indonesian coastal commuter station platform at 06:00 AM bright dawn, a young Indonesian woman, 24, shoulder-length dark-brown hair with mustard-yellow hair clip, beige long coat, white knit scarf, sitting alone on a wooden platform bench cradling a printed comic book and a silver cassette Walkman on her lap; just behind the bench stands the semi-translucent glowing figure of a young Indonesian man, 24, navy bomber jacket, looking down at her with a peaceful gentle smile, morning sea breeze, clean lower platform bricks, no text, no UI.`

#### 23. `assets/images/cg/cg_end_04_raka_dissolve_wind.png` *(Klimaks Emosional)*
* **Teks di layar (Senja, *emas*):** *"...Kamu dateng juga ya, Rak."*
* **Prompt Generator:**
  > `Cinematic anime climactic farewell illustration in Wuthering Waves painterly style, luminous golden morning sunlight and swirling wind ribbons, 16:9 widescreen, low wide angle on a seaside train station platform at sunrise: the translucent figure of young Indonesian man, 24, in navy bomber jacket and headphones gracefully dissolving from his fingertips and shoulders into thousands of radiant golden light motes and pink petals carried away by the morning wind, while the wind lifts the white knit scarf of the young Indonesian woman, 24, looking up toward the warm morning sky with teary eyes and a deeply peaceful relieved smile, clean lower frame, no text, no UI.`

#### 24. `assets/images/cg/cg_end_05_comic_dedication.png`
* **Teks di layar (*italic*):** *"Untuk Raka — gambarmu selalu sampai."*
* **Prompt Generator:**
  > `Cinematic anime epilogue still-life illustration in Wuthering Waves painterly style, 16:9 widescreen, warm morning sunlight falling diagonally across an open printed comic book resting on a wooden station bench beside a retro silver cassette Walkman, showing an intricate hand-drawn ink illustration of a commuter train gliding over the ocean, with a single fresh pale blossom petal resting gently on the open page, soft shallow depth of field, cozy peaceful resolution, clean darker wooden bench bottom edge, no text, no UI.`

#### 25. `assets/images/cg/cg_end_06_empty_train_horizon.png` *(Pasca-Kredit — Opsional)*
* **Teks di layar (*tanpa teks panjang, hanya judul penutup*):** *TRACK 99 akan terus melaju—menemani jiwa yang sedang belajar pulang.*
* **Prompt Generator:**
  > `Cinematic anime post-credit illustration in Makoto Shinkai and Wuthering Waves painterly style, 16:9 widescreen, wide panoramic aerial view of an empty vintage commuter train gliding serenely across railway tracks submerged in a calm bright morning sea toward a luminous pastel horizon, gentle water ripples reflecting pink and turquoise morning sky, deeply tranquil and hopeful atmosphere, uncluttered bottom ocean area, no text, no UI.`
