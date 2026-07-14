"""
RestoranaService - Orchestrator untuk business logic sistem restoran.
Menghubungkan repository layer dengan CLI interface.
"""

from src.models.makanan import Makanan
from src.models.minuman import Minuman
from src.models.pesanan import Pesanan
from src.models.transaksi import Transaksi
from src.exceptions.menu_exception import MenuTidakDitemukanException, MenuSudahAdaException, StokHabiException
from src.exceptions.trans_exception import (
    InputTidakValidException,
    MejaTidakTemukanException,
    PesananKosongException,
    PembayaranTidakValidException
)


class RestoranService:
    """
    Service layer untuk business logic sistem restoran.
    
    Responsibilities:
    - Orchestrate menu operations (CRUD)
    - Manage orders (pesanan)
    - Handle payment processing
    - Coordinate with repository layer
    - Validate business rules
    """
    
    def __init__(self, repository):
        """
        Initialize RestoranService.
        
        Args:
            repository: Repository implementation (e.g., DbRepository)
        """
        self.repository = repository
        self.pesanan_aktif = {}  # Dictionary untuk track pesanan aktif in-memory
    
    # ==================== MENU MANAGEMENT ====================
    
    def tambah_menu_makanan(self, nama, harga, tingkat_pedas=0):
        """
        Tambah menu makanan baru.
        
        Args:
            nama: Nama makanan
            harga: Harga makanan
            tingkat_pedas: Tingkat kepedasan (0-5)
            
        Raises:
            InputTidakValidException: Jika input tidak valid
            MenuSudahAdaException: Jika menu sudah ada
        """
        try:
            makanan = Makanan(nama, harga, tingkat_pedas)
            self.repository.simpan_menu(makanan)
            return makanan
        except ValueError as e:
            raise InputTidakValidException(str(e))
    
    def tambah_menu_minuman(self, nama, harga, jenis_gelas='Medium', dingin=True):
        """
        Tambah menu minuman baru.
        
        Args:
            nama: Nama minuman
            harga: Harga minuman
            jenis_gelas: Jenis gelas ('Small', 'Medium', 'Large')
            dingin: Apakah dingin (True/False)
            
        Raises:
            InputTidakValidException: Jika input tidak valid
            MenuSudahAdaException: Jika menu sudah ada
        """
        try:
            minuman = Minuman(nama, harga, jenis_gelas, dingin)
            self.repository.simpan_menu(minuman)
            return minuman
        except ValueError as e:
            raise InputTidakValidException(str(e))
    
    def lihat_semua_menu(self):
        """
        Get semua menu items.
        
        Returns:
            list: Daftar semua Menu objects
        """
        return self.repository.baca_semua_menu()
    
    def lihat_menu_by_kategori(self, kategori):
        """
        Get menu berdasarkan kategori.
        
        Args:
            kategori: 'Makanan' atau 'Minuman'
            
        Returns:
            list: Daftar Menu dengan kategori yang dipilih
        """
        all_menus = self.repository.baca_semua_menu()
        return [m for m in all_menus if m.kategori == kategori]
    
    def lihat_menu_tersedia(self):
        """
        Get semua menu yang tersedia.
        
        Returns:
            list: Daftar Menu yang status_tersedia = True
        """
        all_menus = self.repository.baca_semua_menu()
        return [m for m in all_menus if m.status_tersedia]
    
    def ubah_menu(self, menu_id, **kwargs):
        """
        Update menu berdasarkan ID.
        
        Args:
            menu_id: ID menu yang akan diubah
            **kwargs: Atribut yang akan diubah (nama, harga, status_tersedia, etc.)
            
        Raises:
            MenuTidakDitemukanException: Jika menu tidak ditemukan
            InputTidakValidException: Jika update tidak valid
        """
        try:
            menu = self.repository.baca_menu(menu_id)
            
            for key, value in kwargs.items():
                if hasattr(menu, key):
                    setattr(menu, key, value)
            
            self.repository.ubah_menu(menu)
            return menu
        except MenuTidakDitemukanException:
            raise
        except ValueError as e:
            raise InputTidakValidException(str(e))
    
    def hapus_menu(self, menu_id):
        """
        Hapus menu.
        
        Args:
            menu_id: ID menu yang akan dihapus
            
        Returns:
            bool: True jika berhasil
        """
        return self.repository.hapus_menu(menu_id)
    
    # ==================== PESANAN MANAGEMENT ====================
    
    def buat_pesanan(self, nomor_meja):
        """
        Buat pesanan baru untuk meja.
        
        Args:
            nomor_meja: Nomor meja (int > 0)
            
        Returns:
            Pesanan: Objek pesanan yang baru dibuat
            
        Raises:
            InputTidakValidException: Jika nomor meja tidak valid
        """
        try:
            pesanan = Pesanan(nomor_meja)
            # Simpan pesanan ke database agar bisa diload kembali
            self.repository.simpan_pesanan(pesanan)
            self.pesanan_aktif[pesanan.id_pesanan] = pesanan
            return pesanan
        except ValueError as e:
            raise InputTidakValidException(str(e))
    
    def tambah_item_ke_pesanan(self, pesanan_id, menu_id, jumlah, catatan=""):
        """
        Tambah item menu ke pesanan.
        
        Args:
            pesanan_id: ID pesanan
            menu_id: ID menu yang akan ditambahkan
            jumlah: Jumlah item
            catatan: Catatan khusus (optional)
            
        Raises:
            MejaTidakTemukanException: Jika pesanan tidak ditemukan
            MenuTidakDitemukanException: Jika menu tidak ditemukan
            InputTidakValidException: Jika input tidak valid
        """
        if pesanan_id not in self.pesanan_aktif:
            raise MejaTidakTemukanException(f"Pesanan #{pesanan_id} tidak ditemukan")
        
        try:
            menu = self.repository.baca_menu(menu_id)
            pesanan = self.pesanan_aktif[pesanan_id]
            pesanan.tambah_item(menu, jumlah, catatan)
            # Simpan pesanan dengan items-nya ke database
            self.repository.ubah_pesanan(pesanan)
        except ValueError as e:
            raise InputTidakValidException(str(e))
    
    def hapus_item_dari_pesanan(self, pesanan_id, item_index):
        """
        Hapus item dari pesanan.
        
        Args:
            pesanan_id: ID pesanan
            item_index: Index item dalam list (0-based)
            
        Raises:
            MejaTidakTemukanException: Jika pesanan tidak ditemukan
            InputTidakValidException: Jika index tidak valid
        """
        if pesanan_id not in self.pesanan_aktif:
            raise MejaTidakTemukanException(f"Pesanan #{pesanan_id} tidak ditemukan")
        
        try:
            pesanan = self.pesanan_aktif[pesanan_id]
            pesanan.hapus_item(item_index)
        except ValueError as e:
            raise InputTidakValidException(str(e))
    
    def lihat_pesanan_aktif(self, pesanan_id):
        """
        Lihat detail pesanan yang sedang aktif.
        
        Args:
            pesanan_id: ID pesanan
            
        Returns:
            Pesanan: Objek pesanan
            
        Raises:
            MejaTidakTemukanException: Jika pesanan tidak ditemukan
        """
        if pesanan_id not in self.pesanan_aktif:
            raise MejaTidakTemukanException(f"Pesanan #{pesanan_id} tidak ditemukan")
        
        return self.pesanan_aktif[pesanan_id]
    
    def lihat_semua_pesanan_aktif(self):
        """
        Get semua pesanan yang masih aktif.
        
        Returns:
            list: List Pesanan objects yang aktif
        """
        return list(self.pesanan_aktif.values())
    
    # ==================== PEMBAYARAN & TRANSAKSI ====================
    
    def buat_transaksi(self, pesanan_id, is_member=False):
        """
        Buat transaksi (billing) dari pesanan.
        
        Args:
            pesanan_id: ID pesanan yang akan dibayar
            is_member: Apakah pelanggan adalah member
            
        Returns:
            Transaksi: Objek transaksi yang baru
            
        Raises:
            MejaTidakTemukanException: Jika pesanan tidak ditemukan
            PesananKosongException: Jika pesanan kosong
        """
        if pesanan_id not in self.pesanan_aktif:
            raise MejaTidakTemukanException(f"Pesanan #{pesanan_id} tidak ditemukan")
        
        pesanan = self.pesanan_aktif[pesanan_id]
        
        try:
            transaksi = Transaksi(pesanan, is_member)
            return transaksi
        except PesananKosongException:
            raise
    
    def proses_pembayaran(self, pesanan_id, jumlah_bayar, is_member=False):
        """
        Proses pembayaran pesanan.
        
        Args:
            pesanan_id: ID pesanan
            jumlah_bayar: Jumlah uang yang dibayarkan
            is_member: Apakah pelanggan adalah member
            
        Returns:
            Transaksi: Objek transaksi yang sudah diproses
            
        Raises:
            MejaTidakTemukanException: Jika pesanan tidak ditemukan
            PesananKosongException: Jika pesanan kosong
            PembayaranTidakValidException: Jika pembayaran tidak valid
        """
        transaksi = self.buat_transaksi(pesanan_id, is_member)
        
        try:
            transaksi.proses_pembayaran(jumlah_bayar)
            # Simpan transaksi ke database
            self.repository.simpan_transaksi(transaksi)
            # Remove dari pesanan aktif
            del self.pesanan_aktif[pesanan_id]
            return transaksi
        except PembayaranTidakValidException:
            raise
    
    def lihat_laporan_harian(self, tanggal):
        """
        Lihat laporan penjualan harian.
        
        Args:
            tanggal: Tanggal dalam format string (YYYY-MM-DD)
            
        Returns:
            dict: Laporan penjualan harian
        """
        return self.repository.get_laporan_penjualan_harian(tanggal)
    
    # ==================== UTILITY METHODS ====================
    
    def cari_menu_by_nama(self, nama):
        """
        Cari menu berdasarkan nama (case-insensitive, partial match).
        
        Args:
            nama: Nama menu atau bagian dari nama
            
        Returns:
            list: Daftar menu yang cocok
        """
        all_menus = self.repository.baca_semua_menu()
        nama_lower = nama.lower()
        return [m for m in all_menus if nama_lower in m.nama.lower()]
    
    def reset_database(self):
        """
        Reset semua data database. GUNAKAN DENGAN HATI-HATI!
        
        Returns:
            bool: True jika berhasil
        """
        self.pesanan_aktif.clear()
        return self.repository.hapus_semua_data()
