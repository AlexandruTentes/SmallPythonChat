import socket
import threading
import sys
import os
import tkinter as tk

window = tk.Tk()
window.title("I hate tkinter")
#window.configure(width=500, height=300)
window.geometry("500x300")
window.configure(bg='lightgray')

T = tk.Text(window, height = 10, width = 52)
F = tk.Label(window, text="", font=("Courier 22 bold"))
T.pack()
F.pack()

entry= tk.Entry(window, width= 40)
entry.focus_set()
entry.pack()

data_size = 1024
server_IP = 'localhost'
server_PORT = 22000
received_message = ''
ERROR_MESSAGE = ''
TCP_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    TCP_server_socket.connect((server_IP, server_PORT))
except:
    print("Cannot connect to the server")
    os.exit()

def send_message():
    if not ERROR_MESSAGE == '':
        return
    
    try:
        TCP_server_socket.send(bytes(entry.get(), 'UTF-8'))
    
    except:
        print("Connection has unexpectedly closed")
        return

B = tk.Button(window, text ="Send", command = send_message)
B.place(rely=1.0, relx=1.0, x=0, y=0)
B.pack()

def get_message():
        return received_message

def msg_handler_recv():
    while True:
        try:
            data = TCP_server_socket.recv(data_size)              
            received_message = str(data, 'utf-8')
            T.insert(tk.END, received_message + "\n")

        except ConnectionResetError:
            print("Connection has unexpectedly closed")
            return

        except:
            print("Closing the program")
            return

recv_message_thread = threading.Thread(target = msg_handler_recv)
recv_message_thread.daemon = True
recv_message_thread.start()

window.mainloop()
