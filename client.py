import socket
import threading

HOST = '127.0.0.1'  # IP address for the server
PORT = 3000  # Port number for the server

# Function to receive messages from the server


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            # If an error occurs, close the client socket and exit the thread
            client_socket.close()
            break


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Create a new thread to receive messages from the server
receive_thread = threading.Thread(
    target=receive_messages, args=(client_socket,))
receive_thread.start()

# Send a welcome message to the client
print("Welcome to the chat room!")

# Send nickname to the server
nickname = input("Please enter your nickname: ")
client_socket.sendall(nickname.encode())

while True:
    message = input()

    if message == "\q":
        # Send a message to the server indicating that the user wants to quit
        client_socket.sendall("\q".encode())
        # Exit the program immediately
        break
    elif message.startswith("@"):
        # If user types a message starting with "@" it is considered a private message
        recipient = message.split(" ")[0][1:]
        private_message = message.split(" ", 1)[1]
        client_socket.sendall(f"@{recipient} {private_message}".encode())

    else:
        # Otherwise, send the message to the server to broadcast to all connected clients
        client_socket.sendall(message.encode())

# Close the client socket
client_socket.close()
