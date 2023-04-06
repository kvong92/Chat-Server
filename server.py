import socket
import threading
import datetime
import os

# Create a class for the server

class ChatServer:

    SHUTDOWN_MSG = "Server is shutting down ..."

    # Initialize the server
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}
        self.server_running = True

    # Server's commands
    def commands(self):
        while self.server_running:
            print("Type /help to see all commands")
            commands = input()
            if commands == "/help":
                print("----------------------")
                print("- List of commands : -")
                print("----------------------")
                print("/shutdown : shutdown the server")
                print("/list : list all users connected")
            if commands == "/list":
                self.print_list_users()
            if commands == "/shutdown":
                self.shutdown_server()
                return

    # Print list of users connected
    def print_list_users(self):
        print("---------------------------")
        print("- List of users connected -")
        print("---------------------------")
        for client in self.clients:
            print(f"{client}")
        # print list of users connected to all users
        self.broadcast("\n---------------------------\n")
        self.broadcast("- List of users connected -\n")
        self.broadcast("---------------------------\n")
        for client in self.clients:
            self.broadcast(f"{client}")
            if not client == list(self.clients)[-1]:
                self.broadcast("\n")

    # Shutdown server
    def shutdown_server(self):
        # print(self.SHUTDOWN_MSG)
        self.server_running = False
        # Disconnect all clients
        for client_sock in self.clients.values():
            # Send server shutting down message to all clients
            client_sock.send("/shutdown".encode())
            client_sock.close()
        self.sock.close()
        print("Server has been closed")

    # Start the server
    def start(self):
        print("Starting server ...")
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print(f"Server started on {self.host}:{self.port}")
        try:
            shutdown_thread = threading.Thread(target=self.commands)
            shutdown_thread.start()
            while self.server_running:
                try:
                    client_sock, client_addr = self.sock.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client, args=(client_sock,))
                    client_thread.start()
                except ConnectionAbortedError:
                    print(self.SHUTDOWN_MSG)
                    return
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected ...")
            print(self.SHUTDOWN_MSG)
            self.shutdown_server()
            os._exit(0)  # Terminate the client process

    # Get time of sending message
    def get_time(self):
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")

    # Get username from client.py
    def get_username(self, client_sock):
        while self.server_running:
            print("Waiting for username...")
            username = client_sock.recv(1024).decode().strip()
            if username in self.clients:
                print("Username is already taken")
                client_sock.send("True".encode())
            else:
                client_sock.send("False".encode())
                return username

    # Write log connecting/disconnecting to the server to file log.txt
    def write_log(self, message):
        now = datetime.datetime.now()
        date_time = now.strftime('%d/%m/%Y - %H:%M:%S')
        with open('log.txt', 'a+') as f:
            f.write("[" + date_time + "] " + message)

    # Handle the client and send messages to other clients
    def handle_client(self, client_sock):
        now = self.get_time()
        username = self.get_username(client_sock)
        print(f"{username} has joined the chat")
        self.broadcast(f"{username} has joined the chat")
        log = f"{username} has joined the chat\n"
        self.write_log(log)
        self.clients[username] = client_sock
        receive_thread = threading.Thread(
            target=self.receive_messages, args=(client_sock, username, now))
        receive_thread.start()

    # Remove a client from the dictionary of clients
    def remove_client(self, username):
        print(f"{username} has left the chat")
        self.broadcast(f"{username} has left the chat")
        log = f"{username} has left the chat\n"
        self.write_log(log)
        self.clients.pop(username)
        return

    # Receive messages from clients
    def receive_messages(self, client_sock, username, now):
        while self.server_running:
            try:
                message = client_sock.recv(1024).decode().strip()
                if message:
                    print(f"<{username}> {message} ({now})")
                    self.broadcast(f"<{username}> {message} ({now})")
                    if message == "/list":
                        self.print_list_users()
                else:
                    self.remove_client(username)
            except:
                return

    # Send a message to all clients
    def broadcast(self, message):
        for client_sock in self.clients.values():
            client_sock.send(message.encode())

# Start the server
chat_server = ChatServer('127.0.0.1', 1234)
chat_server.start()