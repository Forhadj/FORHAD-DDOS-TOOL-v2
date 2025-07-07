#!/bin/bash
clear
echo -e "\e[1;32m"
cat logo.txt
echo -e "\e[0m"

echo "[•] Loading..."
sleep 1

while true; do
    clear
    echo -e "\e[1;34m"
    cat logo.txt
    echo -e "\e[0m"
    echo "╔══════════════════════════════╗"
    echo "║      FORHAD-DDOS-TOOL v2     ║"
    echo "╚══════════════════════════════╝"
    echo "[1] Start UDP Flood"
    echo "[2] Show My IP"
    echo "[3] About"
    echo "[0] Exit"
    read -p ">> Enter your choice: " opt

    case $opt in
        1) python ddos.py ;;
        2) ip addr show wlan0 | grep 'inet ' | awk '{print $2}' ;;
        3) echo -e "\nTool: FORHAD-DDOS-TOOL v2\nAuthor: Forhad Hasan\nGitHub: https://github.com/Forhadj\n" ; read -p "Press enter to continue..." ;;
        0) echo "Goodbye!"; exit ;;
        *) echo "Invalid option!" ;;
    esac
    sleep 2
done
