from tkinter import *
import tkinter as tk
import pyautogui
from pynput import keyboard
import random
from unidecode import unidecode
import webbrowser
import time

import pandas as pd

super_number=0.4
df=pd.read_csv('./data.csv')
random_row=df.loc[random.randint(0,len(df)-1)]
items=df['nombrePrep'].tolist()
global_thing=[]
def on_press(key):
    try:
        global_thing.append(pyautogui.position())
    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key):
    if key == keyboard.Key.space:
        return False
with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:

    listener.join()


currentMouseX, currentMouseY=global_thing[-1]

def exit_app(event=None):
    root.destroy()

root = tk.Tk()

def show_black_overlay(duration=2000):  # duration in milliseconds
    overlay = tk.Toplevel()
    overlay.attributes('-fullscreen', True)
    overlay.attributes('-topmost', True)
    overlay.configure(bg='black')
    overlay.overrideredirect(True)  # Removes window border

    # Automatically close after duration
    overlay.after(duration, overlay.destroy)
# root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.attributes('-alpha', 1)
root.configure(bg='black')
root.overrideredirect(True)

root.bind("<Escape>", exit_app)
from difflib import get_close_matches

# items = ['apple', 'banana', 'grapefruit', 'orange', 'pineapple', 'blueberry', 'apricot']




# Create a frame with fixed size
frame = tk.Frame(root, width=currentMouseX, height=currentMouseY,bg='black')
frame.pack()
frame.pack_propagate(False)  # Prevent shrinking to fit contents


canvas = tk.Canvas(frame, width=currentMouseX, height=currentMouseY, bg='black', highlightthickness=0)


def update_listbox(*args):
    search_term = entry_var.get()
    matches = [i for i in items if unidecode(search_term.lower()) in unidecode(i.lower())] #get_close_matches(search_term, items, n=10, cutoff=0.3)
    
    listbox.delete(0, tk.END)
    for item in matches if search_term else items:
        listbox.insert(tk.END, item)

entry_var = tk.StringVar()
entry_var.trace("w", update_listbox)  # Trigger update on change

entry = tk.Entry(frame, textvariable=entry_var)
entry.pack()

listbox = tk.Listbox(frame,height=8)
# items = ["Python"+str(i) for i in range(100)]
    

# Agregar elementos almacenados en una lista o tupla.
listbox.insert(0, *items)

# http://www.histomap.ar/histoteca/Hipofisis_Tricromico.htm?x=14602&y=8847&z=3
print('Random Row')
print(random_row)
def on_select(event):
    global random_row
    selected_indices = listbox.curselection()
    if selected_indices:
        selected_item = listbox.get(selected_indices[0])
        print(f"Selected item: {selected_item}")
        if selected_item==random_row['nombrePrep']:
            message_label.config(text="Correct", fg="green") 
            message_label.after(2000, lambda: message_label.config(text=""))  # Hide after 2 seconds


            random_row=df.loc[random.randint(0,len(df)-1)]
            print('Random Row')
            print(random_row)
            webbrowser.open(random_row['link'], new = 0)   

            time.sleep(2)
            pyautogui.moveTo((((1-super_number)/2)+random.random()*super_number)*root.winfo_screenwidth(), (((1-super_number)/2)+random.random()*super_number)*root.winfo_screenheight())
            for i in range(random.randint(0,4)):
                time.sleep(0.5)
                pyautogui.click()
        else:
            message_label.config(text="Incorrect", fg="red")
            message_label.after(2000, lambda: message_label.config(text=""))  # Hide after 2 seconds

listbox.bind('<<ListboxSelect>>', on_select)



message_label = tk.Label(frame, text="", font=("Arial", 16))
# def show_correct():



listbox.pack()
message_label.pack()
canvas.pack()
webbrowser.open(random_row['link'])
show_black_overlay(3000)
time.sleep(2)
pyautogui.moveTo((((1-super_number)/2)+random.random()*super_number)*root.winfo_screenwidth(), (((1-super_number)/2)+random.random()*super_number)*root.winfo_screenheight())


for i in range(random.randint(0,4)):
    time.sleep(0.5)
    pyautogui.click()


root.mainloop()




