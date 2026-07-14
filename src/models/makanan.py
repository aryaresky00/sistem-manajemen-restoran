"""
Class Makanan - Subclass dari Menu.
Implementasi polymorphism dengan override hitung_pajak() dan hitung_diskon().
"""

from .menu import Menu


class Makanan(Menu):
    """
    Class untuk item menu makanan.
    
    Attributes:
        __tingkat_pedas: Tingkat kepedasan makanan (0-5 scale)
            - 0: Tidak pedas
            - 1: Sedikit pedas
            - 2: Sedang
            - 3: Pedas
            - 4: Sangat pedas
            - 5: Ekstrem
    
    Polymorphism:
        - hitung_pajak(): Makanan memiliki PPN standard 10%
        - hitung_diskon(): Makanan dapat diskon member 15%, promo item makanan 10%
    """
    
    def __init__(self, nama, harga, tingkat_pedas=0):
        """
        Initialize Makanan.
        
        Args:
            nama: Nama makanan
            harga: Harga makanan
            tingkat_pedas: Tingkat kepedasan (0-5), default 0
        """
        super().__init__(nama, harga, 'Makanan')
        
        if not isinstance(tingkat_pedas, int) or tingkat_pedas < 0 or tingkat_pedas > 5:
            raise ValueError("Tingkat pedas harus integer 0-5")
        
        self.__tingkat_pedas = tingkat_pedas
    
    # ==================== PROPERTIES ====================
    
    @property
    def tingkat_pedas(self):
        """Get tingkat kepedasan."""
        return self.__tingkat_pedas
    
    @tingkat_pedas.setter
    def tingkat_pedas(self, value):
        """Set tingkat kepedasan dengan validasi."""
        if not isinstance(value, int) or value < 0 or value > 5:
            raise ValueError("Tingkat pedas harus integer 0-5")
        self.__tingkat_pedas = value
    
    # ==================== POLYMORPHIC IMPLEMENTATIONS ====================
    
    def hitung_pajak(self, jumlah=1):
        """
        Hitung pajak untuk makanan: PPN 10% (standard).
        
        Args:
            jumlah: Jumlah item
            
        Returns:
            float: Pajak yang harus dibayar
        """
        subtotal = self.hitung_subtotal(jumlah)
        # PPN untuk makanan: 10%
        pajak = subtotal * 0.10
        return round(pajak, 2)
    
    def hitung_diskon(self, jumlah=1, is_member=False):
        """
        Hitung diskon untuk makanan.
        
        Kebijakan diskon:
        - Member: 15% dari subtotal
        - Non-member: 0%
        
        Args:
            jumlah: Jumlah item
            is_member: Apakah pelanggan member (True/False)
            
        Returns:
            float: Total diskon
        """
        subtotal = self.hitung_subtotal(jumlah)
        
        if is_member:
            # Diskon member untuk makanan: 15%
            diskon = subtotal * 0.15
            return round(diskon, 2)
        
        # Tidak ada diskon untuk non-member
        return 0.0
    
    def get_info_detail(self):
        """
        Get informasi detail makanan.
        
        Returns:
            str: Informasi detail dengan deskripsi tingkat pedas
        """
        deskripsi_pedas = {
            0: "Tidak pedas",
            1: "Sedikit pedas",
            2: "Sedang",
            3: "Pedas",
            4: "Sangat pedas",
            5: "Ekstrem"
        }
        
        return (f"Makanan: {self.nama}\n"
                f"  Harga: Rp{self.harga:,.0f}\n"
                f"  Tingkat Pedas: {deskripsi_pedas[self.__tingkat_pedas]} ({self.__tingkat_pedas}/5)\n"
                f"  Status: {'Tersedia' if self.status_tersedia else 'Tidak tersedia'}")
    
    def __str__(self):
        """String representation untuk display."""
        deskripsi_pedas = ["❄️ ", "🌶️  ", "🌶️🌶️ ", "🌶️🌶️🌶️ ", "🔥🔥 ", "🔥🔥🔥 "]
        pedas_info = deskripsi_pedas[self.__tingkat_pedas]
        return f"{self.nama} {pedas_info}(Rp{self.harga:,.0f})"
