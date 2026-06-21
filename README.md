# Network Recon Tool

A Python-based network reconnaissance tool for penetration testing engagements. Performs TCP port scanning and service banner grabbing to identify live services and software versions on target hosts.

## Why I built This

I built this as part of a home pentesting lab to practice the reconnaissance phase of a pentration test. The tool automates the first steps I'd take when landing on a network - identifying live services and their versions to find potential attack vectors.

## Features

- TCP connect scan across custom port ranges
- Service banner grabbing on discovered open ports
- Clean CLI with argparse
- Identifies software versions for vulnerability research

## Usage
python3 recon.py -t <target_ip> [-p <ports>]

### Examples

Scan default common ports:
python3 recon.py -t 10.0.0.2

Scan a custom port range:
python3 recon.py -t 10.0.0.2 -p 1-1024

Scan specific ports:
python3 recon.py -t 10.0.0.2 -p 21,22,80,443,3306

## Sample Output
==================================================

NETWORK RECON TOOL
[*] Running connect scan on 10.0.0.2 (14 ports)...

[+] Port 21 OPEN

[+] Port 22 OPEN

[+] Port 80 OPEN

[+] Port 3306 OPEN
[*] Grabbing banners on 10.0.0.2...

[+] Port 21: 220 (vsFTPd 2.3.4)

[+] Port 22: SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1

[+] Port 80: HTTP/1.1 200 OK — Apache/2.2.8 (Ubuntu)

[+] Port 3306: MySQL 5.0.51a-3ubuntu5
==================================================

SCAN COMPLETE

## Built With

- Python 3
- Socket library for TCP connections and banner grabbing

## Environment

Tested in an isolated VirtualBox lab:
- **Attack machine:** Kali Linux 2026.1
- **Target:** Metasploitable 2 (intentionally vulnerable VM)
- **Network:** VirtualBox Internal Network (no external exposure)

## Disclaimer

This tool is for authorised security testing and educational purposes only. Only use against systems you have explicit permission to test.
