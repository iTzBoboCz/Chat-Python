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
        clients.append(con)
        print(f"[{address}]: connected")
        thread_con = thread.start_new_thread(chat, (con, clients, address,))
        pass
    clients.remove(con)
    con.close()

def chat(con, clients, address):
    while True:
        #if is not None => pokud není prázdná
        # pokud existuje
        if not con.recv(1024):
            print(f"[{address}]: disconnected")

            break
        else:
            msg = con.recv(1024) #zprava

            for client in clients:
                client.send(msg)
    break

clients(server)
