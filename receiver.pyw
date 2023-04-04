import pyautogui as pyg
import socket
import os

PORTDISC = 25723

hostipseed = ".".join(socket.gethostbyname(socket.gethostname()).split(".")[:3])
print(hostipseed)

knowPorts = []

while True:
    for i in range(1, 256):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(0.01)
            client.connect((f"{hostipseed}.{i}", PORTDISC))
            hostname, filename, filesize, PORTSEND = client.recv(1024).decode().split("|")
            filesize = int(filesize)
            PORTSEND = int(PORTSEND)
            client.close()
            if PORTSEND not in knowPorts:
                v = pyg.confirm(f"Host {hostname} is trying to send {filename} of {filesize} bytes", "Receive files?")
                if v == 'OK':
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((f"{hostipseed}.{i}", PORTSEND))
                    data = client.recv(filesize)
                    with open(os.path.join("received", filename), mode='wb') as fl:
                        fl.write(data)
                    client.close()
                    pyg.alert(f"File saved to {os.path.join('received', filename)}", "Saved")
                knowPorts.append(PORTSEND)
        except socket.error as e: pass
        except Exception as e: print(e.with_traceback())
