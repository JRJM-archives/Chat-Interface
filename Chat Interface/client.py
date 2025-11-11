import socket
import threading

name = input("Enter your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

password = input("Enter password: ")

if password == "3556":
    client.connect(('127.0.0.1', 55555))


def receive():
    while True:
        try:
            #get received messages
            message = client.recv(1024).decode('ascii')
            if message == 'NAME':
                client.send(name.encode('ascii'))
            else:
                print(message)

        except:
            print('Error occured. Connection closed')
            client.close()
            break
            
def write():
    while True:
        msg = f'{name}: {input("")}'
        client.send(msg.encode('ascii'))
        
receiveThread = threading.Thread(target=receive)
receiveThread.start()

writeThread = threading.Thread(target=write)
writeThread.start()