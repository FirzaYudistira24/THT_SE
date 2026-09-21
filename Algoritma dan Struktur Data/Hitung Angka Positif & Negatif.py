import time
import sys

def hitung_positif_negatif():

    while True:
        print("\n--- Program Hitung Angka Positif & Negatif ---")
        print("Ketik 'keluar' untuk keluar dari program.")

        input_angka = input("Masukkan angka (pisahkan dengan koma): ")

        # Cek apakah pengguna ingin keluar
        if input_angka.strip().lower() == 'keluar':
            print("\nTerima kasih! Program selesai.")
            break

        # Memisahkan input berdasarkan koma
        list_mentah = input_angka.split(",")
        angka = []
        valid = True

        # Proses validasi setiap elemen
        for item in list_mentah:
            teks_bersih = item.strip() # menghapus spasi di awal dan akhir

            # Abaikan jika ada koma ganda yang menghasilkan string kosong
            if not teks_bersih:
                continue # skip teks kosong diantara koma (, ,)

            try:
                # Mencoba mengubah teks menjadi angka bulat
                num = int(teks_bersih)
                angka.append(num)
            except ValueError:
                # Jika gagal karena berisi huruf, titik, atau simbol lain
                print(f"\nInput '{teks_bersih}' tidak valid, Gunakan angka bulat dan pisahkan dengan koma.\n")
                valid = False
                break

        # Kalau ada input tidak valid, countdown lalu ulangi
        if not valid:
            for i in range(5, 0, -1):
                sys.stdout.write(f'\rMencoba lagi dalam {i} detik...')
                time.sleep(1)
            sys.stdout.write('\r' + ' ' * 60 + '\r')
            continue

        # Hitung angka positif dan negatif
        positif = 0
        negatif = 0

        for n in angka:
            if n > 0:
                positif += 1
            elif n < 0:
                negatif += 1
            # Angka 0 diabaikan

        # Tampilkan hasil
        print(f"\nHasil Perhitungan:")
        print(f"Positif: {positif}, Negatif: {negatif}\n")

        # Countdown 5 detik sebelum ulangi
        for i in range(5, 0, -1):
            sys.stdout.write(f'\rMengulangi dalam {i} detik...')
            time.sleep(1)
        sys.stdout.write('\r' + ' ' * 60 + '\r')

hitung_positif_negatif()