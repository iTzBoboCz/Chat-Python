import socket
import _thread as thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 2205

server.bind((host, port)) #pripojeni

server.listen() #start server

def clients(server):
    clients = []
    while True:
        con, address = server.accept()  # prijmi clienta
        thread_con = thread.start_new_thread(chat, (con, clients, address,))
        clients.append(con) #https://www.youtube.com/watch?v=D0SLpD7JvZI
        con.send(bytes("You have joined chat.", "utf-8"))
        print(f"[{address}]: connected")

def chat(con, clients, address):
    while True:
        #if is not None => pokud není prázdná
        # pokud existuje
        msg = con.recv(1024) #zprava
        if not msg:
            print(f"[{address}]: disconnected")
            clients.remove(con)
            con.close()
            break
        else:
            print(msg.decode("utf-8"))
            for client in clients:
                client.send(msg)
        #print(msg.decode("utf-8"))

clients(server)
