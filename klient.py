import socket
import _thread as thread
import re
from tkinter import *
from tkinter import messagebox
import json
from time import sleep
from lib import *
#import textwrap as tw

root = Tk()
root.configure(background='#bdc3c7')
root.geometry('1000x500')
root.minsize(1000, 500)
root.maxsize(1000, 500)
root.title("OnLuk Super-Chat v0.4") #nazev okna

class MainApp:
    def __init__(self):

        self.host = socket.gethostname()#"89.176.78.154" #doma pouze socket.gethostname()
        self.port = 2205

        # self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #
        # try:
        #     self.serversocket.connect((self.host, self.port))
        # except:
        #     # messagebox.showerror(title="Server", message="hesla se neshodují")
        #     pass

        self.stop = False

        self.form()

    def chat(self):
        self.chatFrame = Frame(root, bg="#bdc3c7")
        self.chatFrame.pack()

        self.scrollbar = Scrollbar(self.chatFrame)
        self.scrollbar.pack( side = RIGHT, fill = Y )

        self.messageList = Listbox(self.chatFrame,width=150, height=20,bg="#ecf0f1", yscrollcommand = self.scrollbar.set)
        self.messageList.selection_set("end")
        self.messageList.pack()

        self.messageInput = Frame(root, bg="#bdc3c7")
        self.messageInput.pack(pady=20)

        self.messageEntry = Text(self.messageInput , height=20, width=50,font=("Arial", 14))
        self.messageEntry.pack(side=LEFT)
        self.messageEntry.see("end")

        self.messageButton = Button(self.messageInput, text="Odeslat", font=("Arial", 14, "bold"), cursor="hand2", bd=0, bg="#4a69bd", activebackground="#82ccdd", fg="#ecf0f1", command=self.client_send)
        self.messageButton.pack(side=LEFT, ipady=20)

        self.thread_receive = thread.start_new_thread(self.client_receive, ())

    def form(self):

        #LOGIN FRAME
        self.loginWindow = Frame(root, bg="#34495e")
        self.loginWindow.grid(row=0,column=0, ipadx=50, ipady=30, padx=50, pady=50)

        labelNameLogin = Label(self.loginWindow, text="Nick:", font=("Arial", 15, "bold"), padx=5, width=4, anchor="w", bg="#34495e",  fg="#ecf0f1")
        labelPasswordLogin = Label(self.loginWindow, text="Heslo", font=("Arial", 15, "bold"), padx=5, width=4, bg="#34495e",  fg="#ecf0f1")
        self.entryNameLogin = Entry(self.loginWindow, width=15, font=("Arial", 14))
        self.entryPassLogin = Entry(self.loginWindow, width=15, font=("Arial", 14), show="*")

        labelLogin = Label(self.loginWindow, text="Přihlášení",font=("Arial", 18, "bold"), bg="#34495e", fg="#ecf0f1")
        labelLogin.grid(row=0,column=1, ipadx=5, ipady=5)

        labelNameLogin.grid(row=1, column=0, padx=20, pady=10)
        labelPasswordLogin.grid(row=2, column=0, padx=20, pady=10)

        self.entryNameLogin.grid(row=1, column=1, ipadx=5, ipady=5)

        self.entryPassLogin.grid(row=2, column=1, ipadx=5, ipady=5)


        buttonLogin = Button(self.loginWindow, text="Přihlásit se", font=("Arial", 12, "bold"),cursor="hand2", bd=0, bg="#4a69bd", activebackground="#82ccdd", fg="#ecf0f1", command=self.login)
        buttonLogin.grid(row=3, column=1, pady=5)

        #REGISTER FRAME
        self.registerWindow = Frame(root, bg="#34495e")
        self.registerWindow.grid(row=0, column=5, ipadx=50, ipady=14, padx=50, pady=50)

        labelNameRegister = Label(self.registerWindow, text="Nick:", font=("Arial", 15, "bold"), padx=5, width=4, anchor="w", bg="#34495e",  fg="#ecf0f1")
        labelPasswordRegister = Label(self.registerWindow, text="Heslo", font=("Arial", 15, "bold"), padx=5, width=4, bg="#34495e",  fg="#ecf0f1")
        self.passwordAgain_text = StringVar()
        labelPasswordAgain = Label(self.registerWindow, text="Heslo znovu", font=("Arial", 15, "bold"), padx=5, bg="#34495e",  fg="#ecf0f1")

        self.entryNameRegistration = Entry(self.registerWindow, width=15, font=("Arial", 14))
        self.entryPassRegistration = Entry(self.registerWindow, width=15, font=("Arial", 14), show="*")
        self.entryPassAgain = Entry(self.registerWindow, textvariable=self.passwordAgain_text, width=15, font=("Arial", 14), show="*")

        labelRegistration = Label(self.registerWindow, text="Registrace",font=("Arial", 18, "bold"), bg="#34495e",  fg="#ecf0f1")
        labelRegistration.grid(row=0, column=1, ipadx=5, ipady=5)

        labelNameRegister.grid(row=1, column=0, padx=20, pady=10)
        labelPasswordRegister.grid(row=2, column=0, padx=20, pady=10)

        self.entryNameRegistration.grid(row=1, column=1, ipadx=5, ipady=5)

        self.entryPassRegistration.grid(row=2, column=1, ipadx=5, ipady=5)

        labelPasswordAgain.grid(row=3, column=0)

        self.entryPassAgain.grid(row=3, column=1, ipadx=5, ipady=5)

        buttonRegister = Button(self.registerWindow, text="Registrovat se", font=("Arial", 12, "bold"), cursor="hand2", bd=0, bg="#4a69bd", activebackground="#82ccdd", fg="#ecf0f1", command=self.register)
        buttonRegister.grid(row=4, column=1, pady=5)

    def register(self):
        nick = self.entryNameRegistration.get()
        password = self.entryPassRegistration.get()
        passwordAgain = self.entryPassAgain.get()

        if nick == "" or password == "" or passwordAgain == "":
            return

        if len(password) < 4:
            messagebox.showerror(title="Registrace se nepodařila", message="Heslo musí obsahovat nejméně 4 znaky")
            return

        if len(nick) < 4:
            messagebox.showerror(title="Registrace se nepodařila", message="Přezdívka musí obsahovat nejméně 4 znaky")
            return

        if password != passwordAgain:
            messagebox.showerror(title="Registrace se nepodařila", message="hesla se neshodují")
            self.passwordAgain_text.set("")
            return

        if re.search("\W", nick):
            messagebox.showerror(title="Registrace se nepodařila", message="Přezdívka obsahuje speciální znak nebo mezeru")
            return

        if re.search("\s", password) or re.search("\s", passwordAgain):
            messagebox.showerror(title="Registrace se nepodařila", message="heslo obsahuje mezeru")
            return

        jsonData = {
            "type": "register",
            "nick": nick,
            "password": hashPassword(self, password)
        }

        jsonData = json.dumps(jsonData)
        try:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serversocket.connect((self.host, self.port))
            self.serversocket.send(bytes(jsonData, "utf-8"))
        except:
            messagebox.showerror(title="ERROR", message="[SERVER] nepodařilo se spojit se serverem, zkuste to prosím později!")
        else:
            try:
                msg = self.serversocket.recv(1024)
                msg = json.loads(msg.decode("utf-8"))

                if msg["type"] == "error":
                    messagebox.showerror(title="ERROR", message=msg["msg"])
                elif msg["type"] == "success":
                    messagebox.showinfo(title="SUCCESS", message=msg["msg"])

                    self.nick = nick
                    self.destroyForm()
                    self.chat()
            except:
                messagebox.showerror(title="ERROR", message="[SERVER] něco se pokazilo, zkuste to prosím později")

    def login(self):
        nick = self.entryNameLogin.get()
        password = self.entryPassLogin.get()

        if nick == "" or password == "":
            return

        jsonData = {
            "type": "login",
            "nick": nick,
            "password": hashPassword(self, password)
        }
        jsonData = json.dumps(jsonData)
        try:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serversocket.connect((self.host, self.port))
            self.serversocket.send(bytes(jsonData, "utf-8"))
        except:
            messagebox.showerror(title="ERROR", message="[SERVER] nepodařilo se spojit se serverem, zkuste to prosím později!")
        else:
            try:
                msg = self.serversocket.recv(1024)
                msg = json.loads(msg.decode("utf-8"))

                if msg["type"] == "error":
                    messagebox.showerror(title="ERROR", message=msg["msg"])
                elif msg["type"] == "success":
                    messagebox.showinfo(title="SUCCESS", message=msg["msg"])

                    self.nick = nick
                    self.destroyForm()
                    self.chat()
            except:
                messagebox.showerror(title="ERROR", message="[SERVER] něco se pokazilo, zkuste to prosím později")

    def destroyForm(self):
        self.loginWindow.grid_forget()
        self.registerWindow.grid_forget()

    def client_send(self):
        if self.stop == True:
            return
        msg = self.messageEntry.get("1.0",END)

        if re.search("\s", msg):
            return
        msgjson = {
            "type": "msg",
            "nick": self.nick,
            "msg": msg,
        }


        msgjson = json.dumps(msgjson)
        #msg = self.nick+": "+msg

        # delka listboxu - uživatel a ": "
        # wrapper = tw.TextWrapper(width=(50 - (len(self.nick) + 2)))
        # msg = wrapper.wrap(text=msg)
        # msg = ("\n" + " "*(len(self.nick)+ 2)).join(msg)
        try:
            self.serversocket.send(bytes(msgjson, "utf-8"))
            self.messageEntry.delete("1.0", END)
        except:
            pass

    def client_receive(self):
        while True:
            if self.stop:
                break
            try:
                msg = self.serversocket.recv(1024)
                if not msg:
                    self.serversocket.close()
                    self.messageList.insert(END, "[SERVER] Nefunguje spojení se serverem. Za 2 sekundy Vás zkusíme připojit znovu.")

                    #Select the new item
                    self.messageList.select_set(END)

                    #Set the scrollbar to the end of the listbox
                    self.messageList.yview(END)
                    self.reconnect()
                else:
                    msg = msg.decode("utf-8")
                    msg = json.loads(msg)

                    self.messageList.insert(END, msg["nick"]+": "+msg["msg"][:-1])
            except:
                self.messageList.insert(END, "[SERVER] Nefunguje spojení se serverem.")
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
    app = MainApp()
    root.mainloop()
    app.stop = True #zastavit app po zavreni okna
