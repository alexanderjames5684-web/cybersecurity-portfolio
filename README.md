# 3/5/26

# cybersecurity-portfolio

# Home Security Lab

## Overview
Isolated virtual lab environment built for practicing 
cybersecurity defense, network monitoring, and malware 
analysis safely without risk to my real network.

## Environment
| Machine | OS | IP | Role |
|---|---|---|---|
| Kali-Attacker | Kali Linux | 192.168.100.10 | Security toolset / attacker simulation |
| Windows-Target | Windows 10 | 192.168.100.20 | Target / defender machine |

## Network
- Platform: VMware
- Network Type: LAN Segment (fully isolated)
- Both VMs confirmed communicating via ping test
- No internet access from either VM — completely air-gapped

## Tools Installed
- Wireshark (coming soon)
- Nmap (coming soon)
- Python scripts (coming soon)

## Status
✅ Phase 1 — VM setup complete
✅ Phase 2 — Isolated network configured
🔄 Phase 3 — Security tools and monitoring (in progress)





# 3/7/26 (nmap)
As I was attacking the Windows-Target, I noticed I wasnt getting a response from my nmap. When I tried to perform bash: nmap 192.168.100.20, I was getting nothing in my response. Nmap was telling me all 1000 ports were scanned, but they are all in ignored states. Which meant that what I was dealing with was a filtered port state. This basically just means the ports arent actually closed, they are being blocked by a firewall. This makes it harder for me as an attacker since a machine that returns all filtered ports is harder to fingerprint than one with an open or closed ports. In a real SOC enviorment, if I were to come across this, I would know there is a possible firewall in place somewhere.
- For testing purposes though, I turned off the firewalls in Windows-Target





# 3/8/26 (Python Script/ JSON report)

# Python Security Scripts

## Script 1 — Automated Port Scanner

### What it does
Automates an Nmap -sV -O scan against a target IP and saves
a structured JSON report of all open ports, services, and
version information.

### Tools Used
- Python 3
- python-libnmap
- Nmap 7.95

### Sample Output
Target: 192.168.100.20 (Windows 10 VM — Lab Environment)
Scan Date: 2026-03-08

| Port | Protocol | Service | Details |
|------|----------|---------|---------|
| 135 | tcp | msrpc | Microsoft Windows RPC |
| 139 | tcp | netbios-ssn | Microsoft Windows NetBIOS |
| 445 | tcp | microsoft-ds | SMB — Server Message Block |

### Security Notes
- Port 445 (SMB) is a high-priority finding in any real scan
- This is the port exploited by WannaCry ransomware in 2017
- In a real environment this would trigger immediate investigation

### How to Run
```bash
sudo python3 port_scanner.py
```




