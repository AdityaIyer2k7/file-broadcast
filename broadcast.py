import os
import random
import socket
import threading

PORTDISC = 25723
PORTSEND = random.randint(0x7FFF, 0xFFFF)

filename = input("File name: ")
data = None
with open(filename, mode='rb') as fl:
    data = fl.read()
filesize = os.path.getsize(filename)
filename = os.path.split(filename)[1]

hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)

running = True

def discover():
    hostdisc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostdisc.bind((hostip, PORTDISC))
    hostdisc.listen()
    while running:
        try:
            conn, addr = hostdisc.accept()
            conn.send(f"{hostname}|{filename}|{filesize}|{PORTSEND}".ljust(1024, " ").encode())
            conn.close()
        except: pass
    hostdisc.close()

threading.Thread(target=discover).start()

hostsend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostsend.bind((hostip, PORTSEND))
hostsend.listen()
while running:
    try:
        conn, addr = hostsend.accept()
        conn.send(data)
        conn.close()
        print(f"{addr} has accepted the file")
    except KeyboardInterrupt:
        print("Program closed... Exiting")
        running = False
        exit()
    except Exception as e:
        print(e)
