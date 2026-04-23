clienti = ["Catalin", "Mihaela", "Constanta"]


def adaugare_client():
    client_nou = input("Cum te numesti")
    clienti.append(client_nou)
    for client in clienti:
        print(client)

def sterge_client(client):
    clienti.remove(client)
    print(clienti)
adaugare_client()
sterge_client('Catalin')
