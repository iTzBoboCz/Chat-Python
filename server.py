import socket
import _thread as thread

mutex = thread.allocate_lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyaddr("localhost")[0]
port = 27015

server.bind((host, port)) #pripojeni

server.listen() #start server

clients = []
def chat(server):
    while True:
        print(address)
        msg = con.recv(1024)
        print(msg.decode('utf8'))
        con.sendall(bytes(" ahojjoha", "utf8"))

con, address = server.accept()  # prijmi clienta

clients.append(con)

mutex.acquire()

chat(server)

con.close()
mutex.release()
