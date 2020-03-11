import socket
import _thread as thread
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()#"89.176.78.154" #doma pouze socket.gethostname()
port = 2205

def client_chat(serversocket):
    while True:

        msg = input("\n: ")
        serversocket.send(bytes(msg, "utf-8"))

        result = serversocket.recv(1024)

        if not result:
            print("server.py disconnect")
            break
        else:
            print(result.decode("utf-8"))

serversocket.connect((host, port))
thread_con = thread.start_new_thread(client_chat, (serversocket,))

serversocket.close()
