import socket
import threading
import sys


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9999
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", port))
print("Serverul sa pornit")
server.listen(5)
clienti = []


def trimitere_mesaj_client(nume, mesaj, con):
    for client in clienti:
        if client == con:
            pass
        else:
            mesaj_client = mesaj.split(":")[1]
            nume_client = mesaj.split(":")[0]
            send = client.send(f"{nume_client}:{mesaj_client}".encode("utf-8"))


def gestioneaza_client(con, adres):
    nume = con.recv(1024).decode("utf-8")
    clienti.append(con)
    print(f"Clientul sa conectat({nume}) la adresa:{adres}")
    while True:

        mesaj = con.recv(1024).decode("utf-8")
        print(mesaj)
        trimitere_mesaj_client(nume, mesaj, con)

        if "exit" in mesaj:
            print(f"{nume[0]} a parasit chatul!")
            con.close()
            break


def inchide_server():
    while True:
        comanda = input()
        if comanda == "exit":
            server.close()
            sys.exit()
        else:
            continue


t2 = threading.Thread(target=inchide_server).start()
while True:
    con, adres = server.accept()
    t1 = threading.Thread(target=gestioneaza_client, args=(con, adres)).start()
