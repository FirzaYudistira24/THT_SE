import os # Tambahkan di paling atas file untuk mengelola folder
from werkzeug.utils import secure_filename # Tambahkan untuk mengamankan nama file
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = 'braincorp-katalog-produk'

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'Gambar')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inisialisasi database saat aplikasi pertama dijalankan
with app.app_context():
    init_db()

# ==================== HALAMAN ====================

# Halaman utama - daftar produk
@app.route('/')
def index():
    search = request.args.get('search', '')
    conn = get_db()
    cursor = conn.cursor()
    
    if search:
        cursor.execute('''
            SELECT * FROM products 
            WHERE nama LIKE ? OR kategori LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{search}%', f'%{search}%'))
    else:
        cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
    
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products, search=search)

# Halaman detail produk
@app.route('/produk/<int:id>')
def detail(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()
    conn.close()
    
    if product is None:
        flash('Produk tidak ditemukan', 'error')
        return redirect(url_for('index'))
    
    return render_template('detail.html', product=product)

# Halaman tambah produk
@app.route('/produk/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        harga = request.form.get('harga', '')
        stok = request.form.get('stok', '')
        kategori = request.form.get('kategori', '').strip()
        
        # Validasi teks
        errors = []
        if not nama: errors.append('Nama produk tidak boleh kosong')
        if not deskripsi: errors.append('Deskripsi tidak boleh kosong')
        if not harga or float(harga) <= 0: errors.append('Harga harus lebih dari 0')
        if not stok or int(stok) < 0: errors.append('Stok tidak boleh negatif')
        if not kategori: errors.append('Kategori tidak boleh kosong')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('form.html', action='tambah', product=None)

        # 1. Ambil file gambar dari form HTML (Gunakan huruf kecil sesuai name="gambar" di HTML)
        file_gambar = request.files.get('gambar')
        nama_file_gambar = 'no-image.jpg' # Foto default jika kosong
        
        if file_gambar and file_gambar.filename != '':
            nama_file_gambar = secure_filename(file_gambar.filename)
            jalur_simpan = os.path.join(app.config['UPLOAD_FOLDER'], nama_file_gambar)
            file_gambar.save(jalur_simpan)
        
        # 2. PERBAIKAN: Masukkan kolom 'Gambar' dan variabel 'nama_file_gambar' ke dalam SQL
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (nama, deskripsi, harga, stok, kategori, Gambar)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nama, deskripsi, float(harga), int(stok), kategori, nama_file_gambar))
        conn.commit()
        conn.close()
        
        flash('Produk berhasil ditambahkan', 'success')
        return redirect(url_for('index'))
    
    return render_template('form.html', action='tambah', product=None)

# Halaman edit produk
@app.route('/produk/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()
    
    if product is None:
        flash('Produk tidak ditemukan', 'error')
        conn.close()
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        deskripsi = request.form.get('deskripsi', '').strip()
        harga = request.form.get('harga', '')
        stok = request.form.get('stok', '')
        kategori = request.form.get('kategori', '').strip()
        
        # Validasi teks
        errors = []
        if not nama: errors.append('Nama produk tidak boleh kosong')
        if not deskripsi: errors.append('Deskripsi tidak boleh kosong')
        if not harga or float(harga) <= 0: errors.append('Harga harus lebih dari 0')
        if not stok or int(stok) < 0: errors.append('Stok tidak boleh negatif')
        if not kategori: errors.append('Kategori tidak boleh kosong')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('form.html', action='edit', product=product)
        
        # 1. TAMBAHAN EDIT GAMBAR: Ambil foto lama sebagai cadangan awal
        nama_file_gambar = product['Gambar']
        
        # 2. Periksa apakah pengguna mengunggah file foto baru
        file_gambar = request.files.get('gambar')
        if file_gambar and file_gambar.filename != '':
            nama_file_gambar = secure_filename(file_gambar.filename)
            jalur_simpan = os.path.join(app.config['UPLOAD_FOLDER'], nama_file_gambar)
            file_gambar.save(jalur_simpan)
        
        # 3. PERBAIKAN: Update kolom 'Gambar' di dalam SQL
        cursor.execute('''
            UPDATE products 
            SET nama=?, deskripsi=?, harga=?, stok=?, kategori=?, Gambar=?
            WHERE id=?
        ''', (nama, deskripsi, float(harga), int(stok), kategori, nama_file_gambar, id))
        conn.commit()
        conn.close()
        
        flash('Produk berhasil diupdate', 'success')
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('form.html', action='edit', product=product)

# Hapus produk
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

@app.route('/api/products', methods=['GET'])
def api_products():
    search = request.args.get('search', '')
    conn = get_db()
    cursor = conn.cursor()
    
    if search:
        cursor.execute('''
            SELECT * FROM products 
            WHERE nama LIKE ? OR kategori LIKE ?
        ''', (f'%{search}%', f'%{search}%'))
    else:
        cursor.execute('SELECT * FROM products')
    
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(products)

@app.route('/api/products/<int:id>', methods=['GET'])
def api_product_detail(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()
    conn.close()
    
    if product is None:
        return jsonify({'error': 'Produk tidak ditemukan'}), 404
    
    return jsonify(dict(product))

if __name__ == '__main__':
    app.run(debug=True)