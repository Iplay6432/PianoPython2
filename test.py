import socket
import pyglet
port = 12345
host = "127.0.0.1" 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pyglet.app.run()
try:
    s.connect((host, port))
    print("Connected to server.")

    initial_data = s.recv(1024).decode('utf-8')
    print("Server says: " + initial_data)

    message = input(" -> ")
    while message.lower().strip() != "bye":
        msg_bytes = message.encode('utf-8')
        s.send(len(msg_bytes).to_bytes(2, 'big'))
        s.send(msg_bytes)

        length_bytes = s.recv(2)
        if not length_bytes:
            print("Server disconnected.")
            break
        msg_length = int.from_bytes(length_bytes, 'big')
        data = s.recv(msg_length).decode('utf-8')

        print("Server says: " + data)
        message = input(" -> ")

except ConnectionRefusedError:
    print(f"Connection refused. Is the server running on {host}:{port}?")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Closing connection.")
    s.close()