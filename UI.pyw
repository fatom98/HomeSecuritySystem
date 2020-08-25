from tkinter import *
from PIL import Image, ImageTk
from FaceRecognition import Recognise
from mail import SendEmail
import tkinter.messagebox, dbm, shutil, os

class GUI(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.recognise = Recognise()
        self.lock = ImageTk.PhotoImage(Image.open("icons/lock.gif"))
        self.unlock = ImageTk.PhotoImage(Image.open("icons/unlock.gif"))
        self.emergent = ImageTk.PhotoImage(Image.open("icons/emergency.png"))
        self.txt = ImageTk.PhotoImage(Image.open("icons/emerg.png"))
        self.address = "Hollywood boulevard  Paramount pictures"
        self.guest = None
        self.login()

    def login(self):

        self.pack(fill = BOTH)

        self.frame1 = Frame(self)
        self.frame1.pack(fill = X)

        self.frame2 = Frame(self)
        self.frame2.pack(fill = BOTH, padx = 30, pady = 30)

        root.geometry("450x180+450+200")
        mainLabel = Label(self.frame1, text = "Welcome. Please login", bg = "#4267B2", fg = "white", font = "ComicSans 16 bold")
        mainLabel.pack(fill = X)

        userNameLabel = Label(self.frame2, text = "Username: ", font = "ComicSans 12")
        userNameLabel.grid(row = 0, column = 0)

        self.userName = Entry(self.frame2)
        self.userName.grid(row = 0, column = 1, padx = 20)
        self.userName.focus()

        passwordLabel = Label(self.frame2, text = "Password: ", font = "ComicSans 12")
        passwordLabel.grid(row = 1, column = 0, pady = 10)

        self.passWord = Entry(self.frame2, show = "*")
        self.passWord.grid(row = 1, column = 1, pady = 10, padx = 20)
        self.passWord.bind("<Return>", lambda event: self.exist())

        login = Button(self.frame2, text = "Login", width = 10, height = 4)
        login.grid(row = 0, column = 2, rowspan = 2, padx = 50)
        login.bind("<ButtonRelease-1>", lambda event: self.exist())

    def exist(self):

        username, password = self.userName.get(), self.passWord.get()

        self.db = dbm.open("db/DB", "c")

        if username == "":
            tkinter.messagebox.showerror("Error", "Username can't be empty")
        elif password == "":
            tkinter.messagebox.showerror("Error", "Password can't be empty")
        elif username not in self.db:
            tkinter.messagebox.showerror("Error", "Wrong Username or Password")
        else:
            if self.db[username] != password.encode("utf-8"):
                tkinter.messagebox.showerror("Error", "Wrong Username or Password")
            else:
                self.guest = username
                tkinter.messagebox.showinfo("Welcome", f"Welcome {username.capitalize()}")
                self.mainScreen()

    def mainScreen(self):
        root.title("Home Security")

        self.frame1.destroy()
        self.frame2.destroy()

        frame1 = Frame(self)
        frame1.pack(fill = X)

        frame2 = Frame(self)
        frame2.pack(fill = X, pady = 20)

        frame3 = Frame(self)
        frame3.pack(fill = X, pady = 20)

        frame4 = Frame(self)
        frame4.pack(pady = 20)

        root.geometry("800x600+250+50")

        mainLabel = Label(frame1, text = "Home Security Management System", bg = "#4267B2", fg = "white", font = "ComicSans 16 bold")
        mainLabel.pack(fill = X)

        #First Column
        users = Label(frame2, text = "Registered Users", font = "ComicSans 16", fg = "orangered3")
        users.grid(row = 0, column = 0)

        listbox = Listbox(frame2)
        listbox.grid(row = 1, column = 0, pady = 10, rowspan = 3)

        for names in os.listdir("faces"):
            listbox.insert(END, names)
        listbox["state"] = DISABLED

        #Second Column
        self.text = Label(frame2, text = "State: Unlock", font = "ComicSans 16", fg = "orangered3")
        self.text.grid(row = 0, column = 1)

        self.state = Label(frame2, image = self.unlock)
        self.state.grid(row = 1, column = 1, rowspan = 3)
        self.state.bind("<ButtonRelease-1>", lambda event: self.click())

        #Third Column
        options = Label(frame2, text = "Options", font = "ComicSans 16", fg = "orangered3")
        options.grid(row = 0, column = 2)

        add = Button(frame2, text = "Register User", command = self.register)
        add.grid(row = 1, column = 2)

        remove = Button(frame2, text = "Delete User", command = self.remove)
        remove.grid(row = 2, column = 2)

        Grid.columnconfigure(frame2, 0, weight = 1)
        Grid.columnconfigure(frame2, 1, weight = 1)
        Grid.columnconfigure(frame2, 2, weight = 1)

        self.unlockButton = Button(frame3, text = "Unlock", height = 3, width = 10, command = self.recog, state = DISABLED)
        self.unlockButton.pack()

        txt = Label(frame4, image=self.txt)
        txt.pack(side=LEFT)

        self.emergency = Label(frame4, image = self.emergent)
        self.emergency.pack(side = LEFT)
        self.emergency.bind("<ButtonRelease-1>", lambda event: self.contact())

    def contact(self):
        self.done = ImageTk.PhotoImage(Image.open("icons/done.png"))
        message = f"Emergency at {self.address}. Contact Police"
        SendEmail(message = message)

        self.emergency["image"] = self.done
        self.state["image"] = self.lock
        tkinter.messagebox.showinfo("Alert", "We alerted the authorities. You are now under lock-down. Dont worry")

    def recog(self):
        ret = self.recognise.train(self.guest)

        if ret == "unlocked":
            self.text["text"] = "State: Unlocked"
            self.state["image"] = self.unlock
            self.unlockButton["state"] = DISABLED

    def click(self):
        self.text["text"] = "State: Lock"
        self.state["image"] = self.lock
        self.unlockButton["state"] = NORMAL


    def register(self):
        self.popup = Toplevel()
        self.popup.grab_set()

        self.popup.geometry("500x200+350+150")

        frame1 = Frame(self.popup)
        frame1.pack(fill = X)

        frame2 = Frame(self.popup)
        frame2.pack(fill=X)

        frame3 = Frame(self.popup)
        frame3.pack(fill=X, pady = 30)

        mainLabel = Label(frame1, text = "Register User", bg = "#4267B2", fg = "white", font = "ComicSans 16 bold")
        mainLabel.pack(fill = X, pady = (0,20))

        nameInfo = Label(frame2, text = "Name: ", font = "ComicSans 14")
        nameInfo.grid(row = 0, column = 0)

        self.name = Entry(frame2)
        self.name.grid(row = 0, column = 1)

        usernameInfo = Label(frame2, text="Username: ", font="ComicSans 14")
        usernameInfo.grid(row=0, column=2, padx = (40,0))

        self.username = Entry(frame2)
        self.username.grid(row=0, column=3, sticky = W)

        ageInfo = Label(frame2, text="Age: ", font="ComicSans 14")
        ageInfo.grid(row=1, column=0)

        self.age = Entry(frame2)
        self.age.grid(row=1, column=1, sticky = W)

        pwdInfo = Label(frame2, text="Password: ", font="ComicSans 14")
        pwdInfo.grid(row=1, column=2, padx = (40,0))

        self.pwd = Entry(frame2)
        self.pwd.grid(row=1, column=3)

        register = Button(frame3, text = "Register", height = 2, width = 10, command = self.control)
        register.pack()

    def control(self):

        name = self.name.get()
        username = self.username.get()
        age = self.age.get()
        password = self.pwd.get()

        if name == "":
            tkinter.messagebox.showerror("Error", "Name can't be empty")
        elif username == "":
            tkinter.messagebox.showerror("Error", "Username can't be empty")
        elif age == "":
            tkinter.messagebox.showerror("Error", "Age can't be empty")
        elif password == "":
            tkinter.messagebox.showerror("Error", "Password can't be empty")
        elif username in self.db:
            tkinter.messagebox.showerror("Error", "Username is already registered")
        else:
            self.db[username] = password
            self.recognise.create(username)
            self.popup.destroy()

    def remove(self):
        self.pop = Toplevel()
        self.pop.grab_set()

        self.pop.geometry("500x200+350+150")

        frame1 = Frame(self.pop)
        frame1.pack(fill = X)

        frame2 = Frame(self.pop)
        frame2.pack(fill=X, pady = 30)

        frame3 = Frame(self.pop)
        frame3.pack(fill = X)

        mainLabel = Label(frame1, text = "Delete User", font = "ComicSans 14", bg = "#4267B2", fg = "white")
        mainLabel.pack(fill = X)

        nameLabel = Label(frame2, text = "Enter the username you want to delete: ", font = "ComicSans 14")
        nameLabel.grid(row = 0, column = 0)

        self.entry = Entry(frame2)
        self.entry.grid(row = 0, column = 1)

        delete = Button(frame3, text = "Delete", command = self.condition)
        delete.pack()

    def condition(self):
        name = self.entry.get()

        if name == "":
            tkinter.messagebox.showerror("Error", "Username can't be empty")
        else:
            ans = tkinter.messagebox.askquestion("Remove", "Are you sure?", icon = "warning")
            if ans == "yes":

                if name not in self.db:
                    tkinter.messagebox.showerror("Error", "There is no such user")
                else:
                    self.pop.destroy()
                    shutil.rmtree(f"faces/{name}")
                    del self.db[name]
                    tkinter.messagebox.showinfo("Success", f"{name} is successfully deleted")


if __name__ == '__main__':
    root = Tk()
    app = GUI(root)
    root.title("Login")
    root.mainloop()