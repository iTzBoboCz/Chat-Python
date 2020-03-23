import socket
import _thread as thread
import re
import tkinter as tk
from tkinter import messagebox as mb
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

        host = socket.gethostname()#"89.176.78.154" #doma pouze socket.gethostname()
        port = 2205

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.connect((host, port))


        self.stop = False

        self.messagesList = tk.Listbox(self.root, height=20, width=50)
        # self.messagesScroll = tk.Scrollbar(self.messagesList, orient="vertical", command=self.messagesList.yview)
        # self.messagesList.configure(yscrollcommand=self.messagesScroll.set)
        self.messagesList.grid(row=0, column=0)
        # self.messagesScroll.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E)
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

        if msg == "":
            return
        msg = self.nick+": "+msg

        # delka listboxu - uživatel a ": "
        # wrapper = tw.TextWrapper(width=(50 - (len(self.nick) + 2)))
        # msg = wrapper.wrap(text=msg)
        # msg = ("\n" + " "*(len(self.nick)+ 2)).join(msg)
        self.serversocket.send(bytes(msg, "utf-8"))

        self.input_field.delete(0, tk.END)

    def client_receive(self):
        while True:
            if self.stop:
                break
            msg = self.serversocket.recv(1024)
            if not msg:
                print("NEFUNGUJE SERVER")
                self.serversocket.close()
                self.stop = True
                self.root.quit()
                break
            else:
                self.messagesList.insert(tk.END, msg.decode("utf-8"))

app = MainApp(root)
app.pack()
root.mainloop()
app.stop = True #zastavit app po zavreni okna
