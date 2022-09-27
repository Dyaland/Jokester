#!/usr/bin/python3

import requests
import tkinter as tk
from tkinter import font


class AutoScrollbar(tk.Scrollbar):
    """Scrollbar that appears only when needed"""
    
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.pack_forget()
            self.grid_forget()
        else:
            try:
                self.grid()
            except Exception:  # This only defaults to grid if pack doesn't work
                self.pack(side="right", fill="y")

        tk.Scrollbar.set(self, lo, hi)


class Jokester(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        # Main window settingsimage
        self.geometry('1000x1000+300+0')
        #self.attributes('-fullscreen', True)
        self.title("The Jokester")
        self.resizable(True, True)
        self.config(bg='lightgray')

        # Default styles
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Courier New", size=30)
        self.option_add("*Font", default_font)
        self.option_add("*HighlightThickness", 0)
        self.option_add("bg", 'light gray')
        
        self.joke = None
        
        # Wigdets
        self.empty_label = tk.Label(self, text='\n\n', bg='lightgray')
        self.empty_label.pack()
        
        self.joke_frame = tk.Frame(self) # For joke_setup & scrollbar
        self.joke_frame.pack()
        
        self.joke_setup = tk.Text(self.joke_frame, wrap=tk.WORD, width=50, height=8, bg='lightgray', bd=0, cursor='hand2')
        self.joke_setup.tag_configure('a', justify=tk.CENTER)
        self.joke_setup.pack(side='left')
        
        self.joke_scrollbar = AutoScrollbar(self.joke_frame, width=16, command=self.joke_setup.yview, orient='vertical')
        self.joke_scrollbar.pack(side='right', fill='y')
        
        self.joke_setup['yscrollcommand'] = self.joke_scrollbar.set
        
        self.joke_delivery = tk.Text(self, wrap=tk.WORD, width=50, height=6, bg='lightgray', bd=0, cursor='hand2')
        self.joke_delivery.tag_configure('a', justify=tk.CENTER)
        self.joke_delivery.pack()
        
        self.joke_button = tk.Button(self, text='New joke', command=self.display_setup, cursor='hand2')
        self.joke_button.pack()
        
        self.quit_button = tk.Button(self, text='Quit', command=exit, cursor='pirate')
        self.quit_button.pack(pady=10)
        
        self.display_setup()
        

    def display_setup(self):
        self.joke_setup.delete('1.0', tk.END)
        self.joke = requests.get('https://v2.jokeapi.dev/joke/Any?safe-mode').json()
        try:
            self.joke_setup.insert('1.0', f"{self.joke['setup']}")
        except KeyError:
            self.joke_setup.insert('1.0', f"{self.joke['joke']}")
        else:
            self.joke_button.config(text='Answer', command=self.display_delivery)
        finally:
            self.joke_setup.tag_add("a", "1.0", tk.END)
            self.joke_delivery.delete('1.0', tk.END)
    
    def display_delivery(self):
        self.joke_delivery.insert('1.0', self.joke['delivery'])
        self.joke_delivery.tag_add("a", "1.0", tk.END)
        self.joke_button.config(text='New joke', command=self.display_setup)


if __name__ == '__main__':
    Jokester().mainloop()
    
