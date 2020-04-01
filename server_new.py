from tkinter import *
from tkinter import messagebox
import re

root = Tk()
root.configure(background='#bdc3c7')
root.geometry('1000x500')
root.minsize(1000, 500)
root.maxsize(1000, 500)
root.title("OnLuk Super-Chat Server v0") #nazev okna
class Form:
	def __init__(self):
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

		messagebox.showinfo(title="OK", message="OK")

	def login(self):
		nick = self.entryNameLogin.get()
		password = self.entryPassLogin.get()

		if nick == "" or password == "":
			return
		messagebox.showinfo(title="OK", message="OK")

	def destroy(self):
		self.loginWindow.grid_forget()
		self.registerWindow.grid_forget()

	def createAgain(self):
		self.loginWindow.grid_forget()
		self.registerWindow.grid_forget()
		return Form()
#MENU
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="Ukončit", menu=filemenu)

root.config(menu=menubar)

class Chat:
	def __init__(self):
		self.chatFrame = Frame(root, bg="#bdc3c7")
		self.chatFrame.pack()

		self.scrollbar = Scrollbar(self.chatFrame)
		self.scrollbar.pack( side = RIGHT, fill = Y )

		self.messageList = Listbox(self.chatFrame,width=150, height=20,bg="#ecf0f1", yscrollcommand = self.scrollbar.set)
		self.messageList.pack()


		self.messageInput = Frame(root, bg="#bdc3c7")
		self.messageInput.pack(pady=20)

		self.messageEntry = Text(self.messageInput , height=20, width=50,font=("Arial", 14))
		self.messageEntry.pack(side=LEFT)

		self.messageButton = Button(self.messageInput, text="Odeslat", font=("Arial", 14, "bold"), cursor="hand2", bd=0, bg="#4a69bd", activebackground="#82ccdd", fg="#ecf0f1")
		self.messageButton.pack(side=LEFT, ipady=20)

class Server:
	def __init__(self):
		self.serverFrame = Frame(root)
		self.serverFrame.pack()

		self.settingsMenu = Menu(menubar, tearoff=0)
		self.settingsMenu.add_command(label="Start", command=root.destroy)
		self.settingsMenu.add_command(label="Stop", command=root.destroy, state="disabled")
		self.settingsMenu.add_command(label="Restart", command=root.destroy, state="disabled")

		menubar.add_cascade(label="Nastavení", menu=self.settingsMenu)

		self.scrollbar = Scrollbar(self.serverFrame)
		self.scrollbar.pack( side = RIGHT, fill = Y )

		self.logList = Listbox(self.serverFrame,width=150, height=20,bg="#ecf0f1", yscrollcommand = self.scrollbar.set)
		self.logList.pack()
		self.logList.insert(END, "test")

		self.buttonStart = Button(root, text="Start",width=10, height=3,font=("Arial", 20, "bold"),  fg="white", bg="#2ecc71")
		self.buttonStop = Button(root, text="Stop", width=10, height=3,font=("Arial", 20, "bold"), fg="white", bg="#c0392b", state="disabled")
		self.buttonRestart = Button(root, text="Restart", width=10, height=3,font=("Arial", 20, "bold"), fg="white", bg="#95a5a6", state="disabled")

		self.buttonStart.pack(side=LEFT, padx=50)
		self.buttonStop.pack(side=LEFT, padx=100)
		self.buttonRestart.pack(side=LEFT, padx=50)

#server = Server()
#root.config(server.menubar)
#form = Form()
#form.createAgain()
chat = Chat()
#zničí form => form.destroy()
root.mainloop()
