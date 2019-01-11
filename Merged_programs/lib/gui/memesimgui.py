''' A GUI for the application '''

import tkinter as tk


class MemeSimGUI():
    ''' Class that handles all GUI related activity. On instantiation, provide a reference to the tkinter root. '''

    def __init__(self, master):
        
        # remember the tkinter root
        self._master = master

        # set window title and size
        self._master.title("Welcome to the MemeSimGUI")
        self._master.geometry('950x700')

        # create a 'Frame' to hold the GUI elements
        self._frame = tk.Frame(self._master)




        # create the option to create smaller frames within the master frame (for meme part)
        self.bottom_frame = tk.Frame(self._frame)
        self.bottom_frame.pack(side=tk.BOTTOM, expand=tk.YES)

        # create a smaller Frame within the master frame (for meme part)
        self.meme_frame = tk.Frame(self.bottom_frame)
        self.meme_frame.pack(side=tk.TOP, expand=tk.NO, fill=tk.Y, ipadx=5, ipady=5)


        self.f1_frame = tk.Frame(self.meme_frame)
        self.f1_frame.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.Y)

        
        # create the GUI elements
        
        # a text label with a meme genome
        self._memelbl = tk.Label(self._frame, text="A meme:")
        # 'pack' determines the layout in the window. Google 'tkinter pack' for more info...
        self._memelbl.pack(fill=tk.X, padx=10, pady=10)




        # a multi-line text box
        self._robot_pos_txt = tk.Text(self._frame, height=5)
        self._robot_pos_txt.insert(tk.INSERT, "Robot Positions:\n\n\n\n")
        self._robot_pos_txt.pack(fill=tk.X, padx=10, pady=10) 

        # a label for the account balance
        self._balance_lbl = tk.Label(self._frame, text="<value>", anchor='w')
        self._balance_lbl.pack(fill=tk.X, padx=10, pady=10)

        x1r=100
        x1l=750

        x2r=650
        x2l=100
        
        #europa
        
        self.memebtn = tk.Button(self.f1_frame, text="Europe", fg = "red", bg = "black", command= self.dbC)
        self.memebtn["width"] = 15
        self.memebtn.pack(anchor=tk.N)

         #europa
        
        self.memebtn = tk.Button(self.f1_frame, text="Afrikaa", fg = "red", bg = "black", command= self.dbC)
        self.memebtn["width"] = 15
        self.memebtn.pack()


         #europa
        
        self.memebtn = tk.Button(self.f1_frame, text="America", fg = "red", bg = "black", command= self.dbC)
        self.memebtn["width"] = 15
        self.memebtn.pack()


         #europa
        
        self.memebtn = tk.Button(self.f1_frame, text="Oceania", fg = "red", bg = "black", command= self.dbC)
        self.memebtn["width"] = 15
        self.memebtn.pack()
        
        
        # a simple button to click
        self._memebtn = tk.Button(self._frame, text="Request query", command= self.rqC)
        self._memebtn.pack(fill=tk.X, padx=(x1r,x1l), pady=10)
        # a simple button to click
        self._memebtn = tk.Button(self._frame, text="Market query", command= self.mqC)
        self._memebtn.pack(fill=tk.X, padx=(x1r,x1l), pady=10)

        # a simple button to click
        self._memebtn = tk.Button(self._frame, text="Interview person", command= self.ipC)
        self._memebtn.pack(fill=tk.X, padx=(x1r,x1l), pady=10)

        # a simple button to click
        self._memebtn = tk.Button(self._frame, text="Process interview", command= self.piC)
        self._memebtn.pack(fill=tk.X, padx=(x1r,x1l), pady=10)

          # a simple button to click
        self._memebtn = tk.Button(self._frame, text="Test meme", command= self.tmC)
        self._memebtn.pack(fill=tk.X, padx=(x1r,x1l), pady=10)

          # a simple button to click
        self._memebtn = tk.Button(self._frame, text="Prepare campaign", command= self.pcC)
        self._memebtn.pack(fill=tk.X, padx=(x1r,x1l), pady=10)

          # a simple button to click
        self._memebtn = tk.Button(self._frame, text="Launch campaign", command= self.lcC)
        self._memebtn.pack(fill=tk.X, padx=(x1r,x1l), pady=10)

          # a simple button to click
        self._memebtn = tk.Button(self._frame, text="Reset Money", command= self.dbC)
        self._memebtn.pack(fill=tk.X, padx=(x1r,x1l), pady=10)

        # a button to close the GUI
        self._closebtn = tk.Button(self._frame, text="Close", command=self.close)
        self._closebtn.pack(fill=tk.X, padx=(x1r,x1l), pady=10)
        

        # organize the frame layout
        self._frame.pack(fill=tk.X)

        # respond to window close event by calling the function '_on_closing'
        self._master.protocol("WM_DELETE_WINDOW", self.close)
        # closing state, will be set to True when the window is being closed
        self.is_closing = False

        # create instance variable to hold the button callback function
        self.button_callback = None


    def rq(self, f):
        ''' Sets the callback function (the function to be executed) for the GUI button. '''
        self.rq = f

    def rqC(self):
        # if the user want us to do something when the button is clicked, do it 
        if not self.rq is None:
            self.rq()

    def mq(self, f):
        ''' Sets the callback function (the function to be executed) for the GUI button. '''
        self.mq = f


    def mqC(self):
        # if the user want us to do something when the button is clicked, do it 
        if not self.mq is None:
            self.mq()

    def ip(self, f):
        ''' Sets the callback function (the function to be executed) for the GUI button. '''
        self.ip = f


    def ipC(self):
        # if the user want us to do something when the button is clicked, do it 
        if not self.ip is None:
            self.ip()

    
    def pi(self, f):
        ''' Sets the callback function (the function to be executed) for the GUI button. '''
        self.pi = f


    def piC(self):
        # if the user want us to do something when the button is clicked, do it 
        if not self.pi is None:
            self.pi()

    
    def tm(self, f):
        ''' Sets the callback function (the function to be executed) for the GUI button. '''
        self.tm = f


    def tmC(self):
        # if the user want us to do something when the button is clicked, do it 
        if not self.tm is None:
            self.tm()

    
    def pc(self, f):
        ''' Sets the callback function (the function to be executed) for the GUI button. '''
        self.pc = f


    def pcC(self):
        # if the user want us to do something when the button is clicked, do it 
        if not self.pc is None:
            self.pc()

    
    def lc(self, f):
        ''' Sets the callback function (the function to be executed) for the GUI button. '''
        self.lc = f


    def lcC(self):
        # if the user want us to do something when the button is clicked, do it 
        if not self.lc is None:
            self.lc()

    
    def db(self, f):
       
        self.db = f


    def dbC(self):
        # if the user want us to do something when the button is clicked, do it 
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
