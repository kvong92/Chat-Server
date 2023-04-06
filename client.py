import socket
import os
import threading
import time

# Create a class for the client

class ChatClient:
    SHUTDOWN_MSG = "/shutdown"

    # Initialize the client
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.username = self.get_username()

    # Get username from client.py
    def get_username(self):
        while True:
            username = input("Enter your username: ")
            if username == "":
                print("You must enter a username")
                continue
            if len(username) > 20:
                print("Your username is too long. It must be less than 20 characters.")
                continue
            self.sock.send(username.encode())
            taken = self.sock.recv(1024).decode().strip()
            if taken == "True":
                print("Username is already taken")
                continue
            else:
                print(f"Welcome {username} to the chat !")
                return username

    def receive_messages(self):
        while self.connected:
            try:
                message = self.sock.recv(1024).decode()
                if message == "/shutdown":
                    print("Server is shutting down...")
                    print("You are now disconnected from the server.")
                    self.connected = False
                    self.sock.close()
                    os._exit(0)  # Terminate the client process
                print(message)
            except KeyboardInterrupt:
                self.connected = False
                os._exit(0)  # Terminate the client process
            except:
                self.connected = False
                os._exit(0)  # Terminate the client process

    def send_messages(self):
        while self.connected:
            try:
                message = input()
                if message == self.SHUTDOWN_MSG:
                    print("You are not allowed to use this command.")
                    continue
                # Logout from server
                if message == "/quit":
                    self.connected = False
                    # self.sock.send(message.encode())
                    self.sock.close()
                    print("Logout from the chat !")
                    return
                self.sock.send(message.encode())
            except KeyboardInterrupt:
                self.connected = False
                os._exit(0)  # Terminate the client process
            except:
                self.connected = False
                os._exit(0)  # Terminate the client process

    # Start the client
    # def start(self):
    #     try:
    #         receive_thread = threading.Thread(target=self.receive_messages)
    #         receive_thread.start()
    #         send_thread = threading.Thread(target=self.send_messages)
    #         send_thread.start()
    #     except KeyboardInterrupt:
    #         print("\nKeyboard interrupt detected ...")
    #         self.logout()
    #         os._exit(0)  # Terminate the client process

     # Start the client
    def start(self):
        try:
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            send_thread = threading.Thread(target=self.send_messages)
            send_thread.start()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected ...")
            self.logout()
        except:
            print("Error starting threads")
            self.logout()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected ... Loggout ...")
            print("You are now disconnected from the server.")
            self.logout()

    # Logout from server
    def logout(self):
        self.connected = False
        self.sock.close()
        print("Logout from the chat !")


client_start = ChatClient('127.0.0.1', 1234)
client_start.start()