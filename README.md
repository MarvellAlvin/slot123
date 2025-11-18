# 🎰 Slot Gacor 123 - Mesin Slot Python CLI

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20termux%20%7C%20colab-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Game mesin slot command-line yang kaya fitur dan berwarna-warni,
dibangun dengan Python.\
Rasakan sensasi casino slot langsung di terminal Anda! 🎮

## ✨ Fitur Unggulan

### 🎯 Gameplay Inti

-   **Sistem 3 Gulungan** dengan simbol klasik: 🍒, 🔔, 7️⃣
-   **Animasi Real-time** dengan efek putaran halus
-   **Multiple Kondisi Menang**: pembayaran 3-sama dan 2-sama
-   **Statistik Progresif** melacak kemenangan, streak, dan performa

### 💰 Sistem Taruhan

-   **Menu Quick Bet** dengan 9 opsi predefined
-   **Taruhan Fixed**: 10, 50, 100, 500, 1K, 5K, 10K
-   **Taruhan Persentase**: HALF (50%), ALL-IN (100%)
-   **Input Custom Bet**
-   **Validasi Cerdas** mencegah taruhan berlebihan

### 💾 Save & Progress

-   **Auto-save** setelah event penting
-   **Save/Load Manual**
-   **Highscore Antar Sesi**
-   **Riwayat Game** 20 spin terakhir
-   **Persistensi Statistik**

### 🎨 Pengalaman Visual

-   **Full Color ANSI**
-   **Warna Spesifik Simbol**
-   **UI Profesional**
-   **Update Balance Real-time**

### 📊 Analitik

-   **Statistik Menang/Kalah**
-   **Win Streak Tracking**
-   **Kemenangan Terbesar**
-   **Spin Counter**

## 🚀 Mulai Cepat

### Prasyarat

-   Python 3.6 atau lebih tinggi
-   Terminal dengan support warna ANSI

### Instalasi

``` bash
git clone https://github.com/yourusername/slot-gacor-123.git
cd slot-gacor-123
wget https://raw.githubusercontent.com/yourusername/slot-gacor-123/main/main.py
```

### Menjalankan Game

``` bash
python main.py
```

### Menjalankan di Platform Berbeda

``` bash
python main.py      # Windows
python3 main.py     # Linux/Mac
python main.py      # Termux
!python main.py     # Google Colab
```

## 🎮 Cara Bermain

### Perintah Dasar

  Perintah        Aksi        Deskripsi
  --------------- ----------- -----------------------
  `S` / `Enter`   Spin        Putar gulungan
  `B`             Quick Bet   Pilihan taruhan cepat
  `H`             History     Riwayat spin
  `R`             Reset       Reset game
  `L`             Save        Simpan game
  `V`             Stats       Statistik
  `?`             Help        Bantuan
  `Q`             Quit        Keluar

### Opsi Quick Bet

1.  10\
2.  50\
3.  100\
4.  500\
5.  1K\
6.  5K\
7.  10K\
8.  HALF\
9.  ALL-IN\
10. Custom

## 🎁 Sistem Pembayaran

### 3 Simbol Sama (JACKPOT! 🎉)

  Simbol   Multiplier
  -------- ------------
  🍒       5x
  🔔       10x
  7️⃣       50x

### 2 Simbol Sama

  Simbol   Multiplier
  -------- ------------
  🍒       1.5x
  🔔       2x
  7️⃣       5x

## 📁 Struktur File

    slot-gacor-123/
    ├── main.py
    ├── slot_save.json
    ├── slot_highscore.txt
    └── README.md

## ⚙️ Konfigurasi

``` python
START_BALANCE = 1000
MIN_BET = 1
SYMBOLS = ["🍒", "🔔", "7"]
SPIN_SPEED = 0.08
```

``` python
WEIGHTS = [50, 30, 10]
PAYOUT_3 = {"🍒": 5, "🔔": 10, "7": 50}
PAYOUT_2 = {"🍒": 1.5, "🔔": 2, "7": 5}
```

## 🎯 Tips & Strategi

1.  Mulai kecil\
2.  Kelola bankroll\
3.  Gunakan history\
4.  Reset bila perlu\
5.  Save rutin

## 🤝 Kontribusi

Silakan ajukan PR, laporan bug, atau saran fitur.

## 📄 Lisensi

MIT License

## 🙏 Penghargaan

Dibangun dengan Python dan inspirasi mesin slot klasik.

------------------------------------------------------------------------

### 🎰 Selamat Memutar Keberuntungan! 🍀
