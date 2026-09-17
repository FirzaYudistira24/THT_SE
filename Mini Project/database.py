import sqlite3

def get_db():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            deskripsi TEXT NOT NULL,
            harga REAL NOT NULL,
            stok INTEGER NOT NULL,
            kategori TEXT NOT NULL,
            Gambar TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tambah data dummy supaya tidak kosong saat pertama dijalankan
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        dummy_data = [
            ('Asus VivoBook 14 A1404', 'Spesifikasi Utama: ' +
            '\n1. Prosesor: Intel Core i3-1215U'+
            '\n2. Grafis: Intel UHD Graphics / Intel Iris Xe Graphics (dukungan dual-channel)'+
            '\n3. Memori (RAM): 8GB DDR4 / DDR5 onboard (bisa ditambah melalui 1 slot SO-DIMM yang tersedia)'+
            '\n4. Penyimpanan: 256GB atau 512GB M.2 NVMe PCIe 4.0 SSD'+
            '\n5. Layar: 14,0 inci, Resolusi FHD (1920 x 1080), rasio 16:9, panel IPS-level, anti-glare, 60Hz, 250 nits'+
            '\n6. Kamera: 720p HD dengan pelindung privasi fisik (privacy shutter)'+
            '\n7. Konektivitas: Wi-Fi 6 / Wi-Fi 6E dan Bluetooth 5.2 / 5.3' +
            '\n8. Port I/O: 1x USB 3.2 Gen 1 Type-C, 1x USB 3.2 Gen 1 Type-A, 1x USB 2.0 Type-A, 1x HDMI 1.4, 1x Audio Jack 3.5mm, 1x DC-in' +
            '\n9. Baterai: 42WHrs, 3-cell Li-ion dengan adaptor daya 45W' +
            '\n10. Berat dan Dimensi: 1,4 kg dengan ketebalan sekitar 1,79 cm'
            , 9500000, 10, 'Elektronik', 'Asus Vivobook.jpg'),
            ('Logitech M331 Silent Plus', 'Spesifikasi Utama: '  +
            '\n1. Resolusi Sensor: 1000 DPI'+
            '\n2. Konektivitas: Wireless 2,4 GHz menggunakan USB Nano Receive'+
            '\n3. Jangkauan Wireless: Hingga 10 meter'+
            '\n4. Daya Tahan Baterai: Hingga 24 bulan (menggunakan 1 baterai AA)'+
            '\n5. Dimensi Mouse: 105,4 mm x 67,9 mm x 38,4 mm'+
            '\n6. Kompatibilitas Sistem Operasi: Win 7, 8, 10, Mac OS X'
            , 250000, 25, 'Aksesoris', 'Mouse Logitech M331.jpg'),
            ('Vortex VX7 Pro', 'Spesifikasi Utama: '  +
            '\n1. Layout: TKL (87 tombol).'+
            '\n2. Hotswap: Mendukung switch universal 3-pin dan 5-pin.'+
            '\n3. Switch Bawaan: Outemu.'+
            '\n4. Keycaps: Plastik ABS Double-shot injection tembus LED dengan font baru.'+
            '\n5. Konektivitas: Kabel dikepang (braided) dengan konektor USB Type-C yang bisa dilepas (detachable).'+
            '\n6. Lampu: RGB yang dapat diprogram lengkap dengan mode ritme musik (music rhythm).'
            , 520000, 15, 'Aksesoris', 'Keyboard Mechanical.jpg'),
            ('Acer Nitro VG240Y', 'Spesifikasi Utama: '  +
            '\n1. Ukuran Layar: 23,8 inci (ZeroFrame / Frameless)'+
            '\n2. Resolusi: Full HD 1920 x 1080 piksel'+
            '\n3. Refresh Rate: 75 HzWaktu Respon (Response Time): 1 ms (VRB)'+
            '\n4. Tipe Panel: IPS (In-Plane Switching) untuk warna tajam dan sudut pandang luas'+
            '\n5. Teknologi Layar: AMD FreeSync untuk mencegah screen tearing'+
            '\n6. Konektivitas: HDMI dan VGA'+
            '\n7. Fitur Tambahan: Built-in speaker stereo dan Acer VisionCare (BlueLightShield & Flickerless)'
            , 2100000, 8, 'Elektronik', 'Acer VG240Y.jpg'),
            ('Fantech Octane 7.1', 'Spesifikasi Utama: '  +
            '\n1. Tipe Driver: 50mm speaker driver'+
            '\n2. Surround Sound: USB Virtual 7.1 Surround Sound'+
            '\n3. Koneksi: Plug USB'+
            '\n4. Panjang Kabel: 2.1 meter'+
            '\n5. Respons Frekuensi: 20Hz – 20KHz'+
            '\n6. Sensitivitas Speaker: 95dB ± 3dB' +
            '\n7. Impedansi Speaker: 32 Ohm ± 15%'+
            '\n8. Sensitivitas Mikrofon: -42dB ± 2dB (Omni-directional)'+
            '\n9. Berat: Sekitar 450 gram'
            , 320000, 5, 'Elektronik', 'Fantech Octane 7.1.jpg'),
            ('Adata Ultimate SU650 2TB', 'Spesifikasi Utama: '  +
            '\n1. Form Factor: 2.5 inci'+
            '\n2. Interface: SATA 6Gb/s (SATA III)'+
            '\n3. NAND Flash: 3D NAND'+
            '\n4. Kecepatan Baca (Sequential Read): Hingga 520 MB/s'+
            '\n5. Kecepatan Tulis (Sequential Write): Hingga 450 MB/s'+
            '\n6. Dimensi (P x L x T): 100,45 x 69,85 x 7 mm'+
            '\n7. Berat: 59,5 gram'
            , 2400000, 12, 'Aksesoris', 'Adata Ultimate.jpg'),
            ('Adata Legend 710 512GB', 'Spesifikasi Utama: '  +
            '\n1. Form Factor: M.2 2280'+
            '\n2. Interface: PCIe Gen3 x4, NVMe 1.4'+
            '\n3. Controller: Realtek RTS5766DL'+
            '\n4. NAND Flash: 3D NAND'+
            '\n5. Kecepatan Baca (Maksimal): Hingga 2.400 MB/s'+
            '\n6. Kecepatan Tulis (Maksimal): Hingga 1.800 MB/s'+
            '\n7. Keamanan & Ketahanan: Enkripsi AES 256-bit, LDPC ECC'
            , 1750000, 20, 'Storage', 'Adata Legend 710.jpg'),
            ('Samsung 8GB DDR4 3200 SODIMM', 'Spesifikasi Utama: '  +
            '\n1. Kapasitas: 8 GB (1x8 GB)'+
            '\n2. Jenis Memori: DDR4'+
            '\n3. Faktor Bentuk: SODIMM'+
            '\n4. Kecepatan (Speed): 3200 MHz / PC4-25600'+
            '\n5. Tegangan (Voltage): 1,2 Volt'+
            '\n6. CAS Latency: CL22'+
            '\n7. Pin: 260-pin'
            , 1200000, 18, 'Komponen', 'RAM Samsung.jpg'),
        ]
        cursor.executemany('''
            INSERT INTO products (nama, deskripsi, harga, stok, kategori, Gambar)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', dummy_data)
    
    conn.commit()
    conn.close()