import socket
import _thread as thread
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()#"89.176.78.154" #doma pouze socket.gethostname()
port = 2205

serversocket.connect((host, port))


def client_send(serversocket):
    while True:
        msg = bytes(input("A:"), "utf-8")
        serversocket.send(msg)

def client_receive(serversocket):
    while True:
        msg = serversocket.recv(1024)
        if not msg:
            print("NEFUNGUJE SERVER")
            serversocket.close()
            break
        else:
            print(msg.decode("utf-8"))

thread_receive = thread.start_new_thread(client_receive, (serversocket,))
client_send(serversocket)
#140175549167360
