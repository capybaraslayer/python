import socket as s
TARGET_HOST = "httpbin.org"
def con():
    try:
        ip_adres=s.gethostbyname(TARGET_HOST)
        print(f'Succes ai aflat IP-ul pentru {TARGET_HOST}:{ip_adres}')
    except s.gaierror:
        print('Ceva nu a mers!Verifica conexiunea')

    soc=s.socket(s.AF_INET,s.SOCK_STREAM)
    try:
        soc.settimeout(2.0)
        soc.connect((ip_adres,80))
        print('Teai conectat la portul 80')
    except ConnectionRefusedError:
        print('Serverul nu accepta vizitatori pe portul 80!')
    except TimeoutError:
        print('Serverul este ocupat')
    return soc

def trimite_mesaj(soc,metoda,cale,id=None,date_json=None):
    date='\r\n\r\n'
    if date_json:
        date = (
            "Content-Type: application/json\r\n"
            "Content-Length:" + str(len(date_json.encode("utf-8"))) + "\r\n"
            "\r\n" + date_json
        )

    if id:
        request = f"{metoda} /{cale}?id={id} HTTP/1.1\r\n"
    else:
        request = f"{metoda} /{cale} HTTP/1.1\r\n"
    host = f"Host:" + TARGET_HOST + "\r\n"
    request+=host+date
    data_to_send=request.encode('utf-8')
    soc.send(data_to_send)
def primire_mesaj(soc):
    txt=''
    while True:
        try:
            data=soc.recv(1024)
            if not data:
                print('Am terminat de descarcat!')
                break
            txt+=data.decode('utf-8','ignore')
        except s.timeout:
            break
    return(txt)

def main():
    while True:
        print('"\n--- START ---"')
        print("0.Exit")
        print("1.Lista de categorii")
        print("2.Detalii despre o anumita categorie")
        print("3.Creeaza o noua categorie")
        print("4.Sterge o categorie")
        print("5.Modifica titlul unei categorii ")
        print("6.Creeaza produse noi intro categorie")
        print("7.Lista produselor dintro categorie")
        comanda = int(input("Introdu numarul comenzii:"))
        if comanda == 1:
            with con() as soc:
                trimite_mesaj( soc,"GET","get")
                print('"\n--- REZULTATE ---"')
                txt=primire_mesaj(soc)
                print(txt)

        elif comanda == 2:
            with con() as soc:
                id=int(input('Introdu id:'))
                trimite_mesaj( soc,"GET","get",id)
                print('"\n--- REZULTATE ---"')
                txt=primire_mesaj(soc)
                print(txt)
        elif comanda == 3:
            with con() as soc:
                nume = input("Numele:")
                corp_json = '{"name": "' + nume + '"}'
                trimite_mesaj(soc, "POST", "post",None, corp_json)
                print('"\n--- REZULTATE ---"')
                txt = primire_mesaj(soc)
                print(txt)
        elif comanda == 4:
            with con() as soc:
                id = int(input("Introdu id:"))
                trimite_mesaj(soc, "DELETE", "delete", id)
                print('"\n--- REZULTATE ---"')
                txt = primire_mesaj(soc)
                print(txt)
        elif comanda==5:
            with con() as soc:
                id = int(input("Introdu id:"))
                nume=input('Numele:')
                corp_json = '{"name": "' + nume + '"}'
                trimite_mesaj(soc, "PUT", "put", id,corp_json)
                print('"\n--- REZULTATE ---"')
                txt = primire_mesaj(soc)
                print(txt)
        elif comanda ==6:
            with con() as soc:
                id = int(input("Introdu id:"))
                nume = input("Numele:")
                corp_json = '{"name": "' + nume + '"}'
                trimite_mesaj(soc, "POST", "post", id, corp_json)
                print('"\n--- REZULTATE ---"')
                txt = primire_mesaj(soc)
                print(txt)
        elif comanda ==7:
            with con() as soc:
                id = int(input("Introdu id:"))
                cale="get?category_id="+str(id)
                trimite_mesaj(soc, "GET",cale)
                print('"\n--- REZULTATE ---"')
                txt = primire_mesaj(soc)
                print(txt)
        elif comanda == 0:
            print('"\n--- END ---"')
            break


if __name__=="__main__":
    main()
