"""
CetakService - Service untuk cetak struk dan laporan.
Implementasi polymorphism untuk berbagai format laporan.
"""

from datetime import datetime
from pathlib import Path


class CetakService:
    """
    Service untuk mengekspor struk dan laporan ke file.
    
    Implementasi polymorphism:
    - Setiap tipe laporan dapat memiliki format berbeda
    - Fleksibel untuk penambahan format baru (PDF, Excel, dll)
    """
    
    def __init__(self, output_dir="data"):
        """
        Initialize CetakService.
        
        Args:
            output_dir: Direktori untuk output file (default: data/)
        """
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    # ==================== STRUK DIGITAL ====================
    
    def cetak_struk_ke_file(self, transaksi):
        """
        Cetak struk belanja ke file .txt (polymorphic).
        
        Args:
            transaksi: Objek Transaksi yang akan dicetak
            
        Returns:
            str: Path file struk yang sudah dicetak
        """
        struk_content = self._format_struk(transaksi)
        
        # Generate filename
        timestamp = transaksi.waktu_transaksi.strftime("%Y%m%d_%H%M%S")
        filename = f"Struk_#{transaksi.id_transaksi}_{timestamp}.txt"
        filepath = Path(self.output_dir) / filename
        
        # Simpan ke file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(struk_content)
        
        return str(filepath)
    
    def _format_struk(self, transaksi):
        """
        Format struk dalam bentuk string.
        
        Args:
            transaksi: Objek Transaksi
            
        Returns:
            str: Struk yang sudah diformat
        """
        struk = ""
        struk += "=" * 60 + "\n"
        struk += " " * 15 + "== STRUK BELANJA ==\n"
        struk += "=" * 60 + "\n\n"
        
        # Header info
        struk += f"Nomor Struk    : #{transaksi.id_transaksi}\n"
        struk += f"Tanggal & Waktu: {transaksi.waktu_transaksi.strftime('%d/%m/%Y %H:%M:%S')}\n"
        struk += f"Meja           : {transaksi.pesanan.nomor_meja}\n"
        struk += f"Status Member  : {'Ya (Member)' if transaksi.is_member else 'Tidak (Umum)'}\n"
        struk += "-" * 60 + "\n\n"
        
        # Items list
        struk += "ITEM-ITEM PESANAN:\n"
        struk += "-" * 60 + "\n"
        
        no = 1
        for item in transaksi.pesanan.items:
            menu_str = item.menu.nama
            if item.catatan:
                menu_str += f" ({item.catatan})"
            
            subtotal = item.hitung_subtotal()
            struk += f"{no:2d}. {item.jumlah:3d}x {menu_str}\n"
            struk += f"    @ Rp{item.harga_satuan:>10,.0f} = Rp{subtotal:>12,.0f}\n"
            no += 1
        
        struk += "\n" + "-" * 60 + "\n"
        
        # Calculation
        struk += f"Subtotal                    : Rp{transaksi.subtotal:>15,.0f}\n"
        struk += f"Pajak (PPN)                 : Rp{transaksi.pajak_total:>15,.0f}\n"
        
        if transaksi.diskon_total > 0:
            struk += f"Diskon                      : Rp{transaksi.diskon_total:>15,.0f}\n"
        
        struk += "-" * 60 + "\n"
        struk += f"TOTAL PEMBAYARAN            : Rp{transaksi.total:>15,.0f}\n"
        struk += "-" * 60 + "\n\n"
        
        # Payment info
        if transaksi.status == 'Selesai':
            struk += "PEMBAYARAN:\n"
            struk += f"Uang Diterima               : Rp{transaksi.bayar:>15,.0f}\n"
            struk += f"Uang Kembalian              : Rp{transaksi.kembalian:>15,.0f}\n"
            struk += "\n" + "=" * 60 + "\n"
            struk += " " * 17 + "TERIMAKASIH!\n"
        else:
            struk += f"Status: {transaksi.status}\n"
            struk += "=" * 60 + "\n"
        
        # Footer
        struk += f"Dicetak pada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        struk += "=" * 60 + "\n"
        
        return struk
    
    # ==================== LAPORAN HARIAN ====================
    
    def cetak_laporan_harian(self, tanggal, laporan_data):
        """
        Cetak laporan penjualan harian ke file .txt (polymorphic).
        
        Args:
            tanggal: Tanggal dalam format YYYY-MM-DD
            laporan_data: Dict berisi data laporan dari service
            
        Returns:
            str: Path file laporan yang sudah dicetak
        """
        laporan_content = self._format_laporan_harian(tanggal, laporan_data)
        
        # Generate filename
        filename = f"Laporan_Harian_{tanggal}.txt"
        filepath = Path(self.output_dir) / filename
        
        # Simpan ke file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(laporan_content)
        
        return str(filepath)
    
    def _format_laporan_harian(self, tanggal, laporan_data):
        """
        Format laporan harian dalam bentuk string.
        
        Args:
            tanggal: Tanggal laporan
            laporan_data: Dict berisi data laporan
            
        Returns:
            str: Laporan yang sudah diformat
        """
        laporan = ""
        laporan += "=" * 70 + "\n"
        laporan += " " * 15 + "== LAPORAN PENJUALAN HARIAN ==\n"
        laporan += "=" * 70 + "\n\n"
        
        # Header
        laporan += f"Tanggal                 : {tanggal}\n"
        laporan += f"Total Transaksi Selesai : {laporan_data['jumlah_transaksi']} transaksi\n"
        laporan += f"Dicetak pada            : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        laporan += "-" * 70 + "\n\n"
        
        # Summary
        laporan += "RINGKASAN KEUANGAN:\n"
        laporan += f"  Total Penjualan (Netto)  : Rp{laporan_data['total_penjualan']:>15,.0f}\n"
        laporan += f"  Total Pajak (PPN)        : Rp{laporan_data['total_pajak']:>15,.0f}\n"
        laporan += f"  Total Diskon             : Rp{laporan_data['total_diskon']:>15,.0f}\n"
        laporan += "-" * 70 + "\n\n"
        
        # Items terjual
        if laporan_data['items_terjual']:
            laporan += "MENU YANG TERJUAL:\n"
            laporan += f"{'No':<3} {'Menu':<35} {'Qty':<5} {'Subtotal':>15}\n"
            laporan += "-" * 70 + "\n"
            
            no = 1
            for menu_nama, info in sorted(laporan_data['items_terjual'].items()):
                laporan += f"{no:<3} {menu_nama:<35} {info['jumlah']:<5} Rp{info['total']:>12,.0f}\n"
                no += 1
            
            laporan += "-" * 70 + "\n"
        else:
            laporan += "Tidak ada penjualan pada tanggal ini.\n"
        
        laporan += "=" * 70 + "\n"
        
        return laporan
    
    # ==================== LAPORAN MENU TERJUAL ====================
    
    def cetak_laporan_menu_terjual(self, laporan_data):
        """
        Cetak laporan menu yang terjual.
        
        Args:
            laporan_data: Dict berisi data laporan
            
        Returns:
            str: Path file laporan yang sudah dicetak
        """
        laporan_content = self._format_laporan_menu(laporan_data)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Laporan_Menu_{timestamp}.txt"
        filepath = Path(self.output_dir) / filename
        
        # Simpan ke file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(laporan_content)
        
        return str(filepath)
    
    def _format_laporan_menu(self, laporan_data):
        """
        Format laporan menu dalam bentuk string.
        
        Args:
            laporan_data: Dict berisi data menu terjual
            
        Returns:
            str: Laporan yang sudah diformat
        """
        laporan = ""
        laporan += "=" * 70 + "\n"
        laporan += " " * 10 + "== LAPORAN MENU PALING BANYAK TERJUAL ==\n"
        laporan += "=" * 70 + "\n\n"
        
        # Header
        laporan += f"Dicetak pada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        laporan += "-" * 70 + "\n\n"
        
        if laporan_data.get('items_terjual'):
            # Sort by jumlah descending
            items_sorted = sorted(
                laporan_data['items_terjual'].items(),
                key=lambda x: x[1]['jumlah'],
                reverse=True
            )
            
            laporan += f"{'Peringkat':<8} {'Menu':<35} {'Qty':<5} {'Subtotal':>15}\n"
            laporan += "-" * 70 + "\n"
            
            for idx, (menu_nama, info) in enumerate(items_sorted, 1):
                laporan += f"{idx:<8} {menu_nama:<35} {info['jumlah']:<5} Rp{info['total']:>12,.0f}\n"
            
            laporan += "-" * 70 + "\n"
        else:
            laporan += "Belum ada data penjualan menu.\n"
        
        laporan += "=" * 70 + "\n"
        
        return laporan
    
    # ==================== UTILITY METHODS ====================
    
    def lihat_file_struk(self, file_path):
        """
        Baca dan tampilkan isi file struk.
        
        Args:
            file_path: Path ke file struk
            
        Returns:
            str: Isi file struk
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"File tidak ditemukan: {file_path}"
    
    def list_file_struk(self):
        """
        List semua file struk yang sudah dibuat.
        
        Returns:
            list: Daftar file struk (.txt)
        """
        struk_files = []
        for file in Path(self.output_dir).glob("Struk_*.txt"):
            struk_files.append({
                'nama': file.name,
                'path': str(file),
                'size': file.stat().st_size,
                'modified': datetime.fromtimestamp(file.stat().st_mtime)
            })
        
        return sorted(struk_files, key=lambda x: x['modified'], reverse=True)
