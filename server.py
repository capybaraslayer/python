import socket 
import threading
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=9999
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(('localhost',port))
print('Serverul sa pornit')
server.listen(5)
con,adres=server.accept()
print(f"Clientul sa conectat:{adres}")

while True:
    mesaj = con.recv(1024).decode('utf-8')
    print(mesaj)
    nume=mesaj.split(':')


    if 'exit' in mesaj:
        print(f'{nume[0]} a parasit chatul!')
        con.close()
        break



