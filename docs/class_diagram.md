# UML Class Diagram - Sistem Manajemen Restoran

Diagram berikut menunjukkan struktur dan relasi antar class dalam sistem.

## Notasi Diagram

- `<<abstract>>`: Abstract class
- `<<interface>>`: Interface/Abstract base class
- `-` : Private member
- `+` : Public member
- `#` : Protected member
- `-->` : Dependency/Association
- `<|--` : Inheritance
- `*` : Composition/Aggregation

---

## 1. MODELS LAYER - Entity Classes

```
┌─────────────────────────────────────────────────────────────┐
│                   <<abstract>>                              │
│                       Menu                                  │
├─────────────────────────────────────────────────────────────┤
│ - __id_menu: int                                            │
│ - __nama: str                                               │
│ - __harga: float                                            │
│ - __status_tersedia: bool                                   │
│ - __kategori: str                                           │
│ - __tanggal_ditambahkan: datetime                          │
├─────────────────────────────────────────────────────────────┤
│ + id_menu: int <<property>>                                 │
│ + nama: str <<property>>                                    │
│ + harga: float <<property>>                                 │
│ + status_tersedia: bool <<property>>                        │
│ + kategori: str <<property>>                                │
│                                                              │
│ + hitung_pajak(jumlah) -> float <<abstract>>              │
│ + hitung_diskon(jumlah, is_member) -> float <<abstract>>  │
│ + get_info_detail() -> str <<abstract>>                    │
│ + hitung_subtotal(jumlah) -> float                         │
│ + __str__() -> str                                         │
└─────────────────────────────────────────────────────────────┘
         ▲              ▲
         |              |
    ┌────┴────┐    ┌────┴────┐
    |         |    |         |
    |         |    |         |
    ▼         ▼    ▼         ▼

┌──────────────────────────────┐  ┌──────────────────────────────┐
│         Makanan              │  │         Minuman              │
├──────────────────────────────┤  ├──────────────────────────────┤
│ - __tingkat_pedas: int (0-5) │  │ - __jenis_gelas: str         │
│                              │  │ - __dingin: bool             │
├──────────────────────────────┤  ├──────────────────────────────┤
│ + tingkat_pedas: int         │  │ + jenis_gelas: str           │
│   <<property>>               │  │   <<property>>               │
│                              │  │ + dingin: bool               │
│ + hitung_pajak() -> 10%      │  │   <<property>>               │
│ + hitung_diskon()            │  │                              │
│   - Member: 15%              │  │ + hitung_pajak() -> 5%       │
│   - Non-member: 0%           │  │ + hitung_diskon()            │
│                              │  │   - Member: 10%              │
│ + get_info_detail()          │  │   - Buy 2+: 5%               │
│ + __str__()                  │  │   - Others: 0%               │
│                              │  │                              │
│                              │  │ + get_info_detail()          │
│                              │  │ + __str__()                  │
└──────────────────────────────┘  └──────────────────────────────┘
```

### Class Menu (Abstract)

- **Purpose**: Mendefinisikan kontrak untuk semua item menu
- **Polymorphism**: Subclass implement `hitung_pajak()` & `hitung_diskon()` dengan cara berbeda
- **Encapsulation**: Semua atribut private, akses via properties

### Class Makanan (Inheritance)

- **Inherit dari**: Menu
- **Atribut spesifik**: tingkat_pedas (0-5 scale)
- **Polymorphic behavior**:
  - Pajak: 10% (standard PPN)
  - Diskon: 15% untuk member

### Class Minuman (Inheritance)

- **Inherit dari**: Menu
- **Atribut spesifik**: jenis_gelas, dingin
- **Polymorphic behavior**:
  - Pajak: 5% (reduced rate)
  - Diskon: 10% member, 5% buy 2+

---

## 2. PESANAN & TRANSAKSI Classes

```
┌──────────────────────────────────────┐
│         ItemPesanan                  │
├──────────────────────────────────────┤
│ - __menu: Menu                       │
│ - __jumlah: int                      │
│ - __catatan: str                     │
│ - __harga_satuan: float (fixed)      │
│ - __waktu_ditambahkan: datetime      │
├──────────────────────────────────────┤
│ + menu: Menu <<property>>            │
│ + jumlah: int <<property>>           │
│ + catatan: str <<property>>          │
│ + harga_satuan: float <<property>>   │
│                                      │
│ + hitung_subtotal() -> float         │
│ + get_info() -> str                  │
└──────────────────────────────────────┘
         △
         |
         | used in
         |
┌──────────────────────────────────────┐
│          Pesanan                     │
├──────────────────────────────────────┤
│ - __id_pesanan: int                  │
│ - __nomor_meja: int                  │
│ - __items: List[ItemPesanan]         │
│ - __status: str (Aktif/Disiapkan/...)│
│ - __waktu_pesan: datetime            │
│ - __waktu_selesai: datetime          │
├──────────────────────────────────────┤
│ + id_pesanan: int <<property>>       │
│ + nomor_meja: int <<property>>       │
│ + items: List[ItemPesanan]           │
│   <<property>>                       │
│ + status: str <<property>>           │
│ + jumlah_items: int <<property>>     │
│                                      │
│ + tambah_item(menu, jumlah, ...)     │
│ + hapus_item(index)                  │
│ + hapus_item_by_menu(menu_id)        │
│ + hitung_subtotal() -> float         │
│ + get_detail() -> str                │
└──────────────────────────────────────┘
         △
         |
         | contains
         |
┌──────────────────────────────────────┐
│        Transaksi                     │
├──────────────────────────────────────┤
│ - __id_transaksi: int                │
│ - __pesanan: Pesanan                 │
│ - __is_member: bool                  │
│ - __subtotal: float                  │
│ - __pajak_total: float               │
│ - __diskon_total: float              │
│ - __total: float                     │
│ - __bayar: float                     │
│ - __kembalian: float                 │
│ - __status: str (Pending/Selesai/...)│
│ - __waktu_transaksi: datetime        │
├──────────────────────────────────────┤
│ + id_transaksi: int <<property>>     │
│ + pesanan: Pesanan <<property>>      │
│ + is_member: bool <<property>>       │
│ + subtotal: float <<property>>       │
│ + pajak_total: float <<property>>    │
│ + diskon_total: float <<property>>   │
│ + total: float <<property>>          │
│ + bayar: float <<property>>          │
│ + kembalian: float <<property>>      │
│ + status: str <<property>>           │
│                                      │
│ - _hitung_pajak_akumulasi()          │
│   [polymorphic - calls item.pajak]   │
│ - _hitung_diskon_akumulasi()         │
│   [polymorphic - calls item.diskon]  │
│ - _hitung_total()                    │
│                                      │
│ + proses_pembayaran(jumlah_bayar)    │
│ + batalkan_transaksi()               │
│ + get_rincian_pembayaran() -> str    │
│ + get_data_untuk_simpan() -> dict    │
└──────────────────────────────────────┘
```

### Class ItemPesanan

- **Composition**: Bagian dari Pesanan
- **Contains**: Reference ke Menu object
- **Responsibility**: Represent satu item dalam order
- **Key Feature**: Fixed harga_satuan saat order dibuat (untuk consistency accounting)

### Class Pesanan

- **Aggregation**: Kumpulan ItemPesanan
- **Status tracking**: Aktif → Disiapkan → Selesai
- **Methods**: CRUD operations untuk items, calculation

### Class Transaksi

- **Key responsibility**: Billing & payment processing
- **Polymorphism**: Memanggil `menu.hitung_pajak()` & `menu.hitung_diskon()` tanpa mengetahui implementasi
- **Data persistence**: `get_data_untuk_simpan()` untuk simpan ke database

---

## 3. REPOSITORY LAYER - Data Persistence

```
┌────────────────────────────────────────────────────────┐
│            <<abstract>>                                │
│           BaseRepository                               │
├────────────────────────────────────────────────────────┤
│ # Abstract interface untuk CRUD operations             │
├────────────────────────────────────────────────────────┤
│ + simpan_menu(menu) -> bool <<abstract>>               │
│ + baca_menu(menu_id) -> Menu <<abstract>>              │
│ + baca_semua_menu() -> List[Menu] <<abstract>>         │
│ + ubah_menu(menu) -> bool <<abstract>>                 │
│ + hapus_menu(menu_id) -> bool <<abstract>>             │
│                                                        │
│ + simpan_pesanan(pesanan) -> bool <<abstract>>         │
│ + baca_pesanan(pesanan_id) -> Pesanan <<abstract>>     │
│ + baca_semua_pesanan() -> List[Pesanan] <<abstract>>   │
│ + ubah_pesanan(pesanan) -> bool <<abstract>>           │
│ + hapus_pesanan(pesanan_id) -> bool <<abstract>>       │
│                                                        │
│ + simpan_transaksi(transaksi) -> bool <<abstract>>     │
│ + baca_transaksi(transaksi_id) -> Transaksi <<...>>    │
│ + baca_semua_transaksi() -> List[Transaksi] <<...>>    │
│ + baca_transaksi_by_tanggal(tanggal) -> List <<...>>   │
│                                                        │
│ + hapus_semua_data() -> bool <<abstract>>              │
└────────────────────────────────────────────────────────┘
         △
         |
         | implements
         |
┌────────────────────────────────────────────────────────┐
│          DbRepository                                  │
├────────────────────────────────────────────────────────┤
│ - db_path: str                                         │
│ - sqlite3.Connection (internal)                        │
│                                                        │
├────────────────────────────────────────────────────────┤
│ + __init__(db_path)                                    │
│ - _get_connection() -> sqlite3.Connection              │
│ - _inisialisasi_database()                             │
│ - _row_to_menu(row) -> Menu                            │
│                                                        │
│ + simpan_menu(menu) -> bool [SQLite INSERT]            │
│ + baca_menu(menu_id) -> Menu [SQLite SELECT]           │
│ + baca_semua_menu() -> List[Menu] [SQLite SELECT ALL]  │
│ + ubah_menu(menu) -> bool [SQLite UPDATE]              │
│ + hapus_menu(menu_id) -> bool [SQLite DELETE]          │
│                                                        │
│ + simpan_pesanan(pesanan) -> bool [+items]            │
│ + baca_pesanan(pesanan_id) -> Pesanan [+reconstruct]  │
│ + baca_semua_pesanan() -> List[Pesanan]               │
│ + baca_pesanan_aktif() -> List[Pesanan]                │
│ + ubah_pesanan(pesanan) -> bool                        │
│ + hapus_pesanan(pesanan_id) -> bool                    │
│                                                        │
│ + simpan_transaksi(transaksi) -> bool [+JSON items]   │
│ + baca_transaksi(transaksi_id) -> Transaksi            │
│ + baca_semua_transaksi() -> List[Transaksi]            │
│ + baca_transaksi_by_tanggal(tanggal) -> List           │
│ + get_laporan_penjualan_harian(tanggal) -> dict        │
│                                                        │
│ + hapus_semua_data() -> bool [DANGER: DROP ALL TABLES] │
└────────────────────────────────────────────────────────┘

Database Schema:
┌──────────────────────────────────────────────────────┐
│ SQLite Tables                                        │
├──────────────────────────────────────────────────────┤
│ menu:                                                │
│   - id_menu (PK)                                     │
│   - nama (UNIQUE)                                    │
│   - harga, kategori                                  │
│   - tingkat_pedas (for Makanan)                      │
│   - jenis_gelas, dingin (for Minuman)                │
│                                                      │
│ pesanan:                                             │
│   - id_pesanan (PK)                                  │
│   - nomor_meja, status                               │
│   - waktu_pesan, waktu_selesai                       │
│                                                      │
│ item_pesanan:                                        │
│   - id (PK)                                          │
│   - id_pesanan (FK -> pesanan)                       │
│   - id_menu (FK -> menu)                             │
│   - jumlah, harga_satuan, catatan                    │
│                                                      │
│ transaksi:                                           │
│   - id_transaksi (PK)                                │
│   - id_pesanan (FK -> pesanan)                       │
│   - subtotal, pajak_total, diskon_total, total       │
│   - bayar, kembalian                                 │
│   - is_member, status                                │
│   - items_json (items in JSON format)                │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Pattern: Repository Pattern

- **Abstraction**: BaseRepository mendefinisikan interface
- **Implementation**: DbRepository mengimplement dengan SQLite
- **Benefit**: Mudah untuk switch ke implementasi lain (MongoDB, File-based, etc)

---

## 4. SERVICES LAYER - Business Logic

```
┌───────────────────────────────────────────────────────────┐
│          RestoranService                                  │
├───────────────────────────────────────────────────────────┤
│ - repository: BaseRepository                              │
│ - pesanan_aktif: Dict[pesanan_id, Pesanan]               │
│                                                           │
├───────────────────────────────────────────────────────────┤
│ # Menu Management                                         │
│ + tambah_menu_makanan(nama, harga, tingkat_pedas)       │
│ + tambah_menu_minuman(nama, harga, jenis_gelas, dingin) │
│ + lihat_semua_menu() -> List[Menu]                       │
│ + lihat_menu_by_kategori(kategori) -> List[Menu]        │
│ + lihat_menu_tersedia() -> List[Menu]                    │
│ + ubah_menu(menu_id, **kwargs)                           │
│ + hapus_menu(menu_id) -> bool                            │
│ + cari_menu_by_nama(nama) -> List[Menu]                 │
│                                                           │
│ # Pesanan Management                                      │
│ + buat_pesanan(nomor_meja) -> Pesanan                   │
│ + tambah_item_ke_pesanan(pesanan_id, menu_id, ...)      │
│ + hapus_item_dari_pesanan(pesanan_id, item_index)       │
│ + lihat_pesanan_aktif(pesanan_id) -> Pesanan            │
│ + lihat_semua_pesanan_aktif() -> List[Pesanan]          │
│                                                           │
│ # Payment & Transaction                                   │
│ + buat_transaksi(pesanan_id, is_member) -> Transaksi    │
│ + proses_pembayaran(pesanan_id, jumlah_bayar,           │
│   is_member) -> Transaksi                               │
│ + lihat_laporan_harian(tanggal) -> dict                 │
│                                                           │
│ # Utility                                                 │
│ + reset_database() -> bool                               │
│                                                           │
│ Relationships:                                            │
│ - uses repository for data access                        │
│ - coordinates Menu, Pesanan, Transaksi objects          │
│ - validates business rules                              │
│ - throws custom exceptions on error                     │
└───────────────────────────────────────────────────────────┘
              △
              |
              | uses Menu, Pesanan, Transaksi
              |

┌────────────────────────────────────────────────────────┐
│           CetakService                                  │
├────────────────────────────────────────────────────────┤
│ - output_dir: str                                       │
│                                                        │
├────────────────────────────────────────────────────────┤
│ # Receipt Export (Polymorphic)                         │
│ + cetak_struk_ke_file(transaksi) -> filepath           │
│ - _format_struk(transaksi) -> str                      │
│                                                        │
│ # Report Export (Polymorphic)                          │
│ + cetak_laporan_harian(tanggal, laporan) -> filepath   │
│ - _format_laporan_harian(tanggal, data) -> str         │
│ + cetak_laporan_menu_terjual(laporan) -> filepath      │
│ - _format_laporan_menu(laporan) -> str                 │
│                                                        │
│ # Utility                                               │
│ + lihat_file_struk(filepath) -> str                    │
│ + list_file_struk() -> List[dict]                      │
│                                                        │
│ Polymorphism Examples:                                  │
│ - Different format for different report types           │
│ - Easily extensible to PDF, Excel, HTML, etc          │
│ - Template-based formatting                            │
└────────────────────────────────────────────────────────┘
```

### RestoranService

- **Orchestrator**: Menghubungkan Models dengan Repository
- **Validation**: Implements business rules (no duplicate menus, etc)
- **Exception handling**: Throws custom exceptions for business rule violations

### CetakService

- **Polymorphism**: Different output formats for different report types
- **File management**: Auto-generates filenames dengan timestamp
- **Formatting**: Template-based untuk consistent output

---

## 5. EXCEPTIONS LAYER

```
┌─────────────────────────────┐
│       Exception             │
│     (Python built-in)       │
└──────────────┬──────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
┌─────────────────┐ ┌──────────────────┐
│ MenuException   │ │TransaksiException│
│  (base)         │ │   (base)         │
└────────┬────────┘ └────────┬─────────┘
         │                   │
    ┌────┴────────┐      ┌───┴────────────────┐
    │             │      │                    │
    ▼             ▼      ▼                    ▼

MenuTidak    MenuSudah  InputTidak    Meja
Ditemukan     Ada      Valid         TidakTemukan

StokHabi                 Pesanan       Pembayaran
Exception                Kosong        TidakValid


Exception Hierarchy:
├── MenuException
│   ├── MenuTidakDitemukanException
│   ├── MenuSudahAdaException
│   └── StokHabiException
│
└── TransaksiException
    ├── InputTidakValidException
    ├── MejaTidakTemukanException
    ├── PesananKosongException
    └── PembayaranTidakValidException
```

### Exception Strategy

- **Specific exceptions** untuk setiap error scenario
- **Custom messages** untuk user-friendly error reporting
- **Try-catch at CLI layer** untuk prevent crashes

---

## 6. OVERALL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                   RestoranCLI (Main.py)                        │
│                   (User Interface Layer)                        │
│                                                                 │
│  - Interactive Menu Loop                                        │
│  - Input Validation & Exception Handling                       │
│  - Display Output                                               │
│                                                                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
    │ Restoran     │ │ Cetak       │ │ (Exceptions) │
    │ Service      │ │ Service     │ │              │
    │              │ │             │ │ (Custom      │
    │ (Business    │ │ (Report     │ │  exceptions) │
    │  Logic)      │ │  Export)    │ │              │
    └──────┬───────┘ └──────┬──────┘ └──────────────┘
           │                 │
           └────────┬────────┘
                    │
                    ▼
        ┌──────────────────────┐
        │   BaseRepository     │
        │   (Interface)        │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   DbRepository       │
        │   (SQLite)           │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   Models Layer       │
        │  (Menu, Pesanan,     │
        │   Transaksi, etc)    │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   SQLite Database    │
        │   (restoran.db)      │
        │                      │
        │   Tables:            │
        │   - menu             │
        │   - pesanan          │
        │   - item_pesanan     │
        │   - transaksi        │
        └──────────────────────┘

Data Flow:
User Input → CLI → Service → Repository → Database
   ↓                                           ↓
User Output ← CLI ← Service ← Repository ← Database

```

---

## 7. KEY OOP CONCEPTS IMPLEMENTATION

### A. Encapsulation

```python
# Example: Menu class
class Menu(ABC):
    def __init__(self, nama, harga, kategori):
        self.__nama = nama              # Private attribute
        self.__harga = harga            # Private attribute

    @property
    def nama(self):                     # Getter
        return self.__nama

    @nama.setter
    def nama(self, value):              # Setter with validation
        if not value:
            raise ValueError("Nama tidak boleh kosong")
        self.__nama = value
```

**Benefit**: Controlled access, validation at entry point, decoupling interface from implementation

---

### B. Inheritance & Polymorphism

```python
# Abstract base class
class Menu(ABC):
    @abstractmethod
    def hitung_pajak(self, jumlah):
        pass

    @abstractmethod
    def hitung_diskon(self, jumlah, is_member):
        pass

# Subclass 1: Different pajak calculation
class Makanan(Menu):
    def hitung_pajak(self, jumlah=1):
        return self.hitung_subtotal(jumlah) * 0.10  # 10%

# Subclass 2: Different pajak calculation
class Minuman(Menu):
    def hitung_pajak(self, jumlah=1):
        return self.hitung_subtotal(jumlah) * 0.05  # 5%

# Usage: Polymorphic behavior
for item in pesanan.items:
    pajak = item.menu.hitung_pajak(item.jumlah)  # Calls appropriate implementation
```

**Benefit**: Extensibility, code reuse, compile-time type safety

---

### C. Abstraction

```python
# Abstract interface
class BaseRepository(ABC):
    @abstractmethod
    def simpan_menu(self, menu):
        pass

    @abstractmethod
    def baca_menu(self, menu_id):
        pass

    # ... other abstract methods

# Concrete implementation
class DbRepository(BaseRepository):
    def simpan_menu(self, menu):
        # SQLite implementation
        cursor.execute("INSERT INTO menu ...")

    def baca_menu(self, menu_id):
        # SQLite implementation
        cursor.execute("SELECT FROM menu WHERE id = ?")
```

**Benefit**: Loose coupling, easy to swap implementations, hide complexity

---

### D. Composition & Aggregation

```python
# Composition: ItemPesanan is part of Pesanan
class Pesanan:
    def __init__(self, nomor_meja):
        self.__items = []  # List of ItemPesanan

    def tambah_item(self, menu, jumlah):
        item = ItemPesanan(menu, jumlah)  # Creates owned object
        self.__items.append(item)

    def hitung_subtotal(self):
        return sum(item.hitung_subtotal() for item in self.__items)

# Aggregation: Transaksi references Pesanan (shared)
class Transaksi:
    def __init__(self, pesanan, is_member):
        self.__pesanan = pesanan  # References existing object
```

**Benefit**: Natural object relationships, flexible data structures

---

## 8. DESIGN PATTERNS USED

| Pattern                  | Location                      | Purpose                                                              |
| ------------------------ | ----------------------------- | -------------------------------------------------------------------- |
| **Repository Pattern**   | repositories/                 | Abstract data access, easy switching between storage implementations |
| **Factory Pattern**      | RestoranService methods       | Creating Menu, Pesanan, Transaksi objects                            |
| **Template Method**      | CetakService                  | \_format_struk, \_format_laporan for consistent formatting           |
| **Singleton**            | DbRepository                  | Single database connection per session                               |
| **Dependency Injection** | RestoranService, CetakService | Inject repository/service dependencies                               |
| **Abstract Factory**     | Menu + subclasses             | Creating different menu types polymorphically                        |

---

## 9. CLASS RESPONSIBILITY SUMMARY

| Class               | Responsibility                                                  | Layer      |
| ------------------- | --------------------------------------------------------------- | ---------- |
| **Menu**            | Define menu contract, encapsulate attributes                    | Model      |
| **Makanan**         | Implement makanan-specific logic (10% pajak, 15% diskon member) | Model      |
| **Minuman**         | Implement minuman-specific logic (5% pajak, flexible diskon)    | Model      |
| **ItemPesanan**     | Represent item dalam order, capture harga satuan                | Model      |
| **Pesanan**         | Manage collection of items, track order status                  | Model      |
| **Transaksi**       | Calculate billing, handle payment, polymorphic pajak/diskon     | Model      |
| **BaseRepository**  | Define CRUD contract                                            | Repository |
| **DbRepository**    | Implement CRUD with SQLite, manage database schema              | Repository |
| **RestoranService** | Orchestrate business logic, validate rules, coordinate objects  | Service    |
| **CetakService**    | Export struk & laporan dalam format berbeda (polymorphic)       | Service    |
| **RestoranCLI**     | User interaction, input/output, exception handling              | Interface  |

---

## 10. Data Flow Diagrams

### Flow: Membuat Pesanan & Membayar

```
User Input
    ↓
RestoranCLI.buat_pesanan()
    ↓
RestoranService.buat_pesanan(nomor_meja)
    ↓
Pesanan.__init__(nomor_meja) [creates new Pesanan object]
    ↓
RestoranService.pesanan_aktif[id] = pesanan [in-memory tracking]
    ↓
[User adds items...]
    ↓
RestoranCLI.tambah_item_pesanan()
    ↓
RestoranService.tambah_item_ke_pesanan()
    ↓
Pesanan.tambah_item(menu, jumlah)
    ↓
ItemPesanan.__init__(menu, jumlah) [captures menu & harga_satuan]
    ↓
[User proceeds to payment...]
    ↓
RestoranCLI.menu_proses_pembayaran()
    ↓
RestoranService.buat_transaksi(pesanan_id, is_member)
    ↓
Transaksi.__init__(pesanan, is_member)
    ├─ _hitung_pajak_akumulasi() [POLYMORPHIC]
    │  └─ for each item: item.menu.hitung_pajak()
    │     [calls Makanan.hitung_pajak() OR Minuman.hitung_pajak()]
    │
    ├─ _hitung_diskon_akumulasi() [POLYMORPHIC]
    │  └─ for each item: item.menu.hitung_diskon()
    │     [calls Makanan.hitung_diskon() OR Minuman.hitung_diskon()]
    │
    └─ _hitung_total()
       └─ subtotal + pajak - diskon
    ↓
User provides payment amount
    ↓
Transaksi.proses_pembayaran(jumlah_bayar)
    ├─ validates amount >= total
    ├─ calculates kembalian
    └─ sets status = 'Selesai'
    ↓
DbRepository.simpan_transaksi(transaksi)
    ├─ Transaksi.get_data_untuk_simpan() → dict
    ├─ INSERT INTO transaksi (with items_json)
    └─ UPDATE pesanan status = 'Selesai'
    ↓
CetakService.cetak_struk_ke_file(transaksi)
    ├─ _format_struk(transaksi) [build formatted string]
    └─ write to file: data/Struk_#ID_TIMESTAMP.txt
    ↓
Display to User
```

### Flow: Hitung Pajak (Polymorphic)

```
Transaksi._hitung_pajak_akumulasi():
    total_pajak = 0

    for item in pesanan.items:
        pajak = item.menu.hitung_pajak(item.jumlah)
        ├─ if item.menu is Makanan:
        │  └─ subtotal * 0.10 = Makanan pajak (10%)
        │
        ├─ if item.menu is Minuman:
        │  └─ subtotal * 0.05 = Minuman pajak (5%)
        │
        └─ total_pajak += pajak

    return total_pajak  # Total pajak dari semua items

Keuntungan Polymorphism:
- Transaksi tidak perlu mengetahui tipe menu (Makanan vs Minuman)
- Mudah add menu type baru dengan pajak berbeda
- Runtime dispatch otomatis ke implementasi yang tepat
```

---

This comprehensive diagram documents the complete architecture, design patterns, and OOP implementation of the Restaurant Management System. Each component has clear responsibility and separation of concerns.

---

**Last Updated**: July 2024  
**Version**: 1.0 Architecture
