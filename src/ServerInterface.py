import tkinter as tk
import tkinter.ttk as ttk
from src.UnoServer import *

RECV_BUFFER = 1024


# Main part of the app. Handles transition from the connection window to the game window and stores the player
# dictionary as well as the socket to connect to the server.
# This code was heavily influenced by: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# since I am new to tkinter.
class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Initialize socket and player vars. We need these for the game window and connection window.
        self.server_sock = {}
        self.players = []
        self.deck = {}

        self.wm_title("PyUno Server")
        # Main frame and config
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary of frames in the app.
        self.frames = {}

        # Loop through the frame tuple (windows) and add it to the frames dictionary
        for F in (ServerWindow, PingWindow):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Showing the connection window first.
        self.show_frame("ServerWindow")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class ServerWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Controller references the main app. Used to access its instance variables.
        self.controller = controller

        # Controls relevant to the server window.
        port_label = ttk.Label(self, text="Port Number: ")
        self.port_entry = ttk.Entry(self)
        playerno_label = ttk.Label(self, text="Number of players: ")
        self.playerno_entry = ttk.Entry(self)
        # Adding relevant controls to grid.
        port_label.grid(row=0, sticky='e')
        self.port_entry.grid(row=0, column=1)
        playerno_label.grid(row=1, sticky='e')
        self.playerno_entry.grid(row=1, column=1)
        start_button = ttk.Button(self, text="Start server", command=self.start)
        start_button.grid(row=2, column=1)

        self.insert_defaults()

    # Start accepting players into the game
    def start(self):
        server_sock = create_socket(int(self.port_entry.get()))
        accept_players(server_sock, self.controller.players, int(self.playerno_entry.get()))
        print(self.controller.players)

    # Insert defaults to entry controls for quick testing.
    def insert_defaults(self):
        self.port_entry.insert('end', 2121)
        self.playerno_entry.insert('end', 1)


class PingWindow(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="PyUno")
        label.pack(side="top", fill="x", pady=10)


server_app = MainApp()
server_app.mainloop()


