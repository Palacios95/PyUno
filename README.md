# PyUno

This is an implementation of the game Uno in Python 3.6 using Tkinter for a GUI as well as TCP and UDP sockets for client/server communication and pings respectively.

# Video
First 5 minutes is a demonstration of the game. The rest of it is an in-depth code review:
https://www.youtube.com/watch?v=97EuVmlbrT8&t=359s

# Usage
  - Run the program by running the ServerInterface.py script. Specify the port numbers for the Server, Chat, and Ping. Finally specify the number of players in the game. Click on "Start Server" to start listening for client connections. (Defaults work fine for testing if you are running everything on the same computer)
  - Next, run the ClientInterface.py and specify the name of the player. Specify the port numbers (same port numbers as server) and the hostname (leave as localhost if running everything on the same computer). Finally, click join game.
  - All ClientInterfaces will say "Waiting for players" until the number of players specified on the server has been reached, at which point the game will start. Keep running ClientInterface.py and join under a different player name until the number of players specified by the server has been reached.
# Game Rules
 - The game rules are to match the card shown with a card in your hand that either has the same color or the same type (0,1,Skip, etc.)
 - Wild cards are special because they can be any card color. When you select a wild card, buttons will appear below for you to select the card color you want.
 - For more detailed game rules, please refer to: http://www.unorules.com/

