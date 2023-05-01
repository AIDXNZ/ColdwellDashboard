import tkinter as tk
from tkinter import *
import pychromecast
from pychromecast import quick_play
import time
import mimetypes
from PIL import ImageTk, Image
import requests
import io
from io import BytesIO
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import sys
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
import os
import time
import threading
import socket
import ssl
from ssl import SSLContext
from ssl import PROTOCOL_SSLv23
from requests.auth import HTTPBasicAuth
from pychromecast.controllers.receiver import CastStatus

# Beginning
window = tk.Tk()
urlVar = tk.StringVar()
ctVar = tk.StringVar()
pathVar = tk.StringVar()
secs= tk.IntVar()


with open('list.txt') as f:
    ips = f.readlines()
ips_list = []
if len(ips) > 0:
    for ip in ips:
        ips_list.append(str(ip))



chromecasts, browser = pychromecast.get_listed_chromecasts(
    friendly_names=["ColdwellDisp"]
)
browser.stop_discovery()

def load(file):
    with open(file, 'rb') as file:
        return file.read()


def getURL():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]   
    except:
            IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def img_paths():
    """Display images."""
    import requests
    
    image_paths = []
    image_links = []
    for r, d, fs in os.walk(os.getcwd() + "/images"):
        for f in fs:
            _p = os.path.join(r, f)
            _f = _p.replace(os.getcwd() + "/images", '').lstrip('/')
            image_paths.append(os.path.join('images', _f))
            image = Image.open(os.getcwd()+"/images/"+f)
            buf = io.BytesIO()
            new_image = image.rotate(90)
            new_image.save(buf, format('JPEG'))
            payload = {'key': '6d207e02198a847aa98d0a2a901485a5','action': 'upload', }
            x = requests.post("https://freeimage.host/api/1/upload", payload, files={"source": buf.getvalue()})
            import json
            data = json.loads(x.text)
            image_links.append(data["image"]["url"])
    print(image_links)
    return image_links
    
def stop():
     for ip in ips_list:
        ip.replace(" ", "")
        os.system("./rust_caster" +" "+"-a "+ip+" --stop-current")

def slideshow():
    paths = img_paths()
    
    for i in paths:
        send_slide(i)
        time.sleep(secs.get()*15)
        
def comand_rust(ip, url):
    os.system("./rust_caster" +" "+"-a "+ip+" -m "+ url)

def send_slide(url):
    if ".jpg" in urlVar.get():
        ctVar.set("image/jpg")
    else:
        ctVar.set(mimetypes.guess_type(url))     
    
    for ip in ips_list:
        ip.replace(" ", "")
        print("./rust_caster" +" "+"-a "+ip+" -m "+ url)
        x = threading.Thread(target=comand_rust, args=(ip,url,))
        x.start()
    ctVar.set("")


def send(url):
    if ".jpg" in urlVar.get():
        ctVar.set("image/jpg")
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=["ColdwellDisp"]
    )
    for ip in ips_list:
        ip.replace(" ", "")
        os.system("./rust_caster" +" "+"-a "+ip+" -m "+ urlVar.get())
        
    
    urlVar.set("")
    ctVar.set("")
# 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'video/mp4')

numOfDevices = len(chromecasts)

window.title("Coldwell Displays")
window.geometry('800x800')
window.configure(background="white")

canvas = Canvas(window, bg="white")
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)


img_url = "https://images.static-ziprealty.com/images_broker/v3/CB/11675/company_logo_Horizontal.png"
response = requests.get(img_url)
img_data = response.content
labelogo = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
panel = tk.Label(canvas, image=labelogo).grid(row=0, column=0)

label = tk.Label(window, text="Current Device Name Scheme: ColdwellDisp").grid(
    row=0, column=0)
labelDN = tk.Label(window, text="Number of Devices").grid(row=2, column=0)
numOfDeez = IntVar()
numOfDeez.set(numOfDevices)
labelDNUM = tk.Label(window, text=numOfDevices).grid(row=3, column=0)


label1 = tk.Label(canvas, text="Media URL").grid(row=1, column=0)
u1 = tk.Entry(canvas, textvariable=urlVar).grid(row=1, column=1)


def items(): return send(u1)


tk.Button(canvas, text="Send to Displays", command=items).grid()
tk.Label(canvas, text="Or").grid()



def images():
    run = True
    while (run == True):
        slideshow()

tk.Spinbox(canvas, from_=1, to=100,textvariable=secs).grid()
tk.Button(canvas, text="Play Slide Show", command=images).grid()
def pause(): return stop()

tk.Button(window, text="stop", command=pause())

window.mainloop()
