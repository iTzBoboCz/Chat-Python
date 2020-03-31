import socket
import _thread as thread
import sqlite3 as sql
import os
import atexit

# vytvoření/otevření souboru s logy
try:
    logfile = open("server_log.db", "r")
    logfile.close()
except:
    logfile = open("server_log.db", "w+")
    logfile.close()

try:
    logdb.execute("""CREATE TABLE logs (
        `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `logType` VARCHAR(30) NOT NULL,
        `logMessage` varchar(75) NOT NULL,
        `date` DATE NOT NULL DEFAULT (datetime('now','localtime'))
    )""")
    #logdb.fetchone()
except:
    pass

class Server:
    def __init__(self):
        try:
            # připojení k DB
            self.logdb = sql.connect("server_log.db")

            # nastavení kurzoru (můžeme vypisovat výsledky z DB)
            self.logdb = self.logdb.cursor()
        except:
            print("[ERROR] Serveru se nepodařilo spojit se s databází na úchovu logů!")
            exit()

        self.port = 2205
        self.host = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.bind((self.host, self.port))
        self.server.listen()
        self.insertData(["Info", "Server Start"], self.logdb)

        atexit.register(self.insertData, data = ["Info", "Server Stopped"], logdb = self.logdb)

    def insertData(self, data, logdb):
        """
        logType - Info (Status, ), Error, Warning, Message
        """

        logdb.execute("INSERT INTO logs ('logType', 'logMessage') VALUES (?, ?)", data)
        logdb.execute("COMMIT")

    def start(self):
        self.clients = []
        while True:
            con, address = self.server.accept()  # prijmi clienta
            thread_con = thread.start_new_thread(self.chat, (con, self.clients, address,))
            self.clients.append(con)
            con.send(bytes("[SERVER->YOU] You have joined chat.", "utf-8"))
            print(f"[{address}]: connected")
            self.insertData(["Message", f"[{address}]: connected"], self.logdb)

    def chat(self, con, clients, address):
        try:
            # připojení k DB
            logdb = sql.connect("server_log.db")

            # nastavení kurzoru (můžeme vypisovat výsledky z DB)
            logdb = logdb.cursor()
        except:
            print("[ERROR] Serveru se nepodařilo spojit se s databází na úchovu logů!")
            return()
        while True:
            #if is not None => pokud není prázdná
            # pokud existuje
            msg = con.recv(1024) #zprava
            if not msg:
                print(f"[{address}]: disconnected")
                self.insertData(["Message", f"[{address}]: disconnected"], logdb)
                self.clients.remove(con)
                con.close()
                break
            else:
                print(msg.decode("utf-8"))
                for client in self.clients:
                    client.send(msg)

if __name__ == "__main__":
    server = Server()
    server.start()
