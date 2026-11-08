# Portofolio Personal - Faris Salman Azhari

**Nama:** Faris Salman Azhari
**NPM:** 2506615223
**Kelas:** PBP F

---

## Deskripsi Proyek

Website portofolio personal berbasis Django yang dibangun menggunakan HTML5 semantik, CSS3, dan JavaScript modular. Website ini menyajikan profil, daftar proyek, pengalaman, dan keahlian teknologi. Halaman Projects dan Experience menggunakan Django REST Framework untuk pertukaran data dan Fetch API untuk interaksi tanpa reload. Model, database, relasi star, serta form dari tugas sebelumnya tetap digunakan. Seluruh halaman memakai template induk yang sama agar navigasi, pesan, metadata dasar, dan footer tetap konsisten.

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

- [X] **Template Inheritance**: Seluruh halaman HTML penuh menggunakan `{% extends "base.html" %}` sehingga struktur navigasi, pesan, dan footer tidak diduplikasi.
- [X] **`ExperienceForm`**: Membuat `ModelForm` dengan field `title`, `description`, `category`, dan `thumbnail` yang mencakup input teks, textarea, pilihan kategori, dan validasi URL; `id`, `started_at`, serta `ended_at` tidak dapat diubah melalui form.
- [X] **Create & Update**: Menambahkan halaman tambah dan ubah Experience dengan validasi bawaan Django, form yang terisi otomatis saat update, CSRF token, pesan sukses, dan redirect setelah penyimpanan.
- [X] **Delete**: Menambahkan penghapusan Experience melalui request `POST`, CSRF token, dan modal konfirmasi; request `GET` ditolak dengan status `405 Method Not Allowed`.
- [X] **JSON Data Delivery**: Menambahkan endpoint `/api/experiences/` yang mendukung filter judul dan mengembalikan hasil serialisasi model dengan content type `application/json`.
- [X] **JSON Deserialization**: Pada iterasi Tugas 3, halaman `/experience/` mendeserialisasikan response endpoint JSON menjadi objek `Experience`; alur ini kemudian digantikan oleh Fetch API pada Tugas 5.
- [X] **UI/UX Tambahan**: Menambahkan pencarian Experience, empty state khusus hasil pencarian, thumbnail opsional, tombol aksi responsif, dan pesan keberhasilan operasi.
- [X] **Automated Testing**: Menambahkan pengujian form field, template inheritance, validasi create, prefilled update, penyimpanan update, proteksi delete, endpoint JSON, filter, dan render hasil deserialisasi.
- [X] **Verifikasi Akhir**: Test untuk cakupan Tugas 3 lulus, `manage.py check` tidak menemukan masalah, dan server lokal merespons halaman Experience serta endpoint JSON dengan status `200`.

### Endpoint Tugas 3

| Method            | Endpoint                        | Fungsi                                               |
| ----------------- | ------------------------------- | ---------------------------------------------------- |
| `GET`           | `/experience/`                | Menampilkan Experience dari hasil deserialisasi JSON |
| `GET`, `POST` | `/experience/add/`            | Menampilkan dan memproses form create                |
| `GET`, `POST` | `/experience/<uuid>/edit/`    | Menampilkan dan memproses form update                |
| `POST`          | `/experience/<uuid>/delete/`  | Menghapus satu Experience                            |
| `GET`           | `/api/experiences/`           | Mengirim semua Experience dalam format JSON          |
| `GET`           | `/api/experiences/?title=...` | Mengirim Experience yang judulnya cocok              |

---

## Progres Pengerjaan (Tugas 4)

- [X] **Empat Peran Pengguna**: Menerapkan pengunjung, pengguna biasa, Editor berbasis Django Group, dan pemilik portofolio (`is_superuser`).
- [X] **Proteksi Server-Side**: Menggunakan decorator akses reusable agar pengguna anonim diarahkan ke login dan pengguna terautentikasi tanpa hak menerima `403 Forbidden`.
- [X] **Hak Editor**: Editor dapat mengubah Experience, tetapi tidak dapat membuat atau menghapusnya.
- [X] **Kontrol Template**: Tombol tambah, ubah, dan hapus hanya dirender untuk peran yang berhak; navbar menampilkan badge peran aktif.
- [X] **Star Experience**: Menambahkan relasi `ManyToManyField` ke `User`, toggle berbasis `POST`, CSRF token, jumlah star, serta status Star/Unstar per pengguna.
- [X] **Integritas API**: Endpoint JSON Experience menggunakan natural foreign key sehingga menampilkan username pemberi star tanpa mengekspos ID internal pengguna.
- [X] **Keamanan Tambahan**: Endpoint toggle menolak `GET`, cookie `last_login` memakai `HttpOnly` dan `SameSite=Lax`, serta redirect `next` hanya menerima host yang aman.
- [X] **Pengujian Otomatis**: Menambahkan test matriks empat peran, request POST langsung, CSRF, star/unstar, visibilitas kontrol, dan keamanan serialisasi JSON.

### Matriks Hak Akses Experience

| Peran                      | Baca | Star/Unstar      | Tambah | Ubah  | Hapus |
| -------------------------- | ---- | ---------------- | ------ | ----- | ----- |
| Pengunjung                 | Ya   | Login diperlukan | Tidak  | Tidak | Tidak |
| Pengguna biasa             | Ya   | Ya               | Tidak  | Tidak | Tidak |
| Editor                     | Ya   | Ya               | Tidak  | Ya    | Tidak |
| Pemilik (`is_superuser`) | Ya   | Ya               | Ya     | Ya    | Ya    |

### Menetapkan Akun Editor

1. Jalankan `python manage.py migrate`; migration data akan memastikan group `Editor` tersedia.
2. Login sebagai superuser dan buka `/admin/`.
3. Buka menu **Users**, pilih akun yang akan menjadi editor, masukkan group `Editor` pada bagian **Groups**, lalu simpan.
4. Akun tersebut akan memperoleh tombol **Ubah** pada halaman Experience tanpa memperoleh tombol tambah atau hapus. Jika group belum muncul pada instalasi lama, buat melalui menu **Groups** dengan nama persis `Editor`.

### Endpoint Tugas 4

| Method            | Endpoint                       | Hak akses                                |
| ----------------- | ------------------------------ | ---------------------------------------- |
| `POST`          | `/experience/<uuid>/star/`   | Semua pengguna yang sudah login          |
| `GET`, `POST` | `/experience/<uuid>/edit/`   | Editor dan superuser                     |
| `GET`, `POST` | `/experience/add/`           | Superuser                                |
| `POST`          | `/experience/<uuid>/delete/` | Superuser                                |
| `GET`           | `/api/experiences/`          | Publik; relasi pengguna memakai username |

Setelah mengambil perubahan terbaru, jalankan `python manage.py migrate` untuk membuat tabel relasi star Experience, kemudian verifikasi dengan `python manage.py test` dan `python manage.py runserver`.

---

## Progres Pengerjaan (Tugas 5)

- [X] **Experience dengan AJAX**: Halaman `/experience/` hanya merender kerangka, lalu mengambil kartu Experience dari endpoint JSON menggunakan `fetch()` tanpa reload.
- [X] **JSON Manual dan Star**: Endpoint menyusun `JsonResponse` secara manual serta menyertakan jumlah star, status star pengguna aktif, dan username pemberi star.
- [X] **State Antarmuka**: Menyediakan tampilan loading, hasil kosong, dan error yang saling eksklusif.
- [X] **Pencarian Debounce**: Pencarian judul berjalan lewat AJAX dengan jeda 300 ms dan membatalkan request sebelumnya menggunakan `AbortController`.
- [X] **Modal Tambah AJAX**: Superuser dapat menambahkan Experience melalui modal, menerima respons JSON `201`, `400`, atau `403`, dan melihat daftar diperbarui tanpa reload.
- [X] **CSRF dan Hak Akses**: Request POST mengirim header `X-CSRFToken`; view tetap memeriksa `is_superuser` sehingga menyembunyikan tombol bukan satu-satunya pengamanan.
- [X] **Toast**: Keberhasilan, kegagalan jaringan, dan pesan validasi server ditampilkan melalui komponen toast reusable.
- [X] **Perlindungan XSS**: Input teks dibersihkan dengan `strip_tags` pada method `clean_<field>` di `ExperienceForm`; JavaScript membuat elemen DOM dengan `textContent` dan memvalidasi URL gambar.
- [X] **Modularisasi**: Helper `getCookie`, `escapeHtml`, dan `safeWebUrl` dipusatkan di `static/js/ajax-utils.js`; logika Experience dipisahkan ke `static/js/experience.js`.
- [X] **Automated Testing**: Seluruh 71 test lulus, mencakup JSON dan metadata star, pencarian, status HTTP AJAX, izin, CSRF, sanitasi XSS, modal berbasis peran, state UI, dan guard JavaScript.

### Endpoint Tugas 5

| Method            | Endpoint                        | Fungsi dan hak akses                                                 |
| ----------------- | ------------------------------- | -------------------------------------------------------------------- |
| `GET`           | `/experience/`                | Kerangka halaman Experience; dapat diakses publik                    |
| `GET`           | `/api/experiences/?title=...` | Data JSON manual dan pencarian; dapat diakses publik                 |
| `POST`          | `/experience/add-ajax/`       | Menambah Experience; hanya superuser, respons`201`/`400`/`403` |
| `POST`          | `/experience/<uuid>/star/`    | Toggle star; pengguna harus login                                    |
| `GET`, `POST` | `/experience/<uuid>/edit/`    | Mengubah Experience; Editor dan superuser                            |
| `POST`          | `/experience/<uuid>/delete/`  | Menghapus Experience; hanya superuser                                |

---

## Progres Pengerjaan (Tugas 6)

Tugas ini melanjutkan **Experience** dari Tugas 3–5. API dan halaman **Projects** dari Tutorial 07 tetap dipertahankan; implementasi tutorial sudah tersedia pada riwayat commit sampai `5156433` (3 November 2026). Tidak ada model pengganti, penghapusan data lama, atau migrasi skema baru.

- [X] **Serializer**: Membuat `ExperienceSerializer` di `main/serializers.py` dengan daftar field eksplisit. `id`, tanggal, label kategori, status berlangsung, dan metadata star bersifat read-only.
- [X] **Validasi**: Membersihkan judul dan deskripsi melalui `validate_<field>` dan `strip_tags`, menolak teks yang kosong setelah dibersihkan, memvalidasi pilihan kategori, serta membatasi URL thumbnail ke HTTP/HTTPS.
- [X] **Privasi**: Hanya menampilkan informasi publik; email, password hash, dan ID internal akun pemberi star tidak dikirim ke klien.
- [X] **Empat Peran**: Menggunakan `IsPortfolioOwnerOrEditorOrReadOnly` dengan pemeriksaan Editor yang sama seperti view lama. Pengunjung dan pengguna biasa dapat membaca, tetapi tidak dapat menambah, mengubah, atau menghapus data; Editor dapat PUT/PATCH; superuser dapat melakukan seluruh CRUD.
- [X] **Star**: Menggunakan `IsAuthenticated`; akun pemberi star selalu berasal dari `request.user`, tanpa mempercayai ID akun dari payload.
- [X] **API dan URL**: Menambahkan function-based API view dengan `@api_view`, `SessionAuthentication`, serta nama URL unik di bawah `/api/v1/experiences/`.
- [X] **Status HTTP**: Menggunakan `201` untuk create, `400` untuk validasi, `403` untuk penolakan akses, `404` untuk objek yang tidak ditemukan, dan `204` tanpa body untuk delete.
- [X] **Integrasi Halaman**: Daftar, pencarian, tambah, star/unstar, ubah dengan modal PATCH, serta hapus dengan DELETE berjalan melalui API baru tanpa reload.
- [X] **CSRF dan XSS**: Semua mutasi mengirim `X-CSRFToken`; cookie CSRF juga tersedia bagi pengguna biasa dan Editor. Teks kartu, toast, dan error menggunakan `textContent`, sedangkan URL gambar divalidasi sebelum dipasang.
- [X] **UI/UX Tambahan**: Filter kategori dan status dapat digabung dengan pencarian, disimpan di URL agar dapat dibagikan, serta dilengkapi jumlah hasil dan tombol reset. Tersedia tombol coba lagi ketika gagal memuat data, error di dekat field, fokus ke field invalid, dan tombol simpan yang dinonaktifkan selama request.
- [X] **Optimasi Query**: Mengambil relasi star dengan `Prefetch` yang hanya memuat ID dan username. Ketiga field star memakai cache yang sama sehingga daftar berisi banyak kartu tetap membutuhkan dua query data.
- [X] **Pengujian API**: Menambahkan `APITestCase` untuk empat peran, pemeriksaan isi database pada request yang ditolak, PUT/PATCH, sanitasi, field read-only, privasi, star, 404, 405, serta jumlah query.
- [X] **Pengujian CSRF Sesi**: Memakai `APIClient(enforce_csrf_checks=True)` dan `.login()` untuk membuktikan seluruh jenis mutasi ditolak tanpa token atau dengan token salah, lalu diterima dengan token yang benar.
- [X] **Verifikasi Eksekusi**: `python manage.py test main` lulus **111 test**, termasuk 27 test API Experience baru dan test Tutorial 07. `manage.py check` bersih dan pemeriksaan migrasi tidak mendeteksi perubahan skema.
- [X] **Verifikasi Browser**: Alur empat peran, CRUD/star tanpa reload, error 400/403, filter, serta retry jaringan lulus pemeriksaan browser pada database uji terpisah tanpa error JavaScript. Tampilan desktop dan mobile 390 px diperiksa; server dengan konfigurasi asli juga merespons halaman utama, Experience, Projects, dan kedua API dengan `200`.
- [X] **Dokumentasi**: Melengkapi empat jawaban reflektif, langkah setup/verifikasi, pemetaan endpoint, analisis bantuan AI, dan prompt ke-7 yang membahas konsep.

### Menjalankan dan Memeriksa Tugas 6

Gunakan virtual environment dan dependency proyek yang sama. Setelah mengaktifkannya, jalankan:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test main
python manage.py runserver
```

Tidak ada migrasi Experience baru untuk tugas ini; `migrate` tetap diperlukan pada instalasi baru agar tabel dan group `Editor` dari tugas sebelumnya tersedia. Untuk pengujian manual, buat pemilik dengan `python manage.py createsuperuser`, daftarkan akun biasa melalui `/register/`, lalu masukkan akun Editor ke group `Editor` melalui `/admin/`.

Buka `/experience/` untuk alur AJAX dan `/api/v1/experiences/` untuk Browsable API. Login melalui `/login/` atau `/api-auth/login/` agar API menggunakan sesi yang sama. Halaman `/projects/` dan `/api/v1/projects/` tetap memakai implementasi Tutorial 07. Route form dan JSON lama dipertahankan untuk kompatibilitas serta pengujian tugas sebelumnya; halaman Experience yang baru mengambil data dari API DRF.

### Endpoint Tugas 6

| Method | Endpoint | Hak akses dan hasil |
| ------ | -------- | ------------------- |
| `GET` | `/api/v1/experiences/` | Publik; daftar berupa array JSON |
| `GET` | `/api/v1/experiences/?title=mentor&category=volunteer&status=ongoing` | Publik; kombinasi pencarian judul, kategori, dan status |
| `POST` | `/api/v1/experiences/` | Superuser; membuat data (`201`) |
| `GET` | `/api/v1/experiences/<uuid>/` | Publik; detail data (`200`) |
| `PUT` | `/api/v1/experiences/<uuid>/` | Editor/superuser; mengganti seluruh field yang dapat ditulis (`200`) |
| `PATCH` | `/api/v1/experiences/<uuid>/` | Editor/superuser; mengubah field yang dikirim (`200`) |
| `DELETE` | `/api/v1/experiences/<uuid>/` | Superuser; menghapus data (`204`, body kosong) |
| `POST` | `/api/v1/experiences/<uuid>/star/` | Semua akun yang login; toggle star akun tersebut (`200`) |

Field input: `title`, `description`, `category`, dan `thumbnail`. Pada PUT, tiga field pertama wajib dikirim; thumbnail yang tidak dikirim kembali menjadi string kosong. PATCH mempertahankan field yang tidak dikirim. Tanggal tetap dikelola seperti pada form tugas sebelumnya. Parameter `status` menerima `ongoing` atau `completed`; tanpa filter, semua status ditampilkan.

Contoh payload tambah atau PUT:

```json
{
  "title": "Mentor Pemrograman",
  "description": "Mendampingi peserta belajar Python dan Django.",
  "category": "volunteer",
  "thumbnail": "https://example.com/mentor.jpg"
}
```

Respons menggunakan struktur datar (`id`, `title`, dan seterusnya), berbeda dari format `pk`/`fields` pada JSON lama. Error validasi berbentuk daftar pesan per field, misalnya `{"title": ["This field is required."]}`; penolakan izin memakai key `detail`. JavaScript menangani keduanya melalui helper request yang sama.

### Alur Verifikasi Manual

1. Sebagai pengunjung, buka daftar dan Browsable API. Tombol star mengarahkan ke login; kontrol tambah, ubah, dan hapus tidak ditampilkan.
2. Login sebagai pengguna biasa, klik star lalu unstar. Jumlah dan status star berubah tanpa reload.
3. Login sebagai Editor, klik **Ubah**, periksa data yang terisi otomatis, lalu simpan. Data berubah melalui PATCH; kontrol tambah dan hapus tidak tersedia.
4. Login sebagai pemilik, tambah data, ubah, dan hapus setelah konfirmasi. Coba kirim judul kosong untuk melihat error field dan toast tanpa kehilangan isi form.
5. Gabungkan pencarian dan filter, salin URL, lalu buka ulang. Filter tetap terpilih. Gunakan **Reset** untuk kembali ke seluruh daftar.
6. Periksa `/projects/` untuk memastikan fitur Tutorial 07 tetap berjalan. Cakupan otomatis juga memeriksa akses dan Browsable API Projects.

### Git dan Pengumpulan

Perubahan Tugas 6 disiapkan pada branch `feat/tugas6`. Pembagian commit yang disarankan mengikuti bagian implementasinya:

1. `feat(api): add Experience serializer permissions and DRF endpoints` — serializer, permission, API view, dan URL.
2. `feat(experience): connect CRUD and star to DRF with filters` — view halaman, template, JavaScript, dan CSS.
3. `test(experience): cover roles validation session CSRF and query count` — test API dan penyesuaian test halaman ke endpoint baru.
4. `docs: document assignment 6 progress API and reflections` — README.

Langkah pengumpulan tetap perlu diselesaikan setelah perubahan ditinjau:

- [ ] Membuat commit bertahap dengan pesan deskriptif pada branch fitur.
- [ ] Push hasil akhir ke repository GitHub publik, lalu memastikan tautan commit dapat dibuka.
- [ ] Mengumpulkan **tautan commit akhir**, bukan hanya URL repository, melalui SCELE paling lambat **9 November 2026 pukul 23.59 WIB**. Prasyarat pengumpulan Tutorial 07 mengikuti ketentuan kelas, dengan tenggat **4 November 2026 pukul 23.59 WIB**.

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
4. **Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?**

   **Jawaban:**
   Tantangan utamanya adalah menjaga alur baca tetap natural saat layout berpindah dari multi-kolom ke satu kolom:

   - **Urutan Visual Hero**: Pada desktop, foto profil berada di kolom kanan sejajar dengan nama dan bio. Di layar mobile, foto harus diletakkan di antara nama dan bio agar pengguna langsung melihat identitas visual sebelum membaca teks panjang. Saya menyelesaikannya menggunakan `grid-template-areas` yang didefinisikan ulang di dalam `@media (max-width: 600px)`.
   - **Skalabilitas Marquee**: Kartu teknologi pada marquee berukuran 160x120px di desktop. Di mobile (`max-width: 480px` dan `360px`), ukuran kartu dikecilkan proporsional menjadi 110x90px dan 90x80px agar tidak memenuhi layar secara berlebihan.
   - **Evaluasi Prioritas**: Elemen informasi primer (nama, deskripsi, tautan kontak) selalu diprioritaskan agar mudah dibaca dan di-tap. Elemen dekoratif atau sekunder disederhanakan ruang dan padding-nya agar tidak menimbulkan horizontal overflow.
5. **Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?**

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

   Pada implementasi Tugas 3, saat `/api/experiences/` diakses, URLconf meneruskan request ke `get_experiences_json`. View mengambil data melalui `Experience.objects.all()` dan menerapkan filter judul bila parameter `title` tersedia. `serializers.serialize("json", experiences)` kemudian mengubah setiap instance model menjadi teks JSON yang memuat nama model, primary key UUID, dan field datanya. Teks tersebut dikirim melalui `HttpResponse` dengan content type `application/json`.

   Serialisasi diperlukan karena instance model dan `QuerySet` adalah objek Python yang juga membawa perilaku ORM; keduanya tidak dapat dikirim secara langsung melalui HTTP. HTTP mengirim byte atau teks, sehingga data harus diubah menjadi format pertukaran yang memiliki representasi standar. Pada Tugas 5, mekanisme ini dikembangkan lebih lanjut menjadi `JsonResponse` manual agar metadata star dapat dibentuk secara eksplisit dan dikonsumsi langsung oleh JavaScript.

### Tugas 5

1. **Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!**

   *Debouncing* adalah teknik menunda pemanggilan fungsi sampai pengguna berhenti memicu sebuah event selama interval tertentu. Pada pencarian Experience, setiap event `input` membatalkan timer sebelumnya dan membuat timer 300 ms yang baru. Request baru hanya dikirim ketika pengguna berhenti mengetik selama jeda tersebut. Teknik ini mencegah satu request untuk setiap karakter, mengurangi beban server dan jaringan, menghindari perubahan hasil yang terlalu sering, serta membuat antarmuka lebih stabil. `AbortController` turut membatalkan request lama agar respons yang terlambat tidak menimpa hasil pencarian terbaru.
2. **Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?**

   `fetch()` langsung mengembalikan `Promise`, bukan objek respons yang sudah berisi data. `await fetch(...)` menahan eksekusi di dalam fungsi `async` sampai request selesai dan menghasilkan objek `Response`. Hal yang sama berlaku pada `await response.json()`, yang menunggu body selesai dibaca dan diparse. Tanpa `await`, variabel masih berisi `Promise`; akses seperti `response.ok` atau iterasi data tidak akan bekerja sebagaimana mestinya. Kode tetap dapat ditulis tanpa `await`, tetapi harus memakai rantai `.then()` dan `.catch()` untuk mengatur urutan serta penanganan error secara eksplisit.
3. **Jelaskan apa itu serangan XSS (*Cross-Site Scripting*) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!**

   XSS adalah serangan ketika input penyerang diperlakukan sebagai HTML atau JavaScript aktif di browser korban, misalnya atribut `onerror` pada tag gambar. Template Django melakukan *auto-escaping* terhadap variabel secara default, sedangkan JavaScript dapat melewati perlindungan itu apabila data AJAX mentah dimasukkan melalui `innerHTML`. Karena itu implementasi Experience memakai `textContent` untuk semua teks, memvalidasi skema URL sebelum memasang `src`, dan membersihkan input di server dengan `strip_tags`. Pertahanan berlapis ini memastikan payload seperti `<img src="x" onerror="alert('XSS!')">` tidak dieksekusi.

---

### Tugas 6

1. **Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan!**

   REST adalah gaya arsitektur untuk mengatur komunikasi antara klien dan server melalui resource dan representasinya. JSON hanya format data. Endpoint yang mengembalikan JSON, tetapi memakai GET untuk menghapus data, belum menerapkan semantik HTTP dengan benar. REST juga mencakup antarmuka yang konsisten, pemisahan klien dan server, statelessness, cacheability, dan sistem berlapis.

   Di proyek saya, `/api/v1/experiences/<uuid>/` mewakili satu Experience, sementara method menyatakan tindakan terhadapnya. PUT saya gunakan ketika klien mengirim seluruh data yang dapat diedit: judul, deskripsi, kategori, dan thumbnail opsional. PATCH cocok ketika hanya judul yang berubah, misalnya `{"title": "Asisten Dosen PBP"}`, sehingga deskripsi dan kategori tetap dipertahankan. Saya juga tidak menyebut implementasi ini REST murni: autentikasinya masih memakai sesi server dan endpoint `/star/` berbentuk aksi. Kontrak resource, method, dan statusnya tetap dibuat konsisten.

2. **Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial 05?**

   Serializer menjadi penghubung antara objek model dan representasi data API. Pada alur baca, `ExperienceSerializer` mengubah objek menjadi tipe data yang kemudian dirender sebagai JSON. Pada alur tulis, serializer memeriksa input, menghasilkan `validated_data`, dan menyimpan data yang valid melalui `.save()`.

   Pada Tugas 5 saya merakit dictionary dan metadata star di view, sedangkan validasi bergantung pada form. Dengan DRF, daftar field, validasi teks, serta field hasil perhitungan dikumpulkan di serializer yang sama untuk list, detail, create, dan update. Ini mengurangi kemungkinan format respons antarlayanan berbeda. Field read-only juga membuat klien tidak bisa menentukan jumlah star atau ID objek sendiri. Error per field langsung dapat dipakai toast dan form. Referensi: [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/).

3. **Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?**

   Autentikasi menjawab siapa yang mengirim request. Di proyek ini, `SessionAuthentication` mengenali akun dari sesi login dan mengisi `request.user`. Otorisasi menentukan tindakan yang boleh dilakukan akun itu. Sebagai contoh, Editor berhasil dikenali sebagai pengguna yang login, tetapi hanya diizinkan PUT/PATCH pada Experience, bukan POST untuk membuat atau DELETE untuk menghapus.

   Menyembunyikan tombol membantu pengguna memahami haknya, tetapi tidak membatasi request HTTP. Pengguna tetap bisa mengirim DELETE langsung melalui alat lain. Karena itu, `IsPortfolioOwnerOrEditorOrReadOnly` harus menolak request tersebut di server sebelum data diubah. Endpoint star mempunyai aturan terpisah melalui `IsAuthenticated`, dan pemilik star selalu diambil dari `request.user`. Pada test penolakan, saya memeriksa status `403` sekaligus isi database agar penolakan benar-benar tidak menyimpan perubahan.

4. **Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication! Mengapa test yang memakai force_authenticate tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?**

   Browser menyertakan cookie sesi secara otomatis pada request yang memenuhi aturan cookie. Identitas yang sah saja belum membuktikan bahwa request berasal dari halaman yang memang dibuka pengguna. Token CSRF membantu server memeriksa hal tersebut sebelum menerima POST, PUT, PATCH, atau DELETE. Karena frontend dan API memakai sesi yang sama, request Fetch saya tetap mengirim header `X-CSRFToken`. Bentuk body JSON tidak menggantikan pemeriksaan ini. Referensi: [DRF SessionAuthentication](https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication).

   `force_authenticate` memasang pengguna uji dengan melewati autentikasi normal, sehingga test yang sukses belum menguji jalur sesi dan CSRF sebenarnya. Saya memakai `APIClient(enforce_csrf_checks=True)` dan `.login()`, mengambil cookie CSRF dari halaman Experience, lalu membandingkan request tanpa token, token salah, dan token benar. Dua skenario pertama harus mendapat `403` tanpa perubahan database; skenario terakhir harus berhasil. Referensi: [DRF CSRF Testing](https://www.django-rest-framework.org/api-guide/testing/#csrf-validation).

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
- **Tugas 4**:
  - Membaca rubrik dan memetakan setiap butir penilaian ke model, view, URL, template, migrasi, serta test yang relevan.
  - Membuat pemeriksaan peran reusable untuk superuser dan anggota group `Editor`, termasuk perilaku redirect login dan `403 Forbidden`.
  - Menambahkan star pada Experience, komponen tombol star reusable, natural foreign key pada JSON, serta indikator peran pada UI.
  - Menyusun test matriks pengunjung, pengguna biasa, Editor, dan superuser, termasuk test CSRF dan request mutasi langsung.
- **Tugas 5**:
  - Membaca PDF tugas dan memetakan checklist serta rubrik ke perubahan view, form, URL, template, JavaScript, test, dan README.
  - Mengubah Experience menjadi alur AJAX end-to-end, membuat endpoint JSON manual, modal tambah, pencarian debounce, state UI, toast, CSRF, dan perlindungan XSS.
  - Mengaudit pemakaian source code, memusatkan helper AJAX yang duplikatif, serta menghapus partial dan CSS yang tidak lagi memiliki pemakai.
  - Menambah test regresi dan test khusus Tugas 5 sebelum verifikasi `manage.py check`, migrasi, test suite, dan server lokal.

- **Tugas 6**:
  - Memetakan rubrik tugas ke implementasi Experience sambil mempertahankan model, data, kontrol peran, dan API Projects dari Tutorial 07.
  - Membantu menyusun serializer, permission, API view berbasis fungsi, serta integrasi CRUD dan star melalui Fetch API.
  - Membantu menambahkan filter, penanganan error field, dan optimasi prefetch untuk metadata star.
  - Membantu menulis pengujian izin dengan pemeriksaan database, validasi, privasi, query, serta CSRF melalui sesi login; jawaban reflektif dikaitkan dengan keputusan kode yang bisa diperiksa.

### 3. Strategi Prompting

- Menggunakan instruksi terarah dan bertahap (*step-by-step*).
- Menetapkan batasan ketat sejak awal: melarang AI melakukan commit mandiri ke repositori Git, mewajibkan arsitektur MVT yang bersih dan modular, serta menjaga navbar dan footer tetap konsisten.
- Memanfaatkan website live saya di Vercel (fufufarizz.vercel.app) sebagai acuan referensi data proyek dan estetika visual.
- Untuk Tugas 3, memberikan checklist fitur dan rubrik penilaian lengkap agar AI dapat memetakan setiap perubahan kode ke kriteria yang harus diverifikasi.
- Untuk Tugas 4, meminta AI membaca PDF dan rubrik terlebih dahulu, mengaudit implementasi Tutorial 04 yang sudah ada, lalu membuktikan setiap aturan akses melalui automated test.
- Untuk Tugas 5, memberikan batasan agar AI hanya mengimplementasikan instruksi PDF, menghapus kode hanya jika terbukti redundan/tidak terpakai.
- Untuk Tugas 6, membahas konsep REST, PUT/PATCH, serializer, serta sesi dan CSRF dengan contoh Experience. Hasil penjelasan dicocokkan dengan kode, dokumentasi resmi, dan perilaku test; AI tidak dijadikan sumber kebenaran tunggal.

### 4. Analisis Kritis & Perbaikan Mandiri

- **Keterbatasan AI yang Ditemukan**:
  - Pada percobaan awal di Tugas 1, AI cenderung menyertakan dependensi JavaScript (seperti GSAP untuk tab switcher dan Lenis untuk scroll) serta menambahkan kartu proyek dengan aset gambar lokal yang sempat menyebabkan broken image di browser.
  - AI sempat menghasilkan typo URL pada tautan GitHub (`https://https://github.com/...`).
  - AI berpotensi membuat commit otomatis jika tidak dibatasi secara tegas dalam prompt perintah.
  - Solusi awal AI perlu diperiksa kembali karena refactor yang terlalu luas dapat menambah kompleksitas tanpa meningkatkan pemenuhan checklist.
  - Browser terintegrasi tidak tersedia ketika Tugas 3 diverifikasi, sehingga pengecekan runtime dilanjutkan melalui request HTTP ke server lokal dan Django test client.
  - AI tidak dapat menentukan siapa yang seharusnya menjadi Editor hanya dari username; keanggotaan group tetap harus ditetapkan secara sadar oleh pemilik melalui Django Admin.
  - Implementasi awal Tugas 5 berpotensi menduplikasi `getCookie`, sanitasi URL, dan escaping pada setiap halaman; helper tersebut perlu diaudit agar satu sumber kebenaran dipakai bersama.
  - Pada Tugas 6, test dengan `force_authenticate` saja bisa memberi kesan bahwa keamanan sesi sudah diuji, padahal jalur pemeriksaan CSRF dilewati. Field star juga perlu diperiksa agar tidak menerima nilai palsu dari payload.
  - Serializer yang memanggil relasi star berkali-kali dapat menimbulkan query tambahan per kartu jika queryset tidak melakukan prefetch. Kode yang terlihat ringkas belum tentu efisien.
- **Perbaikan Manual yang Dilakukan**:
  - Menginstruksikan AI untuk membuat rencana implementasi terlebih dahulu (*implementation plan*) dan melarang tindakan commit Git otomatis agar saya memegang kendali penuh atas riwayat commit repositori.
  - Memastikan data proyek yang dimasukkan ke database selaras dengan aset lokal yang telah disiapkan di `static/img/projects/`.
  - Memverifikasi secara langsung kelulusan seluruh unit test (`python manage.py test`) dan fungsionalitas lokal di browser (`python manage.py runserver`).
  - Menjaga model `Experience` yang sudah sesuai kebutuhan agar tidak membuat migrasi skema yang tidak diperlukan, lalu memusatkan perubahan pada form, view, route, template, dan test.
  - Memastikan aturan UI selalu didukung pemeriksaan server-side dan tidak menganggap tombol yang disembunyikan sebagai mekanisme keamanan.
  - Memverifikasi skenario empat peran dengan test client, termasuk POST tanpa izin, CSRF, dan bentuk data endpoint JSON.
  - Memastikan Experience menggunakan `textContent` alih-alih `innerHTML`, mempertahankan pemeriksaan izin di view, dan menambahkan test payload XSS serta status `201`, `400`, dan `403`.
  - Pada Tugas 6, mencocokkan pemeriksaan Editor dengan helper peran lama, menambahkan test login sesi dengan CSRF aktif, serta memastikan setiap penolakan mempertahankan data dan relasi star.
  - Menguji bahwa payload tidak dapat mengubah field read-only, menolak thumbnail dengan skema selain HTTP/HTTPS, dan membuktikan jumlah query daftar tetap dua melalui `assertNumQueries`.

### 5. Log Prompt Utama

1. *"browser fufufarizz.vercel.app, Berikut saya berikan referensi website dari hasil akhir portofolio website pada source code di tahap 10 (sekarang masih tahap 1, ikuti sesuai tahap) Berikan implementation plannya. Tahap 1: Lanjutkan halaman “About Me” yang sudah dibuat. Tambahkan satu atau lebih section baru ke halaman yang sama, masih murni dengan HTML5 dan CSS3 (belum ada database/MVT). Pilihan saya, saya ingin anda menambahkan section get to know me persis seperti screenshot yang saya berikan dari website referensi. Karena tugas ini sifatnya lebih bebas, kamu dipersilakan membuat tampilan CSS berbeda dari referensi di website - tambahkan animasi, layout grid, atau elemen visual lain sesuai kreativitasmu, selama tetap rapi dan responsif. Satu pesan saya, buat kode html dan css yang mudah dimengerti, tidak bertele tele, dan tulis kode dengan rapi. Pastikan kode yang dibuat tidak mengada ngada agar saya dapat tetap mengerti apa yang ditulis. Desain visual (warna, font, tata letak, dsb.) bebas diubah, desain seluruh halaman “About Me”, bukan cuma section barunya, asal tetap murni HTML5 dan CSS3, terstruktur rapi, dan checklist di bawah tetap terpenuhi. Checklist minimal untuk tugas ini: -Minimal satu section baru ditambahkan ke halaman yang sama. -Section baru tersebut punya isi yang nyata (bukan lorem ipsum atau placeholder kosong), samakan saja dengan website referensi -Halaman tetap terlihat rapi di lebar layar desktop maupun mobile. -Proyek berhasil dijalankan dengan python manage.py runserver tanpa error."*
2. *"Cek website yang saya berikan, saya ingin anda mengcopy seluruh bagian pada Passion, benar benar copy semuanya sama persis. Untuk Element/gambar pada bagian projects, saya telah menaruh sourcenya di img/projects. Proceed dengan revisi: Jangan menggunakan javascript, tambahkan murni html dan css nya saja. bila terdapat kode/fitur yang membutuhkan javascript maka di skip dulu"*
3. *"Commit text: Jangan ubah kode ataupun melakukan commit. Saya ingin melakukan branching di git dan melakukan commit satu persatu, mulai dari bagian get to know me dan bagian cards. Untuk itu, saya ingin anda membuatkan copy writing dengan lengkap dengan format git checkout -b ..., git add ..., git commit -m "..." hingga git push ... saya ingin melakukan 3 commit 1. pembuatan get to know me 2. pembuatan cards 3, penggantian teks lorem ipsum cukup berikan copywritingnya, untuk kode card biar saya yang hapus dahulu untuk commit get to know me, untuk penggantian teks lorem ipsum juga biar saya yang ganti secara mandiri."*
4. *"/browser fufufarizz.vercel.app, Saya memberikan link browser sebagai referensi tahap 10 tugas yang sudah jadi, sedangkan sekarang, saya meminta anda untuk menyelesaikan tahap 2. Berikut saya berikan perintah dan tahapan yang harus anda kerjakan untuk menyelesaikan tugas tahap 2. Tugas: Terapkan pola Model-View-Template (MVT)... Buatkan implementation plannya, jangan melakukan commit apapun secara mandiri."*
5. *"Refactor seluruh berkas HTML identik agar extend template utama, lalu terapkan Create Form, Update Form, Data Deletion, JSON Data Delivery, dan tampilan hasil deserialisasi untuk satu bagian portofolio lain. Pastikan proyek dapat dijalankan tanpa error."*
6. *"Baca kode pada source code, hapus implementasi yang redundan atau tidak terpakai, lalu baca tugas-5.pdf. Buatkan file HINT.md yang memuat panduan untuk menyelesaikan tugas 5 berdasarkan kode yang sudah terimplementasi dan lanjutkan dengan memberikan kode yang perlu diterapkan beserta dengan kegunaannya masing-masing. Jangan mengimplementasi kode secara langsung ke source code dan jangan melakukan commit apapun."*
7. *"Mengapa API yang mengembalikan JSON belum tentu RESTful? Dalam konteks data Experience, kapan PUT lebih tepat daripada PATCH, dan bagaimana serializer membedakan field input dengan field read-only seperti jumlah star? Saya juga ingin memahami mengapa SessionAuthentication tetap membutuhkan CSRF dan mengapa force_authenticate belum membuktikan perlindungan itu berjalan. Jelaskan konsep dan alur request-nya dengan contoh sederhana."*
