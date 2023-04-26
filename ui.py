import tkinter as tk
from tkinter import *
import pychromecast
from pychromecast import quick_play
import time
import mimetypes
from PIL import ImageTk, Image
import requests
from io import BytesIO
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import sys
from pyramid.config import Configurator
import os
import time
import threading
import socket

# Beginning
window = tk.Tk()
urlVar = tk.StringVar()
ctVar = tk.StringVar()
pathVar = tk.StringVar()


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

    image_paths = []
    for r, d, fs in os.walk(os.getcwd() + "/images"):
        for f in fs:
            _p = os.path.join(r, f)
            _f = _p.replace(os.getcwd() + "/images", '').lstrip('/')
            image_paths.append(os.path.join('images', _f))
    return image_paths


def slideshow(paths):
    url = getURL()
    for i in paths:
        send_slide(url+":8000"+"/"+i)
        time.sleep(45)

def send_slide(url):
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=["ColdwellDisp"]
    )
    ctVar.set(mimetypes.guess_type(urlVar.get()))
    for i in chromecasts:
        i.wait()
        mc = i.media_controller
        mc.play_media(url, ctVar.get(), autoplay=True)
        mc.block_until_active()
        mc.play()
        print(mc.status)
    browser.stop_discovery()
    ctVar.set("")

def run():
    HandlerClass = BaseHTTPRequestHandler
    ServerClass = HTTPServer
    Protocol = "HTTP/1.0"

    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 8000
        server_address = (getURL(), port)

    config = Configurator()
    paths = img_paths()

    for i in paths:
        config.add_route(i, "/"+i)

    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    httpd.serve_forever()


def send(url):
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=["ColdwellDisp"]
    )
    ctVar.set(mimetypes.guess_type(urlVar.get()))
    for i in chromecasts:
        i.wait()
        mc = i.media_controller
        mc.play_media(urlVar.get(), ctVar.get(), autoplay=True)
        mc.block_until_active()
        mc.play()
        print(mc.status)
    browser.stop_discovery()
    urlVar.set("")
    ctVar.set("")
# 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'video/mp4')


chromecasts, browser = pychromecast.get_listed_chromecasts(
    friendly_names=["ColdwellDisp"]
)
for i in chromecasts:
    i.wait()
browser.stop_discovery()

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

x = threading.Thread(target=run)
x.start()

paths = img_paths()

def items(): return send(u1)
tk.Button(canvas, text="Send to Displays", command=items).grid()
tk.Label(canvas, text="Or").grid()


def images(): return slideshow(paths)

tk.Button(canvas, text="Play Slide Show", command=images).grid()

window.mainloop()
