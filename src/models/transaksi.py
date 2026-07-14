"""
Class Transaksi - Untuk billing dan payment processing.
Menangani perhitungan pajak, diskon, dan pembayaran.
"""

from datetime import datetime
from src.exceptions.trans_exception import (
    PesananKosongException,
    PembayaranTidakValidException
)


class Transaksi:
    """
    Merepresentasikan transaksi pembayaran dari satu pesanan.
    
    Attributes:
        pesanan: Objek Pesanan yang akan dibayar
        pajak_total: Total pajak yang harus dibayar
        diskon_total: Total diskon
        subtotal: Total sebelum pajak dan diskon
        total: Total akhir yang harus dibayar
        bayar: Jumlah uang yang diberikan pelanggan
        kembalian: Uang kembalian
        status: Status transaksi
        waktu_transaksi: Waktu transaksi dibuat
    """
    
    _id_counter = 5000  # Counter untuk ID transaksi
    
    def __init__(self, pesanan, is_member=False):
        """
        Initialize Transaksi.
        
        Args:
            pesanan: Objek Pesanan yang akan ditransaksikan
            is_member: Apakah pelanggan adalah member (True/False)
        """
        if not pesanan or pesanan.jumlah_items == 0:
            raise PesananKosongException("Pesanan kosong, tidak dapat membuat transaksi")
        
        self.__id_transaksi = Transaksi._id_counter
        Transaksi._id_counter += 1
        self.__pesanan = pesanan
        self.__is_member = is_member
        self.__waktu_transaksi = datetime.now()
        self.__status = 'Pending'  # 'Pending', 'Selesai', 'Batal'
        self.__bayar = 0.0
        self.__kembalian = 0.0
        
        # Hitung pajak dan diskon
        self.__subtotal = pesanan.hitung_subtotal()
        self.__pajak_total = self._hitung_pajak_akumulasi()
        self.__diskon_total = self._hitung_diskon_akumulasi()
        self.__total = self._hitung_total()
    
    # ==================== PRIVATE CALCULATION METHODS ====================
    
    def _hitung_pajak_akumulasi(self):
        """
        Hitung total pajak dari semua items dalam pesanan.
        Menggunakan polymorphism: setiap menu item menghitung pajak sendiri.
        
        Returns:
            float: Total pajak
        """
        total_pajak = 0.0
        for item in self.__pesanan.items:
            pajak_item = item.menu.hitung_pajak(item.jumlah)
            total_pajak += pajak_item
        
        return round(total_pajak, 2)
    
    def _hitung_diskon_akumulasi(self):
        """
        Hitung total diskon dari semua items dalam pesanan.
        Menggunakan polymorphism: setiap menu item menghitung diskon sendiri.
        
        Returns:
            float: Total diskon
        """
        total_diskon = 0.0
        for item in self.__pesanan.items:
            diskon_item = item.menu.hitung_diskon(item.jumlah, self.__is_member)
            total_diskon += diskon_item
        
        return round(total_diskon, 2)
    
    def _hitung_total(self):
        """
        Hitung total akhir: Subtotal + Pajak - Diskon.
        
        Returns:
            float: Total yang harus dibayar
        """
        total = self.__subtotal + self.__pajak_total - self.__diskon_total
        return round(total, 2)
    
    # ==================== PROPERTIES ====================
    
    @property
    def id_transaksi(self):
        """Get ID transaksi."""
        return self.__id_transaksi
    
    @property
    def pesanan(self):
        """Get pesanan object."""
        return self.__pesanan
    
    @property
    def is_member(self):
        """Get status member."""
        return self.__is_member
    
    @property
    def subtotal(self):
        """Get subtotal."""
        return self.__subtotal
    
    @property
    def pajak_total(self):
        """Get total pajak."""
        return self.__pajak_total
    
    @property
    def diskon_total(self):
        """Get total diskon."""
        return self.__diskon_total
    
    @property
    def total(self):
        """Get total akhir."""
        return self.__total
    
    @property
    def bayar(self):
        """Get jumlah pembayaran."""
        return self.__bayar
    
    @property
    def kembalian(self):
        """Get uang kembalian."""
        return self.__kembalian
    
    @property
    def status(self):
        """Get status transaksi."""
        return self.__status
    
    @property
    def waktu_transaksi(self):
        """Get waktu transaksi."""
        return self.__waktu_transaksi
    
    # ==================== PUBLIC METHODS ====================
    
    def proses_pembayaran(self, jumlah_bayar):
        """
        Proses pembayaran dari pelanggan.
        
        Args:
            jumlah_bayar: Jumlah uang yang dibayarkan
            
        Raises:
            PembayaranTidakValidException: Jika pembayaran tidak valid
        """
        try:
            jumlah_bayar = float(jumlah_bayar)
        except ValueError:
            raise PembayaranTidakValidException("Jumlah pembayaran harus berupa angka")
        
        if jumlah_bayar < 0:
            raise PembayaranTidakValidException("Jumlah pembayaran tidak boleh negatif")
        
        if jumlah_bayar < self.__total:
            raise PembayaranTidakValidException(
                f"Pembayaran kurang. Total: Rp{self.__total:,.0f}, Bayar: Rp{jumlah_bayar:,.0f}"
            )
        
        self.__bayar = round(jumlah_bayar, 2)
        self.__kembalian = round(self.__bayar - self.__total, 2)
        self.__status = 'Selesai'
        
        # Update status pesanan
        if self.__pesanan.status != 'Selesai':
            self.__pesanan.status = 'Selesai'
    
    def batalkan_transaksi(self):
        """Batalkan transaksi (untuk kasus pembayaran gagal, dll)."""
        if self.__status == 'Selesai':
            raise PembayaranTidakValidException("Tidak dapat membatalkan transaksi yang sudah selesai")
        
        self.__status = 'Batal'
    
    def get_rincian_pembayaran(self):
        """
        Get rincian pembayaran dalam format string.
        
        Returns:
            str: Rincian pembayaran lengkap
        """
        rincian = f"=== RINCIAN PEMBAYARAN TRANSAKSI #{self.__id_transaksi} ===\n"
        rincian += f"Pesanan: #{self.__pesanan.id_pesanan}\n"
        rincian += f"Meja: {self.__pesanan.nomor_meja}\n"
        rincian += f"Waktu: {self.__waktu_transaksi.strftime('%d/%m/%Y %H:%M:%S')}\n"
        rincian += f"\n--- ITEMS ---\n"
        
        for item in self.__pesanan.items:
            rincian += f"{item.jumlah}x {item.menu.nama} @ Rp{item.harga_satuan:,.0f} = Rp{item.hitung_subtotal():,.0f}\n"
        
        rincian += f"\n--- PERHITUNGAN ---\n"
        rincian += f"Subtotal          : Rp{self.__subtotal:,.0f}\n"
        rincian += f"Pajak (PPN)       : Rp{self.__pajak_total:,.0f}\n"
        rincian += f"Diskon            : Rp{self.__diskon_total:,.0f}\n"
        rincian += f"{'-' * 40}\n"
        rincian += f"TOTAL             : Rp{self.__total:,.0f}\n"
        
        if self.__status == 'Selesai':
            rincian += f"\n--- PEMBAYARAN ---\n"
            rincian += f"Bayar             : Rp{self.__bayar:,.0f}\n"
            rincian += f"Kembalian         : Rp{self.__kembalian:,.0f}\n"
            rincian += f"Status            : SELESAI\n"
        else:
            rincian += f"\nStatus            : {self.__status}\n"
        
        return rincian
    
    def get_data_untuk_simpan(self):
        """
        Get data transaksi dalam format dictionary untuk penyimpanan ke database.
        
        Returns:
            dict: Data transaksi dalam format dictionary
        """
        return {
            'id_transaksi': self.__id_transaksi,
            'id_pesanan': self.__pesanan.id_pesanan,
            'nomor_meja': self.__pesanan.nomor_meja,
            'subtotal': self.__subtotal,
            'pajak_total': self.__pajak_total,
            'diskon_total': self.__diskon_total,
            'total': self.__total,
            'bayar': self.__bayar,
            'kembalian': self.__kembalian,
            'is_member': self.__is_member,
            'status': self.__status,
            'waktu_transaksi': self.__waktu_transaksi.isoformat(),
            'items': [
                {
                    'menu_id': item.menu.id_menu,
                    'menu_nama': item.menu.nama,
                    'jumlah': item.jumlah,
                    'harga_satuan': item.harga_satuan,
                    'subtotal': item.hitung_subtotal(),
                    'catatan': item.catatan
                }
                for item in self.__pesanan.items
            ]
        }
    
    def __str__(self):
        return f"Transaksi #{self.__id_transaksi} - Meja {self.__pesanan.nomor_meja} - Total: Rp{self.__total:,.0f} - {self.__status}"
