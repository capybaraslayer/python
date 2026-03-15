import socket
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=9999
client.connect(('localhost',port))
nume=input('Care este numele tau?:')
while True:
    
    mesaj=input('mesaj:')
    if mesaj =='exit':
        print(f'{nume} a iesit!')
        client.send(f'{nume}:exit'.encode('utf-8'))
        break
    
    client.send(f'{nume}:{mesaj}'.encode('utf-8'))
client.close()