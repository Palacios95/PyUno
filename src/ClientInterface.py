import tkinter as tk
import tkinter.ttk as ttk
from src.UnoClient import UnoClient
from src.ChatClient import ChatClient
from src.PingClient import PingClient
from tkinter.scrolledtext import ScrolledText
import threading
import tkinter.messagebox as messagebox

# Main part of the app. Handles transition from the connection window to the game window and stores the player
# dictionary as well as the socket to connect to the server.
# This code was heavily influenced by: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# since I am new to tkinter.
class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.uno_client = UnoClient()
        self.chat_client = ChatClient()
        self.ping_client = PingClient()
        self.hostname = ''
        self.port_num = 0
        self.chatport_num = 0

        self.wm_title("PyUno Client")
        # Main frame and config
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.geometry("270x140")

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
        self.chatport_label = ttk.Label(self, text="Chat Port Number: ")
        self.chatport_entry = ttk.Entry(self)
        self.pingport_label = ttk.Label(self, text="Ping Port Number: ")
        self.pingport_entry = ttk.Entry(self)
        self.connect_button = ttk.Button(self, text="Connect", command=self.connect)
        # Adding all controls to the grid of the window.
        name_label.grid(row=0, sticky='e')
        self.name_entry.grid(row=0, column=1)
        host_label.grid(row=1, sticky='e')
        self.host_entry.grid(row=1, column=1)
        port_label.grid(row=2, sticky='e')
        self.port_entry.grid(row=2, column=1)
        self.chatport_label.grid(row=3, column=0)
        self.chatport_entry.grid(row=3, column=1)
        self.pingport_label.grid(row=4, column=0)
        self.pingport_entry.grid(row=4, column=1)
        self.connect_button.grid(row=5, column=1)

        self.insert_defaults()

    # Connects to the host and translates to the game window.
    def connect(self):
        uno_client = self.controller.uno_client
        chat_client = self.controller.chat_client
        ping_client = self.controller.ping_client
        self.connect_button['text'] = 'Waiting for other players...'
        self.update()
        self.controller.hostname = self.host_entry.get()
        self.controller.port_num = int(self.port_entry.get())
        uno_client.create_socket(self.controller.hostname, self.controller.port_num)
        uno_client.join_game(self.name_entry.get())
        uno_client.start_game()
        print(uno_client.player)

        self.controller.chatport_num = int(self.chatport_entry.get())
        chat_client.start_client(self.controller.hostname, self.controller.chatport_num)

        ping_client.start_client(self.controller.hostname, int(self.pingport_entry.get()))

        frame = GameWindow(parent=self.parent, controller=self.controller)
        self.controller.frames[GameWindow] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.controller.show_frame(GameWindow)

        self.controller.geometry("600x400")
        self.update()

    # Insert defaults to entry controls for quick testing.
    def insert_defaults(self):
        self.name_entry.insert('end', 'testplayer')
        self.host_entry.insert('end', 'localhost')
        self.port_entry.insert('end', 2121)
        self.chatport_entry.insert('end', 2122)
        self.pingport_entry.insert('end', 2123)


class GameWindow(tk.Frame):
    def __init__(self, parent, controller, ):
        tk.Frame.__init__(self, parent)
        # Controller references the MainApp class. We use this to access its instance variables.
        self.controller = controller
        # Array of button handles
        self.buttons = []
        # iterator to determine which column to place the button in within the grid
        self.current_col = 0
        self.chosen_wildcard = {}

        self.grid_rowconfigure(1)
        self.grid_columnconfigure(1, weight=1)

        title_label = ttk.Label(self, text="PyUno")
        self.turn_label = ttk.Label(self, text="turn")
        self.currentcard_label = ttk.Label(self, text='Current card')
        self.currentcard_frame = ttk.Frame(self)
        card_label = ttk.Label(self, text="Cards in your hand")
        chat_label = ttk.Label(self, text="Chat")
        self.chat_area = ScrolledText(self, height=10)
        chat_frame = ttk.Frame(self)
        sendchat_label = ttk.Label(chat_frame, text='Send Message:')
        self.sendchat_entry = ttk.Entry(chat_frame, text='', width=50)
        sendchat_button = ttk.Button(chat_frame, text='Send message', command=self.send_message)
        ping_button = ttk.Button(self, text='Ping server',
                                 command=lambda player_name=self.controller.uno_client.player['player_name']:
                                 self.controller.ping_client.send_ping(player_name))
        title_label.grid(row=0, column=1)
        self.turn_label.grid(row=1, column=1)
        self.currentcard_label.grid(row=2, column=1)
        self.currentcard_frame.grid(row=3, column=1)
        card_label.grid(row=4, column=1)
        # Button array needs its own frame
        self.button_frame = ttk.Frame(self)
        self.wildcolor_frame = ttk.Frame(self)
        self.skipturn_button = ttk.Button(self, text='Skip your turn', command=self.skip_turn)
        self.buttons.append(self.skipturn_button)
        self.button_frame.grid(row=5, column=1)
        self.skipturn_button.grid(row=6, column=1)
        chat_label.grid(row=8, column=1)
        self.chat_area.grid(row=9, column=1)
        chat_frame.grid(row=10, column=1)
        ping_button.grid(row=11, column=1)


        #Chat stuff is in its own frame
        sendchat_label.grid(row=0, column=0)
        self.sendchat_entry.grid(row=0, column=1)
        sendchat_button.grid(row=0, column=2)

        messagereceive_thread = threading.Thread(target=self.receive_messages)
        messagereceive_thread.start()

        self.show_currentcard()

        self.generate_cardbuttons()
        self.generate_wildcolorbuttons()

        self.init_turn()
        self.change_cardstate()

        if not self.controller.uno_client.your_turn:
            wait_thread = threading.Thread(target=self.done_wait)
            wait_thread.start()

    # Generates the initial hand as buttons.
    def generate_cardbuttons(self):
        # Accessing player's hand
        hand = self.controller.uno_client.player['hand']

        # Iterate through cards in hand and create a new button.
        for card in hand:
            # Initialize Button control
            card_button = ttk.Button(self.button_frame, text=card['type'], style="%s.TButton" % card['color'], width=10,
                                    command=lambda current_card=card: self.button_action(current_card))
            # Append button control to array
            self.buttons.append(card_button)
            # Add button to grid dynamically
            card_button.grid(row=0, column=self.current_col, sticky='ew')
            # Increment for next button
            self.current_col += 1

    # Determine which action to send to the server depending on which button is clicked.
    def button_action(self, card):
        uno_client = self.controller.uno_client

        if card['type'] == 'Wild' or card['type'] == 'Wild 4':
            self.chosen_wildcard = card
            self.wildcolor_frame.grid(row=7, column=1)

        else:
            if card['type'] == uno_client.current_card['type'] or card['color'] == uno_client.current_card['color']:

                uno_client.send_card(card)
                button = self.get_button(card)
                button.destroy()
                self.buttons.remove(button)

                self.next_turn()
            else:
                messagebox.showinfo("Incorrect match", "Incorrect card match! Please match by card type or color. "
                                    + "If you can't, skip your turn")


    def skip_turn(self):
        uno_client = self.controller.uno_client
        skipturn_card = {'type': 'skip turn'}
        uno_client.player['hand'].append(skipturn_card)
        uno_client.send_card(skipturn_card)

        self.next_turn()

    def next_turn(self):
        uno_client = self.controller.uno_client
        self.turn_label['text'] = 'Wait for your turn'
        uno_client.your_turn = False
        self.change_cardstate()

        self.update()

        uno_client.wait_turndata()
        if not uno_client.win:
            self.show_currentcard()
            self.add_draw()
            self.turn_label['text'] = 'Your turn'
            uno_client.your_turn = True
            self.change_cardstate()
        else:
            messagebox.showinfo("Game ended", "%s wins!" % uno_client.win)

    def get_button(self, card):
        for button in self.buttons:
            if button['text'] == card['type'] and button['style'].startswith(card['color']):
                return button

    def show_currentcard(self):
        current_card = self.controller.uno_client.current_card
        card_button = ttk.Button(self.currentcard_frame, text=current_card['type'],
                                 style="%s.TButton" % current_card['color'], width=10)
        card_button.grid(row=0, column=0, sticky='ew')

    def add_draw(self):
        uno_client = self.controller.uno_client
        cards = uno_client.cards_drawn
        for card in cards:
            card_button = ttk.Button(self.button_frame, text=card['type'], style="%s.TButton" % card['color'], width=10,
                                     command=lambda current_card=card: self.button_action(current_card))
            # Append button control to array
            self.buttons.append(card_button)
            # Add button to grid dynamically
            card_button.grid(row=0, column=self.current_col, sticky='ew')
            # Increment for next button
            self.current_col += 1

    def init_turn(self):
        uno_client = self.controller.uno_client
        player = uno_client.player
        turn = uno_client.turn
        if player['player_name'] == turn:
            self.turn_label['text'] = 'Your turn'
            uno_client.your_turn = True
        else:
            self.turn_label['text'] = 'Wait for your turn'

    def change_cardstate(self):
        state = 'normal' if self.controller.uno_client.your_turn else 'disabled'
        for button in self.buttons:
            button['state'] = state

    def done_wait(self):
        self.controller.uno_client.wait_turndata()
        self.turn_label['text'] = 'Your turn'
        self.controller.uno_client.your_turn = True
        self.change_cardstate()
        self.show_currentcard()
        self.add_draw()

    def receive_messages(self):
        chat_client = self.controller.chat_client
        while True:
            messages = chat_client.receive_messages()
            self.chat_area.delete('1.0', 'end')
            for message in messages:
                self.chat_area.insert('end', message)

    def send_message(self):
        player_name = self.controller.uno_client.player['player_name']
        self.controller.chat_client.send_message(player_name, self.sendchat_entry.get())
        self.sendchat_entry.delete('0', 'end')

    def generate_wildcolorbuttons(self):
        color_label = ttk.Label(self.wildcolor_frame, text='Choose wild card color:')
        color_label.grid(row=0, column=0)
        colors = ['yellow', 'green', 'red', 'blue']
        current_col = 1
        for color in colors:
            color_button = ttk.Button(self.wildcolor_frame, text=color, style="%s.TButton" % color, width=10,
                                      command=lambda wild_color=color: self.determine_wildcolor(wild_color))
            # Add button to grid dynamically
            color_button.grid(row=0, column=current_col)
            # Increment for next button
            current_col += 1
        print(self.wildcolor_frame)

    def determine_wildcolor(self, color):
        uno_client = self.controller.uno_client
        uno_client.change_cardcolor(self.chosen_wildcard, color)
        self.change_wildcard_buttoncolor(self.chosen_wildcard)
        self.wildcolor_frame.grid_remove()

        uno_client.send_card(self.chosen_wildcard)
        button = self.get_button(self.chosen_wildcard)
        button.destroy()
        self.buttons.remove(button)
        self.next_turn()

    def change_wildcard_buttoncolor(self, wild_card):
        for button in self.buttons:
            if button['text'] == wild_card['type']:
                button['style'] = '%s.TButton' % wild_card['color']


client_app = MainApp()
client_app.mainloop()






