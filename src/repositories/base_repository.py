"""
Abstract base class untuk repository pattern.
Mendefinisikan kontrak CRUD operations untuk semua implementasi repository.
"""

from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """
    Abstract base class untuk semua repository implementations.
    
    Mendefinisikan interface standar CRUD operations yang harus diimplementasi
    oleh setiap repository (File-based, Database-based, dll).
    """
    
    @abstractmethod
    def simpan_menu(self, menu):
        """
        Simpan menu item baru ke storage.
        
        Args:
            menu: Objek Menu yang akan disimpan
            
        Returns:
            bool: True jika berhasil
        """
        pass
    
    @abstractmethod
    def baca_menu(self, menu_id):
        """
        Baca menu item berdasarkan ID.
        
        Args:
            menu_id: ID menu
            
        Returns:
            Menu: Objek menu jika ditemukan, None jika tidak
        """
        pass
    
    @abstractmethod
    def baca_semua_menu(self):
        """
        Baca semua menu items.
        
        Returns:
            list: List semua Menu objects
        """
        pass
    
    @abstractmethod
    def ubah_menu(self, menu):
        """
        Update menu item.
        
        Args:
            menu: Objek Menu dengan data yang sudah diupdate
            
        Returns:
            bool: True jika berhasil
        """
        pass
    
    @abstractmethod
    def hapus_menu(self, menu_id):
        """
        Hapus menu item.
        
        Args:
            menu_id: ID menu yang akan dihapus
            
        Returns:
            bool: True jika berhasil
        """
        pass
    
    @abstractmethod
    def simpan_pesanan(self, pesanan):
        """
        Simpan pesanan ke storage.
        
        Args:
            pesanan: Objek Pesanan yang akan disimpan
            
        Returns:
            bool: True jika berhasil
        """
        pass
    
    @abstractmethod
    def baca_pesanan(self, pesanan_id):
        """
        Baca pesanan berdasarkan ID.
        
        Args:
            pesanan_id: ID pesanan
            
        Returns:
            Pesanan: Objek pesanan jika ditemukan
        """
        pass
    
    @abstractmethod
    def baca_semua_pesanan(self):
        """
        Baca semua pesanan.
        
        Returns:
            list: List semua Pesanan objects
        """
        pass
    
    @abstractmethod
    def ubah_pesanan(self, pesanan):
        """
        Update pesanan.
        
        Args:
            pesanan: Objek Pesanan dengan data yang sudah diupdate
            
        Returns:
            bool: True jika berhasil
        """
        pass
    
    @abstractmethod
    def hapus_pesanan(self, pesanan_id):
        """
        Hapus pesanan.
        
        Args:
            pesanan_id: ID pesanan yang akan dihapus
            
        Returns:
            bool: True jika berhasil
        """
        pass
    
    @abstractmethod
    def simpan_transaksi(self, transaksi):
        """
        Simpan transaksi ke storage.
        
        Args:
            transaksi: Objek Transaksi yang akan disimpan
            
        Returns:
            bool: True jika berhasil
        """
        pass
    
    @abstractmethod
    def baca_transaksi(self, transaksi_id):
        """
        Baca transaksi berdasarkan ID.
        
        Args:
            transaksi_id: ID transaksi
            
        Returns:
            Transaksi: Objek transaksi jika ditemukan
        """
        pass
    
    @abstractmethod
    def baca_semua_transaksi(self):
        """
        Baca semua transaksi.
        
        Returns:
            list: List semua Transaksi objects
        """
        pass
    
    @abstractmethod
    def baca_transaksi_by_tanggal(self, tanggal):
        """
        Baca transaksi berdasarkan tanggal.
        
        Args:
            tanggal: Tanggal dalam format string (YYYY-MM-DD)
            
        Returns:
            list: List Transaksi pada tanggal tersebut
        """
        pass
    
    @abstractmethod
    def hapus_semua_data(self):
        """
        Hapus semua data (reset database).
        Gunakan dengan hati-hati!
        
        Returns:
            bool: True jika berhasil
        """
        pass
