import socket
import _thread as thread
import sqlite3 as sql
from tkinter import *
import os
import atexit
import json

# vytvoření pozadí + názvu aplikace
root = Tk()
root.configure(background='#bdc3c7')
root.geometry('1000x500')
root.minsize(1000, 500)
root.maxsize(1000, 500)
root.title("OnLuk Super-Chat Server v0.4") #nazev okna

# vytvoření/otevření souboru s logy
try:
    logfile = open("server_log.db", "r")
    logfile.close()
except:
    logfile = open("server_log.db", "w+")
    logfile.close()

class Server:
    def __init__(self):
        self.serverFrame = Frame(root)
        self.serverFrame.pack()

        self.stopped = True

        self.scrollbar = Scrollbar(self.serverFrame)
        self.scrollbar.pack( side = RIGHT, fill = Y )

        self.logList = Listbox(self.serverFrame,width=150, height=20,bg="#ecf0f1", yscrollcommand = self.scrollbar.set)
        self.logList.pack()

        # tlačítka na start, stop a restart
        self.buttonStart = Button(root, text="Start",width=10, height=3,font=("Arial", 20, "bold"),  fg="white", bg="#2ecc71", command=self.start)
        self.buttonStop = Button(root, text="Stop", width=10, height=3,font=("Arial", 20, "bold"), fg="white", bg="#c0392b", state="disabled", command=self.stop)
        self.buttonRestart = Button(root, text="Restart", width=10, height=3,font=("Arial", 20, "bold"), fg="white", bg="#95a5a6", state="disabled", command=self.restart)

        self.buttonStart.pack(side=LEFT, padx=50)
        self.buttonStop.pack(side=LEFT, padx=100)
        self.buttonRestart.pack(side=LEFT, padx=50)

        try:
            # připojení k DB
            self.db = sql.connect("server_log.db")

            # nastavení kurzoru (můžeme vypisovat výsledky z DB)
            self.db = self.db.cursor()
        except:
            self.logList.insert(END, "[ERROR] Serveru se nepodařilo spojit se s databází!")
            exit()

        # vytvoření tabulky logs
        try:
            self.db.execute("""CREATE TABLE logs (
            `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `logType` VARCHAR(30) NOT NULL,
            `logMessage` VARCHAR(75) NOT NULL,
            `date` DATE NOT NULL DEFAULT (datetime('now','localtime'))
            )""")
        except:
            pass
        else:
            self.logList.insert(END, "[DB] Tabulka 'logs' byla vytvořena!")
            self.insertData(["DB", "Vytvořena tabulka 'logs'"], self.db)

        # vytvoření tabulky messages
        try:
            self.db.execute("""CREATE TABLE messages (
            `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `senderID` INT NOT NULL,
            `receiverID` INT NULL,
            `message` VARCHAR(250) NOT NULL,
            `date` DATE NOT NULL DEFAULT (datetime('now','localtime'))
            )""")
        except:
            pass
        else:
            self.logList.insert(END, "[DB] Tabulka 'messages' byla vytvořena!")
            self.insertData(["DB", "Vytvořena tabulka 'messages'"], self.db)

        # vytvoření tabulky users
        try:
            self.db.execute("""CREATE TABLE users (
            `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `nickname` VARCHAR(30) NOT NULL,
            `password` VARCHAR(75) NOT NULL,
            `date` DATE NOT NULL DEFAULT (datetime('now','localtime'))
            )""")
        except:
            pass
        else:
            self.logList.insert(END, "[DB] Tabulka 'users' byla vytvořena!")
            self.insertData(["DB", "Vytvořena tabulka 'users'"], self.db)

            self.db.execute("SELECT COUNT(*) FROM messages")

            if self.db.fetchone()[0] > 0:
                self.db.execute("DELETE FROM messages")

                self.insertData(["DB", "Vyprázdněna tabulka 'messages'"], self.db)
                self.logList.insert(END, "[DB] Vyprázdněna tabulka 'messages'")

        self.port = 2205
        self.host = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.bind((self.host, self.port))
        self.server.listen()

        atexit.register(self.exitProgram)

    # metoda, která obstarává logování do DB
    def insertData(self, data, db):
        """
        logType - Info (Status, ), Error, Warning, Message
        """

        db.execute("INSERT INTO logs ('logType', 'logMessage') VALUES (?, ?)", data)
        db.execute("COMMIT")

    # zapnutí serveru
    def start(self):
        self.buttonStart.configure(state="disabled")
        self.buttonStop.configure(state="normal")
        self.buttonRestart.configure(state="normal")
        self.clients = []

        self.stopped = False
        self.logList.insert(END, "[SERVER] Server byl zapnut.")
        self.insertData(["Info", "Server Start"], self.db)
        thread_conn = thread.start_new_thread(self.connectClients, ())

    # připojení jednotlivého klienta
    def connectClients(self):
        try:
            # připojení k DB
            db = sql.connect("server_log.db")

            # nastavení kurzoru (můžeme vypisovat výsledky z DB)
            db = db.cursor()
        except:
            self.logList.insert(END, "[ERROR] Serveru se nepodařilo spojit se s databází!")
            return
        while self.stopped == False:
            conn, address = self.server.accept()  # prijmi clienta
            thread_conn = thread.start_new_thread(self.chat, (conn, self.clients, address,))

            self.clients.append({"address": address, "conn": conn})

            if self.stopped == False:
                self.logList.insert(END, f"[{address}]: connected")
                self.insertData(["Message", f"[{address}]: connected"], db)

    # přijímání a odesílání dat; uživatel = jedno vlákno
    def chat(self, conn, clients, address):
        try:
            # připojení k DB
            db = sql.connect("server_log.db")

            # nastavení kurzoru (můžeme vypisovat výsledky z DB)
            db = db.cursor()
        except:
            self.logList.insert(END, "[ERROR] Serveru se nepodařilo spojit se s databází!")
            return
        while self.stopped == False:
            #if is not None => pokud není prázdná
            # pokud existuje

            try:
                msg = conn.recv(1024) #zprava
                if not msg:
                    self.logList.insert(END, f"[{address}]: disconnected")
                    self.insertData(["Message", f"[{address}]: disconnected"], db)
                    conn.close()
                    self.clients.remove({"address": address, "conn": conn})
                    break

                else:
                    msgdata = msg.decode("utf-8")
                    msgdata = json.loads(msgdata)

                    # ukázka, jak vypadá msgdata: {"type": "register", "nick": "test", "password": "56af4bde70a47ae7d0f1ebb30e45ed336165d5c9ec00ba9a92311e33a4256d74"}
                    if "type" in msgdata:
                        if msgdata["type"] == "register":
                            db.execute("SELECT COUNT(nickname) FROM users WHERE nickname = ?", (msgdata["nick"],))
                            if db.fetchone()[0] != 0:
                                error = {
                                    "type": "error",
                                    "msg": "[SERVER] Uživatel s touto přezdívkou již existuje!"
                                }
                                error = json.dumps(error)
                                conn.send(bytes(error, "utf-8"))
                            else:
                                db.execute("INSERT INTO users (nickname, password) VALUES (?, ?)", (msgdata["nick"], msgdata["password"]))

                                db.execute("SELECT ID FROM users WHERE nickname = ? AND password = ?", (msgdata["nick"],msgdata["password"]))
                                userID = db.fetchone()[0]

                                success = {
                                    "type": "success",
                                    "ID": userID,
                                    "msg": "[SERVER] Váš účet byl úspěšně zaregistrován!"
                                }
                                success = json.dumps(success)
                                conn.send(bytes(success, "utf-8"))

                        elif msgdata["type"] == "login":
                            db.execute("SELECT COUNT(ID) FROM users WHERE nickname = ? AND password = ?", (msgdata["nick"],msgdata["password"]))
                            userID = db.fetchone()[0]
                            if userID != 0:
                                db.execute("SELECT ID FROM users WHERE nickname = ? AND password = ?", (msgdata["nick"],msgdata["password"]))
                                userID = db.fetchone()[0]
                                success = {
                                    "type": "success",
                                    "ID": userID,
                                    "msg": "[SERVER] Byli jste úspěšně přihlášeni!"
                                }
                                success = json.dumps(success)
                                conn.send(bytes(success, "utf-8"))
                            else:
                                error = {
                                    "type": "error",
                                    "msg": "[SERVER] Špatné heslo nebo přezdívka!"
                                }
                                error = json.dumps(error)
                                conn.send(bytes(error, "utf-8"))
                        elif msgdata["type"] == "msg":
                            # TODO: ukládání zpráv (níže)
                            #db.execute("INSERT INTO messages (senderID, message) VALUES (?, ?)", (msgdata["id"] ,msgdata["msg"]))

                            for client in self.clients:
                                client["conn"].send(bytes(json.dumps(msgdata), "utf-8"))
            except:
                pass
    # zastavení serveru
    def stop(self):

        # vypíná vlákna (uživatele)
        self.stopped = True

        # změní status tlačítek
        self.buttonStart.configure(state="normal")
        self.buttonStop.configure(state="disabled")
        self.buttonRestart.configure(state="disabled")

        # for client in self.clients:
        #     self.logList.insert(END, f"[{client['address']}]: disconnected")
        #     self.insertData(["Message", f"[{client['address']}]: disconnected"], self.db)
        #     client["conn"].close()
        #     self.clients.remove(client)

        self.logList.insert(END, "[SERVER] Server byl zastaven.")

    # restart serveru
    def restart(self):
        self.stop()
        self.start()

    # pro případ, že server ukončíme křížkem
    def exitProgram(self):
        if self.stopped == False:
            try:
                for client in self.clients:
                    self.insertData(["Message", f"[{client['address']}]: disconnected"], self.db)
                    client["conn"].close()
                    self.clients.remove(client)
            except:
                pass
            self.insertData(["Info", "Server Stopped"], self.db)

if __name__ == "__main__":
    server = Server()
    root.mainloop()
