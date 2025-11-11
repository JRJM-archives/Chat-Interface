import socket
import threading

#define host, port

host = '127.0.0.1'
port = 55555

#create socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind host to socket, make sure the socket is listening (trasmit/receive)
s.bind((host, port))
s.listen()

#list of all clients and their names

clients = []
names = []

#broadcast function to send message to all clients

def broadcast(message):
    for client in clients:
        client.send(message)



def handle(client):
    while True:
        try:
            #handle incoming messages (1024 bytes) from the client and broadcast them
            message = client.recv(1024)
            broadcast(message)
        except:
            #exception handling if client disconnects or closes out
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} disconnected'.encode('ascii'))
            names.remove(name)
            break

def receive():
    while True:
        #accept clients all the time, when client connects let us know
        #triggered once the receive() in client.py is triggered and client enters a name
        client, address = s.accept()
        print(f'Connected to {address[0]}:{address[1]}')

        #keyword send (send the name) then append the name to the list
        client.send('NAME'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)

        #broadcast the person who connected and send client back a connection msg

        print(f'Name of client: {name}')
        broadcast(f'{name} connected!'.encode('ascii'))
        client.send('Connected!'.encode('ascii'))

        # start thread handling client connection

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server listening...')
receive()