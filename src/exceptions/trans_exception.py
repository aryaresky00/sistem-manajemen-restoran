"""
Custom exceptions untuk operasi Transaksi dan Pemesanan.
"""


class TransaksiException(Exception):
    """Base exception untuk Transaksi operations."""
    pass


class InputTidakValidException(TransaksiException):
    """Exception ketika input tidak valid."""
    def __init__(self, pesan="Input tidak valid"):
        self.pesan = pesan
        super().__init__(self.pesan)


class MejaTidakTemukanException(TransaksiException):
    """Exception ketika meja tidak ditemukan."""
    def __init__(self, pesan="Meja tidak ditemukan"):
        self.pesan = pesan
        super().__init__(self.pesan)


class PesananKosongException(TransaksiException):
    """Exception ketika pesanan kosong (tidak ada items)."""
    def __init__(self, pesan="Pesanan kosong"):
        self.pesan = pesan
        super().__init__(self.pesan)


class PembayaranTidakValidException(TransaksiException):
    """Exception ketika pembayaran tidak valid."""
    def __init__(self, pesan="Pembayaran tidak valid"):
        self.pesan = pesan
        super().__init__(self.pesan)
