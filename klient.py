import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "172.16.3.121" #doma pouze socket.gethostname()
port = 2205 #2205

serversocket.connect((host, port))

while True:
    msg = input("\n: ")
    serversocket.sendall(bytes(msg, "utf8"))

    result = serversocket.recv(1024)
    print(result.decode("utf8"))

serversocket.close()
