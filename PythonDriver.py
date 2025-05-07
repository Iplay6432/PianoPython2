import socket
from Main import Main
import pyglet
import threading
import time as t
import os
game = Main()
host = "127.0.0.1"
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
b = None
def action(func):
    pyglet.clock.schedule_once(lambda dt: func(), 0)
    
def send_message(s, message):
    msg_bytes = message.encode('utf-8')
    s.sendall(len(msg_bytes).to_bytes(2, 'big'))
    s.sendall(msg_bytes)
    
def receive_message(s):
    length_bytes = s.recv(2)
    if not length_bytes:
        return None
    msg_length = int.from_bytes(length_bytes, 'big')
    data = s.recv(msg_length).decode('utf-8')
    return data
def _server():
    m = receive_message(s)
    
    if m == "0":
        action(game.show)
        while True:
            t.sleep(0.01)
            if game.getDone():
                action(game.hide)
                send_message(s, "0")
                t.sleep(0.01)
                _server()
    if m == "1":
        action(game.freeplay)
        while True:
            t.sleep(0.01)
            if game.getDone():
                action(game.hide)
                send_message(s, "0")
                t.sleep(0.01)
                _server()
    if m == "2":
        os._exit(0)
b = threading.Thread(target=_server, args=())
def server():
    global started 
    b.start()

if __name__ == "__main__":
    try:
        started = False
        server()
        pyglet.app.run()
    except KeyboardInterrupt:
        b.join()
        print("Exiting...")
        exit(0)