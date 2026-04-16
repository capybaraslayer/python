import socket as s

target_host = "httpbin.org"

try:
    ip_adres=s.gethostbyname(target_host)
    print(f'Succes ai aflat IP-ul pentru {target_host}:{ip_adres}')
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
while True:
    print('"\n--- START ---"')
    print('1.Lista de categorii')
    print("2.Detalii despre o anumita categorie")
    print("3.Creeaza o noua categorie")
    print("4.Sterge o categorie")
    print("5.Modifica titlul unei categorii ")
    print("6.Creeaza produse noi intro categorie")
    print("7.Lista produselor dintro categorie")
    comanda=int(input('Introdu numarul comenzii:'))
    if comanda==1:
        request= "GET /get=123 HTTP/1.1\r\nHOST:" + target_host + "\r\n\r\n"
        data_to_send = request.encode("utf-8")
        soc.send(data_to_send)
    if comanda==2:
        request = "GET /get?id=123 HTTP/1.1\r\nHOST:" + target_host + "\r\n\r\n"
        data_to_send = request.encode("utf-8")
        soc.send(data_to_send)
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
soc.close()
print("\n--- REZULTAT FINAL ---")
print(txt)
