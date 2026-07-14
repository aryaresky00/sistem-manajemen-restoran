"""
Abstract base class untuk Menu item.
Menerapkan pilar OOP: Encapsulation dan Abstraction.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Menu(ABC):
    """
    Abstract base class untuk semua item menu di restoran.
    
    Attributes (private/protected):
        __nama: Nama item menu
        __harga: Harga dasar item menu
        __status_tersedia: Status ketersediaan item
        __kategori: Kategori menu (Makanan/Minuman)
        __id_menu: ID unik untuk setiap menu item
    """
    
    _id_counter = 1  # Class variable untuk auto-increment ID
    
    def __init__(self, nama, harga, kategori):
        """
        Initialize Menu dengan validasi encapsulated.
        
        Args:
            nama: Nama menu (string)
            harga: Harga menu (float/int, harus > 0)
            kategori: Kategori menu ('Makanan' atau 'Minuman')
        """
        if not nama or len(nama.strip()) == 0:
            raise ValueError("Nama menu tidak boleh kosong")
        if harga <= 0:
            raise ValueError("Harga menu harus lebih besar dari 0")
        if kategori not in ['Makanan', 'Minuman']:
            raise ValueError("Kategori harus 'Makanan' atau 'Minuman'")
        
        self.__id_menu = Menu._id_counter
        Menu._id_counter += 1
        self.__nama = nama.strip()
        self.__harga = float(harga)
        self.__status_tersedia = True
        self.__kategori = kategori
        self.__tanggal_ditambahkan = datetime.now()
    
    # ==================== GETTERS ====================
    
    @property
    def id_menu(self):
        """Get ID menu."""
        return self.__id_menu
    
    @property
    def nama(self):
        """Get nama menu."""
        return self.__nama
    
    @property
    def harga(self):
        """Get harga menu."""
        return self.__harga
    
    @property
    def status_tersedia(self):
        """Get status ketersediaan."""
        return self.__status_tersedia
    
    @property
    def kategori(self):
        """Get kategori menu."""
        return self.__kategori
    
    @property
    def tanggal_ditambahkan(self):
        """Get tanggal menu ditambahkan."""
        return self.__tanggal_ditambahkan
    
    # ==================== SETTERS ====================
    
    @nama.setter
    def nama(self, value):
        """Set nama menu dengan validasi."""
        if not value or len(value.strip()) == 0:
            raise ValueError("Nama menu tidak boleh kosong")
        self.__nama = value.strip()
    
    @harga.setter
    def harga(self, value):
        """Set harga menu dengan validasi."""
        if value <= 0:
            raise ValueError("Harga menu harus lebih besar dari 0")
        self.__harga = float(value)
    
    @status_tersedia.setter
    def status_tersedia(self, value):
        """Set status ketersediaan."""
        if not isinstance(value, bool):
            raise ValueError("Status harus boolean (True/False)")
        self.__status_tersedia = value
    
    # ==================== ABSTRACT METHODS ====================
    
    @abstractmethod
    def hitung_pajak(self, jumlah=1):
        """
        Hitung pajak (PPN) untuk menu item.
        Implementasi berbeda untuk Makanan dan Minuman.
        
        Args:
            jumlah: Jumlah item yang dibeli (default 1)
            
        Returns:
            float: Total pajak
        """
        pass
    
    @abstractmethod
    def hitung_diskon(self, jumlah=1, is_member=False):
        """
        Hitung diskon untuk menu item.
        Implementasi berbeda untuk Makanan dan Minuman.
        
        Args:
            jumlah: Jumlah item yang dibeli
            is_member: Status member (True/False)
            
        Returns:
            float: Total diskon
        """
        pass
    
    @abstractmethod
    def get_info_detail(self):
        """
        Get informasi detail menu.
        Setiap subclass akan implement dengan cara berbeda.
        
        Returns:
            str: Informasi detail menu
        """
        pass
    
    # ==================== PUBLIC METHODS ====================
    
    def hitung_subtotal(self, jumlah=1):
        """
        Hitung subtotal (harga × jumlah) sebelum pajak dan diskon.
        
        Args:
            jumlah: Jumlah item
            
        Returns:
            float: Subtotal
        """
        if jumlah <= 0:
            raise ValueError("Jumlah harus lebih besar dari 0")
        return self.__harga * jumlah
    
    def __str__(self):
        """String representation untuk display."""
        return f"{self.__nama} (Rp{self.__harga:,.0f}) - {self.__kategori}"
    
    def __repr__(self):
        """Representasi untuk debugging."""
        return f"Menu(id={self.__id_menu}, nama='{self.__nama}', harga={self.__harga}, tersedia={self.__status_tersedia})"
