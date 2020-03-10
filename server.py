import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "172.16.3.121"
port = 2205

server.bind((host, port)) #pripojeni

server.listen() #start server
con, address = server.accept() #prijmi clienta
while True:
    print(address)
    msg = con.recv(1024)
    print(msg.decode('utf8'))
    con.sendall(bytes("ahojjoha", "utf8"))

con.close()
