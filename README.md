# PE Cell — Aplikasi Web Katalog Produk

Aplikasi web katalog produk elektronik menggunakan Python Flask, SQLite, dan HTML/CSS/JavaScript.
Aplikasi ini mendukung operasi CRUD lengkap, fitur pencarian, filter kategori dan harga, serta upload gambar produk.

---

## Fitur

- Menampilkan daftar produk dalam tampilan grid yang responsif (3 kolom)
- Fitur pencarian produk berdasarkan nama
- Filter produk berdasarkan kategori dan kisaran harga
- Halaman detail produk dengan gambar dan deskripsi lengkap
- Tambah produk baru dengan upload gambar dan validasi data sisi server
- Edit produk yang sudah ada
- Hapus produk dengan konfirmasi
- REST API endpoint untuk akses data produk
- Tombol kembali ke atas
- Tampilan responsif untuk mobile dan desktop

---

## Teknologi yang Digunakan

| Komponen        | Teknologi                |
|-----------------|--------------------------|
| Backend         | Python 3.14, Flask 3.1.3 |
| Database        | SQLite3                  |
| Frontend        | HTML5, CSS3, JavaScript  |
| Upload Gambar   | Werkzeug                 |
| Environment     | python-dotenv            |
| Version Control | Git & GitHub             |

---

## Struktur Proyek

```
katalog-produk/
│
├── Algoritma dan Struktur Data/
│  ├── Foobar
│  └── Hitung Angka Positif & Negatif
│
├── Mini-Project/
│  ├── Static/
│  │ ├── css/
│  │ │ └── style.css # Styling seluruh halaman
│  │ ├── js/
│  │ │ └── main.js # JavaScript (Back to Top)
│  │ └── Gambar/ # Folder penyimpanan gambar produk
│  │   ├── hero-bg.jpg # Gambar hero section
│  │   ├── no-image.jpg # Gambar default produk tanpa foto│
│  │   └── ... # Gambar produk lainnya
│  ├── Templates/
│  │ ├── index.html # Halaman utama daftar produk
│  │ ├── detail.html # Halaman detail produk
│  │ └── form.html # Halaman form tambah & edit produk
│  ├── app.py # Backend Flask, routing & validasi
│  ├── database.py # Setup database & inisialisasi data
│  ├── products.db # File database SQLite (auto-generated)
│  ├── .env # Environment variable (tidak di-upload)
│  └── .gitignore 
└─── README.md

```

---

## ⚙️ Panduan Instalasi

### Prasyarat

Pastikan perangkat sudah terinstall:
- **Python 3.x** — download di [python.org](https://python.org/downloads)
- **pip** — biasanya sudah terinstall bersama Python
- **Git** — download di [git-scm.com](https://git-scm.com)

### Langkah Instalasi

**1. Clone repository**
```bash
git clone https://github.com/firzayudistira24/THT_SE.git
cd THT_SE
```

**2. Install dependencies**
```bash
pip install flask werkzeug python-dotenv
```

**3. Buat file `.env`**
```bash
Buat file `.env` di dalam folder `mini-project/` dan isi dengan:
FLASK_SECRET_KEY=kunci-rahasia85
```
**4. Jalankan aplikasi**
```bash
cd "Mini Project"
python app.py
```

**5. Buka browser**
http://127.0.0.1:5000


Aplikasi siap digunakan!
Database (product.db) akan otomatis dibuat dan diisi data produk awal (database.py) saat pertama kali dijalankan.

---

## REST API Endpoint

| Method | Endpoint                       | Deskripsi                    |
|--------|--------------------------------|------------------------------|
| GET    | `/api/products`                | Ambil semua produk           |
| GET    | `/api/products?search=keyword` | Cari produk berdasarkan nama |
| GET    | `/api/products/<int:id>`       | Ambil detail satu produk     |
 
### Contoh Response

**GET /api/products**
```json
[
    {
        "id": 1,
        "nama": "Redmi Pad SE",
        "deskripsi": "Spesifikasi Utama: ...",
        "harga": 2100000,
        "stok": 15,
        "kategori": "Elektronik",
        "Gambar": "Redmi Pad SE.jpg",
        "created_at": "2026-08-13 10:00:00"
    }
]
```

---

## Skema Database

**Tabel: products**

| Kolom      | Tipe      | Keterangan                       |
|------------|-----------|----------------------------------|
| id         | INTEGER   | Primary key, auto increment      |
| nama       | TEXT      | Nama produk (wajib)              |
| deskripsi  | TEXT      | Deskripsi produk (wajib)         |
| harga      | REAL      | Harga produk, harus lebih dari 0 |
| stok       | INTEGER   | Jumlah stok, minimal 0           |
| kategori   | TEXT      | Kategori produk (wajib)          |
| Gambar     | TEXT      | Nama file gambar (opsional)      |
| created_at | TIMESTAMP | Waktu ditambahkan (otomatis)     |

---

## Validasi Data

Aplikasi menerapkan validasi di sisi server untuk setiap input:
- Nama produk tidak boleh kosong
- Deskripsi tidak boleh kosong
- Harga harus lebih dari 0
- Stok tidak boleh negatif
- Kategori tidak boleh kosong
- Format file gambar harus png, jpg, jpeg, gif, atau webp

---

## Tentang Saya

Dibuat oleh **Moch Firza Yudistira Meizia** sebagai bagian dari Take Home Test magang BrainCorp.

- GitHub: [firzayudistira24](https://github.com/firzayudistira24)