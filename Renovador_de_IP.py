import os
import time
import requests
import socket
import tkinter as tk
import threading
import subprocess


def getLocalIp():
    return socket.gethostbyname(socket.gethostname())

def getPublicIp():
    response = requests.get('https://api.ipify.org')
    return response.text

def updateIpLabels():
    localIpLabel.config(text="IP Local: " + getLocalIp())
    publicIpLabel.config(text="IP Publico " + getPublicIp())

def loopFunction():

    activeLoop = activeLoop_var.get()
    renewTime = int(renewTime_entry.get()) * 60

    while activeLoop: 
        subprocess.run(['ipconfig', '/release'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        subprocess.run(['ipconfig', '/renew'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(renewTime)
        updateIpLabels()
        root.update()
        
def executeLoop():
    threading.Thread(target=loopFunction, daemon=True).start()


root = tk.Tk()
root.geometry("300x180")
root.title ("Renovador de IP")


renewTime_label = tk.Label(root, text="Tempo para mudar o IP(minutos):")
renewTime_label.pack()
renewTime_entry = tk.Entry(root)
renewTime_entry.pack()

activeLoop_var = tk.BooleanVar()
activeLoop_var.set(True)
activeLoop_checkbutton = tk.Checkbutton(root , text="Ativar Programa", variable=activeLoop_var)
activeLoop_checkbutton.pack()

startButton = tk.Button(root, text="Iniciar", command=executeLoop)
startButton.pack()

localIpLabel = tk.Label(root, text="IP local: ")
localIpLabel.pack()

publicIpLabel = tk.Label(root, text="IP público: ")
publicIpLabel.pack()

    
updateIpLabels()
root.mainloop()