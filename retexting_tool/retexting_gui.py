from tkinter import *
from tkinter import messagebox

from functools import partial
import argparse
import os

from PIL import ImageTk
from utils import resize_image_to_pil

from data_loader import DataLoader

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, help='file path')
args = parser.parse_args()

data_path = os.path.join(args.path, "*.jpg")
data_loader = DataLoader(data_path)

window=Tk()
window.attributes("-fullscreen", True)
window.title("Re-texting Label")

image_label = Label(window)
text_button_frame = Frame(window)
image_label.grid(row=0, column=0, sticky="nsew")
text_button_frame.grid(row=0, column=1, sticky="nsew")

path_label = Label(text_button_frame)
path_label.grid(row=0, column=0, sticky="nsew")

textbox = Entry(text_button_frame, width=50)
textbox.grid(row=1, column=0, sticky="nsew")

def update(mode):
    curr_image_path = data_loader.curr_image_path
    if mode == "next":
        image_path, text = data_loader.load_next_image_path_label()
        message_text = "마지막입니다."
    elif mode == "prev":
        image_path, text = data_loader.load_prev_image_path_label()
        message_text = "맨 앞 입니다."
    else:
        raise "unknown mode selected"

    if image_path is None and text is None:
        messagebox.showerror("error", message_text)

    else:
        global image
        path_label.config(text=image_path)
        image = ImageTk.PhotoImage(resize_image_to_pil(image_path))
        image_label.config(image=image)

        try:
            with open(curr_image_path.replace("jpg", "txt"), 'w') as f:
                f.write(textbox.get())
        except Exception as e:
            pass
        textbox.delete(0, 'end')
        textbox.insert(END, text)

def delete_image_label():
    answer = messagebox.askquestion("warning", "사진이 삭제됩니다.", icon="warning")
    if answer == "no":
        return

    image_path, text = data_loader.delete_image_path_label()
    
    global image
    curr_image_path = data_loader.get_curr_image_path()
    path_label.config(text=image_path)
    image = ImageTk.PhotoImage(resize_image_to_pil(image_path))
    image_label.config(image=image)

    try:
        with open(curr_image_path.replace("jpg", "txt"), 'w') as f:
            f.write(textbox.get())
    except Exception as e:
        pass
    
    textbox.delete(0, 'end')
    textbox.insert(END, text)

button_frame = Frame(text_button_frame)
prev_button = Button(button_frame, text="이전", width=30, height=5, command=partial(update, "prev"))
next_button = Button(button_frame, text="다음", width=30, height=5, command=partial(update, "next"))
delete_button = Button(button_frame, text="삭제", width=30, height=5, command=delete_image_label)
button_frame.grid(row=2, column=0, sticky="nsew")
prev_button.grid(row=0, column=0, sticky="nsew")
next_button.grid(row=1, column=0, sticky="nsew")
delete_button.grid(row=2, column=0, sticky="nsew")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=3, minsize=640)
window.columnconfigure(1, weight=1)
text_button_frame.rowconfigure(0, weight=1)
text_button_frame.rowconfigure(1, weight=2)
text_button_frame.rowconfigure(2, weight=2)
text_button_frame.columnconfigure(0, weight=1)
button_frame.rowconfigure(0, weight=1)
button_frame.rowconfigure(1, weight=1)
button_frame.rowconfigure(2, weight=1)
button_frame.columnconfigure(0, weight=1)

update("next")

window.mainloop()