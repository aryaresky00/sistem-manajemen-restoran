"""
Main.py - Entry point CLI untuk Sistem Manajemen Restoran.
Interactive menu-based command line interface.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.repositories.db_repository import DbRepository
from src.services.restoran_service import RestoranService
from src.services.cetak_service import CetakService
from src.exceptions.menu_exception import (
    MenuTidakDitemukanException,
    MenuSudahAdaException,
    StokHabiException
)
from src.exceptions.trans_exception import (
    InputTidakValidException,
    MejaTidakTemukanException,
    PesananKosongException,
    PembayaranTidakValidException
)


class RestoranCLI:
    """Interactive CLI untuk Sistem Manajemen Restoran."""
    
    def __init__(self):
        """Initialize CLI dengan repository dan services."""
        self.repository = DbRepository("data/restoran.db")
        # Initialize ID counters dari database untuk menghindari konflik
        self.repository.inisialisasi_id_counters()
        self.service = RestoranService(self.repository)
        self.cetak_service = CetakService("data")
        self.running = True
    
    def clear_screen(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print formatted header."""
        print("\n" + "=" * 70)
        print(f"  {title.center(66)}")
        print("=" * 70)
    
    def print_menu(self, options):
        """Print menu options."""
        for key, value in options.items():
            print(f"  {key}. {value}")
        print()
    
    def input_angka(self, prompt="Pilihan Anda: "):
        """Get integer input from user."""
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("  ❌ Input harus berupa angka!")
    
    def input_teks(self, prompt="Input: "):
        """Get text input from user."""
        return input(prompt).strip()
    
    def input_desimal(self, prompt="Input: "):
        """Get float input from user."""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("  ❌ Input harus berupa angka!")
    
    def pause(self):
        """Pause and wait for user input."""
        input("\n  Tekan ENTER untuk melanjutkan...")
    
    # ==================== MAIN MENU ====================
    
    def main_menu(self):
        """Main menu loop."""
        while self.running:
            self.clear_screen()
            self.print_header("SISTEM MANAJEMEN RESTORAN/KAFE")
            
            options = {
                1: "Manajemen Menu",
                2: "Sistem Pemesanan",
                3: "Lihat Pesanan Aktif",
                4: "Proses Pembayaran",
                5: "Cetak Struk",
                6: "Laporan Penjualan",
                7: "Reset Database (Hati-hati!)",
                0: "Keluar Aplikasi"
            }
            
            self.print_menu(options)
            pilihan = self.input_angka("Pilihan Anda: ")
            
            try:
                if pilihan == 1:
                    self.menu_manajemen_menu()
                elif pilihan == 2:
                    self.menu_sistem_pemesanan()
                elif pilihan == 3:
                    self.menu_lihat_pesanan()
                elif pilihan == 4:
                    self.menu_proses_pembayaran()
                elif pilihan == 5:
                    self.menu_cetak_struk()
                elif pilihan == 6:
                    self.menu_laporan_penjualan()
                elif pilihan == 7:
                    self.menu_reset_database()
                elif pilihan == 0:
                    self.keluar_aplikasi()
                else:
                    print("  ❌ Pilihan tidak valid!")
                    self.pause()
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                self.pause()
    
    # ==================== MANAJEMEN MENU ====================
    
    def menu_manajemen_menu(self):
        """Sub-menu untuk manajemen menu."""
        while True:
            self.clear_screen()
            self.print_header("MANAJEMEN MENU")
            
            options = {
                1: "Lihat Semua Menu",
                2: "Tambah Menu Makanan",
                3: "Tambah Menu Minuman",
                4: "Ubah Menu",
                5: "Hapus Menu",
                6: "Cari Menu",
                0: "Kembali ke Menu Utama"
            }
            
            self.print_menu(options)
            pilihan = self.input_angka("Pilihan Anda: ")
            
            if pilihan == 1:
                self.lihat_semua_menu()
            elif pilihan == 2:
                self.tambah_menu_makanan()
            elif pilihan == 3:
                self.tambah_menu_minuman()
            elif pilihan == 4:
                self.ubah_menu()
            elif pilihan == 5:
                self.hapus_menu()
            elif pilihan == 6:
                self.cari_menu()
            elif pilihan == 0:
                break
            else:
                print("  ❌ Pilihan tidak valid!")
                self.pause()
    
    def lihat_semua_menu(self):
        """Tampilkan semua menu."""
        self.clear_screen()
        self.print_header("DAFTAR SEMUA MENU")
        
        try:
            menus = self.service.lihat_semua_menu()
            
            if not menus:
                print("  Belum ada menu. Tambahkan menu terlebih dahulu.")
                self.pause()
                return
            
            # Group by kategori
            makanan_list = [m for m in menus if m.kategori == 'Makanan']
            minuman_list = [m for m in menus if m.kategori == 'Minuman']
            
            if makanan_list:
                print("\n  === MAKANAN ===")
                print(f"  {'ID':<4} {'Nama':<35} {'Harga':<12} {'Status':<10}")
                print("  " + "-" * 65)
                for m in makanan_list:
                    status = "✓ Ada" if m.status_tersedia else "✗ Habis"
                    print(f"  {m.id_menu:<4} {m.nama:<35} Rp{m.harga:>10,.0f}  {status:<10}")
            
            if minuman_list:
                print("\n  === MINUMAN ===")
                print(f"  {'ID':<4} {'Nama':<35} {'Harga':<12} {'Status':<10}")
                print("  " + "-" * 65)
                for m in minuman_list:
                    status = "✓ Ada" if m.status_tersedia else "✗ Habis"
                    print(f"  {m.id_menu:<4} {m.nama:<35} Rp{m.harga:>10,.0f}  {status:<10}")
            
            print(f"\n  Total Menu: {len(menus)}")
            self.pause()
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            self.pause()
    
    def tambah_menu_makanan(self):
        """Tambah menu makanan."""
        self.clear_screen()
        self.print_header("TAMBAH MENU MAKANAN")
        
        try:
            nama = self.input_teks("Nama Makanan: ")
            harga = self.input_desimal("Harga Makanan (Rp): ")
            
            print("\n  Tingkat Pedas (0-5):")
            print("    0 = Tidak pedas")
            print("    1 = Sedikit pedas")
            print("    2 = Sedang")
            print("    3 = Pedas")
            print("    4 = Sangat pedas")
            print("    5 = Ekstrem")
            
            tingkat_pedas = self.input_angka("Pilihan tingkat pedas: ")
            
            makanan = self.service.tambah_menu_makanan(nama, harga, tingkat_pedas)
            print(f"\n  ✓ Menu makanan '{makanan.nama}' berhasil ditambahkan!")
            self.pause()
        except InputTidakValidException as e:
            print(f"  ❌ Input tidak valid: {e}")
            self.pause()
        except MenuSudahAdaException as e:
            print(f"  ❌ {e}")
            self.pause()
    
    def tambah_menu_minuman(self):
        """Tambah menu minuman."""
        self.clear_screen()
        self.print_header("TAMBAH MENU MINUMAN")
        
        try:
            nama = self.input_teks("Nama Minuman: ")
            harga = self.input_desimal("Harga Minuman (Rp): ")
            
            print("\n  Jenis Gelas:")
            print("    1 = Small")
            print("    2 = Medium")
            print("    3 = Large")
            
            pilihan_gelas = self.input_angka("Pilihan jenis gelas: ")
            gelas_map = {1: 'Small', 2: 'Medium', 3: 'Large'}
            jenis_gelas = gelas_map.get(pilihan_gelas, 'Medium')
            
            print("\n  Suhu Penyajian:")
            print("    1 = Dingin")
            print("    2 = Panas")
            
            pilihan_suhu = self.input_angka("Pilihan suhu: ")
            dingin = pilihan_suhu == 1
            
            minuman = self.service.tambah_menu_minuman(nama, harga, jenis_gelas, dingin)
            print(f"\n  ✓ Menu minuman '{minuman.nama}' berhasil ditambahkan!")
            self.pause()
        except InputTidakValidException as e:
            print(f"  ❌ Input tidak valid: {e}")
            self.pause()
        except MenuSudahAdaException as e:
            print(f"  ❌ {e}")
            self.pause()
    
    def ubah_menu(self):
        """Ubah menu yang ada."""
        self.clear_screen()
        self.print_header("UBAH MENU")
        
        try:
            menu_id = self.input_angka("ID Menu yang akan diubah: ")
            menu = self.service.repository.baca_menu(menu_id)
            
            print(f"\n  Menu saat ini: {menu.nama}")
            print(f"  Harga saat ini: Rp{menu.harga:,.0f}")
            print(f"  Status saat ini: {'Tersedia' if menu.status_tersedia else 'Tidak tersedia'}")
            
            print("\n  Pilih yang akan diubah:")
            print("    1 = Nama")
            print("    2 = Harga")
            print("    3 = Status Ketersediaan")
            
            pilihan = self.input_angka("Pilihan: ")
            
            if pilihan == 1:
                nama_baru = self.input_teks("Nama baru: ")
                self.service.ubah_menu(menu_id, nama=nama_baru)
            elif pilihan == 2:
                harga_baru = self.input_desimal("Harga baru (Rp): ")
                self.service.ubah_menu(menu_id, harga=harga_baru)
            elif pilihan == 3:
                print("    1 = Tersedia")
                print("    2 = Tidak tersedia")
                status_pilihan = self.input_angka("Pilihan status: ")
                status = status_pilihan == 1
                self.service.ubah_menu(menu_id, status_tersedia=status)
            
            print(f"\n  ✓ Menu berhasil diubah!")
            self.pause()
        except MenuTidakDitemukanException as e:
            print(f"  ❌ {e}")
            self.pause()
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            self.pause()
    
    def hapus_menu(self):
        """Hapus menu."""
        self.clear_screen()
        self.print_header("HAPUS MENU")
        
        try:
            menu_id = self.input_angka("ID Menu yang akan dihapus: ")
            menu = self.service.repository.baca_menu(menu_id)
            
            print(f"\n  Anda akan menghapus menu: {menu.nama}")
            print("  Apakah Anda yakin? (y/n): ", end='')
            
            konfirmasi = input().strip().lower()
            if konfirmasi == 'y':
                self.service.hapus_menu(menu_id)
                print(f"  ✓ Menu berhasil dihapus!")
            else:
                print("  Pembatalan.")
            
            self.pause()
        except MenuTidakDitemukanException as e:
            print(f"  ❌ {e}")
            self.pause()
    
    def cari_menu(self):
        """Cari menu berdasarkan nama."""
        self.clear_screen()
        self.print_header("CARI MENU")
        
        try:
            nama = self.input_teks("Kata kunci pencarian: ")
            hasil = self.service.cari_menu_by_nama(nama)
            
            if not hasil:
                print(f"  Tidak ada menu yang cocok dengan '{nama}'")
                self.pause()
                return
            
            print(f"\n  Hasil pencarian untuk '{nama}':")
            print(f"  {'ID':<4} {'Nama':<35} {'Harga':<12} {'Status':<10}")
            print("  " + "-" * 65)
            
            for m in hasil:
                status = "✓ Ada" if m.status_tersedia else "✗ Habis"
                print(f"  {m.id_menu:<4} {m.nama:<35} Rp{m.harga:>10,.0f}  {status:<10}")
            
            print(f"\n  Total hasil: {len(hasil)}")
            self.pause()
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            self.pause()
    
    # ==================== SISTEM PEMESANAN ====================
    
    def menu_sistem_pemesanan(self):
        """Sub-menu untuk sistem pemesanan."""
        while True:
            self.clear_screen()
            self.print_header("SISTEM PEMESANAN")
            
            options = {
                1: "Buat Pesanan Baru",
                2: "Tambah Item ke Pesanan",
                3: "Hapus Item dari Pesanan",
                4: "Lihat Detail Pesanan",
                0: "Kembali ke Menu Utama"
            }
            
            self.print_menu(options)
            pilihan = self.input_angka("Pilihan Anda: ")
            
            if pilihan == 1:
                self.buat_pesanan()
            elif pilihan == 2:
                self.tambah_item_pesanan()
            elif pilihan == 3:
                self.hapus_item_pesanan()
            elif pilihan == 4:
                self.lihat_detail_pesanan()
            elif pilihan == 0:
                break
            else:
                print("  ❌ Pilihan tidak valid!")
                self.pause()
    
    def buat_pesanan(self):
        """Buat pesanan baru."""
        self.clear_screen()
        self.print_header("BUAT PESANAN BARU")
        
        try:
            nomor_meja = self.input_angka("Nomor Meja: ")
            pesanan = self.service.buat_pesanan(nomor_meja)
            
            print(f"\n  ✓ Pesanan #{pesanan.id_pesanan} untuk meja {nomor_meja} berhasil dibuat!")
            print(f"  Waktu: {pesanan.waktu_pesan.strftime('%d/%m/%Y %H:%M:%S')}")
            self.pause()
        except InputTidakValidException as e:
            print(f"  ❌ Input tidak valid: {e}")
            self.pause()
    
    def tambah_item_pesanan(self):
        """Tambah item ke pesanan."""
        self.clear_screen()
        self.print_header("TAMBAH ITEM KE PESANAN")
        
        try:
            # Lihat pesanan aktif
            pesanan_aktif = self.service.lihat_semua_pesanan_aktif()
            if not pesanan_aktif:
                print("  Tidak ada pesanan aktif. Buat pesanan terlebih dahulu.")
                self.pause()
                return
            
            print("\n  Pesanan Aktif:")
            for p in pesanan_aktif:
                print(f"    {p.id_pesanan}. Meja {p.nomor_meja} ({len(p.items)} items)")
            
            pesanan_id = self.input_angka("\nID Pesanan: ")
            pesanan = self.service.lihat_pesanan_aktif(pesanan_id)
            
            # Lihat menu tersedia
            menus = self.service.lihat_menu_tersedia()
            if not menus:
                print("  Tidak ada menu yang tersedia.")
                self.pause()
                return
            
            print("\n  Menu Tersedia:")
            for i, m in enumerate(menus, 1):
                print(f"    {i}. {m.nama:<35} Rp{m.harga:>10,.0f}")
            
            pilihan_menu = self.input_angka("\nNomor Menu (1-{}): ".format(len(menus)))
            if 1 <= pilihan_menu <= len(menus):
                menu = menus[pilihan_menu - 1]
            else:
                print("  ❌ Pilihan menu tidak valid!")
                self.pause()
                return
            
            jumlah = self.input_angka("Jumlah: ")
            catatan = self.input_teks("Catatan khusus (kosongkan jika tidak ada): ")
            
            self.service.tambah_item_ke_pesanan(pesanan_id, menu.id_menu, jumlah, catatan)
            print(f"\n  ✓ {jumlah}x {menu.nama} berhasil ditambahkan ke pesanan!")
            self.pause()
        except MejaTidakTemukanException as e:
            print(f"  ❌ {e}")
            self.pause()
        except InputTidakValidException as e:
            print(f"  ❌ Input tidak valid: {e}")
            self.pause()
    
    def hapus_item_pesanan(self):
        """Hapus item dari pesanan."""
        self.clear_screen()
        self.print_header("HAPUS ITEM DARI PESANAN")
        
        try:
            pesanan_aktif = self.service.lihat_semua_pesanan_aktif()
            if not pesanan_aktif:
                print("  Tidak ada pesanan aktif.")
                self.pause()
                return
            
            print("\n  Pesanan Aktif:")
            for p in pesanan_aktif:
                print(f"    {p.id_pesanan}. Meja {p.nomor_meja} ({len(p.items)} items)")
            
            pesanan_id = self.input_angka("\nID Pesanan: ")
            pesanan = self.service.lihat_pesanan_aktif(pesanan_id)
            
            if not pesanan.items:
                print("  Pesanan ini belum memiliki items.")
                self.pause()
                return
            
            print("\n  Items dalam pesanan:")
            for i, item in enumerate(pesanan.items):
                print(f"    {i}. {item.get_info()}")
            
            item_index = self.input_angka("Nomor item yang akan dihapus: ")
            self.service.hapus_item_dari_pesanan(pesanan_id, item_index)
            
            print(f"\n  ✓ Item berhasil dihapus!")
            self.pause()
        except (MejaTidakTemukanException, InputTidakValidException) as e:
            print(f"  ❌ {e}")
            self.pause()
    
    def lihat_detail_pesanan(self):
        """Lihat detail pesanan."""
        self.clear_screen()
        self.print_header("LIHAT DETAIL PESANAN")
        
        try:
            pesanan_aktif = self.service.lihat_semua_pesanan_aktif()
            if not pesanan_aktif:
                print("  Tidak ada pesanan aktif.")
                self.pause()
                return
            
            print("\n  Pesanan Aktif:")
            for p in pesanan_aktif:
                print(f"    {p.id_pesanan}. Meja {p.nomor_meja} ({len(p.items)} items)")
            
            pesanan_id = self.input_angka("\nID Pesanan: ")
            pesanan = self.service.lihat_pesanan_aktif(pesanan_id)
            
            print("\n" + pesanan.get_detail())
            self.pause()
        except (MejaTidakTemukanException, InputTidakValidException) as e:
            print(f"  ❌ {e}")
            self.pause()
    
    # ==================== LIHAT PESANAN AKTIF ====================
    
    def menu_lihat_pesanan(self):
        """Menu untuk lihat semua pesanan aktif."""
        self.clear_screen()
        self.print_header("PESANAN AKTIF")
        
        try:
            pesanan_list = self.service.lihat_semua_pesanan_aktif()
            
            if not pesanan_list:
                print("  Tidak ada pesanan aktif.")
                self.pause()
                return
            
            print(f"\n  Total Pesanan Aktif: {len(pesanan_list)}\n")
            print(f"  {'ID':<8} {'Meja':<8} {'Items':<8} {'Subtotal':<15} {'Status':<10}")
            print("  " + "-" * 60)
            
            for p in pesanan_list:
                print(f"  {p.id_pesanan:<8} {p.nomor_meja:<8} {len(p.items):<8} Rp{p.hitung_subtotal():>13,.0f}  {p.status:<10}")
            
            self.pause()
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            self.pause()
    
    # ==================== PROSES PEMBAYARAN ====================
    
    def menu_proses_pembayaran(self):
        """Menu untuk proses pembayaran."""
        self.clear_screen()
        self.print_header("PROSES PEMBAYARAN")
        
        try:
            pesanan_aktif = self.service.lihat_semua_pesanan_aktif()
            if not pesanan_aktif:
                print("  Tidak ada pesanan yang siap untuk dibayar.")
                self.pause()
                return
            
            print("\n  Pesanan Aktif:")
            for p in pesanan_aktif:
                print(f"    {p.id_pesanan}. Meja {p.nomor_meja} - Rp{p.hitung_subtotal():,.0f}")
            
            pesanan_id = self.input_angka("\nID Pesanan yang akan dibayar: ")
            pesanan = self.service.lihat_pesanan_aktif(pesanan_id)
            
            # Buat transaksi dan tampilkan rincian
            is_member = self.input_teks("\nApakah pelanggan member? (y/n): ").lower() == 'y'
            transaksi = self.service.buat_transaksi(pesanan_id, is_member)
            
            self.clear_screen()
            self.print_header("RINCIAN PEMBAYARAN")
            print("\n" + transaksi.get_rincian_pembayaran())
            
            # Proses pembayaran
            print("\n" + "=" * 60)
            jumlah_bayar = self.input_desimal("Jumlah pembayaran (Rp): ")
            
            transaksi.proses_pembayaran(jumlah_bayar)
            
            # Simpan transaksi
            self.service.repository.simpan_transaksi(transaksi)
            self.service.pesanan_aktif.pop(pesanan_id, None)
            
            print(f"\n  ✓ Pembayaran berhasil diproses!")
            print(f"  Transaksi ID: #{transaksi.id_transaksi}")
            
            # Tanyakan ingin cetak struk
            print("\nApakah ingin mencetak struk? (y/n): ", end='')
            if input().strip().lower() == 'y':
                filepath = self.cetak_service.cetak_struk_ke_file(transaksi)
                print(f"  ✓ Struk berhasil dicetak ke: {filepath}")
            
            self.pause()
        except MejaTidakTemukanException as e:
            print(f"  ❌ {e}")
            self.pause()
        except PesananKosongException as e:
            print(f"  ❌ {e}")
            self.pause()
        except PembayaranTidakValidException as e:
            print(f"  ❌ {e}")
            self.pause()
    
    # ==================== CETAK STRUK ====================
    
    def menu_cetak_struk(self):
        """Menu untuk cetak/lihat struk."""
        self.clear_screen()
        self.print_header("CETAK STRUK")
        
        try:
            file_list = self.cetak_service.list_file_struk()
            
            if not file_list:
                print("  Belum ada struk yang dibuat.")
                self.pause()
                return
            
            print(f"\n  Total Struk: {len(file_list)}\n")
            print(f"  {'No':<3} {'Nama File':<40} {'Modified':<20}")
            print("  " + "-" * 65)
            
            for i, f in enumerate(file_list, 1):
                modified = f['modified'].strftime('%d/%m/%Y %H:%M:%S')
                print(f"  {i:<3} {f['nama']:<40} {modified:<20}")
            
            pilihan = self.input_angka("\nLihat struk nomor (0 untuk batal): ")
            
            if pilihan == 0:
                return
            
            if 1 <= pilihan <= len(file_list):
                file_path = file_list[pilihan - 1]['path']
                
                self.clear_screen()
                print(self.cetak_service.lihat_file_struk(file_path))
                
                print("\nApakah ingin menyimpan struk? (y/n): ", end='')
                if input().strip().lower() == 'y':
                    # File sudah tersimpan
                    print(f"Struk tersimpan di: {file_path}")
            
            self.pause()
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            self.pause()
    
    # ==================== LAPORAN PENJUALAN ====================
    
    def menu_laporan_penjualan(self):
        """Menu untuk laporan penjualan."""
        while True:
            self.clear_screen()
            self.print_header("LAPORAN PENJUALAN")
            
            options = {
                1: "Laporan Harian",
                2: "Laporan Menu Terjual",
                0: "Kembali ke Menu Utama"
            }
            
            self.print_menu(options)
            pilihan = self.input_angka("Pilihan Anda: ")
            
            if pilihan == 1:
                self.laporan_harian()
            elif pilihan == 2:
                self.laporan_menu_terjual()
            elif pilihan == 0:
                break
            else:
                print("  ❌ Pilihan tidak valid!")
                self.pause()
    
    def laporan_harian(self):
        """Tampilkan laporan harian."""
        self.clear_screen()
        self.print_header("LAPORAN PENJUALAN HARIAN")
        
        try:
            tanggal = self.input_teks("Tanggal (YYYY-MM-DD), kosongkan untuk hari ini: ")
            
            if not tanggal:
                tanggal = datetime.now().strftime('%Y-%m-%d')
            
            laporan = self.service.lihat_laporan_harian(tanggal)
            
            self.clear_screen()
            print("=" * 70)
            print(f"  LAPORAN PENJUALAN HARIAN - {tanggal}".center(66))
            print("=" * 70)
            
            print(f"\n  Total Transaksi Selesai: {laporan['jumlah_transaksi']}")
            print(f"  Total Penjualan         : Rp{laporan['total_penjualan']:>15,.0f}")
            print(f"  Total Pajak (PPN)       : Rp{laporan['total_pajak']:>15,.0f}")
            print(f"  Total Diskon            : Rp{laporan['total_diskon']:>15,.0f}")
            
            if laporan['items_terjual']:
                print("\n  MENU YANG TERJUAL:")
                print(f"  {'Menu':<40} {'Qty':<5} {'Subtotal':>15}")
                print("  " + "-" * 65)
                
                for menu_nama, info in sorted(laporan['items_terjual'].items()):
                    print(f"  {menu_nama:<40} {info['jumlah']:<5} Rp{info['total']:>12,.0f}")
            
            # Tanyakan ingin cetak laporan
            print("\n  Apakah ingin mencetak laporan ke file? (y/n): ", end='')
            if input().strip().lower() == 'y':
                filepath = self.cetak_service.cetak_laporan_harian(tanggal, laporan)
                print(f"  ✓ Laporan berhasil dicetak ke: {filepath}")
            
            self.pause()
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            self.pause()
    
    def laporan_menu_terjual(self):
        """Tampilkan laporan menu terjual."""
        self.clear_screen()
        self.print_header("LAPORAN MENU PALING BANYAK TERJUAL")
        
        try:
            # Get semua transaksi dan compile laporan
            all_transaksi = self.service.repository.baca_semua_transaksi()
            
            items_terjual = {}
            for transaksi in all_transaksi:
                if transaksi.status == 'Selesai':
                    for item in transaksi.pesanan.items:
                        menu_nama = item.menu.nama
                        if menu_nama not in items_terjual:
                            items_terjual[menu_nama] = {'jumlah': 0, 'total': 0}
                        items_terjual[menu_nama]['jumlah'] += item.jumlah
                        items_terjual[menu_nama]['total'] += item.hitung_subtotal()
            
            laporan = {'items_terjual': items_terjual}
            
            self.clear_screen()
            print("=" * 70)
            print("  LAPORAN MENU PALING BANYAK TERJUAL".center(66))
            print("=" * 70)
            
            if items_terjual:
                items_sorted = sorted(items_terjual.items(), key=lambda x: x[1]['jumlah'], reverse=True)
                
                print(f"\n  {'Peringkat':<10} {'Menu':<35} {'Qty':<5} {'Total':>15}")
                print("  " + "-" * 70)
                
                for idx, (menu_nama, info) in enumerate(items_sorted, 1):
                    print(f"  {idx:<10} {menu_nama:<35} {info['jumlah']:<5} Rp{info['total']:>12,.0f}")
            else:
                print("\n  Belum ada data penjualan menu.")
            
            self.pause()
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            self.pause()
    
    # ==================== RESET DATABASE ====================
    
    def menu_reset_database(self):
        """Reset database (dengan konfirmasi)."""
        self.clear_screen()
        self.print_header("RESET DATABASE")
        
        print("\n  ⚠️  PERINGATAN: Operasi ini akan menghapus SEMUA DATA!")
        print("  Data menu, pesanan, dan transaksi akan hilang permanen.")
        print("\n  Apakah Anda yakin ingin melanjutkan? (y/n): ", end='')
        
        konfirmasi = input().strip().lower()
        if konfirmasi == 'y':
            print("  Konfirmasi sekali lagi (y/n): ", end='')
            konfirmasi_2 = input().strip().lower()
            
            if konfirmasi_2 == 'y':
                self.service.reset_database()
                print("\n  ✓ Database berhasil direset!")
            else:
                print("  Pembatalan.")
        else:
            print("  Pembatalan.")
        
        self.pause()
    
    # ==================== EXIT ====================
    
    def keluar_aplikasi(self):
        """Keluar dari aplikasi."""
        self.clear_screen()
        self.print_header("TERIMA KASIH")
        print("\n  Terima kasih telah menggunakan Sistem Manajemen Restoran!")
        print("  Sampai jumpa lagi.\n")
        self.running = False


def main():
    """Entry point aplikasi."""
    cli = RestoranCLI()
    try:
        cli.main_menu()
    except KeyboardInterrupt:
        print("\n\n  Aplikasi dihentikan oleh user.")
    except Exception as e:
        print(f"\n  Error fatal: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
