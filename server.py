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

class Server:
    def __init__(self):

        try:
            # připojení k DB
            self.db = sql.connect("server_log.db")

            # nastavení kurzoru (můžeme vypisovat výsledky z DB)
            self.db = self.db.cursor()
        except:
            print("[ERROR] Serveru se nepodařilo spojit se s databází na úchovu logů!")
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
        self.insertData(["Info", "Server Start"], self.db)

        atexit.register(self.stop)

    def insertData(self, data, db):
        """
        logType - Info (Status, ), Error, Warning, Message
        """

        db.execute("INSERT INTO logs ('logType', 'logMessage') VALUES (?, ?)", data)
        db.execute("COMMIT")

    def start(self):
        self.clients = []
        while True:
            conn, address = self.server.accept()  # prijmi clienta
            thread_conn = thread.start_new_thread(self.chat, (conn, self.clients, address,))
            self.clients.append({"address": address, "conn": conn})
            conn.send(bytes("[SERVER->YOU] You have joined chat.", "utf-8"))
            print(f"[{address}]: connected")
            self.insertData(["Message", f"[{address}]: connected"], self.db)

    def chat(self, conn, clients, address):
        try:
            # připojení k DB
            db = sql.connect("server_log.db")

            # nastavení kurzoru (můžeme vypisovat výsledky z DB)
            db = db.cursor()
        except:
            print("[ERROR] Serveru se nepodařilo spojit se s databází na úchovu logů!")
            return()
        while True:
            #if is not None => pokud není prázdná
            # pokud existuje
            msg = conn.recv(1024) #zprava
            if not msg:
                print(f"[{address}]: disconnected")
                self.insertData(["Message", f"[{address}]: disconnected"], db)
                conn.close()
                self.clients.remove(conn)
                break
            else:
                print(msg.decode("utf-8"))
                for client in self.clients:
                    client["conn"].send(msg)
    def stop(self):
        for client in self.clients:
            self.insertData(["Message", f"[{client['address']}]: disconnected"], self.db)
            client["conn"].close()
            self.clients.remove(client)
        self.insertData(["Info", "Server Stopped"], self.db)

if __name__ == "__main__":
    server = Server()
    server.start()
