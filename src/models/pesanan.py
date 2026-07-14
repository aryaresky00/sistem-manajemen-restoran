"""
Class Pesanan - Untuk manajemen pesanan pelanggan.
Mencakup ItemPesanan (item individual dalam pesanan) dan Pesanan (kumpulan items).
"""

from datetime import datetime
from src.exceptions.trans_exception import PesananKosongException


class ItemPesanan:
    """
    Merepresentasikan satu item dalam pesanan.
    
    Attributes:
        menu: Objek Menu yang dipesan
        jumlah: Jumlah item
        catatan: Catatan khusus untuk item (e.g., "Pedas berkurang")
        harga_satuan: Harga satuan saat dipesan (fixed untuk consistency)
    """
    
    def __init__(self, menu, jumlah, catatan=""):
        """
        Initialize ItemPesanan.
        
        Args:
            menu: Objek Menu yang akan dipesan
            jumlah: Jumlah item (harus > 0)
            catatan: Catatan khusus untuk item (optional)
        """
        if jumlah <= 0:
            raise ValueError("Jumlah item harus lebih besar dari 0")
        
        self.__menu = menu
        self.__jumlah = jumlah
        self.__catatan = catatan.strip() if catatan else ""
        self.__harga_satuan = menu.harga  # Capture harga saat order dibuat
        self.__waktu_ditambahkan = datetime.now()
    
    # ==================== PROPERTIES ====================
    
    @property
    def menu(self):
        """Get menu object."""
        return self.__menu
    
    @property
    def jumlah(self):
        """Get jumlah item."""
        return self.__jumlah
    
    @jumlah.setter
    def jumlah(self, value):
        """Set jumlah dengan validasi."""
        if value <= 0:
            raise ValueError("Jumlah item harus lebih besar dari 0")
        self.__jumlah = value
    
    @property
    def catatan(self):
        """Get catatan item."""
        return self.__catatan
    
    @catatan.setter
    def catatan(self, value):
        """Set catatan item."""
        self.__catatan = value.strip() if value else ""
    
    @property
    def harga_satuan(self):
        """Get harga satuan saat order dibuat."""
        return self.__harga_satuan
    
    @property
    def waktu_ditambahkan(self):
        """Get waktu item ditambahkan ke pesanan."""
        return self.__waktu_ditambahkan
    
    # ==================== PUBLIC METHODS ====================
    
    def hitung_subtotal(self):
        """
        Hitung subtotal (harga_satuan × jumlah).
        
        Returns:
            float: Subtotal untuk item ini
        """
        return self.__harga_satuan * self.__jumlah
    
    def get_info(self):
        """
        Get informasi item dalam format string.
        
        Returns:
            str: Informasi item pesanan
        """
        info = f"{self.__jumlah}x {self.__menu.nama} @ Rp{self.__harga_satuan:,.0f} = Rp{self.hitung_subtotal():,.0f}"
        if self.__catatan:
            info += f" (Catatan: {self.__catatan})"
        return info
    
    def __str__(self):
        return self.get_info()
    
    def __repr__(self):
        return f"ItemPesanan(menu={self.__menu.nama}, jumlah={self.__jumlah}, subtotal={self.hitung_subtotal()})"


class Pesanan:
    """
    Merepresentasikan pesanan lengkap dari satu meja.
    
    Attributes:
        nomor_meja: Nomor meja tempat pelanggan duduk (1-999)
        items: List of ItemPesanan objects
        status: Status pesanan ('Aktif', 'Disiapkan', 'Selesai')
        waktu_pesan: Waktu pesanan dibuat
    """
    
    _id_counter = 1000  # Counter untuk ID pesanan
    
    def __init__(self, nomor_meja):
        """
        Initialize Pesanan.
        
        Args:
            nomor_meja: Nomor meja (int, harus > 0)
        """
        if not isinstance(nomor_meja, int) or nomor_meja <= 0:
            raise ValueError("Nomor meja harus integer positif")
        
        self.__id_pesanan = Pesanan._id_counter
        Pesanan._id_counter += 1
        self.__nomor_meja = nomor_meja
        self.__items = []
        self.__status = 'Aktif'
        self.__waktu_pesan = datetime.now()
        self.__waktu_selesai = None
    
    # ==================== PROPERTIES ====================
    
    @property
    def id_pesanan(self):
        """Get ID pesanan."""
        return self.__id_pesanan
    
    @property
    def nomor_meja(self):
        """Get nomor meja."""
        return self.__nomor_meja
    
    @property
    def items(self):
        """Get list items pesanan (read-only copy)."""
        return list(self.__items)
    
    @property
    def status(self):
        """Get status pesanan."""
        return self.__status
    
    @status.setter
    def status(self, value):
        """Set status pesanan dengan validasi."""
        valid_statuses = ['Aktif', 'Disiapkan', 'Selesai']
        if value not in valid_statuses:
            raise ValueError(f"Status harus salah satu dari: {valid_statuses}")
        self.__status = value
        if value == 'Selesai':
            self.__waktu_selesai = datetime.now()
    
    @property
    def waktu_pesan(self):
        """Get waktu pesanan dibuat."""
        return self.__waktu_pesan
    
    @property
    def waktu_selesai(self):
        """Get waktu pesanan selesai."""
        return self.__waktu_selesai
    
    @property
    def jumlah_items(self):
        """Get jumlah total items dalam pesanan."""
        return len(self.__items)
    
    # ==================== PUBLIC METHODS ====================
    
    def tambah_item(self, menu, jumlah, catatan=""):
        """
        Tambah item ke pesanan.
        
        Args:
            menu: Objek Menu
            jumlah: Jumlah item
            catatan: Catatan khusus (optional)
        """
        if not menu.status_tersedia:
            raise ValueError(f"Menu '{menu.nama}' tidak tersedia")
        
        # Check apakah menu sudah ada di pesanan
        for item in self.__items:
            if item.menu.id_menu == menu.id_menu:
                # Jika sudah ada, tambah jumlahnya
                item.jumlah += jumlah
                return
        
        # Jika belum ada, tambah sebagai item baru
        item_baru = ItemPesanan(menu, jumlah, catatan)
        self.__items.append(item_baru)
    
    def hapus_item(self, index):
        """
        Hapus item dari pesanan berdasarkan index.
        
        Args:
            index: Index item dalam list (0-based)
        """
        if index < 0 or index >= len(self.__items):
            raise ValueError(f"Index {index} tidak valid")
        
        self.__items.pop(index)
    
    def hapus_item_by_menu(self, menu_id):
        """
        Hapus item berdasarkan ID menu.
        
        Args:
            menu_id: ID menu yang akan dihapus
            
        Returns:
            bool: True jika berhasil, False jika menu tidak ditemukan
        """
        for i, item in enumerate(self.__items):
            if item.menu.id_menu == menu_id:
                self.__items.pop(i)
                return True
        return False
    
    def hitung_subtotal(self):
        """
        Hitung subtotal seluruh pesanan (sebelum pajak dan diskon).
        
        Returns:
            float: Subtotal pesanan
        """
        if not self.__items:
            return 0.0
        
        total = sum(item.hitung_subtotal() for item in self.__items)
        return round(total, 2)
    
    def get_items_info(self):
        """
        Get informasi semua items dalam format list.
        
        Returns:
            list: List string informasi setiap item
        """
        return [f"{i+1}. {item.get_info()}" for i, item in enumerate(self.__items)]
    
    def get_detail(self):
        """
        Get detail lengkap pesanan.
        
        Returns:
            str: Detail pesanan dalam format string
        """
        if not self.__items:
            return f"Pesanan #{self.__id_pesanan} Meja {self.__nomor_meja}: KOSONG"
        
        detail = f"=== PESANAN #{self.__id_pesanan} ===\n"
        detail += f"Meja: {self.__nomor_meja}\n"
        detail += f"Status: {self.__status}\n"
        detail += f"Waktu: {self.__waktu_pesan.strftime('%H:%M:%S')}\n"
        detail += f"Items:\n"
        for item_info in self.get_items_info():
            detail += f"  {item_info}\n"
        detail += f"Subtotal: Rp{self.hitung_subtotal():,.0f}"
        
        return detail
    
    def __str__(self):
        return f"Pesanan #{self.__id_pesanan} Meja {self.__nomor_meja} ({len(self.__items)} items) - {self.__status}"
    
    def __repr__(self):
        return f"Pesanan(id={self.__id_pesanan}, meja={self.__nomor_meja}, items={len(self.__items)}, subtotal={self.hitung_subtotal()})"
