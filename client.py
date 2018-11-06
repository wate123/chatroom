from socket import *
import sys, select

#chatroom server address and port
serverName = gethostname()
serverPort = 12000
# initialize the client as Inet and TCP
clientSocket = socket(AF_INET, SOCK_STREAM)
# connect this client to server
clientSocket.connect((serverName,serverPort))

# if current chatroom member is greate than 2, close this connection and exit.
if int(clientSocket.recv(1).decode()) > 2:
    print("Chatroom reach maximum campacity!\nPlease try again later.")
    clientSocket.close()
    sys.exit()

print("Connected to Chat Service!\n")

# Rules from server
rules = clientSocket.recv(2048)
print(rules.decode())


print("Start the conversation\nTo exit the chat, Type bye\n")
# prefix indicate you - the sender
sys.stdout.write("<You> ")
sys.stdout.flush()

# listen messages from server
while True:
    #list of sockets and addrest connect to server
    list_sockets = [sys.stdin, clientSocket]
    read_sockets,write_socket, error_socket = select.select(list_sockets,[],[]) 

    if len(read_sockets):
        # for each client in the list
        for socket in read_sockets:
            if socket:
                if socket == clientSocket:
                    full = socket.recv(2048).decode().split(": ")
                    message = full[1].strip()
                    print()
                    # this client violate the uppercase rule
                    if message == "You are kicked!":
                        # broadcast the user getting kicked by server and teriminate the client
                        clientSocket.send((gethostname()+" kicked").encode())
                        sys.stdout.write(message)
                        sys.stdout.flush()
                        sys.exit(0)
                    else:
                        # get message broadcast from other people 
                        print(full[0] +": > "+ message)
                        sys.stdout.write("<You> ")
                        sys.stdout.flush()
                else:
                    # sender sends message to server and broadcast to other client
                    
                    message = sys.stdin.readline().strip()
                    sender_info = clientSocket.getsockname()[0] + ": "
                    # print("client: "+sender_info)
                    # clientSocket.send(sender_info.encode())
                    clientSocket.send((sender_info+message).encode())
                    sys.stdout.write("<You> ")
                    sys.stdout.flush()
                    # if sender type bye, they will exit the chatroom
                    if message == "bye":
                        sys.exit(1)
            else:
                break
    else:
        break    
clientSocket.close()
sys.exit()