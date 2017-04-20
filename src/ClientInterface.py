import tkinter as tk
from src.UnoClient import *


# Main part of the app. Handles transition from the connection window to the game window and stores the player
# dictionary as well as the socket to connect to the server.
# This code was heavily influenced by: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# since I am new to tkinter.
class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Initialize socket and player vars. We need these for the game window and connection window.
        self.client_sock = {}
        self.player = {}

        # Main frame and config
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary of frames in the app.
        self.frames = {}

        # Loop through the frame tuple (windows) and add it to the frames dictionary
        for F in (ConnectWindow, GameWindow):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Showing the connection window first.
        self.show_frame("ConnectWindow")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# This is the connection window used to establish a connection to the server.
class ConnectWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Controller references the MainApp class. We use this to access its instance variables.
        self.controller = controller

        # Relevant labels, buttons, and entries.
        name_label = tk.Label(self, text="Name")
        self.name_entry = tk.Entry(self)
        host_label = tk.Label(self, text="Host: ")
        self.host_entry = tk.Entry(self)
        port_label = tk.Label(self, text="Port Number: ")
        self.port_entry = tk.Entry(self)
        connect_button = tk.Button(self, text="Connect", command=self.connect)
        # Adding all controls to the grid of the window.
        name_label.grid(row=0, sticky='e')
        self.name_entry.grid(row=0, column=1)
        host_label.grid(row=1, sticky='e')
        self.host_entry.grid(row=1, column=1)
        port_label.grid(row=2, sticky='e')
        self.port_entry.grid(row=2, column=1)
        connect_button.grid(row=3, column=1)

    # Connects to the host and translates to the game window.
    def connect(self):
        self.controller.client_sock = create_socket(self.host_entry.get(), int(self.port_entry.get()))
        self.controller.player = join_game(self.name_entry.get(), self.controller.client_sock)
        self.controller.player['hand'] = receive_hand(self.controller.client_sock)
        print(self.controller.player)
        self.controller.show_frame("GameWindow")


class GameWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="PyUno")
        label.pack(side="top", fill="x", pady=10)


client_app = MainApp()
client_app.mainloop()






