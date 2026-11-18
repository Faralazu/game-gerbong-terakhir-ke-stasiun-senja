# Panduan & Prompt Penulisan Narasi Mendalam
## **Gerbong Terakhir ke Stasiun Senja (*Track 99: Resonance*)**

Dokumen ini berisi **Master Prompt siap copy-paste** jika kamu ingin meminta bantuan AI lain (Claude / ChatGPT / Gemini Web) untuk menulis ulang, memperpanjang, atau membuat variasi dialog bergaya **natural Indonesia** (penuh basa-basi realistis, subteks, konflik batin, dan penokohan berjiwa seperti *A Space for the Unbound*, *To The Moon*, & *OMORI*).

---

## Cara Pakai Cepat (Tanpa Ubah Kode Python!)
1. Copy salah satu prompt di bawah ini ke AI pilihanmu.
2. Minta AI menghasilkan format JSON sesuai struktur di bagian paling bawah dokumen ini.
3. Simpan hasilnya ke **`userdata/custom_dialogues.json`**.
4. Game otomatis membaca dialog dari `userdata/custom_dialogues.json` (tekan **`F5`** di dalam game untuk me-refresh tanpa restart)!

---

## Master Prompt 1: Penulisan Ulang Dialog Penumpang + Konflik Batin Raka
Copy-paste ke AI dan ganti `[NAMA_GERBONG]` sesuai kebutuhan (`gerbong_4_childhood`, `gerbong_3_burnout`, `gerbong_2_crossroads`, atau `gerbong_1_dawn`):

> Kamu adalah penulis naskah game naratif Indonesia bergaya *A Space for the Unbound*, *To The Moon*, dan *OMORI*.
> Tulis skrip percakapan 3 babak (*chapter_1*, *chapter_2*, *chapter_3*) untuk adegan di **[NAMA_GERBONG]** pada game *"Gerbong Terakhir ke Stasiun Senja"*.
>
> **Konteks Karakter Utama (Raka, 22 thn):**
> - Mantan ilustrator komik indie yang berhenti menggambar setelah proyeknya gagal dan sahabat dekatnya (**Senja**) pergi dari hidupnya.
> - Selama setahun terakhir, Raka kehilangan jati dirinya—ia berubah menjadi "yes-man" yang hanya menuruti ekspektasi orang lain dan memendam lelahnya sendiri.
> - Raka bukan penolong sempurna: ia awalnya suka menghindar, pakai basa-basi datar, dan menyangkal perasaannya sendiri (*internal conflict*).
>
> **Aturan Gaya Penulisan (WAJIB):**
> 1. **Dilarang langsung ceramah atau to-the-point.** Mulai setiap pertemuan dengan basa-basi natural (komentar soal gerbong dingin, snack kereta, kopi tumpah, suara hujan, atau hal remeh sehari-hari).
> 2. **Gunakan dialog bahasa Indonesia yang hidup** (kata ganti *aku/kamu* atau *mas/kak/mbak* sesuai karakter, jeda berpikir `...`, kalimat yang tidak langsung menjelaskan moral cerita secara eksplisit).
> 3. **Sisipkan pikiran batin Raka** dalam tanda kurung `(...)` yang menunjukkan penyangkalan, rasa iri, keraguan, lalu kesadaran diri secara bertahap.
> 4. **Setiap karakter penumpang harus punya jiwa dan masalahnya sendiri**—bukan sekadar NPC pemberi kunci pintu.

---

## Master Prompt 2: Tambah Benda Memori Interaktif Baru
> Buatkan 4 deskripsi benda interaktif di gerbong kereta komuter senja (misal: *bekal roti*, *map revisi denah*, *karcis lipat*, *sketsa sobek*). Untuk setiap benda, tulis 3–4 baris monolog batin Raka dalam bahasa Indonesia yang santai, menyentuh, penuh subteks tentang seseorang yang sedang kehilangan jati dirinya, dan diakhiri sedikit pengamatan tentang penumpang di gerbong itu.

---

## Format JSON `userdata/custom_dialogues.json`
Jika ingin mengganti naskah bawaan (`src/core/narrative_script.py`), buat file `userdata/custom_dialogues.json` dengan struktur parsial seperti contoh berikut (cukup isi bagian yang ingin kamu timpa):

```json
{
  "gerbong_3_burnout": {
    "chapters": [
      {
        "title": "Babak 1: Kopi yang Telanjur Dingin",
        "lines": [
          ["npc", "Eh, maaf Mas, tas saya makan tempat ya? Sebentar saya geser."],
          ["raka:calm", "Nggak apa-apa, Mbak. Keretanya juga lagi sepi banget malam ini."],
          ["raka:sad", "(Padahal dari tadi aku ngelihatin dia megangin pelipisnya... persis kayak aku tiap jam sebelas malam.)"]
        ]
      }
    ]
  }
}
```
