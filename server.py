import socket
import _thread as thread
import sqlite3 as sql
from tkinter import *
import os
import atexit

root = Tk()
root.configure(background='#bdc3c7')
root.geometry('1000x500')
root.minsize(1000, 500)
root.maxsize(1000, 500)
root.title("OnLuk Super-Chat Server v0") #nazev okna

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
            self.logList.insert(END, "[ERROR] Serveru se nepodařilo spojit se s databází na úchovu logů!")
            exit()

        try:
            self.db.execute("""CREATE TABLE logs (
                `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                `logType` VARCHAR(30) NOT NULL,
                `logMessage` varchar(75) NOT NULL,
                `date` DATE NOT NULL DEFAULT (datetime('now','localtime'))
            )""")
            #db.fetchone()
        except:
            pass

        self.port = 2205
        self.host = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.bind((self.host, self.port))
        self.server.listen()

        atexit.register(self.exitProgram)

    def insertData(self, data, db):
        """
        logType - Info (Status, ), Error, Warning, Message
        """

        db.execute("INSERT INTO logs ('logType', 'logMessage') VALUES (?, ?)", data)
        db.execute("COMMIT")

    def start(self):
        self.buttonStart.configure(state="disabled")
        self.buttonStop.configure(state="normal")
        self.buttonRestart.configure(state="normal")
        self.clients = []

        self.stopped = False
        self.logList.insert(END, "[SERVER]: start")
        self.insertData(["Info", "Server Start"], self.db)
        thread_conn = thread.start_new_thread(self.connectClients, ())

    def connectClients(self):

        while self.stopped == False:
            conn, address = self.server.accept()  # prijmi clienta
            thread_conn = thread.start_new_thread(self.chat, (conn, self.clients, address,))
            self.clients.append({"address": address, "conn": conn})
            conn.send(bytes("[SERVER->YOU] You have joined chat.", "utf-8"))
            self.logList.insert(END, f"[{address}]: connected")
            #self.insertData(["Message", f"[{address}]: connected"], self.db)
    def chat(self, conn, clients, address):
        try:
            # připojení k DB
            db = sql.connect("server_log.db")

            # nastavení kurzoru (můžeme vypisovat výsledky z DB)
            db = db.cursor()
        except:
            self.logList.insert(END, "[ERROR] Serveru se nepodařilo spojit se s databází na úchovu logů!")
            return()
        while True:
            #if is not None => pokud není prázdná
            # pokud existuje
            try:
                msg = conn.recv(1024) #zprava
                if not msg:
                    self.logList.insert(END, f"[{address}]: disconnected")
                    self.insertData(["Message", f"[{address}]: disconnected"], db)
                    conn.close()
                    self.clients.remove(conn)
                    break
                else:
                    print(msg.decode("utf-8"))
                    for client in self.clients:
                        client["conn"].send(msg)
            except:
                pass
    def stop(self):
        self.stopped = True
        self.buttonStart.configure(state="normal")
        self.buttonStop.configure(state="disabled")
        self.buttonRestart.configure(state="disabled")

        try:
            for client in self.clients:
                self.logList.insert(END, f"[{client['address']}]: disconnected")
                self.insertData(["Message", f"[{client['address']}]: disconnected"], self.db)
                client["conn"].close()
                self.clients.remove(client)
        except:
            pass

        self.logList.insert(END, "[SERVER]: Stopped")
        self.insertData(["Info", "Server Stopped"], self.db)

    def restart(self):
        self.stop()
        self.start()


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
