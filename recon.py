#!/usr/bin/env python3
import sys
import argparse
import socket
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def parse_ports(port_range):
    if "-" in port_range:
        start, end = port_range.split("-")
        return range(int(start), int(end) + 1)
    return [int(p) for p in port_range.split(",")]


def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target, port))
    sock.close()
    return port if result == 0 else None


def connect_scan(target, ports, threads, verbose):
    print(f"\n[*] Scanning {target} ({len(ports)} ports, {threads} threads)...")
    open_ports = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, target, port): port for port in ports}
        for future in as_completed(futures):
            port = futures[future]
            result = future.result()
            if result is not None:
                open_ports.append(result)
                print(f"  [+] Port {result} OPEN")
            elif verbose:
                print(f"  [-] Port {port} closed")
    open_ports.sort()
    if not open_ports:
        print("  [-] No open ports found.")
    return open_ports


def grab_banner(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((target, port))
        try:
            banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        except socket.timeout:
            sock.send(b"HEAD / HTTP/1.1\r\nHost: target\r\n\r\n")
            banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()
        return banner if banner else "No banner"
    except Exception:
        return "No banner"


def save_report(target, results, filename):
    report = {
        "target": target,
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_open_ports": len(results),
        "services": results
    }
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[*] Report saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Network Recon Tool")
    parser.add_argument("-t", "--target", required=True,
                        help="Target IP (e.g. 10.0.0.2)")
    parser.add_argument("-p", "--ports",
                        default="21,22,23,25,53,80,111,139,445,3306,5432,5900,6667,8080",
                        help="Port range or list (default: common ports)")
    parser.add_argument("-T", "--threads", type=int, default=10,
                        help="Number of threads (default: 10)")
    parser.add_argument("-o", "--output",
                        help="Save results to JSON file (e.g. report.json)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show closed ports too")
    args = parser.parse_args()

    print("=" * 50)
    print("  NETWORK RECON TOOL")
    print("=" * 50)

    ports = parse_ports(args.ports)
    open_ports = connect_scan(args.target, ports, args.threads, args.verbose)

    results = []
    if open_ports:
        print(f"\n[*] Grabbing banners on {args.target}...")
        for port in open_ports:
            banner = grab_banner(args.target, port)
            print(f"  [+] Port {port}: {banner}")
            results.append({"port": port, "banner": banner})

    if args.output:
        save_report(args.target, results, args.output)

    print("\n" + "=" * 50)
    print("  SCAN COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()
