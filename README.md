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

## Key Findings
| Port | Service | Risk Level | Notes |
|------|---------|------------|-------|
| 135 | Microsoft RPC | Medium | Standard Windows port |
| 139 | NetBIOS | Medium | Legacy protocol, monitor closely |
| 445 | SMB | High | Priority finding — WannaCry vector |

## Tools Installed
- Wireshark (coming soon)
- Nmap (coming soon)
- Python scripts (coming soon)

## Status
✅ Phase 1 — VM setup complete
✅ Phase 2 — Isolated network configured
🔄 Phase 3 — Security tools and monitoring (in progress)


# 3/7/26 (Nmap Scan & Firewall Discovery)

While scanning the Windows-Target VM from Kali, I received 
no response from Nmap. All 1000 ports were showing as 
filtered rather than open or closed.

A filtered port state means the ports are not actually 
closed, they are being silently blocked by a firewall. 
From an attacker's perspective, this makes the machine 
harder to fingerprint since there is no response to 
analyze. In a real SOC environment, this result would 
indicate a firewall is in place and would be documented 
as a positive security control.

For lab testing purposes, the Windows Defender Firewall 
was temporarily disabled to allow the scan to complete.


# 3/8/26 (Python Script/ JSON report)

# Python Security Scripts

## Script 1 — Automated Port Scanner

### What it does
Automates an Nmap -sV -O scan against a target IP and saves
a structured JSON report of all open ports, services, and
version information.

## Tools Used
- Nmap 7.95 — port scanning and service detection
- Python 3 + python-libnmap — scan automation
- VMware — virtual machine platform

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

## Lessons Learned
- A machine returning all filtered ports indicates a firewall
  is actively dropping probes rather than rejecting them
- Port 445 (SMB) should always be treated as a high priority
  finding and investigated immediately in a real environment
- Documenting findings in structured reports is as important
  as the technical work itself



## Script 2 — Automated Log Parser

### What it does
Parses authentication log files to detect suspicious activity
including brute force attempts, sensitive account targeting,
and failed login patterns. Outputs a full summary report and
saves findings to a JSON file.

### Tools Used
- Python 3
- re (regex), collections, json, datetime modules

### Key Findings from Sample Log
| Finding | Details | Risk Level |
|---------|---------|------------|
| Brute Force — 192.168.100.20 | 12 failed logins | High |
| Brute Force — 192.168.100.10 | 9 failed logins | High |
| Root account targeted | 8 attempts | High |
| Guest account targeted | 6 attempts | Medium |
| Admin login after 5 failures | Possible compromise | High |

### Security Notes
- Any IP with 3+ failed logins triggers an automatic alert
- Sensitive usernames like root, admin, and guest are flagged
  regardless of attempt count
- A successful login following repeated failures is a critical
  finding indicating possible account compromise
- In a real SOC environment the offending IPs would be blocked
  and the admin account investigated immediately

### How to Run
```bash
sudo python3 log_parser.py
```
## Script 3 — Real-Time Brute Force Detector

### What it does
Monitors authentication logs in real time, triggering
progressive alerts as failed login attempts accumulate.
Automatically flags and blocks IPs that exceed configurable
thresholds within a set time window.

### Tools Used
- Python 3
- re, time, json, datetime, collections modules

### How it differs from the Log Parser
| Feature | Log Parser | Brute Force Detector |
|---------|-----------|---------------------|
| Timing | After the fact | Real time |
| Purpose | Forensic analysis | Active monitoring |
| Output | Summary report | Live alerts + report |
| Blocking | No | Yes — flags IPs automatically |

### Key Findings from Sample Log
| Finding | Details | Risk Level |
|---------|---------|------------|
| 192.168.100.20 blocked | 5 failed attempts in 8s | 🔴 Critical |
| 192.168.100.10 blocked | 5 failed attempts in 60s | 🔴 Critical |
| Successful logins from blocked IPs | 4 incidents | 🔴 Critical |
| Total alerts raised | 11 | 🔴 Critical |

### Security Notes
- Successful logins from already-blocked IPs indicate the
  attacker had valid credentials or block came too late
- In a real environment this triggers immediate incident
  response and account lockdown
- Both IPs continued attempting after being blocked showing
  behavior typical of automated brute force tools

### How to Run
```bash
sudo python3 brute_force_detector.py
```
