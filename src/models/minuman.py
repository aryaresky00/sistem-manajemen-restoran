"""
Class Minuman - Subclass dari Menu.
Implementasi polymorphism dengan override hitung_pajak() dan hitung_diskon().
"""

from .menu import Menu


class Minuman(Menu):
    """
    Class untuk item menu minuman.
    
    Attributes:
        __jenis_gelas: Jenis gelas untuk minuman ('Small', 'Medium', 'Large')
        __dingin: Apakah minuman disajikan dingin (True/False)
    
    Polymorphism:
        - hitung_pajak(): Minuman memiliki PPN reduced 5%
        - hitung_diskon(): Minuman dapat diskon member 10%, buy 2 get diskon 5%
    """
    
    JENIS_GELAS_VALID = ['Small', 'Medium', 'Large']
    
    def __init__(self, nama, harga, jenis_gelas='Medium', dingin=True):
        """
        Initialize Minuman.
        
        Args:
            nama: Nama minuman
            harga: Harga minuman
            jenis_gelas: Jenis gelas ('Small', 'Medium', 'Large'), default 'Medium'
            dingin: Apakah dingin (True/False), default True
        """
        super().__init__(nama, harga, 'Minuman')
        
        if jenis_gelas not in self.JENIS_GELAS_VALID:
            raise ValueError(f"Jenis gelas harus salah satu dari: {self.JENIS_GELAS_VALID}")
        
        if not isinstance(dingin, bool):
            raise ValueError("Dingin harus boolean (True/False)")
        
        self.__jenis_gelas = jenis_gelas
        self.__dingin = dingin
    
    # ==================== PROPERTIES ====================
    
    @property
    def jenis_gelas(self):
        """Get jenis gelas."""
        return self.__jenis_gelas
    
    @jenis_gelas.setter
    def jenis_gelas(self, value):
        """Set jenis gelas dengan validasi."""
        if value not in self.JENIS_GELAS_VALID:
            raise ValueError(f"Jenis gelas harus salah satu dari: {self.JENIS_GELAS_VALID}")
        self.__jenis_gelas = value
    
    @property
    def dingin(self):
        """Get status dingin."""
        return self.__dingin
    
    @dingin.setter
    def dingin(self, value):
        """Set status dingin dengan validasi."""
        if not isinstance(value, bool):
            raise ValueError("Dingin harus boolean (True/False)")
        self.__dingin = value
    
    # ==================== POLYMORPHIC IMPLEMENTATIONS ====================
    
    def hitung_pajak(self, jumlah=1):
        """
        Hitung pajak untuk minuman: PPN 5% (reduced rate).
        
        Args:
            jumlah: Jumlah item
            
        Returns:
            float: Pajak yang harus dibayar
        """
        subtotal = self.hitung_subtotal(jumlah)
        # PPN untuk minuman: 5% (reduced rate)
        pajak = subtotal * 0.05
        return round(pajak, 2)
    
    def hitung_diskon(self, jumlah=1, is_member=False):
        """
        Hitung diskon untuk minuman.
        
        Kebijakan diskon:
        - Member: 10% dari subtotal
        - Buy 2 atau lebih (non-member): 5% dari subtotal
        
        Args:
            jumlah: Jumlah item
            is_member: Apakah pelanggan member (True/False)
            
        Returns:
            float: Total diskon
        """
        subtotal = self.hitung_subtotal(jumlah)
        
        if is_member:
            # Diskon member untuk minuman: 10%
            diskon = subtotal * 0.10
            return round(diskon, 2)
        elif jumlah >= 2:
            # Diskon buy 2 atau lebih (non-member): 5%
            diskon = subtotal * 0.05
            return round(diskon, 2)
        
        # Tidak ada diskon untuk 1 item non-member
        return 0.0
    
    def get_info_detail(self):
        """
        Get informasi detail minuman.
        
        Returns:
            str: Informasi detail dengan deskripsi gelas dan suhu
        """
        suhu_info = "Dingin" if self.__dingin else "Panas"
        
        return (f"Minuman: {self.nama}\n"
                f"  Harga: Rp{self.harga:,.0f}\n"
                f"  Gelas: {self.__jenis_gelas}\n"
                f"  Suhu: {suhu_info}\n"
                f"  Status: {'Tersedia' if self.status_tersedia else 'Tidak tersedia'}")
    
    def __str__(self):
        """String representation untuk display."""
        suhu_icon = "❄️" if self.__dingin else "☕"
        ukuran_abbrev = self.__jenis_gelas[0]  # S, M, L
        return f"{self.nama} {suhu_icon} {ukuran_abbrev} (Rp{self.harga:,.0f})"
