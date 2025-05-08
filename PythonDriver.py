import socket
from Main import Main
import pyglet
import threading
import time as t
import os
import json as j
import sys
import os
import traceback
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    if not os.path.isfile(resource_path("backend/data/data.json")):
        fp = "backend/data/data.json"
        data = {
            "levels":{}
        }
        json = j.dumps(data)
        with open(resource_path("backend/data/data.json"), "w") as f:
            f.write(json)
            f.close() 
    root = ""
    if getattr(sys, 'frozen', False):
        root = os.path.dirname(sys.executable)
    else:
        root = os.path.dirname(os.path.abspath(__file__))
    game = Main(root)
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
except Exception as e:
    error = f"Timestamp: {t.asctime()}\n"
    error += f"Error: {type.__name__}: {e}\n"
    error += traceback.format_exc()
    with open("error_log.log", "a") as f:
        f.write(error)
        f.close()
    print("An error occurred. Please check the error_log.log file for details.")
    sys.exit(1)