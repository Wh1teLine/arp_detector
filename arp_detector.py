import subprocess
import time
from datetime import datetime
import sys
import os

def get_arp_table():
    """
    Menjalankan perintah 'arp -a' dari terminal/CMD secara otomatis di latar belakang.
    Mengembalikan seluruh teks hasil perintah tersebut.
    """
    # Menggunakan subprocess lokal OS agar tidak bergantung pada library eksternal yang rumit
    result = subprocess.check_output(['arp', '-a'], encoding='utf-8', errors='ignore')
    return result

def parse_arp_table(raw_output):
    """
    Menganalisis teks arp -a untuk mencari anomali Duplikat.
    Struktur data yang dihasilkan: dictionary { 'MAC_ADDRESS': ['IP1', 'IP2'] }
    """
    mac_dict = {}
    lines = raw_output.split('\n')
    
    for line in lines:
        parts = line.strip().split()
        # Baris yang valid berisi IP Address [0] dan MAC Address [1]
        if len(parts) >= 2:
            ip = parts[0]
            mac = parts[1]
            
            # Validasi sederhana: IP memiliki 3 titik, MAC memiliki strip/titik dua
            if ip.count('.') == 3 and ('-' in mac or ':' in mac):
                # Abaikan alamat Broadcast dan Multicast sistem internal
                if mac.lower() in ('ff-ff-ff-ff-ff-ff', '00-00-00-00-00-00') or mac.lower().startswith(('01-00-5e', '33-33-')):
                    continue
                    
                if mac not in mac_dict:
                    mac_dict[mac] = []
                mac_dict[mac].append(ip)
                
    return mac_dict

def start_monitor(interval_detik=5):
    print("=" * 65)
    print("🛡️  Sistem Pertahanan Anti-ARP Spoofing (Layer 2 IDS) 🛡️")
    print(f"Memantau aktivitas jaringan lokal setiap {interval_detik} detik...")
    print("Tekan Ctrl+C untuk menghentikan penjagaan.")
    print("=" * 65 + "\n")
    
    try:
        while True:
            # 1. Ambil data mentah ARP
            raw_arp = get_arp_table()
            
            # 2. Olah menjadi data yang mudah dicek
            mac_table = parse_arp_table(raw_arp)
            
            spoof_detected = False
            
            # 3. Analisis Keamanan Siber: Cari yang Duplikat
            for mac, ips in mac_table.items():
                if len(ips) > 1:
                    spoof_detected = True
                    print("\n[!!!] ALERT: SERANGAN MAN-IN-THE-MIDDLE TERDETEKSI [!!!]")
                    print(f"Waktu       : {datetime.now().strftime('%H:%M:%S')}")
                    print(f"Analisis    : Seseorang mencoba menyadap lalu lintas jaringan!")
                    print(f"MAC Penyerang: {mac}")
                    print("MAC Penyerang menipu komputer Anda untuk mengaku sebagai IP berikut:")
                    for ip in ips:
                        if ip.endswith('.1') or ip.endswith('.254'):
                            print(f" -> {ip} (KEMUNGKINAN BESAR INI ADALAH ROUTER/GATEWAY UTAMA)")
                        else:
                            print(f" -> {ip}")
                    print("Saran       : Segera putuskan koneksi dari Wi-Fi / Jaringan ini!\n")
                    
            if not spoof_detected:
                # Timpa/hapus baris agar tidak memenuhi layar (Carriage Return)
                sys.stdout.write(f"\r[{datetime.now().strftime('%H:%M:%S')}] Status Aman: Tidak ada penyadapan (ARP Spoofing) lokal di jaringan.")
                sys.stdout.flush()
                
            time.sleep(interval_detik)
            
    except KeyboardInterrupt:
        print("\n\n[INFO] Sistem radar pertahanan dihentikan. Berhenti memonitor.")
        sys.exit()

if __name__ == '__main__':
    # Membersihkan layar CMD (Clear Screen)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Jalankan monitor dengan jeda 5 detik
    start_monitor(interval_detik=5)
