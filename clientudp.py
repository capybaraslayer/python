import socket
import threading

PORT_PRIVAT = 9998
PORT_PUBLIC = 9999
BROADCAST_IP = "255.255.255.255"

user = input("Username: ")

s_public = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_public.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s_public.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_public.bind(("", PORT_PUBLIC))

s_privat = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_privat.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_privat.bind(("", PORT_PRIVAT))


def asculta_general():
    while True:
        try:
            data, addr = s_public.recvfrom(1024)
            print(f"[GENERAL] {data.decode('utf-8')} ({addr[0]})")
        except:
            pass


def asculta_privat():
    while True:
        try:
            data, addr = s_privat.recvfrom(1024)
            print(f"[PRIVAT] {data.decode('utf-8')} ({addr[0]})")
        except:
            pass


threading.Thread(target=asculta_general, daemon=True).start()
threading.Thread(target=asculta_privat, daemon=True).start()

print("g <mesaj> - general | p <ip> <mesaj> - privat")

while True:
    inp = input().strip()
    if inp.startswith("g "):
        s_public.sendto(f"{user}: {inp[2:]}".encode(), (BROADCAST_IP, PORT_PUBLIC))
    elif inp.startswith("p "):
        parts = inp[2:].split(" ", 1)
        if len(parts) == 2:
            s_privat.sendto(f"{user}: {parts[1]}".encode(), (parts[0], PORT_PRIVAT))
