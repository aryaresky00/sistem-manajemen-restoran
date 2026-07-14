"""
SQLite Repository Implementation.
Implementasi konkrit dari BaseRepository menggunakan SQLite database.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from src.repositories.base_repository import BaseRepository
from src.models.menu import Menu
from src.models.makanan import Makanan
from src.models.minuman import Minuman
from src.models.pesanan import Pesanan, ItemPesanan
from src.models.transaksi import Transaksi
from src.exceptions.menu_exception import MenuTidakDitemukanException, MenuSudahAdaException


class DbRepository(BaseRepository):
    """
    SQLite database implementation dari BaseRepository.
    
    Database Schema:
        - menu: Menyimpan semua item menu
        - pesanan: Menyimpan pesanan
        - item_pesanan: Menyimpan items dalam setiap pesanan
        - transaksi: Menyimpan transaksi pembayaran
    """
    
    def __init__(self, db_path="data/restoran.db"):
        """
        Initialize SQLite database.
        
        Args:
            db_path: Path ke database file
        """
        self.db_path = db_path
        self._inisialisasi_database()
    
    def _get_connection(self):
        """
        Get database connection.
        
        Returns:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Untuk akses kolom dengan nama
        return conn
    
    def _inisialisasi_database(self):
        """Initialize database schema jika belum ada."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Create menu table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS menu (
                    id_menu INTEGER PRIMARY KEY,
                    nama TEXT NOT NULL UNIQUE,
                    harga REAL NOT NULL,
                    kategori TEXT NOT NULL,
                    tingkat_pedas INTEGER,
                    jenis_gelas TEXT,
                    dingin INTEGER,
                    status_tersedia INTEGER DEFAULT 1,
                    tanggal_ditambahkan TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create pesanan table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pesanan (
                    id_pesanan INTEGER PRIMARY KEY,
                    nomor_meja INTEGER NOT NULL,
                    status TEXT DEFAULT 'Aktif',
                    waktu_pesan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    waktu_selesai TIMESTAMP
                )
            """)
            
            # Create item_pesanan table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS item_pesanan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_pesanan INTEGER NOT NULL,
                    id_menu INTEGER NOT NULL,
                    jumlah INTEGER NOT NULL,
                    harga_satuan REAL NOT NULL,
                    catatan TEXT,
                    waktu_ditambahkan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_pesanan) REFERENCES pesanan(id_pesanan),
                    FOREIGN KEY (id_menu) REFERENCES menu(id_menu)
                )
            """)
            
            # Create transaksi table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transaksi (
                    id_transaksi INTEGER PRIMARY KEY,
                    id_pesanan INTEGER NOT NULL,
                    nomor_meja INTEGER NOT NULL,
                    subtotal REAL NOT NULL,
                    pajak_total REAL NOT NULL,
                    diskon_total REAL NOT NULL,
                    total REAL NOT NULL,
                    bayar REAL DEFAULT 0,
                    kembalian REAL DEFAULT 0,
                    is_member INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'Pending',
                    waktu_transaksi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    items_json TEXT,
                    FOREIGN KEY (id_pesanan) REFERENCES pesanan(id_pesanan)
                )
            """)
            
            conn.commit()
        finally:
            conn.close()
    
    def inisialisasi_id_counters(self):
        """
        Inisialisasi ID counters dari database untuk menghindari konflik.
        Method ini harus dipanggil saat aplikasi startup.
        Semua model classes sudah di-import di top level untuk menghindari circular import issue.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Initialize Menu counter
            cursor.execute("SELECT MAX(id_menu) FROM menu")
            max_menu_id = cursor.fetchone()[0] or 0
            if max_menu_id >= Menu._id_counter:
                Menu._id_counter = max_menu_id + 1
            
            # Initialize Pesanan counter
            cursor.execute("SELECT MAX(id_pesanan) FROM pesanan")
            max_pesanan_id = cursor.fetchone()[0] or 0
            if max_pesanan_id >= Pesanan._id_counter:
                Pesanan._id_counter = max_pesanan_id + 1
            
            # Initialize Transaksi counter
            cursor.execute("SELECT MAX(id_transaksi) FROM transaksi")
            max_transaksi_id = cursor.fetchone()[0] or 0
            if max_transaksi_id >= Transaksi._id_counter:
                Transaksi._id_counter = max_transaksi_id + 1
                
        except Exception as e:
            print(f"Warning: Error initializing counters: {e}")
            import traceback
            traceback.print_exc()
        finally:
            conn.close()
    
    # ==================== MENU OPERATIONS ====================
    
    def simpan_menu(self, menu):
        """Simpan menu baru ke database."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            if isinstance(menu, Makanan):
                cursor.execute("""
                    INSERT INTO menu (nama, harga, kategori, tingkat_pedas, status_tersedia)
                    VALUES (?, ?, ?, ?, ?)
                """, (menu.nama, menu.harga, menu.kategori, menu.tingkat_pedas, 
                      1 if menu.status_tersedia else 0))
            elif isinstance(menu, Minuman):
                cursor.execute("""
                    INSERT INTO menu (nama, harga, kategori, jenis_gelas, dingin, status_tersedia)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (menu.nama, menu.harga, menu.kategori, menu.jenis_gelas, 
                      1 if menu.dingin else 0, 1 if menu.status_tersedia else 0))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            raise MenuSudahAdaException(f"Menu '{menu.nama}' sudah ada")
        finally:
            conn.close()
    
    def baca_menu(self, menu_id):
        """Baca menu berdasarkan ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM menu WHERE id_menu = ?", (menu_id,))
            row = cursor.fetchone()
            
            if not row:
                raise MenuTidakDitemukanException(f"Menu dengan ID {menu_id} tidak ditemukan")
            
            return self._row_to_menu(row)
        finally:
            conn.close()
    
    def baca_semua_menu(self):
        """Baca semua menu."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM menu ORDER BY kategori, nama")
            rows = cursor.fetchall()
            
            return [self._row_to_menu(row) for row in rows]
        finally:
            conn.close()
    
    def ubah_menu(self, menu):
        """Update menu yang sudah ada."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            if isinstance(menu, Makanan):
                cursor.execute("""
                    UPDATE menu SET nama = ?, harga = ?, tingkat_pedas = ?, status_tersedia = ?
                    WHERE id_menu = ?
                """, (menu.nama, menu.harga, menu.tingkat_pedas, 
                      1 if menu.status_tersedia else 0, menu.id_menu))
            elif isinstance(menu, Minuman):
                cursor.execute("""
                    UPDATE menu SET nama = ?, harga = ?, jenis_gelas = ?, dingin = ?, status_tersedia = ?
                    WHERE id_menu = ?
                """, (menu.nama, menu.harga, menu.jenis_gelas, 
                      1 if menu.dingin else 0, 1 if menu.status_tersedia else 0, menu.id_menu))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def hapus_menu(self, menu_id):
        """Hapus menu."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM menu WHERE id_menu = ?", (menu_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def _row_to_menu(self, row):
        """Convert database row ke Menu object."""
        # Simpan dan kembalikan counter agar reconstruct tidak increment ID
        old_counter = Menu._id_counter
        if row['kategori'] == 'Makanan':
            menu = Makanan(row['nama'], row['harga'], row['tingkat_pedas'] or 0)
        else:  # Minuman
            menu = Minuman(row['nama'], row['harga'], row['jenis_gelas'] or 'Medium', 
                          bool(row['dingin']))
        Menu._id_counter = old_counter
        
        # Set ID dari database
        menu._Menu__id_menu = row['id_menu']
        menu._Menu__status_tersedia = bool(row['status_tersedia'])
        
        return menu
    
    # ==================== PESANAN OPERATIONS ====================
    
    def simpan_pesanan(self, pesanan):
        """Simpan pesanan baru ke database."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO pesanan (id_pesanan, nomor_meja, status, waktu_pesan)
                VALUES (?, ?, ?, ?)
            """, (pesanan.id_pesanan, pesanan.nomor_meja, pesanan.status, 
                  pesanan.waktu_pesan))
            
            # Simpan items pesanan
            for item in pesanan.items:
                cursor.execute("""
                    INSERT INTO item_pesanan (id_pesanan, id_menu, jumlah, harga_satuan, catatan)
                    VALUES (?, ?, ?, ?, ?)
                """, (pesanan.id_pesanan, item.menu.id_menu, item.jumlah, 
                      item.harga_satuan, item.catatan))
            
            conn.commit()
            return True
        finally:
            conn.close()
    
    def baca_pesanan(self, pesanan_id):
        """Baca pesanan berdasarkan ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM pesanan WHERE id_pesanan = ?", (pesanan_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            # Reconstruct pesanan object
            old_counter = Pesanan._id_counter
            pesanan = Pesanan(row['nomor_meja'])
            Pesanan._id_counter = old_counter
            pesanan._Pesanan__id_pesanan = row['id_pesanan']
            pesanan._Pesanan__status = row['status']
            pesanan._Pesanan__waktu_pesan = datetime.fromisoformat(row['waktu_pesan'])
            
            if row['waktu_selesai']:
                pesanan._Pesanan__waktu_selesai = datetime.fromisoformat(row['waktu_selesai'])
            
            # Load items
            cursor.execute("""
                SELECT * FROM item_pesanan WHERE id_pesanan = ?
                ORDER BY waktu_ditambahkan
            """, (pesanan_id,))
            
            pesanan._Pesanan__items = []
            for item_row in cursor.fetchall():
                menu = self.baca_menu(item_row['id_menu'])
                item = ItemPesanan(menu, item_row['jumlah'], item_row['catatan'])
                item._ItemPesanan__harga_satuan = item_row['harga_satuan']
                pesanan._Pesanan__items.append(item)
            
            return pesanan
        finally:
            conn.close()
    
    def baca_semua_pesanan(self):
        """Baca semua pesanan."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id_pesanan FROM pesanan ORDER BY waktu_pesan DESC")
            rows = cursor.fetchall()
            
            pesanan_list = []
            for row in rows:
                pesanan = self.baca_pesanan(row['id_pesanan'])
                if pesanan:
                    pesanan_list.append(pesanan)
            
            return pesanan_list
        finally:
            conn.close()
    
    def baca_pesanan_aktif(self):
        """Baca pesanan yang masih aktif (belum selesai)."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id_pesanan FROM pesanan WHERE status != 'Selesai' ORDER BY waktu_pesan")
            rows = cursor.fetchall()
            
            pesanan_list = []
            for row in rows:
                pesanan = self.baca_pesanan(row['id_pesanan'])
                if pesanan:
                    pesanan_list.append(pesanan)
            
            return pesanan_list
        finally:
            conn.close()
    
    def ubah_pesanan(self, pesanan):
        """Update pesanan dan items-nya."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Update pesanan status
            cursor.execute("""
                UPDATE pesanan SET status = ?, waktu_selesai = ?
                WHERE id_pesanan = ?
            """, (pesanan.status, pesanan.waktu_selesai, pesanan.id_pesanan))
            
            # Delete old items
            cursor.execute("DELETE FROM item_pesanan WHERE id_pesanan = ?", 
                         (pesanan.id_pesanan,))
            
            # Insert new items
            for item in pesanan.items:
                cursor.execute("""
                    INSERT INTO item_pesanan (id_pesanan, id_menu, jumlah, harga_satuan, catatan, waktu_ditambahkan)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (pesanan.id_pesanan, item.menu.id_menu, item.jumlah, 
                      item.harga_satuan, item.catatan, datetime.now()))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def hapus_pesanan(self, pesanan_id):
        """Hapus pesanan dan item-itemnya."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM item_pesanan WHERE id_pesanan = ?", (pesanan_id,))
            cursor.execute("DELETE FROM pesanan WHERE id_pesanan = ?", (pesanan_id,))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    # ==================== TRANSAKSI OPERATIONS ====================
    
    def simpan_transaksi(self, transaksi):
        """Simpan transaksi ke database."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            data = transaksi.get_data_untuk_simpan()
            
            cursor.execute("""
                INSERT INTO transaksi 
                (id_transaksi, id_pesanan, nomor_meja, subtotal, pajak_total, diskon_total, 
                 total, bayar, kembalian, is_member, status, waktu_transaksi, items_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (data['id_transaksi'], data['id_pesanan'], data['nomor_meja'],
                  data['subtotal'], data['pajak_total'], data['diskon_total'],
                  data['total'], data['bayar'], data['kembalian'],
                  1 if data['is_member'] else 0, data['status'], data['waktu_transaksi'],
                  json.dumps(data['items'])))
            
            # Update pesanan status in same transaction to avoid database lock
            cursor.execute("""
                UPDATE pesanan SET status = ?, waktu_selesai = ?
                WHERE id_pesanan = ?
            """, (transaksi.pesanan.status, transaksi.pesanan.waktu_selesai, transaksi.pesanan.id_pesanan))
            
            conn.commit()
            return True
        finally:
            conn.close()
    
    def baca_transaksi(self, transaksi_id):
        """Baca transaksi berdasarkan ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM transaksi WHERE id_transaksi = ?", (transaksi_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            # Reconstruct transaksi object by loading pesanan first
            pesanan = self.baca_pesanan(row['id_pesanan'])
            
            # Create transaksi object only if pesanan has items
            if pesanan and pesanan.jumlah_items > 0:
                old_counter = Transaksi._id_counter
                transaksi = Transaksi(pesanan, bool(row['is_member']))
                Transaksi._id_counter = old_counter
                # Override with values from database to preserve exact history
                transaksi._Transaksi__id_transaksi = row['id_transaksi']
                transaksi._Transaksi__status = row['status']
                transaksi._Transaksi__bayar = row['bayar']
                transaksi._Transaksi__kembalian = row['kembalian']
                
                return transaksi
            else:
                return None
        finally:
            conn.close()
    
    def baca_semua_transaksi(self):
        """Baca semua transaksi."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id_transaksi FROM transaksi ORDER BY waktu_transaksi DESC")
            rows = cursor.fetchall()
            
            transaksi_list = []
            for row in rows:
                transaksi = self.baca_transaksi(row['id_transaksi'])
                if transaksi:
                    transaksi_list.append(transaksi)
            
            return transaksi_list
        finally:
            conn.close()
    
    def baca_transaksi_by_tanggal(self, tanggal):
        """Baca transaksi berdasarkan tanggal (format YYYY-MM-DD)."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id_transaksi FROM transaksi 
                WHERE DATE(waktu_transaksi) = ?
                ORDER BY waktu_transaksi DESC
            """, (tanggal,))
            
            rows = cursor.fetchall()
            transaksi_list = []
            
            for row in rows:
                transaksi = self.baca_transaksi(row['id_transaksi'])
                if transaksi:
                    transaksi_list.append(transaksi)
            
            return transaksi_list
        finally:
            conn.close()
    
    def get_laporan_penjualan_harian(self, tanggal):
        """
        Get laporan penjualan untuk tanggal tertentu.
        
        Returns:
            dict: Laporan dengan total, jumlah transaksi, detail items
        """
        transaksi_list = self.baca_transaksi_by_tanggal(tanggal)
        
        laporan = {
            'tanggal': tanggal,
            'jumlah_transaksi': len(transaksi_list),
            'total_penjualan': 0,
            'total_pajak': 0,
            'total_diskon': 0,
            'items_terjual': {}
        }
        
        for transaksi in transaksi_list:
            if transaksi.status == 'Selesai':
                laporan['total_penjualan'] += transaksi.total
                laporan['total_pajak'] += transaksi.pajak_total
                laporan['total_diskon'] += transaksi.diskon_total
                
                for item in transaksi.pesanan.items:
                    menu_nama = item.menu.nama
                    if menu_nama not in laporan['items_terjual']:
                        laporan['items_terjual'][menu_nama] = {'jumlah': 0, 'total': 0}
                    laporan['items_terjual'][menu_nama]['jumlah'] += item.jumlah
                    laporan['items_terjual'][menu_nama]['total'] += item.hitung_subtotal()
        
        return laporan
    
    def hapus_semua_data(self):
        """Hapus semua data (DANGER: Reset database)."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM item_pesanan")
            cursor.execute("DELETE FROM transaksi")
            cursor.execute("DELETE FROM pesanan")
            cursor.execute("DELETE FROM menu")
            
            conn.commit()
            return True
        finally:
            conn.close()
