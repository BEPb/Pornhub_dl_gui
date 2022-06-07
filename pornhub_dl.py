"""
Python 3.9 программа скачивания pornhub
Название файла pornhub_bot.py

Version: 0.1
Author: Andrej Marinchenko
Date: 2022-04-19
"""

import youtube_dl
import requests
import sys
import urllib.parse as urlparse

from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image


def ph_url_check():
    url = url_dl.get()
    parsed = urlparse.urlparse(url)
    regions = ["www", "cn", "cz", "de", "es", "fr", "it", "nl", "jp", "pt", "pl", "rt"]
    for region in regions:
        if parsed.netloc == region + ".pornhub.com":
            # print("PornHub url validated.")
            Output.insert(END, 'PornHub url validated.')
            return

    # print("This is not a PornHub url.")
    Output.insert(END, 'This is not a PornHub url.')
    sys.exit()


def ph_alive_check():
    url = url_dl.get()
    requested = requests.get(url)
    if requested.status_code == 200:
        print("and the URL is existing.")
        # Output.insert(END, 'and the URL is existing')
    else:
        # print("but the URL does not exist.")
        Output.insert(END, 'but the URL does not exist.')
        sys.exit()
    # return url


def Download_video():
    url = url_dl.get()
    ph_url_check()
    ph_alive_check()

    outtmpl = 'Download/' + '%(title)s.%(ext)s'
    ydl_opts = {
        'format': 'best',
        'outtmpl': outtmpl,
        'nooverwrites': True,
        'no_warnings': False,
        'ignoreerrors': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(tk.END, text) # write text to textbox
            # could also scroll to end of textbox here to make sure always visible

    def flush(self):  # needed for file like object
        pass


# url = 'https://rt.pornhub.com/view_video.php?viewkey=ph60c0bd38c9329'
root = tk.Tk()
root.title('Pornhub Downloader')  # титул окна
root.geometry('800x700')
root.maxsize(800, 700)
root.minsize(800, 700)

header = Label(root, bg="orange", width=300, height=2)
header.place(x=0, y=0)

h1 = Label(root, text="Pornhub", bg="orange", fg="black", font=('verdana', 13, 'bold'))  # подпись окна вверху
h1.place(x=135, y=5)

img = ImageTk.PhotoImage(Image.open('pornhub.png'))  # вставляем картинку logo
logo = Label(root, image=img, borderwidth=0)
logo.place(x=150, y=38)

# определяем первое поле URL для скачивания
e = Label(root, text="URL Address", font=('verdana', 10, 'bold'))  # надпись над полем ввода
e.place(x=150, y=170)
url_dl = Entry(root, width=60, relief=RIDGE, borderwidth=3)
url_dl.place(x=150, y=190)



# кнопка скачать
download = Button(root, text="Download", padx=30, bg="orange", relief=RIDGE, borderwidth=1,
               font=('verdana', 10, 'bold'),
               cursor="hand2", command=Download_video)
download.place(x=150, y=240)

# Окно для вывода результата скачивания
Output = Text(root, height = 22, width = 97)
Output.place(x=10, y=290)
pl = PrintLogger(Output)
sys.stdout = pl


root.mainloop()