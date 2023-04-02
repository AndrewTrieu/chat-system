import socket
import threading

HOST = '127.0.0.1'  # IP address for the server
PORT = 3000  # Port number for the server
MAX_CONNECTIONS = 10  # Maximum number of clients allowed to connect

# Dictionary to store connected clients and their nicknames
clients = {}

# Function to handle each client connection


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # Ask the client to set a nickname
    nickname = conn.recv(1024).decode()

    # Add the client to the dictionary of connected clients
    clients[conn] = nickname

    # Notify all other clients that a new client has joined the chat
    broadcast(f"{nickname} has joined the chat!".encode())

    while True:
        # Receive message from the client
        message = conn.recv(1024).decode()
        if message:
            # Check if the message is a private message to a specific client
            if message == "\q":
                # If the message is "quit", remove the client from the dictionary of connected clients
                del clients[conn]
                # Notify all other clients that the client has left the chat
                broadcast(f"{nickname} has left the chat.".encode())
                print(f"[DISCONNECTED] {addr} disconnected.")
                # Close the client connection
                conn.close()
                break
            elif message.startswith("@"):
                recipient = message.split(" ")[0][1:]
                message = message.split(" ", 1)[1]
                send_private_message(conn, recipient, message)
            else:
                # Broadcast the message to all connected clients
                broadcast(f"{nickname}: {message}".encode())

        else:
            # If message is empty, remove the client from the dictionary of connected clients
            del clients[conn]
            # Notify all other clients that the client has left the chat
            broadcast(f"{nickname} has left the chat.".encode())
            # Close the client connection
            conn.close()
            break

# Function to broadcast a message to all connected clients


def broadcast(message):
    for client in clients:
        client.sendall(message)

# Function to send a private message to a specific client


def send_private_message(sender_conn, recipient, message):
    for client, nickname in clients.items():
        if nickname == recipient:
            client.sendall(
                f"(Private) {clients[sender_conn]}: {message}".encode())
            sender_conn.sendall(
                f"(Private) {clients[sender_conn]}: {message}".encode())
            break


# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket object to the specified host and port number
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(MAX_CONNECTIONS)

print(f"[LISTENING] Server is listening on {HOST}:{PORT}.")

while True:
    # Accept incoming connections
    conn, addr = server_socket.accept()

    # Create a new thread to handle the client connection
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

    # Print the number of active connections
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
