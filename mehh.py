import tkinter
import tkinter as tk  # python 3
from tkinter import font as tkfont  # python 3
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3
import socket
import pickle

global conn
conn = sqlite3.connect("newv.db", check_same_thread=False)
if conn:
    print("Connected Successfully")
else:
    print("Connection Not Established")
global cur
cur = conn.cursor()

IP = socket.gethostbyname(socket.gethostname())  # replace with my IP on hotspot
PORT = 2003
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
HEADERSIZE = 10
DISCONNECT_MSG = "DISCONNECT"
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(ADDR)
print(f"[Connected] at {IP}:{PORT}")

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('VOTING SYSTEM')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('925x500')
        self.resizable(0, 0)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Welcome_Page, PageOne, PageTwo, Adminpage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Welcome_Page")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Welcome_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Welcome_Page.controller = controller
        Welcome_Page.hold = []
        Welcome_Page.mainframe = ctk.CTkFrame(self, fg_color='white')
        Welcome_Page.mainframe.pack(expand=1, fill=tk.BOTH)

        Welcome_Page.create_widgets()

    @classmethod
    def create_widgets(cls):

        Welcome_Page.test = ctk.CTkFrame(Welcome_Page.mainframe, fg_color='white', width=250, height=350)
        Welcome_Page.test.place(x=673, y=70)
        Welcome_Page.test.my_img = ImageTk.PhotoImage(Image.open('IMG_1177.png'))
        Welcome_Page.test.my_label = tk.Label(Welcome_Page.mainframe, image=Welcome_Page.test.my_img)
        Welcome_Page.test.my_label.place(x=0, y=0)

        # =======================================WIDGET========================================================================
        Welcome_Page.heading = tk.Label(Welcome_Page.test, text='SIGN IN', fg='#299bdd', bg='white',
                                        font=('Microsoft YaHei UI Light', 23, 'bold')).place(x=50, y=5)

        Welcome_Page.username = ctk.CTkEntry(Welcome_Page.test, width=200, height=40, placeholder_text='Username',
                                             border_color='black',
                                             border_width=1
                                             , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Welcome_Page.username.place(x=15, y=90)

        Welcome_Page.password = ctk.CTkEntry(Welcome_Page.test, width=200, height=40, placeholder_text='Password',
                                             show='', border_width=1,
                                             border_color='black'
                                             , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Welcome_Page.password.place(x=15, y=150)

        Welcome_Page.signin = ctk.CTkButton(Welcome_Page.test, width=200, command=Welcome_Page.signin, height=40,
                                            fg_color='#299bdd', text='Sign in', text_color='white'
                                            , bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Welcome_Page.signin.place(x=15, y=230)

        Welcome_Page.check_status = 'off'
        Welcome_Page.check = ctk.CTkCheckBox(Welcome_Page.test, command=Welcome_Page.showpassword, text='Show Password',
                                             width=18, height=18,
                                             text_font=('Microsoft YaHei UI Light', 8, 'bold'))
        Welcome_Page.check.place(x=15, y=200)

        Welcome_Page.doyou = ctk.CTkLabel(Welcome_Page.test, fg_color='white', text='Do you have an account ?'
                                          , text_font=('Microsoft YaHei UI Light', 8, 'bold'))
        Welcome_Page.doyou.place(x=15, y=280)
        Welcome_Page.signup = ctk.CTkButton(Welcome_Page.test,
                                            command=lambda: Welcome_Page.controller.show_frame('PageOne'),
                                            fg_color='white', text='Signup', width=25, text_color='#299bdd'
                                            , bg_color='white', cursor='hand2',

                                            hover=False, text_font=('Microsoft YaHei UI Light', 8, 'bold'))
        Welcome_Page.signup.place(x=167, y=280)

    @classmethod
    def signin(cls):
        global username
        username = Welcome_Page.username.get()
        password = Welcome_Page.password.get()
        name = cur.execute('''SELECT ? FROM users''', (username,)).fetchone()[0]
        pas = cur.execute('''SELECT Password FROM users WHERE Username=? ''', (name,)).fetchone()[0]
        print(name, pas)
        profile = cur.execute('''SELECT Profile_id FROM users WHERE Username=? ''', (username,)).fetchone()[0]
        validity = cur.execute('''SELECT Validity FROM users WHERE Username=? ''', (username,)).fetchone()[0]
        if password == pas:
            if profile == 1:
                Welcome_Page.controller.show_frame('Adminpage')
                Welcome_Page.clearall()
            elif profile == 2:
                if validity == 'valid':
                    Welcome_Page.controller.show_frame('PageTwo')
                    try:
                        na = username
                        print(na, type(na))
                        status = cur.execute('''SELECT Status FROM users WHERE Username=? ''', (na,)).fetchone()[0]
                        if status == 'voted':
                            PageTwo.Vote.configure(state=tkinter.DISABLED)
                        else:
                            PageTwo.Vote.configure(state=tkinter.NORMAL)
                        cur.execute('''UPDATE users SET status='voted' WHERE Username=?''', (na,))
                    except:
                        print('no')
                    Welcome_Page.clearall()
                else:
                    tk.messagebox.showwarning(title="Error", message="Not eligible to vote.")
        else:
            tk.messagebox.showwarning(title="Error", message="Incorrect Login details.")

    @classmethod
    def clearall(cls):
        Welcome_Page.username.delete(0, 'end')
        Welcome_Page.password.delete(0, 'end')

    @classmethod
    def showpassword(cls):
        if Welcome_Page.check_status == 'off':
            Welcome_Page.password.configure(show='')
            Welcome_Page.check_status = 'on'
        else:
            Welcome_Page.password.configure(show='*')
            Welcome_Page.check_status = 'off'


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        PageOne.controller = controller
        self.configure(bg='white')
        PageOne.mainframe = ctk.CTkFrame(self, fg_color='white')
        PageOne.mainframe.pack(expand=1, fill=tk.BOTH)
        PageOne.create()
        print(Welcome_Page.hold)

    @classmethod
    def create(cls):
        PageOne.testwindow = ctk.CTkFrame(PageOne.mainframe, fg_color='white', width=250, height=500)
        PageOne.testwindow.place(x=679, y=20)
        PageOne.testwindow.my_img = ImageTk.PhotoImage(Image.open('IMG_1177.png'))
        PageOne.testwindow.my_label = tk.Label(PageOne.mainframe, image=PageOne.testwindow.my_img)
        PageOne.testwindow.my_label.place(x=0, y=0)
        # ====================================================widgets====================================================
        PageOne.heading = tk.Label(PageOne.testwindow, text='SIGN UP', fg='#299bdd', bg='white',
                                   font=('Microsoft YaHei UI Light', 23, 'bold')).grid(row=0, column=0)

        PageOne.firstlab = tk.Label(PageOne.testwindow, text='Firstname', fg='#299bdd', bg='white',
                                    font=('Microsoft YaHei UI Light', 8, 'bold')).grid(row=1, column=0, sticky='w',
                                                                                       pady=(5, 0))

        PageOne.firstname1_entry = ctk.CTkEntry(PageOne.testwindow, width=200, height=30, placeholder_text='Firstname',
                                                border_color='black',
                                                border_width=1
                                                , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        PageOne.firstname1_entry.grid(row=2, column=0)

        PageOne.lastlab = tk.Label(PageOne.testwindow, text='Lastname', fg='#299bdd', bg='white',
                                   font=('Microsoft YaHei UI Light', 8, 'bold')).grid(row=3, column=0, sticky='w',
                                                                                      pady=(5, 0))
        PageOne.lastname1_entry = ctk.CTkEntry(PageOne.testwindow, width=200, height=30, placeholder_text='Lastname',
                                               border_color='black',
                                               border_width=1
                                               , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        PageOne.lastname1_entry.grid(row=4, column=0)

        PageOne.userlab = tk.Label(PageOne.testwindow, text='Username', fg='#299bdd', bg='white',
                                   font=('Microsoft YaHei UI Light', 8, 'bold')).grid(row=5, column=0, sticky='w',
                                                                                      pady=(5, 0))
        PageOne.username_entry = ctk.CTkEntry(PageOne.testwindow, width=200, height=30, placeholder_text='Username',
                                              border_color='black',
                                              border_width=1
                                              , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        PageOne.username_entry.grid(row=6, column=0)

        PageOne.passlab = tk.Label(PageOne.testwindow, text='Password', fg='#299bdd', bg='white',
                                   font=('Microsoft YaHei UI Light', 8, 'bold')).grid(row=7, column=0, sticky='w',
                                                                                      pady=(5, 0))
        PageOne.password_entry = ctk.CTkEntry(PageOne.testwindow, width=200, height=30, placeholder_text='Password',
                                              border_color='black',
                                              border_width=1
                                              , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        PageOne.password_entry.grid(row=8, column=0)

        PageOne.conflab = tk.Label(PageOne.testwindow, text='Confirm Password', fg='#299bdd', bg='white',
                                   font=('Microsoft YaHei UI Light', 8, 'bold')).grid(row=9, column=0, sticky='w',
                                                                                      pady=(5, 0))
        PageOne.confirm_entry = ctk.CTkEntry(PageOne.testwindow, width=200, height=30,
                                             placeholder_text='Confirm Password',
                                             border_color='black',
                                             border_width=1
                                             , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        PageOne.confirm_entry.grid(row=10, column=0)

        PageOne.submit = ctk.CTkButton(PageOne.testwindow, width=200, height=30, fg_color='#299bdd', text='Submit',
                                       text_color='white',
                                       command=PageOne.submit
                                       , bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        PageOne.submit.grid(row=11, column=0, pady=(10, 0))

        PageOne.signup = ctk.CTkButton(PageOne.testwindow, fg_color='white', text='Back To Signin', width=25,
                                       text_color='#299bdd'
                                       , bg_color='white', cursor='hand2',
                                       command=lambda: PageOne.controller.show_frame('Welcome_Page'),
                                       hover=False, text_font=('Microsoft YaHei UI Light', 8, 'bold'))
        PageOne.signup.grid(row=12, column=0, sticky='w', pady=(5, 0))

    # =============================================functions================================================
    @classmethod
    def submit(cls):
        msg = 'sign up'
        c.send(msg.encode(FORMAT))
        firstname = PageOne.firstname1_entry.get()
        lastname = PageOne.lastname1_entry.get()
        conf = PageOne.confirm_entry.get()
        password = PageOne.password_entry.get()
        username = PageOne.username_entry.get()
        c.send(str(firstname).encode(FORMAT))
        c.send(str(lastname).encode(FORMAT))
        c.send(str(username).encode(FORMAT))
        c.send(str(password).encode(FORMAT))

        if password and username and conf and firstname and lastname:
            if password == conf:
                PageOne.controller.show_frame("Welcome_Page")
                PageOne.clearall()
                tk.messagebox.showinfo('ACCOUNT CREATED', 'Account Succesfully Created')

            else:
                tk.messagebox.showwarning(title="Error", message="Password Incorrect")
        else:
            tk.messagebox.showwarning(title="Error", message="Must fill all parameters.")

    @classmethod
    def clearall(cls):
        PageOne.firstname1_entry.delete(0, 'end')
        PageOne.lastname1_entry.delete(0, 'end')
        PageOne.username_entry.delete(0, 'end')
        PageOne.password_entry.delete(0, 'end')
        PageOne.confirm_entry.delete(0, 'end')


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')
        PageTwo.mainframe = ctk.CTkFrame(self, fg_color='white')
        PageTwo.mainframe.pack(expand=1, fill=tk.BOTH)
        PageTwo.create()
        PageTwo.controller = controller

    @classmethod
    def create(cls):
        PageTwo.testwindow = ctk.CTkFrame(PageTwo.mainframe, height=490, width=230, corner_radius=20,
                                          border_color="#6960Ec", border_width=
                                          2, fg_color='#2B547E', bg_color='white')
        PageTwo.testwindow.grid(row=0, column=0, padx=(7, 0), pady=(5, 5))
        PageTwo.testwindow.grid_propagate(False)

        PageTwo.managementlabel = ctk.CTkLabel(PageTwo.testwindow, text="Management", fg='white', bg='white',
                                               text_color='white', text_font=('Microsoft YaHei UI Light', 13, 'bold'))
        PageTwo.managementlabel.grid(row=0, column=0)

        PageTwo.vote = ctk.CTkButton(PageTwo.testwindow, corner_radius=30, fg_color='white', command=PageTwo.vote1,
                                     text='Vote', width=200, text_color='#299bdd'
                                     , text_font=('Microsoft YaHei UI Light', 10, 'bold'))
        PageTwo.vote.grid(row=2, column=0, pady=20, padx=(15, 0))
        PageTwo.vote.grid_propagate(False)

        PageTwo.view = ctk.CTkButton(PageTwo.testwindow, corner_radius=30, command=PageTwo.view, fg_color='white',
                                     text='View Results', width=200, text_color='#299bdd'
                                     , text_font=('Microsoft YaHei UI Light', 10, 'bold'))
        PageTwo.view.grid(row=3, column=0, pady=20, padx=(15, 0))
        PageTwo.view.grid_propagate(False)

        PageTwo.logout = ctk.CTkButton(PageTwo.testwindow, corner_radius=10, fg_color='#2B547E', text='Logout',
                                       width=200, text_color='white', hover=False
                                       , text_font=('Microsoft YaHei UI Light', 10, 'bold'),
                                       command=lambda: PageTwo.controller.show_frame("Welcome_Page"))
        PageTwo.logout.place(x=25, y=400)
        PageTwo.logout.grid_propagate(False)
        # ==================FRAMES FRAMES FRAMES=================================================================================#

        PageTwo.framevote = ctk.CTkFrame(PageTwo.mainframe, height=490, corner_radius=20, width=660,
                                         border_color="#6960Ec", border_width=2)
        PageTwo.framevote.configure(fg_color='white')
        PageTwo.framevote.grid(row=0, column=1, padx=(20, 0), pady=(5, 5))
        PageTwo.framevote.grid_propagate(False)

        PageTwo.frameview = ctk.CTkFrame(PageTwo.mainframe, height=490, corner_radius=20, width=660,
                                         border_color="#6960Ec", border_width=2)
        PageTwo.frameview.configure(fg_color='white')
        PageTwo.frameview.grid(row=0, column=1, padx=(20, 0), pady=(5, 5))
        PageTwo.frameview.grid_propagate(False)

        # ======================================WIDGETS================================================================

        PageTwo.entrylabel = tk.Label(PageTwo.framevote, text='VOTE FOR A CANDIDATE', fg='black', bg='white',
                                      font=('Microsoft YaHei UI Light', 20, 'bold'))
        PageTwo.entrylabel.grid(row=1, column=0, pady=5, padx=50)

        PageTwo.label = ctk.CTkLabel(PageTwo.frameview, text=' Candidates Vote Count',
                                     text_font=('Microsoft YaHei UI Light', 20, 'bold'))
        PageTwo.label.grid(row=0, column=1, sticky='w', pady=5, padx=10)

        PageTwo.placeholder = ctk.CTkLabel(PageTwo.frameview, text='RESULTS WILL BE '
                                                                   'RELEASED SOON .......',
                                           text_color='#9897A9', text_font=('Microsoft YaHei UI Light', 20))
        PageTwo.placeholder.grid(row=1, column=1, sticky='w', pady=180, padx=(20, 0))

    #   PageTwo.scrollbar=tk.Scrollbar(PageTwo.framevote).place(x=600)

    # =============================================functions================================================

    @classmethod
    def vote1(cls):
        PageTwo.framevote.tkraise()

    @classmethod
    def view(cls):
        PageTwo.frameview.tkraise()

    @classmethod
    def votecount(cls):
        pass


class Adminpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='white')
        Adminpage.mainframe = ctk.CTkFrame(self, fg_color='white')
        Adminpage.mainframe.pack(expand=1, fill=tk.BOTH)
        Adminpage.create()
        Adminpage.controller = controller

        Adminpage.keep = []

    @classmethod
    def create(cls):

        Adminpage.testwindow1 = ctk.CTkFrame(Adminpage.mainframe, height=490, width=230, corner_radius=20,
                                             border_color="#6960Ec", border_width=2
                                             , fg_color='#2B547E', bg_color='white')
        Adminpage.testwindow1.grid(row=0, column=0, padx=(7, 0), pady=(5, 5))
        Adminpage.testwindow1.grid_propagate(False)
        Adminpage.managementlabel = ctk.CTkLabel(Adminpage.testwindow1, text="Management", fg='white', bg='white',
                                                 text_color='white', text_font=('Microsoft YaHei UI Light', 13, 'bold'))
        Adminpage.managementlabel.grid(row=0, column=0)
        Adminpage.candidates = ctk.CTkButton(Adminpage.testwindow1, fg_color='white', corner_radius=30,
                                             command=Adminpage.cand,
                                             text='Candidates', width=200, text_color='#299bdd'
                                             , text_font=('Microsoft YaHei UI Light', 10, 'bold'))
        Adminpage.candidates.grid(row=1, column=0, pady=20, padx=(15, 0))
        Adminpage.candidates.grid_propagate(False)

        Adminpage.voterverification = ctk.CTkButton(Adminpage.testwindow1, corner_radius=30,
                                                    fg_color='white', command=Adminpage.vote, text='Voter Verification',
                                                    width=200, text_color='#299bdd'
                                                    , text_font=('Microsoft YaHei UI Light', 10, 'bold'))
        Adminpage.voterverification.grid(row=2, column=0, pady=20, padx=(15, 0))
        Adminpage.voterverification.grid_propagate(False)

        Adminpage.Showcand = ctk.CTkButton(Adminpage.testwindow1, corner_radius=30,
                                           fg_color='white', command=Adminpage.candid, text='Confirmation',
                                           width=200, text_color='#299bdd'
                                           , text_font=('Microsoft YaHei UI Light', 10, 'bold'))
        Adminpage.Showcand.grid(row=3, column=0, pady=20, padx=(15, 0))
        Adminpage.Showcand.grid_propagate(False)

        Adminpage.view = ctk.CTkButton(Adminpage.testwindow1, corner_radius=30, command=Adminpage.view,
                                       fg_color='white',
                                       text='View Results', width=200, text_color='#299bdd'
                                       , text_font=('Microsoft YaHei UI Light', 10, 'bold'))
        Adminpage.view.grid(row=4, column=0, pady=20, padx=(15, 0))
        Adminpage.view.grid_propagate(False)

        Adminpage.logout = ctk.CTkButton(Adminpage.testwindow1, corner_radius=10, fg_color='#2B547E', text='Logout',
                                         width=200,
                                         text_color='white', hover=False
                                         , text_font=('Microsoft YaHei UI Light', 10, 'bold'),
                                         command=lambda: Adminpage.controller.show_frame("Welcome_Page"))
        Adminpage.logout.place(x=25, y=400)
        Adminpage.logout.grid_propagate(False)
        # =====================================frames=============================================================================

        Adminpage.frameview = ctk.CTkFrame(Adminpage.mainframe, height=490, corner_radius=20, width=660, border_width=2,
                                           border_color="#6960Ec")
        Adminpage.frameview.configure(fg_color='white')
        Adminpage.frameview.grid(row=0, column=1, padx=(20, 0), pady=(5, 5))
        Adminpage.frameview.grid_propagate(False)

        Adminpage.frameadd = ctk.CTkFrame(Adminpage.mainframe, height=490, corner_radius=20, width=660, border_width=2,
                                          border_color="#6960Ec")
        Adminpage.frameadd.configure(fg_color='white')
        Adminpage.frameadd.grid(row=0, column=1, padx=(20, 0), pady=(5, 5))
        Adminpage.frameadd.grid_propagate(False)

        Adminpage.infor = ctk.CTkFrame(Adminpage.frameadd, width=250, height=240, corner_radius=20, border_width=2,
                                       border_color="#6960Ec")
        Adminpage.infor.grid(row=0, column=1, padx=(220, 0), pady=(50, 5))
        Adminpage.infor.configure(fg_color='white')
        Adminpage.infor.grid_propagate(False)

        Adminpage.show = ctk.CTkFrame(Adminpage.mainframe, height=490, corner_radius=20, width=660, border_width=2,
                                      border_color="#6960Ec")
        Adminpage.show.configure(fg_color='white')
        Adminpage.show.grid(row=0, column=1, padx=(20, 0), pady=(5, 5))
        Adminpage.show.grid_propagate(False)

        Adminpage.verify = ctk.CTkFrame(Adminpage.mainframe, height=490, corner_radius=20, width=660, border_width=2,
                                        border_color="#6960Ec")
        Adminpage.verify.configure(fg_color='white')
        Adminpage.verify.grid(row=0, column=1, padx=(20, 0), pady=(5, 5))
        Adminpage.verify.grid_propagate(False)

        Adminpage.need = ctk.CTkFrame(Adminpage.verify, width=200, height=235, corner_radius=20, border_width=2,
                                      border_color="#6960Ec")
        Adminpage.need.place(x=437, y=50)
        Adminpage.need.configure(fg_color='white')
        Adminpage.need.grid_propagate(False)

        Adminpage.show = ctk.CTkFrame(Adminpage.mainframe, height=490, corner_radius=20, width=660, border_width=2,
                                      border_color="#6960Ec")
        Adminpage.show.configure(fg_color='white')
        Adminpage.show.grid(row=0, column=1, padx=(20, 0), pady=(5, 5))
        Adminpage.show.grid_propagate(False)

        Adminpage.delete = ctk.CTkFrame(Adminpage.show, width=200, height=235, corner_radius=20, border_width=2,
                                        border_color="#6960Ec")
        Adminpage.delete.place(x=437, y=50)
        Adminpage.delete.configure(fg_color='white')
        Adminpage.delete.grid_propagate(False)

        Adminpage.framecandidate = ctk.CTkFrame(Adminpage.mainframe, height=490, corner_radius=20, width=660,
                                                border_width=2, border_color="#6960Ec")
        Adminpage.framecandidate.grid(row=0, column=1, padx=(20, 0), pady=(5, 5))
        Adminpage.framecandidate.configure(fg_color='white')
        Adminpage.framecandidate.grid_propagate(False)
        # =================================================================widgets===============================================

        Adminpage.heading = tk.Label(Adminpage.framecandidate, text='ADD CANDIDATES(ADMIN ONLY)', fg='black',
                                     bg='white',
                                     font=('Microsoft YaHei UI Light', 15, 'bold')).place(x=15, y=30)

        Adminpage.head = tk.Label(Adminpage.framecandidate, text='Admin Code', fg='black', bg='white',
                                  font=('Microsoft YaHei UI Light', 9, 'bold')).place(x=15, y=90)
        Adminpage.code = ctk.CTkEntry(Adminpage.framecandidate, width=200, height=40, border_color='black',
                                      border_width=1
                                      , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.code.place(x=15, y=110)
        Adminpage.submit = ctk.CTkButton(Adminpage.framecandidate, command=Adminpage.add, text='Submit',
                                         text_color='white'
                                         , fg_color='#299bdd')
        Adminpage.submit.place(x=15, y=160)

        Adminpage.heading = tk.Label(Adminpage.infor, text='Candidate Information', fg='#299bdd', bg='white',
                                     font=('Microsoft YaHei UI Light', 14, 'bold')).grid(row=0, column=0, pady=(10, 0),
                                                                                         padx=(20, 0))

        Adminpage.firstlab = tk.Label(Adminpage.infor, text='Firstname', fg='#299bdd', bg='white',
                                      font=('Microsoft YaHei UI Light', 8, 'bold'))
        Adminpage.firstlab.grid(row=1, column=0, sticky='w', pady=(5, 0), padx=(12, 0))
        Adminpage.firstname1_entry = ctk.CTkEntry(Adminpage.infor, width=200, height=30, placeholder_text='Firstname',
                                                  border_color='black',
                                                  border_width=1
                                                  , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.firstname1_entry.grid(row=2, column=0)

        Adminpage.lastlab = tk.Label(Adminpage.infor, text='Lastname', fg='#299bdd', bg='white',
                                     font=('Microsoft YaHei UI Light', 8, 'bold'))
        Adminpage.lastlab.grid(row=3, column=0, sticky='w', pady=(5, 0), padx=(20, 0))
        Adminpage.lastname1_entry = ctk.CTkEntry(Adminpage.infor, width=200, height=30, placeholder_text='Lastname',
                                                 border_color='black',
                                                 border_width=1
                                                 , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.lastname1_entry.grid(row=4, column=0)

        Adminpage.submit = ctk.CTkButton(Adminpage.infor, width=200, height=30, fg_color='#299bdd', text='Submit',
                                         text_color='white', command=Adminpage.collect,
                                         bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.submit.grid(row=9, column=0, pady=(30, 0))

        Adminpage.label = ctk.CTkLabel(Adminpage.show, text='All Candidates',
                                       text_font=('Microsoft YaHei UI Light', 20, 'bold'))
        Adminpage.label.grid(row=0, column=1, sticky='w', pady=5, padx=10)

        Adminpage.heading1 = tk.Label(Adminpage.delete, text='Confirmation', fg='#299bdd', bg='white',
                                      font=('Microsoft YaHei UI Light', 12, 'bold')).grid(row=0, column=0, pady=(10, 0),
                                                                                          padx=(20, 0))

        Adminpage.index = tk.Label(Adminpage.delete, text='Delete Candidate(ID)', fg='#299bdd', bg='white',
                                   font=('Microsoft YaHei UI Light', 8, 'bold'))
        Adminpage.index.grid(row=1, column=0, sticky='w', pady=(5, 0), padx=(18, 0))
        Adminpage.indexentry = ctk.CTkEntry(Adminpage.delete, width=160, height=30,
                                            placeholder_text='Candidate ID',
                                            border_color='black',
                                            border_width=1
                                            , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.indexentry.grid(row=2, column=0, padx=(18, 0))

        Adminpage.deletecan = ctk.CTkButton(Adminpage.delete, width=160, height=30, fg_color='#299bdd',
                                            text='Delete Candidate',
                                            text_color='white', command=Adminpage.delete1,
                                            bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.deletecan.grid(row=3, column=0, pady=(15, 0), padx=(18, 0))

        Adminpage.confirm = ctk.CTkButton(Adminpage.delete, width=160, height=30, fg_color='#299bdd',
                                          text='Confirm Candidates',
                                          text_color='white', command=Adminpage.cont,
                                          bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.confirm.grid(row=4, column=0, pady=(15, 0), padx=(18, 0))

        Adminpage.label = ctk.CTkLabel(Adminpage.frameview, text=' Candidates Vote Count',
                                       text_font=('Microsoft YaHei UI Light', 20, 'bold'))
        Adminpage.label.grid(row=0, column=1, sticky='w', pady=5, padx=10)

        Adminpage.updatevote = ctk.CTkButton(Adminpage.frameview, command=Adminpage.display, text='Show Result',
                                             text_color='white'
                                             , fg_color='#299bdd')
        Adminpage.updatevote.place(x=500, y=440)

        Adminpage.placeholder = ctk.CTkLabel(Adminpage.frameview, text='RESULTS WILL BE '
                                                                       'RELEASED SOON .......',
                                             text_color='#9897A9', text_font=('Microsoft YaHei UI Light', 20))
        Adminpage.placeholder.grid(row=1, column=1, sticky='w', pady=180, padx=(20, 0))

        #  Adminpage.waiting = ctk.CTkLabel(Adminpage.show, text='No current Candidtes',
        #                                text_font=('Retro', 20))
        # Adminpage.waiting.grid(row=3, column=1, sticky='w', pady=150, padx=10)

        ######this is for verifying   voterssss######3
        ######################################################################################################3333
        Adminpage.label1 = ctk.CTkLabel(Adminpage.verify, text='Voter Verification',
                                        text_font=('Microsoft YaHei UI Light', 20, 'bold'))
        Adminpage.label1.grid(row=0, column=1, sticky='w', pady=5, padx=10)

        Adminpage.heading2 = tk.Label(Adminpage.need, text='Verify', fg='#299bdd', bg='white',
                                      font=('Microsoft YaHei UI Light', 12, 'bold')).grid(row=0, column=0, pady=(10, 0),
                                                                                          padx=(20, 0))

        Adminpage.index1 = tk.Label(Adminpage.need, text='Verify Candidate(Index)', fg='#299bdd', bg='white',
                                    font=('Microsoft YaHei UI Light', 8, 'bold'))
        Adminpage.index1.grid(row=1, column=0, sticky='w', pady=(5, 0), padx=(18, 0))
        Adminpage.indexentry1 = ctk.CTkEntry(Adminpage.need, width=160, height=30,
                                             placeholder_text='Voter Index',
                                             border_color='black',
                                             border_width=1
                                             , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.indexentry1.grid(row=2, column=0, padx=(18, 0))

        Adminpage.deletecan1 = ctk.CTkButton(Adminpage.need, width=160, height=30, fg_color='#299bdd',
                                             text='Invalidate',
                                             text_color='white',
                                             command=Adminpage.delete_voter,
                                             bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.deletecan1.grid(row=3, column=0, pady=(15, 0), padx=(18, 0))

        Adminpage.confirm1 = ctk.CTkButton(Adminpage.need, width=160, height=30, fg_color='#299bdd',
                                           text='Verify Voter',
                                           text_color='white',
                                           bg_color='white',
                                           command=Adminpage.verify_voter,
                                           text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.confirm1.grid(row=4, column=0, pady=(15, 0), padx=(18, 0))

    # ================================================functions==========================================
    @classmethod
    def display(cls):
        PageTwo.placeholder.destroy()
        tk.messagebox.showinfo('Results Released', 'Voters May Now View Results')
        results = cur.execute('''SELECT Firstname, Lastname FROM candidates WHERE Validity='valid' ''').fetchall()
        cunt = cur.execute('''SELECT vote_count FROM candidates WHERE Validity='valid' ''').fetchall()
        currow = 2
        y = 1
        for i in results:
            Adminpage.see = tk.Label(PageTwo.frameview, text=f"{y}. {i[0]} {i[1]}",
                                     font=('Microsoft YaHei UI Light', 12))
            Adminpage.see.grid(row=currow, column=1, sticky='w', pady=5, padx=10)
            currow += 1
            y += 1

        seerow = 2
        for i in cunt:
            Adminpage.see = tk.Label(PageTwo.frameview, text=f"{i[0]}",
                                     font=('Microsoft YaHei UI Light', 12))
            Adminpage.see.grid(row=seerow, column=2, sticky='w')
            seerow += 1

    @classmethod
    def delete1(cls):
        index = Adminpage.indexentry.get()
        who = cur.execute('''SELECT Firstname, Lastname FROM candidates WHERE candidate_id=?''', (index,)).fetchone()
        cur.execute('''UPDATE candidates SET validity='invalid' WHERE candidate_id=?''', (index,))
        conn.commit()
        tk.messagebox.showinfo('Candidate blocked', f'{who[0]} {who[1]} with ID {index} has been blocked successfully')
        Voters.remove()

    # ================================================new functions start==========================================
    @classmethod
    def delete_voter(cls):
        index = Adminpage.indexentry1.get()
        msg = 'delete voter'
        c.send(msg.encode(FORMAT))
        c.send(str(index).encode(FORMAT))
        can = pickle.loads(c.recv(SIZE))
        who = c.recv(SIZE).decode(FORMAT)
        tk.messagebox.showinfo('Voter blocked', f'{who[0]} {who[1]} with ID {index} has been blocked successfully')
        currow = 2
        for i in can:
            PageTwo.votersshow = ctk.CTkLabel(Adminpage.verify, text=f"{i[0]}. {i[1]} {i[2]} {i[3]} ",
                                              text_font=('Microsoft YaHei UI Light', 12))
            PageTwo.votersshow.grid(row=currow, column=1, sticky='w', pady=5, padx=10)
            currow += 1

        Voters.remove1()

    @classmethod
    def verify_voter(cls):
        index = Adminpage.indexentry1.get()
        who = cur.execute('''SELECT Firstname, Lastname FROM users WHERE User_id=?''', (index,)).fetchone()
        cur.execute('''UPDATE users SET validity='valid' WHERE User_id=?''', (index,))
        conn.commit()
        tk.messagebox.showinfo('Voter verified', f'{who[0]} {who[1]} with ID {index} has been verified successfully')
        can = cur.execute(
            '''SELECT User_id, Firstname, Lastname, Validity FROM users WHERE Profile_id=2 ''').fetchall()
        currow = 2

        for i in can:
            PageTwo.votersshow = ctk.CTkLabel(Adminpage.verify, text=f"{i[0]}. {i[1]} {i[2]} {i[3]} ",
                                              text_font=('Microsoft YaHei UI Light', 12))
            PageTwo.votersshow.grid(row=currow, column=1, sticky='w', pady=5, padx=10)
            currow += 1

            Voters.remove1()

    # ================================================new functions end==========================================

    @classmethod
    def cont(cls):
        tk.messagebox.showinfo('Candidates confirmed', 'Voting May Begin')
        Voters.vote_candidate()

    @classmethod
    def collect(cls):
        firstname1 = Adminpage.firstname1_entry.get()
        lastname1 = Adminpage.lastname1_entry.get()

        firstname2 = firstname1.capitalize()
        lastname2 = lastname1.capitalize()

        Voters.add_candidate(firstname2, lastname2)
        Adminpage.showcand()
        tk.messagebox.showinfo('Candidates Added', 'Candidate Added Sucessfully')
        Adminpage.clearall()

    @classmethod
    def clearall(cls):
        Adminpage.firstname1_entry.delete(0, 'end')
        Adminpage.lastname1_entry.delete(0, 'end')

    @classmethod
    def vote(cls):
        Adminpage.verify.tkraise()

        currow = 2
        can = cur.execute(
            '''SELECT User_id, Firstname, Lastname, Validity FROM users WHERE Profile_id=2 ''').fetchall()
        for i in can:
            PageTwo.votersshow = ctk.CTkLabel(Adminpage.verify, text=f"{i[0]}. {i[1]} {i[2]} {i[3]} ",
                                              text_font=('Microsoft YaHei UI Light', 12))
            PageTwo.votersshow.grid(row=currow, column=1, sticky='w', pady=5, padx=10)
            currow += 1

    @classmethod
    def ver(cls):
        currow = 2
        can = cur.execute(
            '''SELECT User_id, Firstname, Lastname, Validity FROM users WHERE Profile_id=2 ''').fetchall()
        for i in can:
            PageTwo.votersshow = ctk.CTkLabel(Adminpage.verify, text=f"{i[0]}. {i[1]} {i[2]} {i[3]} ",
                                              text_font=('Microsoft YaHei UI Light', 12))
            PageTwo.votersshow.grid(row=currow, column=1, sticky='w', pady=5, padx=10)
            currow += 1

    @classmethod
    def cand(cls):
        Adminpage.framecandidate.tkraise()

    @classmethod
    def view(cls):
        Adminpage.frameview.tkraise()

    @classmethod
    def candid(cls):
        Adminpage.show.tkraise()
        currow = 2
        can = cur.execute(
            '''SELECT candidate_id, Firstname, Lastname, Validity FROM candidates WHERE validity='valid' ''').fetchall()
        for i in can:
            PageTwo.votersshow = ctk.CTkLabel(Adminpage.show, text=f"{i[0]}. {i[1]} {i[2]} {i[3]} ",
                                              text_font=('Microsoft YaHei UI Light', 12))
            PageTwo.votersshow.grid(row=currow, column=1, sticky='w', pady=5, padx=10)
            currow += 1

    @classmethod
    def showcand(cls):
        msg = 'candidates'
        c.send(msg.encode(FORMAT))
        can = pickle.loads(c.recv(SIZE))
        currow = 2
        for i in can:
            PageTwo.votersshow = ctk.CTkLabel(Adminpage.show, text=f"{i[0]}. {i[1]} {i[2]} {i[3]}",
                                              text_font=('Microsoft YaHei UI Light', 12))
            PageTwo.votersshow.grid(row=currow, column=1, sticky='w', pady=5, padx=10)
            currow += 1

        """currow = 2
        can = cur.execute(
            '''SELECT candidate_id, Firstname, Lastname, Validity FROM candidates WHERE validity='valid' ''').fetchall()
        for i in can:
            PageTwo.votersshow = ctk.CTkLabel(Adminpage.show, text=f"{i[0]}. {i[1]} {i[2]} {i[3]} ",
                                              text_font=('Microsoft YaHei UI Light', 12))
            PageTwo.votersshow.grid(row=currow, column=1, sticky='w', pady=5, padx=10)
            currow += 1"""

    @classmethod
    def add(cls):
        password = Adminpage.code.get()
        msg = 'admin'
        c.send(msg.encode(FORMAT))
        c.send(str(password).encode(FORMAT))
        detail = c.recv(SIZE).decode(FORMAT)

        if password == detail:
            Adminpage.clearall1()
            Adminpage.frameadd.tkraise()

        else:
            tk.messagebox.showwarning(title="Error", message="Invalid Admin Code")

    @classmethod
    def clearall1(cls):
        Adminpage.code.delete(0, 'end')

        for i in range(2, 100):
            Adminpage.keep.append(i)

    @classmethod
    def votecount(cls):
        pass


class Voters:
    @classmethod
    def add_candidate(cls, firstname, lastname):
        gender = 'Male'
        votes = 0  # till I find a better alternative
        validity = 'valid'
        cur.execute(
            '''INSERT INTO candidates(Firstname, Lastname, Gender, vote_count, validity) VALUES (?,?, ?,?,?)''',
            (firstname, lastname, gender, votes, validity))
        conn.commit()

    @classmethod
    def vote_candidate(cls):
        currow = 2
        Voters.voted_candidate = ctk.StringVar()
        can = cur.execute('''SELECT Firstname, Lastname FROM candidates WHERE validity='valid' ''').fetchall()
        j = 0
        for i in can:
            PageTwo.votersradio = ctk.CTkRadioButton(PageTwo.framevote, text=f"{i[0]} {i[1]}", value=i[0]
                                                     , variable=Voters.voted_candidate,
                                                     text_font=('Microsoft YaHei UI Light', 12))
            PageTwo.votersradio.grid(row=currow, column=0, sticky='w', pady=5, padx=10)

            currow += 1
            j += 1

        PageTwo.Vote = ctk.CTkButton(PageTwo.framevote, width=600,
                                     height=30, fg_color='#299bdd', text='cast', command=Voters.holding,
                                     text_color='white',
                                     bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        PageTwo.Vote.place(x=35, y=450)

    @classmethod
    def holding(cls):
        Adminpage.placeholder.destroy()
        na = username
        status = cur.execute('''SELECT Status FROM users WHERE Username=? ''', (na,)).fetchone()[0]
        if status == 'voted':
            PageTwo.Vote.configure(state=tkinter.DISABLED)
        else:
            PageTwo.Vote.configure(state=tkinter.NORMAL)
        cur.execute('''UPDATE users SET status='voted' WHERE Username=?''', (na,))
        tk.messagebox.showinfo('Vote Successful', 'Results Will Be Released Soon')
        fish = Voters.voted_candidate.get()
        print(fish)
        Voters.Votecount(fish)

    @classmethod
    def Votecount(cls, candidate):
        candidate = Voters.voted_candidate.get()
        cur.execute("UPDATE candidates SET vote_count=vote_count+1 WHERE Firstname=?", (candidate,))
        conn.commit()
        Voters.viewresult()

    @classmethod
    def show(cls):
        msg = 'candidates'
        c.send(msg.encode(FORMAT))
        can = pickle.loads(c.recv(SIZE))
        currow = 2
        for i in can:
            PageTwo.votersshow = ctk.CTkLabel(Adminpage.show, text=f"{i[0]}. {i[1]} {i[2]} {i[3]}",
                                              text_font=('Microsoft YaHei UI Light', 12))
            PageTwo.votersshow.grid(row=currow, column=1, sticky='w', pady=5, padx=10)
            currow += 1

    @classmethod
    def remove1(cls):
        for widgets in Adminpage.verify.winfo_children():
            widgets.destroy()
        Adminpage.need = ctk.CTkFrame(Adminpage.verify, width=200, height=235, corner_radius=20, border_width=2,
                                      border_color="#6960Ec")
        Adminpage.need.place(x=437, y=50)
        Adminpage.need.configure(fg_color='white')
        Adminpage.need.grid_propagate(False)
        Adminpage.label1 = ctk.CTkLabel(Adminpage.verify, text='Voter Verification',
                                        text_font=('Microsoft YaHei UI Light', 20, 'bold'))
        Adminpage.label1.grid(row=0, column=1, sticky='w', pady=5, padx=10)
        Adminpage.heading2 = tk.Label(Adminpage.need, text='Verify', fg='#299bdd', bg='white',
                                      font=('Microsoft YaHei UI Light', 12, 'bold')).grid(row=0, column=0, pady=(10, 0),
                                                                                          padx=(20, 0))

        Adminpage.index1 = tk.Label(Adminpage.need, text='Verify Candidate(Index)', fg='#299bdd', bg='white',
                                    font=('Microsoft YaHei UI Light', 8, 'bold'))
        Adminpage.index1.grid(row=1, column=0, sticky='w', pady=(5, 0), padx=(18, 0))
        Adminpage.indexentry1 = ctk.CTkEntry(Adminpage.need, width=160, height=30,
                                             placeholder_text='Candidate Index',
                                             border_color='black',
                                             border_width=1
                                             , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.indexentry1.grid(row=2, column=0, padx=(18, 0))

        Adminpage.deletecan1 = ctk.CTkButton(Adminpage.need, width=160, height=30, fg_color='#299bdd',
                                             text='Invalidate',
                                             text_color='white',
                                             command=Adminpage.delete_voter,
                                             bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.deletecan1.grid(row=3, column=0, pady=(15, 0), padx=(18, 0))

        Adminpage.confirm1 = ctk.CTkButton(Adminpage.need, width=160, height=30, fg_color='#299bdd',
                                           text='Verify Voter',
                                           text_color='white',
                                           bg_color='white',
                                           command=Adminpage.verify_voter,
                                           text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.confirm1.grid(row=4, column=0, pady=(15, 0), padx=(18, 0))
        Adminpage.ver()

    @classmethod
    def remove(cls):
        # Voters.candidate_votes.
        for widgets in Adminpage.show.winfo_children():
            widgets.destroy()
        Adminpage.delete = ctk.CTkFrame(Adminpage.show, width=200, height=235, corner_radius=20, border_width=2,
                                        border_color="#6960Ec")
        Adminpage.delete.place(x=437, y=50)
        Adminpage.delete.configure(fg_color='white')
        Adminpage.delete.grid_propagate(False)

        Adminpage.label = ctk.CTkLabel(Adminpage.show, text='All Candidates',
                                       text_font=('Microsoft YaHei UI Light', 20))
        Adminpage.label.grid(row=0, column=1, sticky='w', pady=5, padx=10)
        Adminpage.heading1 = tk.Label(Adminpage.delete, text='Confirmation', fg='#299bdd', bg='white',
                                      font=('Microsoft YaHei UI Light', 12, 'bold')).grid(row=0, column=0, pady=(10, 0),
                                                                                          padx=(20, 0))

        Adminpage.index = tk.Label(Adminpage.delete, text='Delete Candidate(index)', fg='#299bdd', bg='white',
                                   font=('Microsoft YaHei UI Light', 8, 'bold'))
        Adminpage.index.grid(row=1, column=0, sticky='w', pady=(5, 0), padx=(18, 0))
        Adminpage.indexentry = ctk.CTkEntry(Adminpage.delete, width=160, height=30,
                                            placeholder_text='Enter index eg 1,2',
                                            border_color='black',
                                            border_width=1
                                            , text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.indexentry.grid(row=2, column=0, padx=(18, 0))

        Adminpage.deletecan = ctk.CTkButton(Adminpage.delete, width=160, height=30, fg_color='#299bdd',
                                            text='Delete Candidate',
                                            text_color='white', command=Adminpage.delete1,
                                            bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.deletecan.grid(row=3, column=0, pady=(15, 0), padx=(18, 0))

        Adminpage.confirm = ctk.CTkButton(Adminpage.delete, width=160, height=30, fg_color='#299bdd',
                                          text='Confirm Candidates',
                                          text_color='white', command=Adminpage.cont,
                                          bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
        Adminpage.confirm.grid(row=4, column=0, pady=(15, 0), padx=(18, 0))

        Adminpage.showcand()

    @classmethod
    def viewresult(cls):
        currow = 2
        y = 1
        results = cur.execute('''SELECT Firstname, Lastname FROM candidates WHERE Validity='valid' ''').fetchall()
        cunt = cur.execute('''SELECT vote_count FROM candidates WHERE Validity='valid' ''').fetchall()
        print(results)
        for i in results:
            Adminpage.see = tk.Label(Adminpage.frameview, text=f"{y}. {i[0]} {i[1]}", bg='white',
                                     font=('Microsoft YaHei UI Light', 12))
            Adminpage.see.grid(row=currow, column=1, sticky='w', pady=5, padx=10)
            print(i)
            currow += 1
            y += 1

        seerow = 2
        for i in cunt:
            Adminpage.see = ctk.CTkLabel(Adminpage.frameview, text=f"{i[0]}",
                                         text_font=('Microsoft YaHei UI Light', 12))
            Adminpage.see.grid(row=seerow, column=2, sticky='w')
            print(i)
            seerow += 1


# ================================================I need a button for this function to show graph==========================================
"""
        PageTwo.Vote = ctk.CTkButton(PageTwo.framevote, width=600,
                                     height=30, fg_color='#299bdd', text='Show graph',
                                     text_color='white',
                                     bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
    def project():
    names = []
    votes = []
    for i in range(len(r)):
        data = r[i]
        names.append(data[0])
        votes.append(data[1])
        plt.title('Poll Result')
    plt.pie(votes, labels=names, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()
PageTwo.Vote = ctk.CTkButton(PageTwo.framevote, width=600,
                                     height=30, fg_color='#299bdd', text='cast', command=Voters.holding,
                                     text_color='white',
                                     bg_color='white', text_font=('Microsoft YaHei UI Light', 11, 'bold'))
Button(res, text='Project Results', command=project).grid(row=2 + i + 1, column=2)"""
# ================================================I'll complete the fixing later==========================================


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
