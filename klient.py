import socket
import _thread as thread
import re
import tkinter as tk
import os

root = tk.Tk()

class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.root = root
        self.root.configure(bg = "grey")
        self.root.title("OnLuk Super-Chat v0")
        self.root.geometry("1000x500")
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = socket.gethostname()#"89.176.78.154" #doma pouze socket.gethostname()
        port = 2205

        self.serversocket.connect((host, port))

        while True:
            nick = input("Vložte svou přezdívku:\n ")

            if nick != "":
                if re.search("\s|\W", nick):
                    print("Přezdívka obsahuje nepovolené znaky (mezeru nebo speciální znaky)")
                else:
                    self.nick = nick
                    break

        thread_receive = thread.start_new_thread(self.client_receive, ())
        thread_send = thread.start_new_thread(self.client_send, ())

    def client_send(self):
        while True:
            #print(self.nick+": ")
            msg = input(self.nick+": ")

            if msg == "":
                pass

            self.serversocket.send(bytes(self.nick+": "+msg, "utf-8"))

    def client_receive(self):
        while True:
            msg = self.serversocket.recv(1024)
            if not msg:
                print("NEFUNGUJE SERVER")
                self.serversocket.close()
                break
            else:
                print(msg.decode("utf-8"))
                #msg_list.insert(tk.END, msg)

app = MainApp(root)
app.pack()
root.mainloop()

'''window = tk.Tk()
title = window.title("OnLuk Chat")
frame = window.configure(width=1000, height=500, bg="grey")

scrollbar = tk.Scrollbar(window)  # To navigate through past messages.
msg_list = tk.Listbox(window, height=15, width=50, yscrollcommand=scrollbar.set)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
# Following will contain the messages.
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# entry_field = tk.Entry(top, textvariable=msg.get())
# entry_field.bind("<Return>", send)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()#"89.176.78.154" #doma pouze socket.gethostname()
port = 2205

serversocket.connect((host, port))

while True:
    nick = input("Vložte svou přezdívku:\n ")

    if nick != "":
        if re.search("\s|\W", nick):
            print("Přezdívka obsahuje nepovolené znaky (mezeru nebo speciální znaky)")
        else:
            break
def client_send(serversocket):
    while True:
        print("Zadejte zprávu:")
        msg = input()
        serversocket.send(bytes(nick+": "+msg, "utf-8"))

def client_receive(serversocket):
    while True:
        msg = serversocket.recv(1024)
        if not msg:
            print("NEFUNGUJE SERVER")
            serversocket.close()
            break
        else:
            print(msg.decode("utf-8"))
            msg_list.insert(tk.END, msg)

client_send(serversocket)
thread_receive = thread.start_new_thread(client_receive, (serversocket,))
window.mainloop()
'''
#140175549167360
