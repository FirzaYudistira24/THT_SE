import time
import sys

def foobar():
    # Perulangan tanpa batas agar program terus berjalan
    while True:
        print("\n--- Program FooBar ---")
        input_user = input("Masukkan Total angka (atau ketik 'keluar' untuk berhenti): ").strip().lower()
        
        # Kondisi untuk keluar dari program
        if input_user == 'keluar' or input_user == 'exit':
            print("Terima kasih! Program selesai.")
            break # Berhenti dari perulangan while
            
        try:
            # Mengubah input teks menjadi angka bulat
            n = int(input_user)
        except ValueError:
            print("Input tidak valid, Masukkan angka bulat atau ketik 'keluar'.")

            # Countdown 5 detik tanpa counter kelihatan
            for i in range(5, 0, -1): #start, stop, step
                sys.stdout.write(f'\rMelanjutkan dalam {i} detik...')
                sys.stdout.flush()
                time.sleep(1)
    
            # Hapus baris countdown setelah selesai
            sys.stdout.write('\r' + ' ' * 60 + '\r')
            sys.stdout.flush()
            continue # Kembali ke atas untuk meminta input lagi

        hasil = []
        
        # Logika FooBar
        for i in range(1, n + 1):
            if i % 3 == 0 and i % 5 == 0: #setiap angka yang bisa dibagi 3 dan 5
                hasil.append("FooBar")
            elif i % 3 == 0:
                hasil.append("Foo")
            elif i % 5 == 0:
                hasil.append("Bar")
            else:
                hasil.append(str(i))
        
        # Cetak hasil angka FooBar
        print(", ".join(hasil))

        # Countdown 5 detik tanpa counter kelihatan
        for i in range(5, 0, -1): #start, stop, step
            sys.stdout.write(f'\rMelanjutkan dalam {i} detik...')
            sys.stdout.flush()
            time.sleep(1)
            
                    # Hapus baris countdown setelah selesai
        sys.stdout.write('\r' + ' ' * 60 + '\r')
        sys.stdout.flush()

# Menjalankan fungsi
foobar()
