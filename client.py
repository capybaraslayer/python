import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9999
client.connect(("localhost", port))
nume = input("Care este numele tau?:")
client.send(nume.encode("utf-8"))


def primeste_mesaj():
    while True:
        mesaj = client.recv(1024).decode("utf-8")
        print(mesaj)


def mesaj():
    while True:
        mesaj = input()
        if mesaj == "exit":
            print(f"{nume} a iesit!")
            client.send(f"{nume}:exit".encode("utf-8"))
            break
        else:
            client.send(f"{nume}:{mesaj}".encode("utf-8"))


t1 = threading.Thread(target=primeste_mesaj).start()
t2 = threading.Thread(target=mesaj).start()
