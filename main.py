import tkinter as tk
import time
import threading
import random
import requests
import sys
import os


class WordDashGUI:
    def __init__(self):
        self.reset = self.reset
        self.running = False  # Initialize running flag
        self.root = tk.Tk()
        self.root.title("Word Dash")
        self.root.geometry("800x600")

        self.frame = tk.Frame(self.root)

        self.sample_label = tk.Label(self.frame, text=get_new_quote(), font=("Roboto", "18"))
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.input_entry = tk.Entry(self.frame, width=40, font=("Roboto", "24"))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyPress>", self.start)

        self.speed_label = tk.Label(self.frame, text="Speed: \n0.00 CPS\n0.00 CPM", font=("Roboto", "18"))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.started = False

        self.root.mainloop()

    def start(self, event):
        if not self.running:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                t = threading.Thread(target=self.timethread)
                t.start()
        if not self.sample_label.cget('text') == self.input_entry.get():
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")
        if self.input_entry.get() == self.sample_label.cget('text')[:-1]:  # Remove extra char
            self.running = False
            self.input_entry.config(fg="green")

    def timethread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            cps = len(self.input_entry.get()) / self.counter
            cpm = cps * 60
            self.speed_label.config(text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM")

    def reset(self):
        pass


# quote api request
phrase = requests.get('https://quotable.io/random?minLength=10?tags=famous-quotes')
phrase = phrase.json()
phrase = phrase['content']
phrase_length = len(phrase.split())


def get_new_quote():
    try:
        new_quote = requests.get('https://quotable.io/random?minLength=10?tags=famous-quotes')
        new_quote = new_quote.json()
        new_quote = new_quote['content']
    except:
        new_quote = phrase
    return new_quote


WordDashGUI()
