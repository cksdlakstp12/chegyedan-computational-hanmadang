from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

from functools import partial

from PIL import ImageTk, Image

import argparse
from datetime import date
import os

from data_manager import DataManager

parser = argparse.ArgumentParser()
parser.add_argument('--ip', type=str, help='colab server ip')
args = parser.parse_args()

data_manager = DataManager(args.ip)
RESPONSE_IMAGE = None

window=Tk()
window.attributes("-fullscreen", True)
window.title("Dalle Client")

image_label = Label(window)
image_label.grid(row=0, column=0, sticky="nsew")

text_button_frame = Frame(window)
text_button_frame.grid(row=0, column=1, sticky="nsew")

textbox = Entry(text_button_frame, width=50)
textbox.grid(row=0, column=0, sticky="nsew")

def update():
    try:
        response = data_manager.request_generate(textbox.get())
    except Exception as e:
        print(e)
        response = "error"

    if response == "error":
        image_label.config(image="")
        image_label.config(text="ERROR")
    else:
        global image, RESPONSE_IMAGE
        RESPONSE_IMAGE = Image.fromarray(response)
        image = ImageTk.PhotoImage(RESPONSE_IMAGE)
        image_label.config(image=image)
        image_label.config(text="")

def save_image():
    dir = filedialog.askdirectory(initialdir='', title='폴더선택')
    filename = date.today().isoformat()
    save_path = os.path.join(dir, filename)
    if RESPONSE_IMAGE is None:
        image_label.config(text="생성한 이미지가 없습니다...")
    else:
        RESPONSE_IMAGE.save(save_path)

def init():
    global RESPONSE_IMAGE
    RESPONSE_IMAGE = None
    image_label.config(image="")
    image_label.config(text="문장을 쓰고 버튼을 눌러 이미지를 생성해보세요!")
    textbox.delete(0, 'end')

button_frame = Frame(text_button_frame)
button_frame.grid(row=1, column=0, sticky="nsew")
request_button = Button(button_frame, text="사진 생성 시작", width=30, height=5, command=update)
request_button.grid(row=0, column=0, sticky="nsew")
save_button = Button(button_frame, text="사진 저장", width=30, height=5, command=save_image)
save_button.grid(row=1, column=0, sticky="nsew")
init_button = Button(button_frame, text="다시하기", width=30, height=5, command=init)
init_button.grid(row=2, column=0, sticky="nsew")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=3, minsize=640)
window.columnconfigure(1, weight=1)
text_button_frame.rowconfigure(0, weight=1)
text_button_frame.rowconfigure(1, weight=1)
text_button_frame.columnconfigure(0, weight=1)
button_frame.rowconfigure(0, weight=1)
button_frame.rowconfigure(1, weight=1)
button_frame.rowconfigure(2, weight=1)
button_frame.columnconfigure(0, weight=1)

init()

window.mainloop()