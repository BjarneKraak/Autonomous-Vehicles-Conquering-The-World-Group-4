# gui pack probeersel

''' A GUI for the application '''

import tkinter as tk


class MemeSimGUI():
    ''' Class that handles all GUI related activity. On instantiation, provide a reference to the tkinter root. '''

    def __init__(self, master):

        # parameters for spacing, borderwidth...
        x=5
        bwidth=17
        # remember the tkinter root
        self._master = master

        # set window title and size
        self._master.title("Welcome to the MemeSimGUI")
        self._master.geometry('900x600')

        # Creation of all frames
        self._frame = tk.Frame(self._master)
        self._frame.pack(expand=tk.YES, fill=tk.BOTH)

        # create the option to create smaller frames within the master frame (for meme part)
        self.bottom_frame = tk.Frame(self._frame)
        self.bottom_frame.pack(side=tk.TOP, expand=tk.YES)

        # create a smaller Frame within the master frame (for meme part)
        self.meme_frame = tk.Frame(self.bottom_frame)
        self.meme_frame.pack(side=tk.TOP, expand=tk.NO, fill=tk.Y, ipadx=5, ipady=5)

        #Frame for all buttons
        self.btn = tk.Frame(self._frame)
        self.btn.pack(side=tk.TOP, expand=tk.NO)

        #coomands frame
        self.commands = tk.Frame(self.btn, borderwidth=bwidth)
        self.commands.pack(side=tk.LEFT, expand=tk.YES, anchor=tk.N)

        #continents frame
        self.cont_f = tk.Frame(self.btn, borderwidth=bwidth)
        self.cont_f.pack(  side=tk.LEFT, expand=tk.YES, anchor=tk.N)

        #Frame for Europeans cities
        self.europe_f = tk.Frame(self.btn, borderwidth=bwidth)
        self.europe_f.pack(  side=tk.LEFT, expand=tk.YES, anchor=tk.N)

        #Frame for Afrikans cities
        self.africa_f = tk.Frame(self.btn, borderwidth=bwidth)
        self.africa_f.pack(  side=tk.LEFT, expand=tk.YES, anchor=tk.N)

        #Frame for Americans cities
        self.america_f = tk.Frame(self.btn, borderwidth=bwidth)
        self.america_f.pack(side=tk.LEFT, expand=tk.YES, anchor=tk.N)


        #Creation of all buttons

        self.btn = tk.Button(self.commands, text="Robot query",command= self.rqC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn= tk.Button(self.commands, text="Market query",  command= self.mqC, width=13)
        self.btn.pack(side=tk.TOP,  pady=x)


        self.btn = tk.Button(self.commands, text="Interview person", command= self.mqC,width=13)
        self.btn.pack(side=tk.TOP,  pady=x)


        self.btn= tk.Button(self.commands, text="Process interview", command= self.ipC, width=13)
        self.btn.pack(side=tk.TOP,  pady=x)


        self.btn = tk.Button(self.commands, text="Test meme", command= self.piC, width=13)
        self.btn.pack(side=tk.TOP,  pady=x)

        self.btn = tk.Button(self.commands, text="Prepare campaign",  command= self.tmC, width=13)
        self.btn.pack(side=tk.TOP,  pady=x)


        self.btn = tk.Button(self.commands, text="Launch campaign",  command= self.pcC, width=13)
        self.btn.pack(side=tk.TOP,  pady=x)


        self.btn = tk.Button(self.commands, text="Check account", command= self.lcC, width=13)
        self.btn.pack(side=tk.TOP,  pady=x)


        self.btn = tk.Button(self.commands, text="Debug",  command= self.dbC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)

        self.btn = tk.Button(self.commands, text="Lab 4", command= self.lab4C, width=13)
        self.btn.pack(side=tk.TOP,  pady=x)


        self.btn = tk.Button(self.cont_f, text="Europe", command= self.eurC,  width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.cont_f, text="Africa",  command= self.afrC,  width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.cont_f, text="America",  command= self.ameC,  width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.cont_f, text="Labland",  command= self.labC,  width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.europe_f, text="Eindhoven",  command= self.einC,  width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.europe_f, text="London", command= self.lonC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.europe_f, text="Madrid",  command= self.madC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.europe_f, text="Milan",  command= self.milC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.africa_f, text="Johannesburg",  command= self.johC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.africa_f, text="Lagos",  command= self.lagC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.africa_f, text="Khartoum", command= self.khaC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.africa_f, text="Cairo",  command= self.caiC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.america_f, text="Washington", command= self.wasC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn= tk.Button(self.america_f, text="Bogota",  command= self.bogC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)

        self.btn = tk.Button(self.america_f, text="Atlanta",  command= self.atlC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)


        self.btn = tk.Button(self.america_f, text="Lima",  command= self.limC, width=13)
        self.btn.pack(side=tk.TOP, pady=x)




        # create the GUI elements

        # a text label with a meme genome
        self._memelbl = tk.Label(self.meme_frame, text="A meme:")
        # 'pack' determines the layout in the window. Google 'tkinter pack' for more info...
        self._memelbl.pack(fill=tk.X, padx=10, pady=10)


        self._robot_pos_txt = tk.Text(self.meme_frame, height=5)
        self._robot_pos_txt.insert(tk.INSERT, "Robot Positions:\n\n\n\n")
        self._robot_pos_txt.pack(side=tk.TOP,fill=tk.X)

        # a label for the account balance
        self._balance_lbl = tk.Label(self.meme_frame, text="<value>", anchor='w')
        self._balance_lbl.pack(side=tk.TOP, fill=tk.X)

        # a button to close the GUI
        self._closebtn = tk.Button(self.meme_frame, text="Close", command=self.close)
        self._closebtn.pack(side=tk.TOP, fill=tk.X)

        # organize the frame layout
        self._frame.pack(fill=tk.X)

        # respond to window close event by calling the function '_on_closing'
        self._master.protocol("WM_DELETE_WINDOW", self.close)
        # closing state, will be set to True when the window is being closed
        self.is_closing = False


    def eur(self, f):
        self.eur = f

    def eurC(self):
        if not self.eur is None:
            self.eur()

    def afr(self, f):
        self.afr = f

    def afrC(self):
        if not self.afr is None:
            self.afr()

    def ame(self, f):
        self.ame = f

    def ameC(self):
        if not self.ame is None:
            self.ame()

    def lab(self, f):
        self.lab = f

    def labC(self):
        if not self.lab is None:
            self.lab()

    def ein(self, f):
        self.ein = f

    def einC(self):
        if not self.ein is None:
            self.ein()

    def lon(self, f):
        self.lon= f

    def lonC(self):
        if not self.lon is None:
            self.lon()

    def mad(self, f):
        self.mad = f

    def madC(self):
        if not self.mad is None:
            self.mad()

    def mil(self, f):
        self.mil = f

    def milC(self):
        if not self.mil is None:
            self.mil()

    def joh(self, f):
        self.joh = f

    def johC(self):
        if not self.joh is None:
            self.joh()

    def lag(self, f):
        self.lag = f

    def lagC(self):
        if not self.lag is None:
            self.lag()

    def kha(self, f):
        self.kha = f

    def khaC(self):
        if not self.kha is None:
            self.kha()

    def cai(self, f):
        self.cai = f

    def caiC(self):
        if not self.cai is None:
            self.cai()

    def was(self, f):
        self.was = f

    def wasC(self):
        if not self.was is None:
            self.was()

    def bog(self, f):
        self.bog = f

    def bogC(self):
        if not self.bog is None:
            self.bog()

    def lim(self, f):
        self.lim = f

    def limC(self):
        if not self.lim is None:
            self.lim()

    def atl(self, f):
        self.atl = f

    def atlC(self):
        if not self.atl is None:
            self.atl()

    def lab4(self, f):
        self.lab4 = f

    def lab4C(self):
        if not self.lab4 is None:
            self.lab4()

    def rq(self, f):
        self.rq = f

    def rqC(self):
        if not self.rq is None:
            self.rq()

    def mq(self, f):
        self.mq = f


    def mqC(self):
        if not self.mq is None:
            self.mq()

    def ip(self, f):
        self.ip = f


    def ipC(self):
        if not self.ip is None:
            self.ip()


    def pi(self, f):
        self.pi = f


    def piC(self):
        if not self.pi is None:
            self.pi()


    def tm(self, f):
        self.tm = f


    def tmC(self):
        if not self.tm is None:
            self.tm()


    def pc(self, f):
        self.pc = f


    def pcC(self):
        if not self.pc is None:
            self.pc()


    def lc(self, f):
        self.lc = f


    def lcC(self):
        if not self.lc is None:
            self.lc()


    def db(self, f):
        self.db = f


    def dbC(self):
        if not self.db is None:
            self.db()


    def close(self):
        ''' Close the window. '''
        self.is_closing = True

    def show_meme(self, meme):
        ''' Show a meme genome in the GUI '''

        # adapt the text of the text label
        self._memelbl.configure(text=meme.genomestring())

    def show_location(self, id, x, y, phi):
        ''' show information about a robot position and orientation in the text box '''
        # determine the text to show
        newtext = "Robot: {0:d} at ({1:.1f}, {2:.1f}), {3:.1f} degrees\n".format(id, x, y, phi/3.14159265*180)
        # modify the line corresponding to the robot in the text
        self._robot_pos_txt.replace("{0}.0".format((id-1)%3 + 2), "{0}.0".format((id-1)%3 + 3), newtext)

    def show_balance(self, b):
        ''' Show the account balance on the GUI. '''
        self._balance_lbl.configure(text="Bank account: {0:.2f} euro.".format(float(b)))
