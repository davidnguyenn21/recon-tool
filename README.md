# Network Recon Tool

A Python-based network reconnaissance tool for penetration testing engagements. Performs threaded TCP port scanning and service banner grabbing to identify live services and software versions on target hosts.

## Why I Built This

I built this as part of a home pentesting lab to practise the reconnaissance phase of a penetration test. The tool automates the first steps I'd take when landing on a network — identifying live services and their versions to find potential attack vectors.

## Features

- Threaded TCP connect scan for fast parallel port scanning
- Service banner grabbing on discovered open ports
- JSON report output for integration with other tools
- Verbose mode to show closed ports for debugging
- Configurable thread count and port ranges via CLI

## Usage
python3 recon.py -t <target_ip> [-p <ports>] [-T <threads>] [-o <file>] [-v]

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-t` | Target IP (required) | — |
| `-p` | Port range or list | Common ports |
| `-T` | Number of threads | 10 |
| `-o` | Save results to JSON file | — |
| `-v` | Show closed ports too | Off |

### Examples

Scan default common ports:
python3 recon.py -t 10.0.0.2

Scan a full range with 50 threads and save a report:
python3 recon.py -t 10.0.0.2 -p 1-1024 -T 50 -o report.json

Scan specific ports with verbose output:
python3 recon.py -t 10.0.0.2 -p 21,22,80,443,3306 -v

## Sample Output
==================================================

NETWORK RECON TOOL
[*] Scanning 10.0.0.2 (14 ports, 10 threads)...

[+] Port 21 OPEN

[+] Port 22 OPEN

[+] Port 23 OPEN

[+] Port 25 OPEN

[+] Port 80 OPEN

[+] Port 3306 OPEN

[+] Port 5900 OPEN
[*] Grabbing banners on 10.0.0.2...

[+] Port 21: 220 (vsFTPd 2.3.4)

[+] Port 22: SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1

[+] Port 25: 220 metasploitable.localdomain ESMTP Postfix (Ubuntu)

[+] Port 80: HTTP/1.1 200 OK — Apache/2.2.8 (Ubuntu)

[+] Port 3306: MySQL 5.0.51a-3ubuntu5

[+] Port 5900: RFB 003.003
[*] Report saved to report.json
==================================================

SCAN COMPLETE

## Built With

- Python 3
- Socket library for TCP connections and banner grabbing
- concurrent.futures for threaded scanning

## Environment

Tested in an isolated VirtualBox lab:
- **Attack machine:** Kali Linux 2026.1
- **Target:** Metasploitable 2 (intentionally vulnerable VM)
- **Network:** VirtualBox Internal Network (no external exposure)

## Disclaimer

This tool is for authorised security testing and educational purposes only. Only use against systems you have explicit permission to test.
