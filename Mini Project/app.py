import os # Mengelola path folder dan file di sistem operasi
from werkzeug.utils import secure_filename # Mengamankan nama file yang diupload
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import get_db, init_db
from dotenv import load_dotenv

# ==================== KONFIGURASI APLIKASI ====================

load_dotenv() # Memuat variabel dari file .env

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'kunci-cadangan-jika-env-tidak-terbaca')

# Folder penyimpanan gambar produk yang diupload
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'gambar')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ekstensi file gambar yang diizinkan untuk diupload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    # Periksa apakah ekstensi file termasuk yang diizinkan
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Inisialisasi database saat aplikasi pertama dijalankan
with app.app_context():
    init_db()


# ==================== HALAMAN ====================

# Halaman utama - daftar produk dengan fitur pencarian dan filter
@app.route('/')
def index():
    
    # Ambil parameter pencarian dan filter dari URL
    search = request.args.get('search', '')
    kategori_filter = request.args.get('kategori_filter', '')
    harga_filter = request.args.get('harga_filter', '')

    conn = get_db()
    cursor = conn.cursor()

    # Query dasar — WHERE 1=1 supaya filter berikutnya bisa ditambah dengan AND
    query = 'SELECT * FROM products WHERE 1=1'
    params = []

    # Filter pencarian berdasarkan nama produk atau kategori
    if search:
        query += ' AND (nama LIKE ? OR kategori LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])

    # Filter berdasarkan kategori yang dipilih di dropdown
    if kategori_filter:
        query += ' AND kategori = ?'
        params.append(kategori_filter)

    # Filter berdasarkan kisaran harga yang dipilih di dropdown
    if harga_filter:
        harga_min, harga_max = harga_filter.split('-')
        query += ' AND harga >= ? AND harga <= ?'
        params.extend([float(harga_min), float(harga_max)])

    # Urutkan produk dari yang terbaru
    query += ' ORDER BY created_at DESC'
    cursor.execute(query, params)

    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products, search=search)


# Halaman detail - menampilkan informasi lengkap satu produk
@app.route('/produk/<int:id>')
def detail(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()
    conn.close()

    # Jika produk tidak ditemukan, redirect ke halaman utama
    if product is None:
        flash('Produk tidak ditemukan', 'error')
        return redirect(url_for('index'))

    return render_template('detail.html', product=product)


# Halaman tambah - form untuk menambah produk baru
@app.route('/produk/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        # Ambil data dari form dan hapus spasi di awal/akhir
        nama = request.form.get('nama', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        harga = request.form.get('harga', '')
        stok = request.form.get('stok', '')
        kategori = request.form.get('kategori', '').strip()

        # Validasi data di sisi server sebelum disimpan ke database
        errors = []
        if not nama: errors.append('Nama produk tidak boleh kosong')
        if not deskripsi: errors.append('Deskripsi tidak boleh kosong')
        if not harga or float(harga) <= 0: errors.append('Harga harus lebih dari 0')
        if not stok or int(stok) < 0: errors.append('Stok tidak boleh negatif')
        if not kategori: errors.append('Kategori tidak boleh kosong')

        # Jika ada error, kirim pesan dan tampilkan form kembali
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('form.html', action='tambah', product=None)

        # Proses upload gambar produk
        file_gambar = request.files.get('gambar')
        nama_file_gambar = 'no-image.jpg' # Gambar default jika tidak diupload

        if file_gambar and file_gambar.filename != '':
            # Validasi ekstensi file gambar di sisi server
            if allowed_file(file_gambar.filename):
                nama_file_gambar = secure_filename(file_gambar.filename)
                jalur_simpan = os.path.join(app.config['UPLOAD_FOLDER'], nama_file_gambar)
                file_gambar.save(jalur_simpan)
            else:
                flash('Format file tidak diizinkan! Gunakan format png, jpg, jpeg, gif, atau webp.', 'error')
                return render_template('form.html', action='tambah', product=None)

        # Simpan produk baru ke database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (nama, deskripsi, harga, stok, kategori, gambar)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nama, deskripsi, float(harga), int(stok), kategori, nama_file_gambar))
        conn.commit()
        conn.close()

        flash('Produk berhasil ditambahkan', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', action='tambah', product=None)


# Halaman edit - form untuk mengubah data produk yang sudah ada
@app.route('/produk/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()

    # Jika produk tidak ditemukan, redirect ke halaman utama
    if product is None:
        flash('Produk tidak ditemukan', 'error')
        conn.close()
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Ambil data baru dari form
        nama = request.form.get('nama', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        harga = request.form.get('harga', '')
        stok = request.form.get('stok', '')
        kategori = request.form.get('kategori', '').strip()

        # Validasi data di sisi server sebelum disimpan ke database
        errors = []
        if not nama: errors.append('Nama produk tidak boleh kosong')
        if not deskripsi: errors.append('Deskripsi tidak boleh kosong')
        if not harga or float(harga) <= 0: errors.append('Harga harus lebih dari 0')
        if not stok or int(stok) < 0: errors.append('Stok tidak boleh negatif')
        if not kategori: errors.append('Kategori tidak boleh kosong')

        # Jika ada error, kirim pesan dan tampilkan form kembali
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('form.html', action='edit', product=product)

        # Gunakan gambar lama sebagai cadangan jika tidak ada gambar baru
        nama_file_gambar = product['gambar']

        # Proses upload gambar baru jika ada
        file_gambar = request.files.get('gambar')
        if file_gambar and file_gambar.filename != '':
            if allowed_file(file_gambar.filename):
                nama_file_gambar = secure_filename(file_gambar.filename)
                jalur_simpan = os.path.join(app.config['UPLOAD_FOLDER'], nama_file_gambar)
                file_gambar.save(jalur_simpan)
            else:
                flash('Format file tidak diizinkan! Gunakan format png, jpg, jpeg, gif, atau webp.', 'error')
                return render_template('form.html', action='edit', product=product)

        # Simpan perubahan produk ke database
        cursor.execute('''
            UPDATE products
            SET nama=?, deskripsi=?, harga=?, stok=?, kategori=?, gambar=?
            WHERE id=?
        ''', (nama, deskripsi, float(harga), int(stok), kategori, nama_file_gambar, id))
        conn.commit()
        conn.close()

        flash('Produk berhasil diupdate', 'success')
        return redirect(url_for('index'))

    conn.close()
    return render_template('form.html', action='edit', product=product)


# Hapus produk dari database berdasarkan id
@app.route('/produk/hapus/<int:id>', methods=['POST'])
def hapus(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('Produk berhasil dihapus', 'success')
    return redirect(url_for('index'))


# ==================== REST API ====================

# Endpoint API - ambil semua produk dengan dukungan pencarian dan filter
@app.route('/api/products', methods=['GET'])
def api_products():

    # Ambil parameter pencarian dan filter dari URL
    search = request.args.get('search', '')
    kategori_filter = request.args.get('kategori_filter', '')
    harga_filter = request.args.get('harga_filter', '')

    conn = get_db()
    cursor = conn.cursor()

    # Query dasar — WHERE 1=1 supaya filter berikutnya bisa ditambah dengan AND
    query = 'SELECT * FROM products WHERE 1=1'
    params = []

    # Filter pencarian berdasarkan nama produk atau kategori
    if search:
        query += ' AND (nama LIKE ? OR kategori LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])

    # Filter berdasarkan kategori yang dipilih
    if kategori_filter:
        query += ' AND kategori = ?'
        params.append(kategori_filter)

    # Filter berdasarkan kisaran harga
    if harga_filter:
        harga_min, harga_max = harga_filter.split('-')
        query += ' AND harga >= ? AND harga <= ?'
        params.extend([float(harga_min), float(harga_max)])

    cursor.execute(query, params)
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(products)


# Endpoint API - ambil detail satu produk berdasarkan id
@app.route('/api/products/<int:id>', methods=['GET'])
def api_product_detail(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()
    conn.close()

    # Kembalikan 404 jika produk tidak ditemukan
    if product is None:
        return jsonify({'error': 'Produk tidak ditemukan'}), 404

    return jsonify(dict(product))


# ==================== JALANKAN APLIKASI ====================

if __name__ == '__main__':
    app.run(debug=True)