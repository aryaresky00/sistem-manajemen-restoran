"""
Custom exceptions untuk operasi Menu.
"""


class MenuException(Exception):
    """Base exception untuk Menu operations."""
    pass


class MenuTidakDitemukanException(MenuException):
    """Exception ketika menu tidak ditemukan."""
    def __init__(self, pesan="Menu tidak ditemukan"):
        self.pesan = pesan
        super().__init__(self.pesan)


class MenuSudahAdaException(MenuException):
    """Exception ketika menu sudah ada (duplikat)."""
    def __init__(self, pesan="Menu sudah ada"):
        self.pesan = pesan
        super().__init__(self.pesan)


class StokHabiException(MenuException):
    """Exception ketika stok menu habis."""
    def __init__(self, pesan="Stok menu habis"):
        self.pesan = pesan
        super().__init__(self.pesan)
