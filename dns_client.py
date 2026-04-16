import socket as s

DNS_SERVER = "8.8.8.8"
DNS_PORT = 53
pachet = ""
soc = s.socket(s.AF_INET, s.SOCK_DGRAM)
while True:
    msg = input(">").strip()
    comanda = msg.split(" ")
    if comanda[0] == "":
        continue
    if comanda[0] == "resolve":
        tinta = comanda[1]
        if tinta[0].isdigit():
            ip=tinta.split('.')
            ip.reverse()
            tinta_string='.'.join(ip)
            tinta = tinta_string+".in-addr.arpa"
            f = b"\x00\x0c\x00\x01"
        else:

            f = b"\x00\x01\x00\x01"
        parti = tinta.split(".")
        rezultat = b""
        for i in range(len(parti)):
            lungime = len(parti[i])
            header = bytes([lungime])
            cuvant_encodat = parti[i].encode("ascii")
            rezultat += header + cuvant_encodat
        rezultat += b"\x00"
        h = b"\xaa\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
        pachet=h+rezultat+f
        soc.sendto(pachet,(DNS_SERVER,DNS_PORT))
        data,adresa=soc.recvfrom(512)
        ip=data[-4:]
        lista=list(ip)
        saritura = 12 +4 +len(rezultat)
        if f == b"\x00\x01\x00\x01":
            ip_final = data[-4:]
            lista = list(ip_final)
            print(f"IP: {lista[0]}.{lista[1]}.{lista[2]}.{lista[3]}")
        else:
            print(f"Numele este: {data[saritura + 12:]}")
    if comanda[0]=='use' and comanda[1]=='dns':
        DNS_SERVER=comanda[2]
        print(f"Acum folosim serverul DNS: {DNS_SERVER}")
