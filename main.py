import customtkinter as ctk
from tkinter import ttk
from pynput.keyboard import *
import pynput.mouse as mse


# listener.stop()

LIGHT_GREY = "#474444"
GREY = "#2b2a2a"






class App(ctk.CTk):

    def __init__(self):
        super().__init__(fg_color=LIGHT_GREY)

        # Attributes
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.7)
        self.geometry("300x400")
        # Exiting event
        self.bind("<Escape>", lambda _: exit())

        self.minsize(170, 170)

        # Window resize widget
        ttk.Sizegrip(self).place(relx=1, rely=1, anchor="se")

        # Keys dict
        self.keys_dict = {}

        self.total_clicks = 0

        # Keys List
        self.keys_list = []
        self.lift()
        # New title bar
        self.create_title_bar()
        # Keyboard Listener
        k_listener = Listener(on_press=self.on_press, on_release=self.on_release)
        k_listener.start()

        # Mouse Listener
        m_listener = mse.Listener(on_click=self.on_pr2ess)
        m_listener.start()
        self.label = ctk.CTkLabel(self, anchor="nw", font=("Arial", 17), text="")
        self.label.place(relx=0.1, rely=0.15, relwidth=1, relheight=0.75)


        self.total_clicks_label = ctk.CTkLabel(
            self,
            font=("Arial", 20),
            text="Total clicks: 0",
            anchor="n")
        self.total_clicks_label.place(relx=0.53, rely=0.12)

        # Main loop
        self.mainloop()

        # Keyboard and mouse Listener threads
        k_listener.join()
        m_listener.join()

    def create_title_bar(self):
        frame = ctk.CTkFrame(
            self,
            fg_color=GREY)
        frame.place(relx=0, rely=0, relwidth=1, relheight=0.1, anchor="nw")
        frame.bind()

        close_btn = ctk.CTkButton(
            frame,
            text="X",
            fg_color=GREY,
            hover_color="red",
            command=exit)
        
        close_btn.place(
            relx=1,
            rely=0,
            relheight=1,
            relwidth=0.2,
            anchor="ne")

    def on_press(self, key):
        name = ""
        if type(key) != Key:
            name = key.char.upper()
        else:
            name = key.name.upper()
        if name == "F8":
            self.keys_dict = {}
            self.keys_list = []
            self.label.configure(text="")
        else:
            keys_list = self.keys_dict.get(name)

            if keys_list is None:

                self.keys_dict.update({name: [1, len(self.keys_list), False]})
                self.total_clicks += 1
                self.keys_list.append(name)

            else:
                if keys_list[2]:
                    keys_list[0] += 1
                    self.total_clicks += 1
                    if keys_list[1] != 0:
                        self.sort(key_list=keys_list, name=name)

                    keys_list[2] = False
        self.show()
                
                
    def on_pr2ess(self, *args):

        if args[3]:
            name = f"{args[2].name} click".upper()
            key_num = self.keys_dict.get(name)

            if key_num is None:
                self.keys_dict.update({name: [1, len(self.keys_list)]})
                self.keys_list.append(name)
            else:
                self.total_clicks += 1
                key_num[0] += 1
                if key_num[1] != 0:
                    self.sort(key_list=key_num, name=name)
            self.show()
                 
    def on_release(self, key):
        name = ""
        if type(key) != Key:
            name = key.char
        else:
            name = key.name

        key_list = self.keys_dict.get(name.upper())
        if key_list is not None:
            key_list[2] = True

    def sort(self, key_list, name):
        next_item_index = key_list[1] - 1
        next_item = self.keys_list[next_item_index]

        next_item_dict = self.keys_dict[next_item]

        if next_item_dict[0] < key_list[0]:
            key_list[1] -= 1
            next_item_dict[1] += 1
            self.keys_list[next_item_index] = name
            self.keys_list[next_item_index + 1] = next_item

    def show(self):
        text = ""
        for i in range(len(self.keys_list)):
            text = text + f"{self.keys_list[i]}: {self.keys_dict[self.keys_list[i]][0]}\n"
    
        self.label.configure(text=text)        
        self.total_clicks_label.configure(text=f"Total clicks: {self.total_clicks}")
        
App()
