# Sistem Manajemen Restoran/Kafe - CLI Application

Aplikasi Command Line Interface (CLI) untuk manajemen restoran/kafe yang kokoh dengan menerapkan konsep **Pemrograman Berorientasi Objek (OOP)** tingkat lanjut, penanganan memori/file yang aman, dan integrasi penyimpanan data persisten menggunakan SQLite.

## Fitur Utama

### 1. **Manajemen Menu (CRUD)**

- ✅ Menambah menu makanan dan minuman
- ✅ Melihat semua menu (dengan pengelompokan kategori)
- ✅ Memperbarui informasi menu (nama, harga, status ketersediaan)
- ✅ Menghapus menu yang tidak digunakan
- ✅ Mencari menu berdasarkan nama
- ✅ Menampilkan detail menu dengan atribut spesifik (tingkat pedas untuk makanan, jenis gelas untuk minuman)

### 2. **Sistem Pemesanan & Manajemen Meja**

- ✅ Membuat pesanan baru untuk meja tertentu
- ✅ Menambah item menu ke pesanan (dengan catatan khusus)
- ✅ Menghapus item dari pesanan
- ✅ Melihat detail pesanan secara real-time
- ✅ Tracking pesanan aktif yang sedang berlangsung
- ✅ Automatic subtotal calculation

### 3. **Kalkulasi Billing Otomatis**

- ✅ Perhitungan pajak (PPN) **polymorphic** berdasarkan kategori:
  - Makanan: 10% PPN
  - Minuman: 5% PPN (reduced rate)
- ✅ Perhitungan diskon **polymorphic** dengan berbagai kebijakan:
  - Diskon member untuk makanan: 15%
  - Diskon member untuk minuman: 10%
  - Diskon buy 2+ untuk minuman: 5%
- ✅ Kalkulasi uang kembalian secara presisi
- ✅ Tracking transaksi dengan rincian lengkap

### 4. **Cetak Struk Digital**

- ✅ Mengekspor struk belanja final ke file `.txt` dengan format profesional
- ✅ Automatic filename generation dengan timestamp
- ✅ Struk berisi: header, items, perhitungan, dan footer
- ✅ Melihat kembali struk yang sudah dicetak

### 5. **Laporan Penjualan**

- ✅ Laporan harian dengan summary penjualan
- ✅ Laporan menu paling banyak terjual (ranking)
- ✅ Export laporan ke file `.txt`
- ✅ Filter transaksi berdasarkan tanggal

## Spesifikasi Teknis

### 1. **Pilar OOP Tingkat Lanjut**

#### **Encapsulation**

- Semua atribut data entity (`Menu`, `Pesanan`, `Transaksi`) bersifat `private` (prefix `__`)
- Akses hanya melalui property getters dan setters dengan validasi
- Contoh: `@property` dan `@setter` di class `Menu` untuk `nama`, `harga`, `status_tersedia`

#### **Inheritance & Polymorphism**

- **Kelas Induk**: `Menu` (abstract base class)
  - Mendefinisikan struktur umum dan abstract methods
  - Methods: `hitung_pajak()`, `hitung_diskon()`, `get_info_detail()`
- **Kelas Turunan**:
  - `Makanan(Menu)`: Implementasi spesifik dengan atribut `tingkat_pedas`
    - `hitung_pajak()`: 10% dari subtotal
    - `hitung_diskon()`: 15% untuk member
  - `Minuman(Menu)`: Implementasi spesifik dengan atribut `jenis_gelas`, `dingin`
    - `hitung_pajak()`: 5% dari subtotal
    - `hitung_diskon()`: 10% member, 5% buy 2+

#### **Abstraction**

- **Interfaces (Abstract Classes)**:
  - `BaseRepository`: Kontrak CRUD operations
  - `Menu`: Abstrak untuk semua item menu
- **Polymorphic Behavior**:
  - Transaksi memanggil `menu.hitung_pajak()` dan `menu.hitung_diskon()` tanpa perlu mengetahui implementasi spesifik
  - CetakService memiliki berbagai format laporan yang bisa diperluas

### 2. **Manajemen Data & Exception Handling**

#### **Penyimpanan Data Persisten**

- **Database**: SQLite (`data/restoran.db`)
- **Schema Tables**:
  - `menu`: Menyimpan item menu
  - `pesanan`: Menyimpan pesanan pelanggan
  - `item_pesanan`: Detail items dalam setiap pesanan
  - `transaksi`: Record pembayaran dan transaksi
- **Object Serialization**: Data objek dikonversi ke/dari format database

#### **Robust Exception Handling**

- **Custom Exceptions**:
  - `menu_exception.py`: `MenuTidakDitemukanException`, `MenuSudahAdaException`, `StokHabiException`
  - `trans_exception.py`: `InputTidakValidException`, `MejaTidakTemukanException`, `PesananKosongException`, `PembayaranTidakValidException`
- **Try-Catch Blocks**: Semua operasi user input dibungkus dalam exception handling
- **Graceful Error Messages**: User-friendly error messages tanpa crash aplikasi

## Struktur Folder Proyek

```
Sistem-Managemen-Restoran/
├── data/                           # Penyimpanan data persisten
│   ├── restoran.db                # SQLite database
│   └── Struk_*.txt                # File struk digital yang dicetak
│   └── Laporan_*.txt              # File laporan penjualan
├── docs/                          # Dokumentasi
│   └── class_diagram.md           # UML Class Diagram (text-based)
├── src/                           # Source code utama aplikasi
│   ├── Main.py                    # Entry point - Interactive CLI menu
│   ├── models/                    # LAYER 1: Entity & OOP
│   │   ├── menu.py               # Abstract class Menu dengan encapsulation
│   │   ├── makanan.py            # Class Makanan (inherits Menu) - polymorphism
│   │   ├── minuman.py            # Class Minuman (inherits Menu) - polymorphism
│   │   ├── pesanan.py            # Class Pesanan & ItemPesanan
│   │   └── transaksi.py          # Class Transaksi dengan billing logic
│   ├── repositories/              # LAYER 2: Data Persistence (Repository Pattern)
│   │   ├── base_repository.py    # Abstract interface CRUD
│   │   └── db_repository.py      # SQLite implementation
│   ├── services/                  # LAYER 3: Business Logic
│   │   ├── restoran_service.py   # Orchestrator untuk menu, pesanan, pembayaran
│   │   └── cetak_service.py      # Polymorphic export ke struk & laporan
│   └── exceptions/                # LAYER 4: Custom Exceptions
│       ├── menu_exception.py     # Menu-related exceptions
│       └── trans_exception.py    # Transaction-related exceptions
├── README.md                      # File ini - Panduan instalasi & usage
└── requirements.txt               # Dependensi (sqlite3 built-in)
```

### Penjelasan Struktur 4-Layer

1. **Models Layer** (`src/models/`)
   - Mendefinisikan entity dan business rules
   - Implementasi OOP tingkat lanjut (Inheritance, Polymorphism, Encapsulation)
   - Validasi data di level objek

2. **Repository Layer** (`src/repositories/`)
   - Abstraksi akses data
   - Implementasi SQLite untuk CRUD operations
   - Isolation antara business logic dan data persistence

3. **Services Layer** (`src/services/`)
   - Orchestration dan business logic
   - Koordinasi antar repository
   - Kalkulasi kompleks dan validasi workflow

4. **CLI Interface** (`src/Main.py`)
   - User interaction
   - Input validation
   - Exception handling di boundary layer

## Instalasi & Cara Menjalankan

### Prerequisite

- Python 3.8 atau lebih tinggi
- pip (Python Package Manager)

### Setup Awal

1. **Clone atau download project**

   ```bash
   cd Sistem-Managemen-Restoran
   ```

2. **Install dependencies (opsional, sqlite3 built-in)**

   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi**
   ```bash
   python src/Main.py
   ```

### Struktur File yang Akan Dibuat Otomatis

Saat pertama kali dijalankan, aplikasi akan otomatis membuat:

- `data/restoran.db` - Database SQLite dengan schema lengkap
- `data/` folder - Untuk output struk dan laporan

## Panduan Penggunaan

### Menu Utama

```
SISTEM MANAJEMEN RESTORAN/KAFE
==============================================================================

  1. Manajemen Menu                    # CRUD menu items
  2. Sistem Pemesanan                  # Buat & kelola pesanan
  3. Lihat Pesanan Aktif               # View active orders
  4. Proses Pembayaran                 # Billing & payment processing
  5. Cetak Struk                       # Print & view receipts
  6. Laporan Penjualan                 # Sales reports & analytics
  7. Reset Database                    # Reset all data (hati-hati!)
  0. Keluar Aplikasi                   # Exit
```

### Contoh Workflow

#### Scenario 1: Menambah Menu Makanan

```
1. Pilih "Manajemen Menu" (Menu #1)
2. Pilih "Tambah Menu Makanan" (#2)
3. Input:
   - Nama: Nasi Goreng Spesial
   - Harga: 35000
   - Tingkat Pedas: 3
4. Menu berhasil ditambahkan!
```

#### Scenario 2: Membuat Pesanan & Membayar

```
1. Pilih "Sistem Pemesanan" (#2)
2. Pilih "Buat Pesanan Baru" (#1)
   - Nomor Meja: 5
   - Pesanan #1001 dibuat
3. Pilih "Tambah Item ke Pesanan" (#2)
   - Pilih pesanan #1001
   - Pilih menu (Nasi Goreng Spesial)
   - Jumlah: 2
   - Catatan: Pedas berkurang
4. Pilih "Proses Pembayaran" (#4)
   - Pesanan #1001 akan dibayar
   - Sistem otomatis menghitung:
     * Subtotal: Rp70.000
     * Pajak (10% makanan): Rp7.000
     * Diskon (jika member): Rp10.500
     * Total: Rp66.500
   - Pembayaran: Rp70.000
   - Kembalian: Rp3.500
5. Struk otomatis dicetak ke `data/Struk_#5001_TIMESTAMP.txt`
```

#### Scenario 3: Melihat Laporan Harian

```
1. Pilih "Laporan Penjualan" (#6)
2. Pilih "Laporan Harian" (#1)
3. Input tanggal: 2024-07-14 (atau kosongkan untuk hari ini)
4. Sistem menampilkan:
   - Total transaksi selesai
   - Total penjualan netto
   - Total pajak & diskon
   - Menu yang terjual dengan kuantitas & subtotal
```

## Contoh Output Struk Digital

```
======================================================================
                      == STRUK BELANJA ==
======================================================================

Nomor Struk    : #5001
Tanggal & Waktu: 14/07/2024 14:30:45
Meja           : 5
Status Member  : Tidak (Umum)

----------------------------------------------------------------------
ITEM-ITEM PESANAN:
----------------------------------------------------------------------
 1.   2x Nasi Goreng Spesial (Pedas berkurang)
    @ Rp   35,000 = Rp    70,000

----------------------------------------------------------------------
Subtotal                    : Rp        70,000
Pajak (PPN)                 : Rp         7,000
----------------------------------------------------------------------
TOTAL PEMBAYARAN            : Rp        77,000
----------------------------------------------------------------------

PEMBAYARAN:
Uang Diterima               : Rp        80,000
Uang Kembalian              : Rp         3,000

======================================================================
                        TERIMAKASIH!
======================================================================
Dicetak pada: 14/07/2024 14:31:02
======================================================================
```

## Fitur Advanced

### 1. **Polymorphic Discount & Tax Calculation**

Sistem otomatis menghitung pajak dan diskon berbeda untuk setiap kategori:

- Makanan: PPN 10%, Member discount 15%
- Minuman: PPN 5%, Member discount 10%, Buy 2+ discount 5%

### 2. **Transaction Tracking**

Semua transaksi tercatat dengan detail:

- Items yang dibeli
- Harga satuan saat pembelian (fixed untuk consistency)
- Pajak & diskon per item
- Total dan kembalian

### 3. **Data Persistence**

Semua data otomatis disimpan ke SQLite:

- Menu tidak hilang saat aplikasi tutup
- Pesanan & transaksi terrecord lengkap
- Query efficient dengan indexed tables

### 4. **Report Generation**

Laporan otomatis yang bisa diexport ke file:

- Laporan harian dengan summary
- Ranking menu terjual
- Ekstensibel untuk format baru (PDF, Excel, dll)

## Teknologi & Library yang Digunakan

- **Python**: 3.8+
- **SQLite3**: Built-in untuk database
- **Datetime**: Untuk timestamp & date handling
- **Pathlib**: Untuk file management
- **ABC (Abstract Base Class)**: Untuk interface abstraction

## Catatan & Limitasi

1. **Single Process**: Aplikasi CLI bersifat single-user dan single-session
2. **In-Memory Pesanan**: Pesanan aktif di-track in-memory selama session
3. **No Concurrency**: Tidak ada handling untuk concurrent access (designed untuk single terminal)
4. **Report Export**: Output format terbatas pada `.txt` (ekstensibel ke PDF/Excel di masa depan)

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'src'"

**Solution**: Pastikan menjalankan dari root project directory:

```bash
cd sistem-manajemen-restoran
python src/Main.py
```

### Error: "sqlite3.OperationalError: database is locked"

**Solution**: Tutup aplikasi & coba lagi. Database tidak support concurrent access.

### Data tidak tersimpan

**Solution**: Pastikan folder `data/` ada dan accessible. Aplikasi akan auto-create jika tidak ada.

## Dokumentasi Kode

Setiap class, method, dan function memiliki docstring lengkap yang menjelaskan:

- Tujuan & responsibility
- Parameters & return values
- Exception yang mungkin dilempar
- Contoh usage

## License & Credits

Dibuat sebagai project pembelajaran OOP dan sistem informasi restoran.

---

**Created**: July 2026  
**Version**: 1.0  
**Status**: Production Ready
