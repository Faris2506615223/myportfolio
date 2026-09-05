# Portofolio Personal - Faris Salman Azhari

**Nama:** Faris Salman Azhari
**NPM:** 2506615223
**Kelas:** PBP F

---

## Deskripsi Proyek

Website portofolio personal berbasis Django yang dibangun menggunakan HTML5 semantik dan CSS3 murni tanpa dependensi JavaScript. Website ini menyajikan informasi profil, latar belakang dan nilai personal (*Get to Know Me*), serta daftar keahlian teknologi (*Passion / Tech Stacks*) dengan animasi marquee dua arah murni CSS yang interaktif dan responsif di berbagai ukuran layar.

---

## Cara Menjalankan Proyek Secara Lokal

1. **Clone repository:**

   ```bash
   git clone https://github.com/Faris2506615223/myportfolio.git
   cd myportfolio
   ```
2. **Buat dan aktifkan virtual environment:**

   ```bash
   python -m venv env

   # Windows (PowerShell):
   .\env\Scripts\Activate.ps1
   # Windows (Command Prompt):
   .\env\Scripts\activate.bat
   # macOS/Linux:
   source env/bin/activate
   ```
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Jalankan migrasi dan server Django:**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
5. Buka browser dan akses: `http://127.0.0.1:8000/`

---

## Progres Pengerjaan (Tugas 1)

- [X] Inisialisasi proyek Django, konfigurasi aplikasi `portofolio`, dan penataan direktori `static/` serta `templates/`.
- [X] Penyusunan struktur dokumen HTML5 menggunakan tag semantik (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<blockquote>`, `<footer>`).
- [X] Desain layout Hero Section dan About Me responsif dengan CSS Grid (`grid-template-areas`) dan Flexbox.
- [X] Pembuatan section Passion dengan animasi Tech Stacks Marquee dua baris (kiri dan kanan) murni CSS tanpa JavaScript.
- [X] Penambahan breakpoint media queries untuk desktop, tablet, dan mobile.
- [X] Pengelolaan version control Git dengan branching `feat/tugas1`, conventional commits, dan merge ke `main`.

---

## Pertanyaan Reflektif

### 1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

**Jawaban:**
Ya, saya menggunakan elemen semantik HTML5 secara ekstensif, antara lain `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`, `<blockquote>`, serta `<dl>`, `<dt>`, dan `<dd>`.

Elemen-elemen ini membantu pembuatan static web dalam beberapa aspek:

1. **Hierarki dan Keterbacaan Kode**: Memisahkan bagian halaman berdasarkan fungsinya (misalnya `<section id="profile">` untuk hero dan `<section id="works">` untuk passion) membuat struktur file HTML jauh lebih mudah dipahami dan dikelola dibandingkan tumpukan `<div>` generik.
2. **Aksesibilitas (A11y)**: Screen reader dan perangkat bantu disabilitas dapat mengenali navigasi, konten utama, dan kutipan secara otomatis tanpa konfigurasi ARIA berlebih.
3. **SEO Dasar**: Mesin pencari dapat memahami bobot konten mana yang merupakan navigasi, konten editorial, atau footer halaman.

### 2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

**Jawaban:**Tantangan utamanya adalah menjaga alur baca tetap natural saat layout berpindah dari multi-kolom ke satu kolom:

1. **Urutan Visual Hero**: Pada desktop, foto profil berada di kolom kanan sejajar dengan nama dan bio. Di layar mobile, foto harus diletakkan di antara nama dan bio agar pengguna langsung melihat identitas visual sebelum membaca teks panjang. Saya menyelesaikannya menggunakan `grid-template-areas` yang didefinisikan ulang di dalam `@media (max-width: 600px)`.
2. **Skalabilitas Marquee**: Kartu teknologi pada marquee berukuran 160x120px di desktop. Di mobile (`max-width: 480px` dan `360px`), ukuran kartu dikecilkan proporsional menjadi 110x90px dan 90x80px agar tidak memenuhi layar secara berlebihan.
3. **Evaluasi Prioritas**: Elemen informasi primer (nama, deskripsi, tautan kontak) selalu diprioritaskan agar mudah dibaca dan di-tap. Elemen dekoratif atau sekunder disederhanakan ruang dan padding-nya agar tidak menimbulkan horizontal overflow.

### 3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

**Jawaban:**Batasan terbesar dari static web murni adalah seluruh data (keahlian, proyek, biografi) harus di-hardcode langsung ke file HTML. Jika ingin memperbarui portofolio atau menambah entri baru:

- Harus mengubah kode HTML secara manual, yang memakan waktu dan rawan merusak struktur tata letak.
- Tidak ada validasi data atau pemisahan antara data dan tampilan (*presentation layer*).

Fungsionalitas dinamis yang paling ingin saya tambahkan berikutnya memanfaatkan pola MVT Django:

1. **Model Database (`models.Model`)**: Membuat model `Skill` dan `Project` di database SQLite Django untuk menyimpan nama teknologi, kategori, deskripsi, dan URL gambar.
2. **Django Admin**: Mengelola konten portofolio langsung melalui antarmuka bawaan Django tanpa menyentuh file HTML.
3. **Dynamic Template Rendering**: Menggunakan loop Django template (`{% for skill in skills %}`) untuk me-render kartu marquee secara otomatis dari query database.

---

## AI Disclosure

### 1. Tools yang Digunakan

- **Google Antigravity** (dengan model Gemini Flash 3.8 High).

### 2. Bagian yang Dibantu AI

- Mengambil dan menyalin struktur devicon SVG dari referensi website live saya di Vercel (fufufarizz.vercel.app).
- Menghitung keyframes animasi CSS untuk efek marquee looping tanpa putus (`marquee-scroll-left` dan `marquee-scroll-right`).
- Membantu menyusun urutan perintah Git untuk proses branching `feat/tugas1`, staging, commit berformat conventional commits, dan resolusi merge conflict di branch `main`.

### 3. Strategi Prompting

- Menggunakan instruksi terarah dan bertahap (*step-by-step*).
- Menetapkan batasan ketat sejak awal: melarang penggunaan JavaScript, mewajibkan pure HTML & CSS, dan meminta penghapusan kode yang tidak diperlukan.
- Memberikan feedback langsung ketika ada output yang tidak sesuai (misalnya meminta menghapus panel project yang gambarnya belum siap tampil).

### 4. Analisis Kritis & Perbaikan Mandiri

- **Keterbatasan AI yang Ditemukan**:
  - Pada percobaan awal, AI cenderung menyertakan dependensi JavaScript (seperti GSAP untuk tab switcher dan Lenis untuk scroll) serta menambahkan kartu proyek dengan aset gambar lokal yang sempat menyebabkan broken image di browser.
  - AI sempat menghasilkan typo URL pada tautan GitHub (`https://https://github.com/...`).
  - AI cenderung membuat komentar kode dan copywriting yang terlalu panjang/klise (*slop*) jika tidak dibatasi.
- **Perbaikan Manual yang Dilakukan**:
  - Menginstruksikan penghapusan seluruh kode JavaScript agar tugas tetap patuh pada materi static web HTML & CSS murni.
  - Memutuskan untuk menghapus sementara bagian project di bawah marquee agar tampilan rapi dan bebas broken image.
  - Mengoreksi tautan GitHub dan menambahkan atribut pengaman `target="_blank" rel="noopener noreferrer"`.
  - Merapikan seluruh komentar kode di HTML dan CSS menjadi singkat dan natural, serta menulis dokumentasi README secara jujur dan faktual.

### 5. Log Prompt Utama (ril aseli no fek fek)

1. *"browser fufufarizz.vercel.app, Berikut saya berikan referensi website dari hasil akhir portofolio website pada source code di tahap 10 (sekarang masih tahap 1, ikuti sesuai tahap) Berikan implementation plannya. Tahap 1: Lanjutkan halaman “About Me” yang sudah dibuat. Tambahkan satu atau lebih section baru ke halaman yang sama, masih murni dengan HTML5 dan CSS3 (belum ada database/MVT). Pilihan saya, saya ingin anda menambahkan section get to know me persis seperti screenshot yang saya berikan dari website referensi. Karena tugas ini sifatnya lebih bebas, kamu dipersilakan membuat tampilan CSS berbeda dari referensi di website - tambahkan animasi, layout grid, atau elemen visual lain sesuai kreativitasmu, selama tetap rapi dan responsif. Satu pesan saya, buat kode html dan css yang mudah dimengerti, tidak bertele tele, dan tulis kode dengan rapi. Pastikan kode yang dibuat tidak mengada ngada agar saya dapat tetap mengerti apa yang ditulis. Desain visual (warna, font, tata letak, dsb.) bebas diubah, desain seluruh halaman “About Me”, bukan cuma section barunya, asal tetap murni HTML5 dan CSS3, terstruktur rapi, dan checklist di bawah tetap terpenuhi. Checklist minimal untuk tugas ini: -Minimal satu section baru ditambahkan ke halaman yang sama. -Section baru tersebut punya isi yang nyata (bukan lorem ipsum atau placeholder kosong), samakan saja dengan website referensi -Halaman tetap terlihat rapi di lebar layar desktop maupun mobile. -Proyek berhasil dijalankan dengan python manage.py runserver tanpa error."*
2. *"Cek website yang saya berikan, saya ingin anda mengcopy seluruh bagian pada Passion, benar benar copy semuanya sama persis. Untuk Element/gambar pada bagian projects, saya telah menaruh sourcenya di img/projects. Proceed dengan revisi: Jangan menggunakan javascript, tambahkan murni html dan css nya saja. bila terdapat kode/fitur yang membutuhkan javascript maka di skip dulu"*
3. *"Commit text: Jangan ubah kode ataupun melakukan commit. Saya ingin melakukan branching di git dan melakukan commit satu persatu, mulai dari bagian get to know me dan bagian cards. Untuk itu, saya ingin anda membuatkan copy writing dengan lengkap dengan format git checkout -b ..., git add ..., git commit -m "..." hingga git push ... saya ingin melakukan 3 commit 1. pembuatan get to know me 2. pembuatan cards 3, penggantian teks lorem ipsum cukup berikan copywritingnya, untuk kode card biar saya yang hapus dahulu untuk commit get to know me, untuk penggantian teks lorem ipsum juga biar saya yang ganti secara mandiri."*
4. *"pastikan komentar penjelasan pada setiap kode yang dibuat bersifat natural dan tidak slop... Begitupun untuk AI disclosure, pastikan bahasa yang dibuat natural dan tidak AI slop"*
