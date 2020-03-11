import socket
import _thread as thread
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()#"89.176.78.154" #doma pouze socket.gethostname()
port = 2205

serversocket.connect((host, port))

check = False
def client_send(serversocket):
    global check
    while True:
    	if check:
    		msg = bytes(input("A:"), "utf-8")
    		serversocket.send(msg)
    		check = False
    	else:
    		check = True

def client_receive(serversocket):
    global check
    while True:
        if check == False:
            msg = serversocket.recv(1024)
            if not msg:
                print("NEFUNGUJE SERVER")
                serversocket.close()
                break
            else:
                print(msg.decode("utf-8"))
            check = True
        else:
            check = False

thread_send = thread.start_new_thread(client_send, (serversocket,))

thread_receive = thread.start_new_thread(client_receive, (serversocket,))
#140175549167360
