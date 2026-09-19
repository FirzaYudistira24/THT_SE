// ========================Tombol Kembali Ke Atas ===============================
document.addEventListener('DOMContentLoaded', function() {
    const tombolBackToTop = document.getElementById('backToTop');

    if (tombolBackToTop) {
        window.addEventListener('scroll', function() {
            // Hitung total tinggi dokumen keseluruhan
            const tinggiDokumen = document.documentElement.scrollHeight;
            
            // Hitung tinggi layar monitor browser yang terlihat saat ini
            const tinggiLayar = window.innerHeight;
            
            // Ambil posisi guliran layar saat ini dari atas
            const posisiScroll = window.scrollY;

            // Munculkan jika sisa jarak ke dasar halaman kurang dari 200px
            if ((tinggiDokumen - tinggiLayar - posisiScroll) < 200) {
                tombolBackToTop.classList.add('show');
            } else {
                tombolBackToTop.classList.remove('show');
            }
        });

        // Logika klik meluncur ke atas tetap sama
        tombolBackToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});

// ======================== Pesan Flash Otomatis Hilang ========================
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500); // tunggu animasi fade selesai baru hilang
        }, 5000); // 5000ms = 5 detik
    });
});