import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# socket.gethostbyaddr("89.176.78.154")[0]
host = socket.gethostbyaddr("localhost")[0] #doma pouze socket.gethostname()
port = 27015 #2205

serversocket.connect((host, port))

while True:
    msg = input("\n: ")
    serversocket.sendall(bytes(msg, "utf8"))

    result = serversocket.recv(1024)
    print(result.decode("utf8"))

serversocket.close()
