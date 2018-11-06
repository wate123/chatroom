from socket import *
from threading import *
import sys

# Chatroom rules
rules = '''Welcome to this chatroom! 
 To create a friendly and safe chatting environments.
 Please follow the rules below!
    1. No all uppercase sentence allow here. You will be kicked after second time.
    1. Be polite, courteous and introduce yourself upon entering the room.
    2. Respect the opinions and practices of others in the room. 
    3. Do not argue or openly debate.  However, questions and opposing opinions are encouraged just do so respectfully.
    4. Limit negative comments as these have a tendency not to help anyone's trading.  Alternatively, try to put the comment in a positive light.  The use of negative metaphors have a tendency to amplify negative emotions.
    5. The use of rude or abusive language, blatantly insensitive remarks or purposely annoying comments is not acceptable.
    6. For personal safety reasons, be cautious to whom you disclosure your last name, home address, telephone number.\n'''

# Broadcast message to everyone in chatroom except sender
def broadcast( message, connection): 
    # print(connection)
    #for each client in the list
    for client in list_clients: 
        # if client is not the sender, send the message to everyone except sender
        if client!=connection: 
            try: 
                # client.send(sender_info)
                client.send(message) 
                # print(connection.getsockname() + message)
            except: 
                # close the connection if fail.
                client.close()
                # if the link is broken, we remove the client 
                list_clients.remove(client) 


# thread for each client
def client_thread(conn, addr):
    # send current number of people in chat room
    conn.send(str(len(list_clients)).encode())
    # add this client to the list of people
    list_clients.append(conn)

    # try send the rules when the client is join the room.
    try:
        conn.send(rules.encode())
    except:
        print(conn)
    
    # count for number of warning of this person
    warning_num = 0

    while True:
        # listen for client's message
        try:
            message = conn.recv(2048)
            # sender_info = message.decode().split(": ")[0]
            if message:
                # if message is uppercase warn once, next time, send kick message to that client
                if message.isupper():
                    warning_num += 1
                    if warning_num == 2:
                        conn.send("You are kicked!".encode())
                        # reset the warning counter to 0
                        warning_num = 0
                    else:
                        conn.send("Warning Once! This chatroom doesn't allow uppercase sentence".encode())
                else:
                    # message is not uppercase, broadcast to everyone.
                    broadcast(message, conn)
            else:
                #the message is fail, remove it from the room
                list_clients.remove(conn)
        except:
            continue

# the server port open for this chatroom
serverPort = 12000
# initialize the server as Inet and TCP
serverSocket = socket(AF_INET,SOCK_STREAM)

# bind the socket to a public host
serverSocket.bind((gethostname(),serverPort))
# listen for 3 clients
serverSocket.listen(3)

# list of clients in the chatroom
list_clients = []

print ('The chat server is live!')

# listen for new client connect to server and accept it.
while 1:
    connectionSocket, addr = serverSocket.accept()
    ## start a thread for each client
    Thread(target=client_thread, args=(connectionSocket, addr)).start()

# when done close out everything and exit    
connectionSocket.close()
serverSocket.close()
sys.exit()
