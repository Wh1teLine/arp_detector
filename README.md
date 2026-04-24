# 📡 ARP Spoofing Detector

A lightweight, Python-based Layer-2 Intrusion Detection System (IDS) that monitors your local network for Man-In-The-Middle (MITM) attacks via ARP Spoofing.

## 📌 Features
- **Passive Monitoring:** Continuously scans the Windows ARP cache table (`arp -a`) in the background.
- **Duplicate MAC Detection:** Alerts you instantly if multiple IP addresses (especially your gateway/router) are mapped to the same MAC address.
- **No External Dependencies:** Built entirely using native Python libraries (`subprocess`, `time`, etc.). No need to install Scapy or WinPcap/Npcap.

## 🚀 Usage

1. Clone or download this repository.
2. Open your terminal/Command Prompt.
3. Run the script:
   ```bash
   python arp_detector.py
   ```
4. The tool will scan the network every 5 seconds. To stop the monitor, press `Ctrl+C`.

## ⚠️ Disclaimer
**Educational Purposes Only!**  
This tool is strictly for educational purposes and network defense. The author is not responsible for any misuse of this tool.
