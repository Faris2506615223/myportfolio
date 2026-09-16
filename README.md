# Portofolio Personal - Faris Salman Azhari

**Nama:** Faris Salman Azhari
**NPM:** 2506615223
**Kelas:** PBP F

---

## Deskripsi Proyek

Website portofolio personal berbasis Django yang dibangun menggunakan HTML5 semantik dan CSS3 murni tanpa dependensi JavaScript. Website ini menyajikan profil, daftar proyek, pengalaman, dan keahlian teknologi. Data proyek dan pengalaman dikelola melalui form tervalidasi, disimpan pada database, serta tersedia melalui endpoint JSON. Seluruh halaman memakai template induk yang sama agar navigasi, pesan, metadata dasar, dan footer tetap konsisten.

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

## Progres Pengerjaan (Tugas 2)

- [X] **Model `Project`**: Membuat model baru `Project` di `main/models.py` dengan 6 field (`id` UUID, `title`, `category`, `description`, `thumbnail`, `project_url`, `created_at`) serta konfigurasi `class Meta` (`ordering`, `verbose_name`).
- [X] **Migrasi Database**: Membuat dan menerapkan migrasi database (`0002_project.py` dan `0003_alter_experience_options_alter_project_options.py`) ke SQLite.
- [X] **Kustomisasi Django Admin**: Mendaftarkan model `Project` dan `Experience` dengan kustomisasi kelas `ModelAdmin` (`list_display`, `list_filter`, `search_fields`, `readonly_fields`) di `main/admin.py`.
- [X] **Controller / Views**: Membuat fungsi view `show_projects` dan fitur tambahan halaman detail `show_project_detail` dengan proteksi `get_object_or_404` di `main/views.py`.
- [X] **URL Routing**: Mendaftarkan named routes `path("projects/", show_projects, name="show_projects")` dan `path("projects/<uuid:id>/", show_project_detail, name="show_project_detail")` di `main/urls.py`.
- [X] **Template Daftar Proyek**: Membuat `templates/projects.html` dengan loop DTL `{% for %}`, penanganan kondisi kosong `{% empty %}`, tombol tautan detail, serta styling kartu responsif murni CSS.
- [X] **Template Detail Proyek (Fitur Tambahan)**: Membuat `templates/project_detail.html` dengan hero banner, metadata tanggal, deskripsi lengkap, tautan eksternal demo/repo, dan navigasi breadcrumb kembali ke daftar proyek.
- [X] **Konsistensi Navigasi**: Memperbarui navbar di `index.html`, `experience.html`, `projects.html`, dan `project_detail.html` menggunakan tag `{% url %}` secara konsisten.
- [X] **Unit Testing Komprehensif**: Menulis 12 unit test di `main/tests.py` yang mencakup isolasi model, aksesibilitas URL (status 200), validasi template, rendering data dinamis, penanganan empty state, navigasi navbar, serta penanganan 404 pada detail view.
- [X] **Refleksi & Dokumentasi**: Menjawab seluruh pertanyaan reflektif Tugas 2 di `README.md` secara terstruktur dan komprehensif.
- [X] **Verifikasi Kelulusan**: Memastikan proyek lolos 100% pada `python manage.py test` (12 test passed) dan berjalan lancar tanpa error pada `python manage.py runserver`.

---

## Progres Pengerjaan (Tugas 3)

- [X] **Template Inheritance**: Seluruh halaman HTML penuh menggunakan `{% extends "base.html" %}`; modal konfirmasi hapus Project dan Experience memakai satu partial reusable.
- [X] **`ExperienceForm`**: Membuat `ModelForm` dengan field `title`, `description`, `category`, dan `thumbnail` yang mencakup input teks, textarea, pilihan kategori, dan validasi URL; `id`, `started_at`, serta `ended_at` tidak dapat diubah melalui form.
- [X] **Create & Update**: Menambahkan halaman tambah dan ubah Experience dengan validasi bawaan Django, form yang terisi otomatis saat update, CSRF token, pesan sukses, dan redirect setelah penyimpanan.
- [X] **Delete**: Menambahkan penghapusan Experience melalui request `POST`, CSRF token, dan modal konfirmasi; request `GET` ditolak dengan status `405 Method Not Allowed`.
- [X] **JSON Data Delivery**: Menambahkan endpoint `/api/experiences/` yang mendukung filter judul dan mengembalikan hasil serialisasi model dengan content type `application/json`.
- [X] **JSON Deserialization**: Halaman `/experience/` mengambil response endpoint JSON, mendeserialisasikannya menjadi objek `Experience`, lalu menampilkan data tersebut pada template.
- [X] **UI/UX Tambahan**: Menambahkan pencarian Experience, empty state khusus hasil pencarian, thumbnail opsional, tombol aksi responsif, dan pesan keberhasilan operasi.
- [X] **Automated Testing**: Menambahkan pengujian form field, template inheritance, validasi create, prefilled update, penyimpanan update, proteksi delete, endpoint JSON, filter, dan render hasil deserialisasi.
- [X] **Verifikasi Akhir**: Seluruh 29 automated test lulus, `manage.py check` tidak menemukan masalah, dan server lokal merespons halaman Experience serta endpoint JSON dengan status `200`.

### Endpoint Tugas 3

| Method | Endpoint | Fungsi |
| --- | --- | --- |
| `GET` | `/experience/` | Menampilkan Experience dari hasil deserialisasi JSON |
| `GET`, `POST` | `/experience/add/` | Menampilkan dan memproses form create |
| `GET`, `POST` | `/experience/<uuid>/edit/` | Menampilkan dan memproses form update |
| `POST` | `/experience/<uuid>/delete/` | Menghapus satu Experience |
| `GET` | `/api/experiences/` | Mengirim semua Experience dalam format JSON |
| `GET` | `/api/experiences/?title=...` | Mengirim Experience yang judulnya cocok |

---

## Pertanyaan Reflektif

### Tugas 1

1. **Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?**

**Jawaban:**
Ya, saya menggunakan elemen semantik HTML5 secara ekstensif, antara lain `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`, `<blockquote>`, serta `<dl>`, `<dt>`, dan `<dd>`.

Elemen-elemen ini membantu pembuatan static web dalam beberapa aspek:

1. **Hierarki dan Keterbacaan Kode**: Memisahkan bagian halaman berdasarkan fungsinya (misalnya `<section id="profile">` untuk hero dan `<section id="works">` untuk passion) membuat struktur file HTML jauh lebih mudah dipahami dan dikelola dibandingkan tumpukan `<div>` generik.
2. **Aksesibilitas (A11y)**: Screen reader dan perangkat bantu disabilitas dapat mengenali navigasi, konten utama, dan kutipan secara otomatis tanpa konfigurasi ARIA berlebih.
3. **SEO Dasar**: Mesin pencari dapat memahami bobot konten mana yang merupakan navigasi, konten editorial, atau footer halaman.

2. **Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?**

   **Jawaban:**
   Tantangan utamanya adalah menjaga alur baca tetap natural saat layout berpindah dari multi-kolom ke satu kolom:
   - **Urutan Visual Hero**: Pada desktop, foto profil berada di kolom kanan sejajar dengan nama dan bio. Di layar mobile, foto harus diletakkan di antara nama dan bio agar pengguna langsung melihat identitas visual sebelum membaca teks panjang. Saya menyelesaikannya menggunakan `grid-template-areas` yang didefinisikan ulang di dalam `@media (max-width: 600px)`.
   - **Skalabilitas Marquee**: Kartu teknologi pada marquee berukuran 160x120px di desktop. Di mobile (`max-width: 480px` dan `360px`), ukuran kartu dikecilkan proporsional menjadi 110x90px dan 90x80px agar tidak memenuhi layar secara berlebihan.
   - **Evaluasi Prioritas**: Elemen informasi primer (nama, deskripsi, tautan kontak) selalu diprioritaskan agar mudah dibaca dan di-tap. Elemen dekoratif atau sekunder disederhanakan ruang dan padding-nya agar tidak menimbulkan horizontal overflow.

3. **Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?**

   **Jawaban:**
   Batasan terbesar dari static web murni adalah seluruh data (keahlian, proyek, biografi) harus di-hardcode langsung ke file HTML. Jika ingin memperbarui portofolio atau menambah entri baru:
   - Harus mengubah kode HTML secara manual, yang memakan waktu dan rawan merusak struktur tata letak.
   - Tidak ada validasi data atau pemisahan antara data dan tampilan (*presentation layer*).

   Fungsionalitas dinamis yang paling ingin saya tambahkan berikutnya memanfaatkan pola MVT Django:
   - **Model Database (`models.Model`)**: Membuat model `Skill` dan `Project` di database SQLite Django untuk menyimpan nama teknologi, kategori, deskripsi, dan URL gambar.
   - **Django Admin**: Mengelola konten portofolio langsung melalui antarmuka bawaan Django tanpa menyentuh file HTML.
   - **Dynamic Template Rendering**: Menggunakan loop Django template (`{% for skill in skills %}`) untuk me-render kartu marquee secara otomatis dari query database.

### Tugas 2

1. **Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.**

   Ketika seorang pengguna mengakses halaman portofolio baru (misalnya rute `/projects/`), alur yang terjadi di dalam arsitektur Model-View-Template (MVT) Django adalah sebagai berikut:
   - **Klien / Browser**: Pengguna mengklik tautan navigasi `Projects` atau mengakses URL `http://127.0.0.1:8000/projects/`. Browser mengirimkan permintaan HTTP dengan metode `GET` ke web server Django.
   - **`urls.py` Proyek (`portofolio/urls.py`)**: Berfungsi sebagai *root URLconf* (pintu gerbang utama). Django mengevaluasi pola URL yang masuk. Karena terdapat entri `path("", include("main.urls"))`, Django mendelegasikan penanganan URL tersebut ke berkas routing tingkat aplikasi `main`.
   - **`urls.py` Aplikasi (`main/urls.py`)**: Berfungsi sebagai *application URLconf*. Django mencocokkan path spesifik `"projects/"` dengan daftar `urlpatterns`. Pola ini memetakan request ke fungsi view `show_projects` dengan named route `name="show_projects"`.
   - **`views.py` Aplikasi (`main/views.py`)**: Fungsi view `show_projects(request)` bertindak sebagai pengendali logika (*controller/view*):
     - View meminta data ke layer model melalui Django ORM: `Project.objects.all().order_by("-created_at")`.
   - **`models.py` Aplikasi (`main/models.py`)**: Model mendefinisikan skema struktur tabel `main_project` pada basis data SQLite. Query ORM diterjemahkan oleh Django menjadi perintah SQL (`SELECT ... FROM main_project ...`) dan dieksekusi ke database. Hasil query dipetakan kembali menjadi queryset berisi objek-objek Python dari kelas `Project`.
   - **Penyusunan Context**: View mengemas queryset data tersebut bersama data statis lainnya ke dalam dictionary: `context = {"name": "Faris", "project_list": ...}`. View kemudian memanggil `render(request, "projects.html", context)`.
   - **`templates/projects.html`**: Django Template Engine memproses template HTML:
     - Tag DTL `{% for project in project_list %}` melakukan iterasi pada setiap objek proyek untuk membuat kartu proyek.
     - Tag `{% empty %}` dieksekusi apabila data proyek belum tersedia untuk menampilkan pesan ramah kondisi kosong (*empty state*).
     - Tag `{% url %}` dievaluasi untuk membuat tautan navigasi yang valid ke halaman lain.
     - Variabel seperti `{{ project.title }}` dan `{{ project.description }}` digantikan dengan nilai teks nyata dari database.
   - **HTTP Response**: Dokumen HTML lengkap yang telah selesai di-render dikembalikan sebagai objek `HttpResponse` berstatus `200 OK` ke browser, yang kemudian menampilkannya secara visual kepada pengguna.

2. **Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.**

   Menyimpan data di model (basis data) alih-alih melakukan *hard-coding* di dalam berkas template HTML memberikan sejumlah keuntungan krusial:
   - **Pemisahan Peran (*Separation of Concerns*)**: Arsitektur MVT memisahkan dengan tegas antara layer presentasi (*template*) dan layer data/bisnis (*model*). Template hanya bertugas mengatur tata letak semantik dan visual, sementara model bertanggung jawab atas persistensi data.
   - **Kemudahan Pemeliharaan (*Maintainability*)**: Ketika ingin memperbarui informasi proyek (misalnya merevisi teks deskripsi, mengubah thumbnail, atau menambahkan portofolio baru), kita dapat melakukannya secara langsung melalui antarmuka Django Admin (`/admin/`) atau database. Pengembang tidak perlu lagi menyunting kode HTML secara manual, sehingga mengeliminasi risiko rusaknya tag HTML (*unclosed tags*) atau tata letak CSS yang tidak disengaja.
   - **Validasi dan Integritas Data**: Model Django menerapkan validasi tipe data yang ketat (seperti `CharField` dengan batasan `max_length`, `URLField` dengan validasi sintaks URL, `DateTimeField` otomatis, serta `UUIDField` unik). Hal ini menjamin bahwa seluruh data yang masuk konsisten dan terbebas dari inkonsistensi format.
   - **Reusabilitas Data (*Data Reusability*)**: Data yang tersimpan di model dapat digunakan secara fleksibel di berbagai bagian aplikasi tanpa duplikasi. Sebagai contoh, data proyek yang sama dapat ditampilkan pada halaman daftar `/projects/`, disajikan sebagai kartu ringkasan di beranda `/`, diekspor menjadi format JSON untuk API REST bagi aplikasi mobile di masa depan, atau diintegrasikan dengan fitur pencarian dan filter kategori secara instan.
   - **Skalabilitas (*Scalability*)**: Dengan perulangan DTL `{% for %}`, bertambahnya data proyek dari 1 hingga 100 entri tidak akan menambah ukuran baris kode template HTML sama sekali, menjaga ukuran berkas template tetap ringkas dan efisien dibaca.

3. **Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.**

   - **`python manage.py makemigrations`**:
     - *Fungsi*: Bertugas memeriksa definisi kelas model di `models.py` dan mendeteksi perubahan skema yang terjadi (seperti model baru yang ditambahkan, penghapusan model, atau penambahan/pengubahan atribut field), lalu menghasilkan berkas migrasi baru (file Python di direktori `migrations/`, misalnya `0002_project.py`).
     - *Karakteristik*: Perintah ini **belum menyentuh atau mengubah isi basis data fisik**. Berkas migrasi yang terbentuk bertindak sebagai cetak biru (*blueprint*) dan rekam jejak version control atas evolusi skema database dari waktu ke waktu.
   - **`python manage.py migrate`**:
     - *Fungsi*: Bertugas membaca berkas-berkas migrasi yang belum diterapkan (berdasarkan tabel riwayat `django_migrations`), menerjemahkan operasi migrasi tersebut ke dalam instruksi DDL SQL spesifik sesuai DBMS yang digunakan (misalnya perintah `CREATE TABLE`, `ALTER TABLE` pada SQLite), lalu mengeksekusinya langsung ke basis data fisik.
     - *Karakteristik*: Perintah inilah yang secara nyata memperbarui tabel dan kolom fisik di `db.sqlite3` agar strukturnya sinkron dengan kode model.
   - **Contoh Perubahan Model yang Mengharuskan Menjalankan Kedua Perintah**:
     - **Contoh 1 (Pembuatan Model Baru)**: Ketika membuat model baru `Project` di `main/models.py`. Kita harus menjalankan `makemigrations` untuk membuat berkas `0002_project.py` yang berisi operasi `CreateModel`, kemudian menjalankan `migrate` untuk mengeksekusi pembuatan tabel `main_project` di database SQLite.
     - **Contoh 2 (Penambahan Field Baru)**: Jika kemudian kita ingin menambahkan field tautan repositori `github_repo = models.URLField(blank=True, null=True)` pada model `Project`, kita harus menjalankan `makemigrations` untuk membuat migrasi dengan operasi `AddField`, lalu menjalankan `migrate` agar kolom baru tersebut benar-benar ditambahkan ke tabel database fisik melalui perintah `ALTER TABLE`.

### Tugas 3

1. **Jelaskan mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!**

   `ModelForm` menghubungkan form langsung dengan definisi model. Django dapat membentuk field dan widget yang sesuai, menjalankan validasi berdasarkan tipe serta batasan field model, menampilkan pesan error, dan menyimpan hasil validasi melalui `form.save()`. Jika form ditulis manual, pemetaan setiap input, validasi, konversi tipe, dan proses pembuatan atau pembaruan objek perlu ditangani sendiri sehingga kode lebih panjang dan lebih mudah tidak sinkron dengan model.

   `{% csrf_token %}` menambahkan token rahasia ke form yang menggunakan metode `POST`. `CsrfViewMiddleware` membandingkan token tersebut dengan token milik sesi pengguna sebelum menerima perubahan data. Mekanisme ini mencegah situs lain mengirim request berbahaya memakai sesi pengguna tanpa sepengetahuannya. Token dibutuhkan pada form create, update, dan delete karena ketiganya mengubah state aplikasi.

2. **Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?**

   JSON umumnya lebih ringkas karena tidak membutuhkan pasangan tag pembuka dan penutup seperti XML. Struktur object dan array JSON juga langsung sesuai dengan tipe data yang lazim dipakai JavaScript, sehingga respons API lebih mudah diproses oleh browser dan banyak framework frontend. Ukuran payload yang lebih kecil serta ketersediaan parser bawaan di hampir semua bahasa membuat pertukaran data lebih praktis. XML tetap berguna pada sistem yang membutuhkan namespace, schema yang kompleks, atau integrasi lama, tetapi kebutuhan API web pada umumnya dapat dipenuhi dengan lebih sederhana oleh JSON.

3. **Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?**

   Saat `/api/experiences/` diakses, URLconf meneruskan request ke `get_experiences_json`. View mengambil data melalui `Experience.objects.all()` dan menerapkan filter judul bila parameter `title` tersedia. `serializers.serialize("json", experiences)` kemudian mengubah setiap instance model menjadi teks JSON yang memuat nama model, primary key UUID, dan field datanya. Teks tersebut dikirim melalui `HttpResponse` dengan content type `application/json`.

   Serialisasi diperlukan karena instance model dan `QuerySet` adalah objek Python yang juga membawa perilaku ORM; keduanya tidak dapat dikirim secara langsung melalui HTTP. HTTP mengirim byte atau teks, sehingga data harus diubah menjadi format pertukaran yang memiliki representasi standar. Pada halaman `/experience/`, respons JSON tersebut dideserialisasi kembali memakai `serializers.deserialize`, lalu objek hasilnya diberikan ke template agar alur data delivery dan konsumsi JSON dapat terlihat lengkap.

---

## AI Disclosure

### 1. Tools yang Digunakan

- **Google Antigravity** (dengan model Gemini Flash 3.8 High).

### 2. Bagian yang Dibantu AI

- **Tugas 1**:
  - Mengambil dan menyalin struktur devicon SVG dari referensi website live saya di Vercel (fufufarizz.vercel.app).
  - Menghitung keyframes animasi CSS untuk efek marquee looping tanpa putus (`marquee-scroll-left` dan `marquee-scroll-right`).
  - Membantu menyusun urutan perintah Git untuk proses branching `feat/tugas1`, staging, commit berformat conventional commits, dan resolusi merge conflict di branch `main`.
- **Tugas 2**:
  - Merancang arsitektur Model-View-Template (MVT) untuk bagian portofolio baru (`Project`), mencakup pembuatan model `Project` dengan field UUID, judul, kategori, deskripsi, thumbnail, dan link proyek.
  - Membantu eksekusi migrasi database Django (`makemigrations` dan `migrate`) serta pendaftaran model ke Django Admin.
  - Membuat fungsi controller `show_projects` pada `main/views.py`, rute bernama `show_projects` pada `main/urls.py`, dan template terpisah `templates/projects.html` dengan loop DTL serta penanganan *empty state*.
  - Menyusun 10 unit test komprehensif pada `main/tests.py` untuk menguji fungsionalitas URL, template, rendering data dinamis, empty state, dan integritas navigasi navbar.
  - Membantu memformulasikan penjelasan alur request-response Django MVT dan perbedaan `makemigrations` vs `migrate` untuk pertanyaan reflektif.
- **Tugas 3**:
  - Mengaudit template, model, form, view, URL, test, dan dokumentasi yang telah ada sebelum melakukan perubahan.
  - Membuat `ExperienceForm`, alur create/update/delete Experience, endpoint JSON, dan proses deserialisasi untuk tampilan halaman.
  - Merefactor modal hapus Project menjadi partial generik yang juga dipakai Experience serta memastikan semua halaman penuh mewarisi `base.html`.
  - Menambahkan automated test untuk alur normal, data tidak valid, proteksi method delete, filtering JSON, dan template inheritance.
  - Membantu merapikan tatanan bahasa pada dokumentasi, jawaban reflektif, serta AI disclosure yang spesifik terhadap perubahan kode.

### 3. Strategi Prompting

- Menggunakan instruksi terarah dan bertahap (*step-by-step*).
- Menetapkan batasan ketat sejak awal: melarang AI melakukan commit mandiri ke repositori Git, mewajibkan arsitektur MVT yang bersih dan modular, serta menjaga navbar dan footer tetap konsisten.
- Memanfaatkan website live saya di Vercel (fufufarizz.vercel.app) sebagai acuan referensi data proyek dan estetika visual.
- Untuk Tugas 3, memberikan checklist fitur dan rubrik penilaian lengkap agar AI dapat memetakan setiap perubahan kode ke kriteria yang harus diverifikasi.

### 4. Analisis Kritis & Perbaikan Mandiri

- **Keterbatasan AI yang Ditemukan**:
  - Pada percobaan awal di Tugas 1, AI cenderung menyertakan dependensi JavaScript (seperti GSAP untuk tab switcher dan Lenis untuk scroll) serta menambahkan kartu proyek dengan aset gambar lokal yang sempat menyebabkan broken image di browser.
  - AI sempat menghasilkan typo URL pada tautan GitHub (`https://https://github.com/...`).
  - AI berpotensi membuat commit otomatis jika tidak dibatasi secara tegas dalam prompt perintah.
  - Solusi awal AI perlu diperiksa kembali karena refactor yang terlalu luas dapat menambah kompleksitas tanpa meningkatkan pemenuhan checklist.
  - Browser terintegrasi tidak tersedia ketika Tugas 3 diverifikasi, sehingga pengecekan runtime dilanjutkan melalui request HTTP ke server lokal dan Django test client.
- **Perbaikan Manual yang Dilakukan**:
  - Menginstruksikan AI untuk membuat rencana implementasi terlebih dahulu (*implementation plan*) dan melarang tindakan commit Git otomatis agar saya memegang kendali penuh atas riwayat commit repositori.
  - Memastikan data proyek yang dimasukkan ke database selaras dengan aset lokal yang telah disiapkan di `static/img/projects/`.
  - Memverifikasi secara langsung kelulusan seluruh unit test (`python manage.py test`) dan fungsionalitas lokal di browser (`python manage.py runserver`).
  - Menjaga model `Experience` yang sudah sesuai kebutuhan agar tidak membuat migrasi skema yang tidak diperlukan, lalu memusatkan perubahan pada form, view, route, template, dan test.

### 5. Log Prompt Utama (ril aseli no fek fek)

1. *"browser fufufarizz.vercel.app, Berikut saya berikan referensi website dari hasil akhir portofolio website pada source code di tahap 10 (sekarang masih tahap 1, ikuti sesuai tahap) Berikan implementation plannya. Tahap 1: Lanjutkan halaman “About Me” yang sudah dibuat. Tambahkan satu atau lebih section baru ke halaman yang sama, masih murni dengan HTML5 dan CSS3 (belum ada database/MVT). Pilihan saya, saya ingin anda menambahkan section get to know me persis seperti screenshot yang saya berikan dari website referensi. Karena tugas ini sifatnya lebih bebas, kamu dipersilakan membuat tampilan CSS berbeda dari referensi di website - tambahkan animasi, layout grid, atau elemen visual lain sesuai kreativitasmu, selama tetap rapi dan responsif. Satu pesan saya, buat kode html dan css yang mudah dimengerti, tidak bertele tele, dan tulis kode dengan rapi. Pastikan kode yang dibuat tidak mengada ngada agar saya dapat tetap mengerti apa yang ditulis. Desain visual (warna, font, tata letak, dsb.) bebas diubah, desain seluruh halaman “About Me”, bukan cuma section barunya, asal tetap murni HTML5 dan CSS3, terstruktur rapi, dan checklist di bawah tetap terpenuhi. Checklist minimal untuk tugas ini: -Minimal satu section baru ditambahkan ke halaman yang sama. -Section baru tersebut punya isi yang nyata (bukan lorem ipsum atau placeholder kosong), samakan saja dengan website referensi -Halaman tetap terlihat rapi di lebar layar desktop maupun mobile. -Proyek berhasil dijalankan dengan python manage.py runserver tanpa error."*
2. *"Cek website yang saya berikan, saya ingin anda mengcopy seluruh bagian pada Passion, benar benar copy semuanya sama persis. Untuk Element/gambar pada bagian projects, saya telah menaruh sourcenya di img/projects. Proceed dengan revisi: Jangan menggunakan javascript, tambahkan murni html dan css nya saja. bila terdapat kode/fitur yang membutuhkan javascript maka di skip dulu"*
3. *"Commit text: Jangan ubah kode ataupun melakukan commit. Saya ingin melakukan branching di git dan melakukan commit satu persatu, mulai dari bagian get to know me dan bagian cards. Untuk itu, saya ingin anda membuatkan copy writing dengan lengkap dengan format git checkout -b ..., git add ..., git commit -m "..." hingga git push ... saya ingin melakukan 3 commit 1. pembuatan get to know me 2. pembuatan cards 3, penggantian teks lorem ipsum cukup berikan copywritingnya, untuk kode card biar saya yang hapus dahulu untuk commit get to know me, untuk penggantian teks lorem ipsum juga biar saya yang ganti secara mandiri."*
4. *"pastikan komentar penjelasan pada setiap kode yang dibuat bersifat natural dan tidak slop... Begitupun untuk AI disclosure, pastikan bahasa yang dibuat natural dan tidak AI slop"*
5. *"/browser fufufarizz.vercel.app, Saya memberikan link browser sebagai referensi tahap 10 tugas yang sudah jadi, sedangkan sekarang, saya meminta anda untuk menyelesaikan tahap 2. Berikut saya berikan perintah dan tahapan yang harus anda kerjakan untuk menyelesaikan tugas tahap 2. Tugas: Terapkan pola Model-View-Template (MVT)... Buatkan implementation plannya, jangan melakukan commit apapun secara mandiri."*
6. *"Refactor seluruh berkas HTML identik agar extend template utama, lalu terapkan Create Form, Update Form, Data Deletion, JSON Data Delivery, dan tampilan hasil deserialisasi untuk satu bagian portofolio lain. Pastikan proyek dapat dijalankan tanpa error."*