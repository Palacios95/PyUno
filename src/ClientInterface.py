from tkinter import *
from src.UnoClient import *
root = Tk()

root.geometry("170x70")
name_label = Label(root, text="Name")
name_entry = Entry(root)
client_sock = create_socket('localhost', 2121)


def connect():
    player = join_game(name_entry.get(), client_sock)
    player['hand'] = receive_hand(client_sock)
    print(player)

connect_button = Button(root, text="Connect", command=connect)
name_label.grid(row=0, sticky=E)
name_entry.grid(row=0, column=1)
connect_button.grid(row=1, column=1)

root.mainloop()



