import tkinter as tk
import tkinter.ttk as ttk
from src.UnoClient import *
from tkinter.scrolledtext import ScrolledText


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

        self.wm_title("PyUno Client")
        # Main frame and config
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.geometry("220x100")

        # Configure button styling
        style = ttk.Style()
        style.configure("red.TButton", foreground="red")
        style.configure("blue.TButton", foreground="blue")
        style.configure("green.TButton", foreground="green")
        style.configure("yellow.TButton", foreground="yellow")
        style.configure("black.TButton", foreground="black")

        # Dictionary of frames in the app.
        self.frames = {}

        # Loop through the frame tuple (windows) and add it to the frames dictionary
        frame = ConnectWindow(parent=container, controller=self)
        self.frames[ConnectWindow] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        # Showing the connection window first.
        self.show_frame(ConnectWindow)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# This is the connection window used to establish a connection to the server.
class ConnectWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Controller references the MainApp class. We use this to access its instance variables.
        self.controller = controller
        self.parent = parent

        # Relevant labels, buttons, and entries.
        name_label = ttk.Label(self, text="Name")
        self.name_entry = ttk.Entry(self)
        host_label = ttk.Label(self, text="Host: ")
        self.host_entry = ttk.Entry(self)
        port_label = ttk.Label(self, text="Port Number: ")
        self.port_entry = ttk.Entry(self)
        connect_button = ttk.Button(self, text="Connect", command=self.connect)
        # Adding all controls to the grid of the window.
        name_label.grid(row=0, sticky='e')
        self.name_entry.grid(row=0, column=1)
        host_label.grid(row=1, sticky='e')
        self.host_entry.grid(row=1, column=1)
        port_label.grid(row=2, sticky='e')
        self.port_entry.grid(row=2, column=1)
        connect_button.grid(row=3, column=1)

        self.insert_defaults()

    # Connects to the host and translates to the game window.
    def connect(self):
        self.controller.client_sock = create_socket(self.host_entry.get(), int(self.port_entry.get()))
        self.controller.player = join_game(self.name_entry.get(), self.controller.client_sock)
        self.controller.player['hand'] = receive_hand(self.controller.client_sock)
        print(self.controller.player)

        frame = GameWindow(parent=self.parent, controller=self.controller)
        self.controller.frames[GameWindow] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.controller.show_frame(GameWindow)

        self.controller.geometry("600x400")

    # Insert defaults to entry controls for quick testing.
    def insert_defaults(self):
        self.name_entry.insert('end', 'testplayer')
        self.host_entry.insert('end', 'localhost')
        self.port_entry.insert('end', 2121)


class GameWindow(tk.Frame):
    def __init__(self, parent, controller, ):
        tk.Frame.__init__(self, parent)
        # Controller references the MainApp class. We use this to access its instance variables.
        self.controller = controller

        self.grid_rowconfigure(1)
        self.grid_columnconfigure(1, weight=1)

        title_label = ttk.Label(self, text="PyUno")
        card_label = ttk.Label(self, text="Cards in your hand")
        chat_label = ttk.Label(self, text="Chat")
        chat_area = ScrolledText(self)
        title_label.grid(row=0, column=1)
        card_label.grid(row=1, column=1)
        self.generate_cardbuttons()
        chat_label.grid(row=3, column=1)
        chat_area.grid(row=4, column=1)

    # Generates the initial hand as buttons.
    def generate_cardbuttons(self):
        # Accessing player's hand
        hand = self.controller.player['hand']
        # iterator to determine which column to place the button in within the grid
        current_col = 0
        # Button array needs its own frame
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=1)
        # Array of buttons for purposes of mutation
        buttons = []
        # Iterate through cards in hand and create a new button.
        for card in hand:
            # Initialize Button control
            card_button = ttk.Button(button_frame, text=card['type'], style="%s.TButton" % card['color'], width=5,
                                    command=lambda button_array=buttons, button_index=current_col, current_card=card:
                                    self.button_action(button_array, button_index, current_card))
            # Append button control to array
            buttons.append(card_button)
            # Add button to grid dynamically
            card_button.grid(row=0, column=current_col, sticky='ew')
            # Increment for next button
            current_col += 1


    # Determine which action to send to the server depending on which button is clicked.
    def button_action(self, buttons, button_index, card):
        buttons[button_index].destroy()


client_app = MainApp()
client_app.mainloop()






