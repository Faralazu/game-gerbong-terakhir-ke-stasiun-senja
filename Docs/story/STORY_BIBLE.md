# STORY BIBLE — *Gerbong Terakhir ke Stasiun Senja*
### Dokumen acuan final: alur, karakter, petunjuk tersembunyi, cutscene, dan pacing

> [!IMPORTANT]
> Dokumen ini adalah **sumber kebenaran (source of truth)** untuk cerita game. Naskah prosa lengkapnya ada di [NOVEL_TRACK99.md](NOVEL_TRACK99.md), prompt gambar cutscene ada di [PROMPT_CG_NARASI.md](PROMPT_CG_NARASI.md), dan prompt aset tambahan ada di [PROMPT_ASET_TAMBAHAN.md](PROMPT_ASET_TAMBAHAN.md).
> Naskah lama di `src/core/narrative_script.py` dan `PROMPT_NARASI_MENDALAM.md` akan **diganti** mengikuti dokumen ini saat implementasi.

---

## 1. Premis dalam Satu Napas

Raka terbangun di kereta senja yang melaju di atas laut. Ia mengira dirinya cuma ketiduran sepulang lembur. Sambil berjalan dari Gerbong 5 ke Gerbong 1, ia menolong penumpang yang masing-masing terjebak oleh penyesalannya sendiri, dan setiap pintu gerbong memunculkan kilas balik yang tidak mau ia ingat.

Yang tidak Raka (dan pemain) sadari: **semua penumpang kereta ini sudah meninggal, termasuk Raka.** Kereta itu baru berhenti setelah jiwanya bisa memaafkan dirinya sendiri. Saat akhirnya ia turun di Stasiun Fajar, tubuhnya perlahan tembus pandang, lalu hilang terbawa angin pagi.

### Dua Twist Berlapis (Disusun Supaya Pemain Tertipu)
| Lapis | Yang Dipercaya Pemain Sepanjang Game | Kebenaran di Ending |
| :--- | :--- | :--- |
| **Twist 1: Senja** | Senja adalah orang yang "pergi". Dialog sengaja ambigu ("sejak Senja pergi", "aku nggak datang di perpisahannya"), jadi pemain mengira **Senja sudah meninggal** dan Raka dihantui rasa bersalah. | Senja **masih hidup**. Dulu ia cuma pindah kota (berangkat dengan kereta pagi ke Yogyakarta). **Raka-lah yang tidak pernah sampai ke peron.** |
| **Twist 2: Raka** | Kereta ini cuma mimpi, metafora, atau "ruang batin" orang yang kelelahan. | Raka meninggal di kereta terakhir pukul **23:59**, malam sebelum ia berniat menemui Senja. Sosok Senja di Gerbong 1 adalah **Senja yang hidup di ingatan Raka**, bukan arwah. |

> [!NOTE]
> **Penyebab kematian Raka tidak pernah disebut secara eksplisit** (sesuai arahanmu). Petunjuk yang tersebar mengarah pada tafsiran lembut: ia tertidur di kereta terakhir setelah berbulan-bulan kelelahan dan *tidak pernah bangun lagi*. Pemain boleh menafsirkannya sendiri, dan tidak ada adegan kecelakaan atau darah.

---

## 2. Tema & Arc Batin Raka

**Tema utama:** *Memaafkan diri sendiri bukan berarti melupakan kesalahan. Artinya kamu berhenti menjadikan kesalahan itu tempat tinggal.*

Kelima gerbong dirancang sebagai **tahapan Raka memaafkan dirinya**. Setiap penumpang membawa luka yang menjadi cermin luka Raka. Saat menolong mereka, Raka sebenarnya sedang menolong dirinya sendiri tanpa sadar.

| Gerbong | Tahap Batin Raka | Cermin di Penumpang | Kalimat Penyangkalan Raka di Awal | Yang Akhirnya Ia Pahami |
| :--- | :--- | :--- | :--- | :--- |
| **5 — Keheningan** | **Penyangkalan** | — (sendirian) | "Aku cuma ketiduran. Sebentar lagi juga bangun." | Ada yang tidak beres, dan ia memilih untuk mencari tahu. |
| **4 — Rak Buku & Langit Sore** | **"Aku cuma beban"** | **Bima** merasa sakitnya menghancurkan mimpi kakaknya. | "Ibu nyekolahin aku seni, dan aku malah berhenti. Aku buang-buang uang mereka." | Orang yang mencintai kita tidak menghitung kita sebagai beban. |
| **3 — Meja Kerja & Jam Dinding** | **Kata-kata yang tak sempat** | **Nadia** membentak ibunya di telepon terakhir mereka. | "Senja ngechat terus. Nanti aja aku bales kalau udah lebih baik." | Kata yang tak sempat diucapkan tetap boleh diucapkan sekarang. "Nanti" bukan janji. |
| **2 — Cermin & Hujan** | **Membenci diri sendiri** | **Bayangan Raka**: suara di kepala yang terus bilang "kamu gagal". | "Aku memang pengecut. Pantas semua orang ninggalin aku." | Luka boleh disambung dengan emas (*Kintsugi*). Bagian dirinya yang dulu suka menggambar masih menunggu. |
| **1 — Ruang Masinis** | **Melepaskan** | **Senja** (dalam ingatan) | "Kalau aku turun, berarti semuanya selesai." | Ia memaafkan dirinya karena tidak sempat datang, lalu mengizinkan dirinya pergi. |
| **Peron — Stasiun Fajar** | **Pulang** | Kakek (Kondektur) & Senja yang hidup | — | "Maaf aku telat. Terima kasih sudah nunggu." |

---

## 3. Karakter (Desain Final)

> [!TIP]
> Blok **"Jangkar Visual"** di setiap karakter dipakai ulang secara utuh di semua prompt gambar supaya wajah dan pakaian tetap konsisten antar-CG.

### 3.1 Raka Adiwangsa (24) — Protagonis
* **Latar:** Lahir di Surabaya, dibesarkan Ibu (penjahit) dan **Kakek Harjo**, mantan masinis kereta "Senja Utama". Raka kecil sering diajak Kakek nonton kereta lewat dan menggambar lokomotif di buku tulis bekas. Ia kuliah Desain Komunikasi Visual di kota besar dengan uang tabungan Ibu.
* **Mimpi:** Bersama sahabatnya, Senja, ia membuat *webcomic* **"TRACK 99"** tentang kereta yang membawa penumpang ke tempat yang paling mereka rindukan. Senja menulis ceritanya, Raka menggambarnya.
* **Luka:** Proposal komik mereka ditolak tiga penerbit, dan satu bab yang viral justru dihujani komentar kejam soal gambarnya. Raka merobek buku sketsanya di bawah hujan, berhenti menggambar, lalu bekerja sebagai desainer banner promosi ("revisi logo diperbesar") di agensi iklan. Ia berubah menjadi orang yang selalu bilang "iya, siap" dan perlahan menjauhi Senja karena malu: setiap chat Senja ia jawab "nanti ya". Setahun ia hidup seperti kereta yang jalan tanpa tujuan.
* **Malam terakhir (rahasia ending):** Pukul 23:41 Senja mengirim pesan: besok pukul 06.00 ia berangkat ke Yogyakarta dari Peron 2 Stasiun Kotabaru dan akan membawa bab terakhir *TRACK 99*. Raka mengetik "Aku dateng", menghapusnya, mengetik lagi... lalu naik kereta terakhir dengan pesan belum terkirim. Ia memasang Walkman Kakek, memejamkan mata, dan tidak pernah bangun.
* **Kepribadian di game:** Sopan, suka bercanda kering untuk menutupi lelah, menghindari topik tentang dirinya, dan pandai menghibur orang lain tapi buruk menghibur diri sendiri. Kebiasaan kecilnya: menggosok ibu jari ke telunjuk seperti memegang pensil yang tidak ada.
* **Jangkar Visual:** *young Indonesian man, 24, warm tan skin, messy dark-brown hair with a cowlick, tired gentle dark-brown eyes, navy blue bomber jacket over white t-shirt, dark jeans, black sneakers, retro silver headphones with orange foam pads around neck, small silver cassette Walkman clipped on belt.* (Sesuai sprite `Raka_idle/walk/sit` buatanmu.)

### 3.2 Senja Kirana (24) — Sahabat, Penulis "TRACK 99"
* **Latar:** Teman satu kampus Raka (Sastra Indonesia). Mereka bertemu di halte bus kampus saat senja; Senja menunjuk buku sketsa Raka dan bilang, "Keretamu kelihatan kayak lagi kangen sesuatu." Ia pembuat *mixtape*: keempat kaset di Walkman Raka diberi label dengan **tulisan tangan Senja**.
* **Kebenaran:** Senja **tidak meninggal**. Setahun setelah kepergian Raka, ia menerbitkan *TRACK 99* volume pertama memakai sketsa-sketsa lama Raka yang diberikan Ibu Raka.
* **Di kereta (Gerbong 1):** Yang Raka temui adalah **Senja versi ingatannya**: hangat, jahil, lebih bijak dari Raka. Ia tidak pernah bilang dirinya arwah. Ia hanya bilang, *"Stasiunku bukan di sini, Rak."*
* **Jangkar Visual:** *young Indonesian woman, 24, shoulder-length dark-brown hair with a small mustard-yellow hair clip on the left side, bright mischievous eyes, beige long coat over a cream knit sweater, soft white knit scarf, carries a worn blue manuscript folder.* (Versi kampus di kilas balik: *mustard cardigan, tote bag full of books*.)

### 3.3 Bima Sakti Pratama (9) — Penumpang Gerbong 4
* **Latar:** Anak Surabaya yang sakit leukemia dan dirawat di Ruang Anggrek 3. Kakaknya, **Mas Dimas** (17), pandai menggambar komik dan berjanji mengajak Bima naik kereta ke laut. Saat biaya pengobatan menumpuk, Dimas berhenti les gambar untuk kerja paruh waktu, dan Ibu menjual motor.
* **Luka:** Bima yakin dirinya **beban** yang membuat kakaknya berhenti menggambar. Ia memegang pesawat kertas terakhir (dilipat dari halaman komik Dimas) tapi tidak berani menerbangkannya, karena "kalau jatuh, nanti rusak kayak semuanya."
* **Kebiasaan:** Menghitung tiang listrik, karena kata Mas Dimas, "kalau sampai seratus, lautnya kelihatan." Hitungannya selalu berhenti di 99.
* **Petunjuk tersembunyi:** Gelang rumah sakit di pergelangan tangan tertutup lengan jas hujan; jas hujan kuning hadiah Dimas "buat ke laut pas musim hujan" yang tidak pernah terjadi.
* **Jangkar Visual:** *small Indonesian boy, 9, short messy black hair, big curious dark eyes, oversized bright-yellow raincoat with hood down, dark shorts, a white hospital wristband peeking from the sleeve, holding a paper airplane folded from a comic page.*

### 3.4 Nadia Larasati (26) — Penumpang Gerbong 3
* **Latar:** Arsitek junior dari Semarang, perantau, anak tunggal. Mimpinya membangun **rumah kecil di tepi laut untuk Ibu**, dan sketsanya selalu ia selipkan di balik gambar proyek kantor.
* **Luka:** Malam ulang tahun Ibunya, Ibu menelepon 14 kali dan mengajaknya pulang makan malam. Nadia yang sedang dikejar revisi pukul satu dini hari menjawab ketus, *"Bu, aku lagi kerja! Jangan telepon terus!"* Itu percakapan terakhir mereka. Nadia mengendarai motor pulang kantor larut malam... (tidak dijelaskan lebih jauh).
* **Petunjuk tersembunyi:** Helm dengan retakan halus di kursi; jam dinding gerbong berhenti di **01.14**; kotak bekal dari Ibu yang belum dibuka.
* **Jangkar Visual:** *Indonesian woman, 26, round thin-framed glasses, dark hair in a messy low bun with loose strands, tired kind eyes, blue-gray oversized knit cardigan over cream blouse, office ID lanyard, holding a spiral notebook and pencil.*

### 3.5 Bayangan Raka — "Suara di Kepala" (Gerbong 2)
* **Wujud:** Pantulan Raka di kaca jendela yang **tidak bergerak mengikuti Raka**, lalu keluar dari kaca. Siluet biru-hitam dengan tepian meleleh seperti tinta yang kena hujan, dan sepasang mata kuning redup.
* **Peran:** Antagonis batin. Ia mengucapkan semua kalimat kejam yang selama ini Raka katakan pada dirinya sendiri. Kalimat kuncinya punya makna ganda: *"Kamu sudah lama berhenti hidup, Raka."*
* **Transformasi:** Setelah Kintsugi dan Waveform Tuner, bayangan itu menyusut menjadi **Raka kecil (8 tahun)** yang memegang krayon. Ternyata yang selama ini menangis dan marah di dalam Raka adalah anak yang dulu bahagia menggambar kereta bersama Kakek.
* **Jangkar Visual (Raka kecil):** *small Indonesian boy, 8, same cowlick messy dark-brown hair as Raka, oversized red-and-white striped t-shirt, shorts, holding a crayon and a small worn sketchbook, gap-toothed grin.*

### 3.6 Pak Kondektur — Kakek Harjo (Pemandu yang Menyamar)
* **Peran:** Sosok tua berseragam kondektur yang muncul sebentar di setiap gerbong. Ia **melubangi tiket** penumpang yang sudah "siap turun" dan meninggalkan potongan tiket berstempel di kursi mereka (bisa dikoleksi). Saat ia mencoba melubangi tiket Raka di Gerbong 5, ia hanya tersenyum: *"Belum bisa, Mas. Nanti saja, kalau Mas sudah siap turun."*
* **Kebenaran (ending):** Ia adalah **Kakek Harjo**, masinis kereta Senja Utama yang meninggal saat Raka kuliah. Di peron ia membuka topinya dan memanggil Raka dengan panggilan masa kecilnya: *"Waktunya turun, Le."*
* **Jangkar Visual:** *elderly Indonesian man, around 70, kind wrinkled face, neat white mustache, old-fashioned navy railway conductor uniform with brass buttons, peaked cap that shadows his eyes, holding a warm brass lantern and a brass ticket punch.*

---

## 4. Benang Merah: Petunjuk Tersembunyi (*Foreshadowing*)

Petunjuk disebar halus supaya pemain baru *"ngeh"* ketika mengingat ulang setelah ending.

| # | Petunjuk | Lokasi | Tafsiran Pemain Saat Itu | Makna Sebenarnya |
| :- | :--- | :--- | :--- | :--- |
| 1 | Tiket Raka tercetak **23:59**, dan tujuannya terhapus | Gerbong 5 | Kereta aneh / mimpi | Waktu kematian Raka |
| 2 | Jam saku retak juga berhenti di **23:59** | Gerbong 5 | Simbol penyesalan | Sama |
| 3 | Ponsel Raka: *"Tidak ada sinyal"*, **99+ notifikasi** yang tidak berani ia buka | Gerbong 5 → dibuka di ending | Raka menghindari dunia | Pesan duka dan panggilan tak terjawab dari Senja & Ibu |
| 4 | Kondektur menolak melubangi tiket Raka | Gerbong 5 | Raka belum "selesai" urusannya | Jiwanya belum siap pergi |
| 5 | Penumpang yang ditolong **menghilang jadi cahaya** setelah bilang "Terima kasih, Raka" | Setiap gerbong | "Mereka sudah turun di stasiun mereka" | Jiwa mereka bebas |
| 6 | Gelang rumah sakit Bima, helm retak & jam 01.14 Nadia | Gerbong 4 & 3 | Detail latar | Mereka meninggal |
| 7 | Pantulan Raka di jendela **tertinggal sepersekian detik** (hanya saat Kaset HUJAN diputar) | Gerbong 5–3 | Efek visual keren | Raka bukan lagi bagian dunia nyata |
| 8 | Bima: *"Mas juga naik kereta ini, berarti Mas juga..."* (kalimatnya dipotong suara rel) | Gerbong 4 | Bima polos | Bima tahu |
| 9 | Bayangan: *"Kamu sudah lama berhenti hidup, Raka."* | Gerbong 2 | Metafora jadi *yes-man* | Makna harfiah |
| 10 | Senja: *"Stasiunku bukan di sini, Rak."* | Gerbong 1 | Senja sudah meninggal di tempat lain | Senja masih hidup |
| 11 | Papan rute kereta: Stasiun Rumah → Kampus → Hujan → **Fajar** | Gerbong 5 | Dekorasi | Rute hidup Raka; Fajar = peron yang tidak pernah ia capai |
| 12 | Kaset D tersegel: *"FAJAR — dengerin pas kamu udah siap. — S"* | Gerbong 5, dibuka di Gerbong 1 | Hadiah Senja | Senja memberikannya setahun lalu dan Raka belum pernah mendengarnya |

---

## 5. Struktur Alur Lengkap (Beat-by-Beat)

> Simbol **🎬 CG** = cutscene gambar statis bergaya *Wuthering Waves* (hanya terpicu sekali, lalu tersimpan di save flag). Kode CG mengacu ke [PROMPT_CG_NARASI.md](PROMPT_CG_NARASI.md).

### PROLOG
1. **Video** `vid_01_intro_sea_train.mp4`: kereta melaju di atas laut senja.
2. **🎬 CG_00A – CG_00C (Terbangun):** Raka membuka mata dengan kepala bersandar di jendela, di dunia yang masih hitam-putih. Ia melihat tiket 23:59 di tangannya dan Walkman Kakek di bangku sebelah. *"Aku... ketiduran lagi?"*
3. **Fade dari hitam → gameplay Gerbong 5 (Sketsa).**

### GERBONG 5 — Keheningan (± 6 menit)
* Eksplorasi mode sketsa (hanya Walkman yang bisa disentuh dulu) → **Efek WOW**: Kaset A *SENJA* diputar dan dunia berwarna.
* **Benda (7):** Walkman Kakek, Tiket 23:59, Teh Melati, Jam Saku 23:59, **Ponsel Retak** *(baru)*, **Papan Rute Kereta** *(baru)*, **Kaset D Tersegel** *(baru)*.
* **Kondektur muncul** di pintu kanan: memeriksa tiket Raka, menolak melubanginya, lalu menghilang ke gerbong depan. → Pintu Gerbong 4 terbuka.

### GERBONG 4 — Bima (± 9 menit)
1. **🎬 Kilas Balik 1 — CG_FB1A & CG_FB1B: "Kakek dan Kereta Senja Utama."** Raka kecil di pundak Kakek, lalu Kakek memberikan Walkman dan buku sketsa. Raka di layar memegangi kepala: *"Kenapa aku inget ini sekarang...?"*
2. **Babak 1 — Menghitung Tiang Listrik:** basa-basi dengan Bima (tiang listrik, bekal roti, kenapa Mas pakai *headphone* tapi nggak dengerin apa-apa).
3. **Eksplorasi wajib (membuka Babak 2):** Buku Komik "Kereta ke Laut" karya Dimas, **Gelang Rumah Sakit**, Papan Kapur (hitungan 99), **Kaset B "HUJAN"** di rak buku (membuka Kaset 2 + bisikan hati).
4. **Babak 2 — Takut Kertasnya Robek:** Bima bercerita tentang Dimas yang berhenti menggambar. Raka tersentak karena itu kisahnya sendiri. Bima balik bertanya, *"Mas juga lagi nyimpen sesuatu yang nggak berani dikeluarin ya?"*
5. **Babak 3 → Mini-game "Pesawat Kertas" → Waveform Tuner (Kaset A).**
6. **🎬 Perpisahan — CG_BIMA_A & CG_BIMA_B:** Raka dan Bima menerbangkan pesawat kertas dari jendela kereta yang terbuka di atas laut senja. Pesawat itu membawa pesan *"Mas Dimas, gambar lagi ya."* Bima memudar menjadi cahaya keemasan: **"Terima kasih, Mas Raka!"**
7. **Fade putih → gameplay:** Kursi Bima kosong, tersisa **potongan tiket berlubang** dan **Kaset C "DETAK"** di atas pesawat kertas. Raka: *"...Dia udah turun duluan, ya."*

### GERBONG 3 — Nadia (± 9 menit)
1. **🎬 Kilas Balik 2 — CG_FB2A & CG_FB2B: "Halte Kampus & Atap Gedung."** Pertemuan pertama dengan Senja, lalu mereka menggambar *TRACK 99* bersama di atap kampus saat senja. Senja memberikan *mixtape*.
2. **Babak 1 — Kopi yang Telanjur Dingin:** basa-basi soal gulungan kertas yang makan tempat, lembur, dan etika penumpang malam. Nadia membalikkan perhatian: *"Mata Mas kayak orang yang udah lupa kapan terakhir tidur nyenyak."*
3. **Eksplorasi wajib:** **Ponsel Nadia (14 panggilan tak terjawab: "Ibu")**, **Kotak Bekal dari Ibu**, Blueprint **"Rumah Ibu di Tepi Laut"**, **Helm Retak**, Jam Dinding 01.14.
4. **Babak 2 — Di Balik "Nanti Aja":** Nadia menceritakan telepon terakhirnya. Raka diam lama, lalu untuk pertama kalinya mengaku: *"Aku juga punya puluhan chat yang kujawab 'nanti'."*
5. **Babak 3 → Waveform Tuner (Kaset C DETAK).**
6. **🎬 Perpisahan — CG_NADIA_A & CG_NADIA_B:** Raka dan Nadia merakit maket kertas "Rumah Ibu di Tepi Laut" di meja lipat, ditemani teh hangat dan hujan di jendela. Nadia merekam pesan suara untuk Ibunya, lalu memudar menjadi cahaya biru lembut: **"Terima kasih, Raka. Kamu juga... jangan bilang 'nanti' lagi, ya."**
7. **Fade putih → gameplay:** Maket rumah kecil tertinggal di meja, bersama potongan tiket berlubang.

### GERBONG 2 — Bayangan (± 8 menit)
1. **🎬 Kilas Balik 3 — CG_FB3A & CG_FB3B: "Hujan & Buku Sketsa yang Robek."** Raka merobek buku sketsanya di bawah hujan. Senja datang membawa payung, dan Raka memalingkan wajah: *"Udah, Ja. Mimpi kita ketinggian."*
2. Gerbong gelap berhujan. Pantulan Raka di kaca **tidak ikut bergerak**, lalu keluar dari jendela.
3. **Babak 1 — Orang Asing Bernama Diriku** (konfrontasi; Raka balas berteriak, menyangkal).
4. **Eksplorasi wajib:** 4 Sobekan Sketsa, **Surat Penolakan Penerbit**, **Poster Webcomic TRACK 99** yang lusuh, **Payung Senja**, Cermin Jendela.
5. **Babak 2 — Retakan yang Tidak Harus Disembunyikan** → **Mini-game Kintsugi** → **Babak 3** → **Waveform Tuner (Kaset B HUJAN)**.
6. **🎬 Perpisahan — CG_BAYANGAN_A & CG_BAYANGAN_B:** Bayangan menyusut menjadi Raka kecil. Mereka menggambar kereta bersama di buku sketsa yang sudah disambung dengan garis emas. Raka kecil memeluknya dan larut menjadi tinta emas: **"Terima kasih udah inget aku lagi, Raka."**
7. **Fade putih → gameplay:** Segel **Kaset D** robek sendiri. Hujan berhenti.

### GERBONG 1 — Senja (± 8 menit)
1. **🎬 Kilas Balik 4 — CG_FB4A & CG_FB4B: "Malam Terakhir."** Kantor pukul 23:41, pesan Senja di layar ponsel, lalu Raka di kereta terakhir yang kosong dengan *headphone* terpasang. Mata Raka terpejam pelan sementara jam peron di luar menunjukkan 23:59. *(Pemain mengira ini momen ia ketiduran lalu "terbangun di kereta senja".)*
2. **Babak 1 — Seperti Sore Biasa di Peron:** Basa-basi hangat seperti dua sahabat yang lama tidak bertemu: makanan kantin kampus, kucing oren di halte, *mixtape* yang lagunya norak.
3. **Eksplorasi:** **Naskah TRACK 99 Bab Terakhir**, **Foto Polaroid** Raka & Senja, **Topi Masinis** di gantungan (milik Kakek), Panel Kemudi, Tiket Akhir.
4. **Babak 2 — Bab Terakhir:** Senja membacakan bab terakhir *TRACK 99*: tokoh utamanya turun dari kereta dan ternyata stasiunnya sudah lama menunggunya. *"Aku nggak bisa turun bareng kamu, Rak. Stasiunku bukan di sini."*
5. **Babak 3 → Raka membuka Kaset D FAJAR (rekaman suara Senja di awal kaset) → Waveform Tuner di panel masinis.**
6. **🎬 Perpisahan — CG_SENJA_A & CG_SENJA_B:** Mereka duduk di kokpit masinis menonton matahari terbit di atas laut. Senja menyerahkan halaman terakhir naskah: gambar dua orang di peron. Ia memudar ke dalam cahaya pagi: **"Terima kasih, Raka. Sekarang giliran kamu yang pulang."**

### ENDING — Stasiun Fajar (± 5 menit)
1. **Video** `vid_05_ending_dawn_station.mp4`: pintu kereta terbuka.
2. **🎬 CG_END_01:** Kondektur menunggu di pintu, melubangi tiket Raka, lalu membuka topinya. Ternyata ia Kakek Harjo. *"Waktunya turun, Le."*
3. **🎬 CG_END_02 (TWIST):** Raka menapakkan kaki di peron. Kelopak bunga **menembus telapak tangannya** yang tembus pandang. Ponselnya akhirnya menyala dan menampilkan puluhan pesan yang tertunda, tertanggal **setahun** setelah 23:59. *"...Oh. Jadi begitu."*
4. **🎬 CG_END_03:** Peron 2 Stasiun Kotabaru di dunia nyata, pukul 06.00, satu tahun kemudian. **Senja yang hidup** duduk di bangku dengan komik *TRACK 99* volume 1 dan Walkman perak di pangkuannya. Raka berdiri di belakangnya, tembus cahaya: *"Maaf aku telat, Ja. Terima kasih udah nunggu."*
5. **🎬 CG_END_04:** Angin pagi berembus. Raka perlahan larut menjadi kelopak bunga dan cahaya. Syal Senja terangkat angin, dan ia mendongak dengan mata berkaca-kaca tapi tersenyum: *"...Kamu dateng juga ya, Rak."*
6. **🎬 CG_END_05:** Halaman persembahan komik: **"Untuk Raka — gambarmu selalu sampai."** Ada sehelai kelopak bunga terselip di sana.
7. **Kredit** diiringi `bgm_06_ending_wind.mp3`.
8. **🎬 Pasca-kredit CG_END_06 (opsional):** Kereta Track 99 kosong melaju menjauh di bawah langit pagi; di bangku Gerbong 5 tersisa Walkman yang memutar kaset pelan.

---

## 6. Sistem Kunci Kaset (Progres Mekanik yang Menyatu dengan Cerita)

| Kaset | Label Tulisan Tangan Senja | Didapat | Dipakai untuk |
| :--- | :--- | :--- | :--- |
| **A — SENJA** | *"buat pulang kantor yang capek"* | Sudah terpasang di Walkman (Gerbong 5) | Tuner Bima |
| **B — HUJAN** | *"kalau pengen nangis tapi gengsi"* | Rak buku Gerbong 4 | Bisikan hati penumpang; Tuner Bayangan |
| **C — DETAK** | *"buat hari-hari yang butuh nekat dikit"* | Ditinggalkan Bima setelah perpisahan | Tuner Nadia |
| **D — FAJAR** | *"dengerin pas kamu udah siap. — S"* | Tersegel sejak Gerbong 5; segelnya robek setelah perpisahan Bayangan | Tuner Senja & Ending |

> [!NOTE]
> Kaset D diawali **rekaman suara Senja** (bisa direkam pengisi suara atau cukup teks): *"Rak, kalau kamu dengerin ini, berarti kamu udah siap. Aku nggak marah. Aku cuma kangen gambar keretamu."*

---

## 7. Sistem Cutscene Gambar (CG Narasi Bergaya *Wuthering Waves*)

### 7.1 Gaya Tampilan
* Gambar ilustrasi penuh layar (1920×1080, ditampilkan di 1280×720) dengan **gerak kamera halus *Ken Burns*** (zoom 1.00 → 1.05 dan geser 1–2% selama gambar tampil).
* **Tanpa kotak dialog.** Teks di tengah bawah di atas gradasi gelap transparan: nama pembicara berwarna emas di atas teks putih, persis seperti contoh *Imperator* yang kamu kirim.
* Monolog batin Raka memakai **huruf miring serif** tanpa nama pembicara.
* Tombol kecil **"LEWATI ▷"** di pojok kiri atas, plus indikator ◇ berdenyut di bawah teks saat menunggu klik.

### 7.2 Transisi (Sesuai Permintaanmu: Mulus dengan Pudar Hitam/Putih)
| Jenis CG | Masuk dari Gameplay | Antar-Gambar | Kembali ke Gameplay | Efek Khusus |
| :--- | :--- | :--- | :--- | :--- |
| **Prolog** | Video → putih 0,8 dtk → CG | *Crossfade* 0,7 dtk | Pudar hitam 0,8 dtk → gameplay | Desaturasi bertahap (CG terakhir mulai berwarna) |
| **Kilas Balik (masuk gerbong)** | Layar bergetar halus 0,3 dtk + *chromatic aberration* → pudar **hitam** 0,6 dtk | *Crossfade* 0,7 dtk | Pudar hitam 0,8 dtk; Raka memegang kepala (animasi singkat) | Filter sepia/kusam lembut, *film grain*, vinyet, dan suara rel teredam |
| **Perpisahan (setelah Tuner)** | Banner *Resonance* → pudar **putih** 1,0 dtk | *Crossfade* 0,9 dtk dengan *bloom* | Pudar putih 1,2 dtk → kursi kosong | Partikel cahaya melayang di atas CG |
| **Ending** | Video → putih | *Crossfade* 1,2 dtk (lebih lambat) | Pudar putih panjang ke kredit | CG_END_04 diberi partikel kelopak bunga bergerak di atas gambar |

### 7.3 Aturan Teknis (Untuk Implementasi Nanti)
* Setiap rangkaian CG punya ID (`cg_prolog`, `cg_fb1`, `cg_farewell_bima`, dst.) yang disimpan di `save_data["seen_cg"]`, sehingga **hanya terpicu sekali**. Galeri CG di menu utama bisa membukanya ulang.
* BGM di-*duck* ke 40% saat CG, dan kilas balik memakai `bgm_05_flashback_musicbox.mp3`.
* File gambar: `assets/images/cg/<kode>.png`. Jika belum ada, game menampilkan *placeholder* buram dari latar gerbong supaya alur tetap bisa diuji.

---

## 8. Daftar Benda Interaktif Final (Per Gerbong)

> ✅ = sprite sudah ada · 🆕 = perlu dibuat (prompt di [PROMPT_ASET_TAMBAHAN.md](PROMPT_ASET_TAMBAHAN.md))

| Gerbong | Benda | Status | Fungsi |
| :--- | :--- | :--- | :--- |
| **5** | Walkman Perak Kakek | ✅ | Memicu Efek WOW |
| | Tiket 23:59 | ✅ | Petunjuk #1 |
| | Teh Melati (seperti buatan Ibu) | ✅ | Kenangan Ibu |
| | Jam Saku Retak 23:59 | ✅ | Petunjuk #2 |
| | Ponsel Retak "Tidak Ada Sinyal" | 🆕 | Petunjuk #3 (dibuka di ending) |
| | Papan Rute Kereta | 🆕 | Petunjuk #11 |
| | Kaset D Tersegel | 🆕 | Petunjuk #12 |
| **4** | Buku Komik "Kereta ke Laut" (karya Dimas) | 🆕 | Membuka Babak 2 |
| | Gelang Rumah Sakit | 🆕 | Petunjuk #6 |
| | Papan Kapur Hitungan 99 | (latar) | Lore |
| | Kaset B HUJAN di rak | 🆕 | Membuka Kaset 2 |
| | Termos Roket | ✅ (tea) | Basa-basi |
| | Pesawat Kertas | 🆕 | Mini-game |
| **3** | Ponsel Nadia (14 panggilan "Ibu") | 🆕 | Membuka Babak 2 |
| | Kotak Bekal dari Ibu | 🆕 | Emosi |
| | Blueprint "Rumah Ibu di Tepi Laut" | 🆕 | Perpisahan |
| | Helm Retak | 🆕 | Petunjuk #6 |
| | Jam Dinding 01.14 | (latar) | Petunjuk #6 |
| | Kopi Dingin | ✅ (tea) | Basa-basi |
| **2** | 4 Sobekan Sketsa | (mini-game) | Kintsugi |
| | Surat Penolakan Penerbit | 🆕 | Lore |
| | Poster *TRACK 99* Lusuh | 🆕 | Lore |
| | Payung Senja | 🆕 | Kilas balik |
| | Cermin Jendela | (latar) | Petunjuk #7 |
| | Kaset Kusut | ✅ (walkman) | Lore |
| **1** | Naskah *TRACK 99* Bab Terakhir | 🆕 | Babak 2 |
| | Foto Polaroid Raka & Senja | 🆕 | Emosi |
| | Topi Masinis Kakek | 🆕 | Petunjuk Kakek |
| | Panel Kemudi Masinis | (latar) | Tuner Final |
| | Tiket Akhir "Stasiun Fajar" | ✅ | Penutup |
| **Semua** | Potongan Tiket Berlubang (koleksi) | 🆕 | Ditinggalkan penumpang yang sudah "turun" |

---

## 9. Pacing Target 45 Menit

| Bagian | Isi | Durasi |
| :--- | :--- | :--- |
| Prolog | Video + 3 CG | 1,5 mnt |
| Gerbong 5 | Sketsa → WOW, 7 benda, Kondektur | 4,5 mnt |
| Gerbong 4 | Kilas Balik 1, 3 babak, 6 benda, Pesawat Kertas, Tuner, Perpisahan | 9 mnt |
| Gerbong 3 | Kilas Balik 2, 3 babak, 6 benda, Tuner, Perpisahan | 9 mnt |
| Gerbong 2 | Kilas Balik 3, 3 babak, 5 benda, Kintsugi, Tuner, Perpisahan | 8 mnt |
| Gerbong 1 | Kilas Balik 4, 3 babak, 5 benda, Kaset D, Tuner, Perpisahan | 8 mnt |
| Ending | Video + 5 CG + kredit | 5 mnt |
| **Total** | | **± 45 menit** |

> [!TIP]
> Durasi naik dari ±15 menit karena (1) **babak 2 baru terbuka setelah benda wajib diperiksa**, sehingga pemain terdorong menjelajah; (2) 22 CG narasi; (3) dialog basa-basi yang lebih panjang; (4) koleksi potongan tiket dan papan rute bersifat opsional.
