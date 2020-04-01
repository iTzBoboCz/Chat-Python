import socket
import _thread as thread
import re
import tkinter as tk
from tkinter import messagebox as mb
import json
from time import sleep
#import textwrap as tw

root = tk.Tk()

class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        # nastavení okna
        self.root = root
        self.root.configure(bg = "grey") #barva
        self.root.title("OnLuk Super-Chat v0") #nazev okna
        self.root.geometry("960x540") #rozmer
        self.root.minsize(960,540)

        self.host = socket.gethostname()#"89.176.78.154" #doma pouze socket.gethostname()
        self.port = 2205

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.serversocket.connect((self.host, self.port))
        except:
            self.reconnect()

        self.stop = False

        self.messagesList = tk.Listbox(self.root, height=20, width=50)

        self.messagesList.grid(row=0, column=0)

        self.messagesList.pack(side=tk.TOP)

        # tvorba inputů
        self.label_text = tk.StringVar()
        self.label_text.set("Zadejte svou přezdívku")
        self.label = tk.Label(self.root, textvariable=self.label_text, pady=5, padx=5)
        self.label.pack()

        self.nick = ""
        self.nickname_input = tk.StringVar()
        self.nickname_field = tk.Entry(self.root, textvariable=self.nickname_input)
        self.nickname_field.pack()

        self.user_input = tk.StringVar()
        self.input_field = tk.Entry(self.root, textvariable=self.user_input, state="disabled")
        self.input_field.pack()
        self.input_button = tk.Button(self.root, text="Odeslat", command=self.client_send)
        self.input_button.pack()

        self.thread_receive = thread.start_new_thread(self.client_receive, ())

    def client_send(self):
        if self.nick == "":
            nick = self.nickname_field.get()
            if nick == "":
                mb.showerror(title="CHYBA!", message="Přezdívka nesmí být prázná!")
            elif re.search("\s|\W", nick):
                mb.showerror(title="CHYBA!", message="Přezdívka obsahuje nepovolené znaky (mezeru nebo speciální znaky)")
            else:
                self.nick = nick
                self.input_field.configure(state="normal")
                self.nickname_field.configure(state="disabled")
                self.label_text.set("Zadejte zprávu")
                return
        if self.stop == True:
            return
        msg = self.user_input.get()
        msgjson = {
            "nick": self.nick,
            "msg": msg,
        }

        if msg == "":
            return

        msgjson = json.dumps(msgjson)
        msg = self.nick+": "+msg

        print(msgjson)
        # delka listboxu - uživatel a ": "
        # wrapper = tw.TextWrapper(width=(50 - (len(self.nick) + 2)))
        # msg = wrapper.wrap(text=msg)
        # msg = ("\n" + " "*(len(self.nick)+ 2)).join(msg)
        try:
            self.serversocket.send(bytes(msg, "utf-8"))
        except:
            pass

        self.input_field.delete(0, tk.END)

    def client_receive(self):
        while True:
            if self.stop:
                break
            try:
                msg = self.serversocket.recv(1024)
                if not msg:
                    self.serversocket.close()
                    self.messagesList.insert(tk.END, "[SERVER] Nefunguje spojení se serverem. Za 2 sekundy Vás zkusíme připojit znovu.")
                    self.reconnect()
                else:
                    self.messagesList.insert(tk.END, msg.decode("utf-8"))
            except:
                self.messagesList.insert(tk.END, "[SERVER] Nefunguje spojení se serverem.")
                break
    def reconnect(self):
        while True:
            sleep(2)
            try:
                self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.serversocket.connect((self.host, self.port))

            except:
                pass
            else:
                break

if __name__ == '__main__':
    app = MainApp(root)
    app.pack()
    root.mainloop()
    app.stop = True #zastavit app po zavreni okna
