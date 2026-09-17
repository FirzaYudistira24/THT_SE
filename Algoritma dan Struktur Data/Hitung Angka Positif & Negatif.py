def hitung_positif_negatif():
    input_angka = input("Masukkan angka (pisahkan dengan koma): ")
    
    # Memisahkan input berdasarkan koma
    list_mentah = input_angka.split(",") # memotong teks yang ada koma (,) nya
    angka = []
    
    # Proses validasi setiap elemen
    for item in list_mentah:
        teks_bersih = item.strip()#menghapus spasi diawal dan akhir
        
        # Abaikan jika ada koma ganda yang menghasilkan string kosong
        if not teks_bersih:
            continue # ngeskip teks diatanra koma (, ,) yang kosong
            
        try:
            # Mencoba mengubah teks menjadi angka bulat (integer)
            num = int(teks_bersih)
            angka.append(num)
        except ValueError:
            # Jika gagal karena berisi huruf, titik (desimal), atau simbol lain
            print(f"⚠️ Input '{teks_bersih}' tidak valid! Gunakan angka bulat dan pisahkan dengan koma.")
            return # Menghentikan fungsi agar tidak lanjut menghitung data yang salah

    positif = 0
    negatif = 0
    
    # Menghitung angka yang valid
    for n in angka:
        if n > 0:
            positif += 1
        elif n < 0:
            negatif += 1
        # Angka 0 diabaikan (tidak positif maupun negatif)
    
    print(f"\nHasil Perhitungan:")
    print(f"Positif: {positif}, Negatif: {negatif}\n")

hitung_positif_negatif()
