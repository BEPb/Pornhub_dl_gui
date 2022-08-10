"""
Python 3.9 программа скачивания pornhub
Название файла pornhub_bot.py

Version: 0.2
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
        text = text + '\n'
        self.textbox.insert(tk.END, text) # write text to textbox
        self.textbox.see(tk.END)
        root.update()
            # could also scroll to end of textbox here to make sure always visible

    def flush(self):  # needed for file like object
        pass


if __name__ == '__main__':
    # PornHub Color Palette
    background_black = '#000000'
    title_black = '#1b1b1b'
    button_orange = '#ff9000'
    text_color = '#ffffff'

    HEIGHT = 700
    WIDTH = 800

    # url = 'https://rt.pornhub.com/view_video.php?viewkey=ph60c0bd38c9329'
    root = tk.Tk()
    root.title('Pornhub Downloader')  # титул окна
    root.iconbitmap('icon.ico') # show icon
    root.geometry('800x700')
    root.maxsize(WIDTH, HEIGHT)
    root.minsize(WIDTH, HEIGHT)
    root.resizable(0,0) # this removes the maximize button
    root.configure(bg=background_black) #set window color

    w = root.winfo_width()
    h = root.winfo_height()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # Centering window
    
    header = Label(root, bg=button_orange, width=300, height=2)
    header.place(x=0, y=0)
    
    h1 = Label(root, text="Pornhub", bg=button_orange, fg=background_black, font=('arial', 13, 'bold'))  # подпись окна вверху
    h1.place(x=WIDTH/2, y=18, anchor=CENTER)
    
    img = ImageTk.PhotoImage(Image.open('pornhub.png'))  # вставляем картинку logo
    logo = Label(root, image=img, borderwidth=0)
    logo.place(x=WIDTH/2, y=120, anchor=CENTER)
    
    # определяем первое поле URL для скачивания
    e = Label(root, text="URL Address", font=('arial', 10, 'bold'), bg=background_black, fg=text_color)  # надпись над полем ввода
    e.place(x=WIDTH/2, y=190, anchor=CENTER)
    url_dl = Entry(root, width=60, relief=RIDGE, borderwidth=3)
    url_dl.place(x=WIDTH/2, y=220, anchor=CENTER)
    url_dl.focus_set()
    
    # кнопка скачать
    download = Button(root, text="Download", padx=30, bg=button_orange, relief=RIDGE, borderwidth=1,
                   font=('arial', 10, 'bold'),
                   cursor="hand2", command=Download_video)
    download.place(x=WIDTH/2, y=260, anchor=CENTER)
    
    # Окно для вывода результата скачивания
    Output = Text(root, height = 22, width = 97)
    Output.place(x=10, y=290)
    Output.configure(bg=title_black, fg=text_color)
    pl = PrintLogger(Output)
    sys.stdout = pl
    
    root.mainloop()