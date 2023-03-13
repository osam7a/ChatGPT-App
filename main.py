import tkinter as tk
import openai as ai
import customtkinter as ctk
import threading

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")
ai.api_key = open("api_key.txt", "r").readlines()[0]

class ChatGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.create_widgets()
        self.history = []

    def create_widgets(self):
        self.main = ctk.CTkFrame(self)

        self.chatlog = ctk.CTkTextbox(self.main, font=("Arial", 20), wrap=tk.WORD)
        self.chatlog.pack(expand=1, fill=tk.BOTH)
        self.chatlog.configure(state=tk.DISABLED)

        self.entries = ctk.CTkFrame(self.main)

        self.userentry = ctk.CTkEntry(self.entries, font=("Arial", 20))
        self.userentry.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.userentry.bind("<Return>", self.send_return)

        self.sendbutton = ctk.CTkButton(self.entries, text="Send", command=self.send, font=("Arial", 20))
        self.sendbutton.pack(side=tk.LEFT, fill=tk.BOTH)

        self.entries.pack(fill=tk.BOTH)

        self.main.pack(fill=tk.BOTH, expand=1, padx=32, pady=32)

    def send_return(self, e):
        self.send()

    def send(self):
        usermsg = self.userentry.get()
        if len(usermsg) == 0: return
        self.userentry.delete(0, tk.END)
        self.chatlog.configure(state=tk.NORMAL)
        self.chatlog.insert(tk.END, 'You: ' + usermsg + '\n')
        self.chatlog.configure(state=tk.DISABLED)
        threading.Thread(target=self.process_message, args=(usermsg,)).start()

    def process_message(self, usermsg):
        msgs = []
        for message in self.history:
            msgs.append(message)
        msgs.append({"role": "user", "content": usermsg})
        chat = ai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=msgs
        )
        dummy_response = chat.choices[0].message['content'].strip()
        self.chatlog.configure(state=tk.NORMAL)
        self.chatlog.insert(tk.END, 'AI: ' + dummy_response + '\n')
        self.chatlog.configure(state=tk.DISABLED)
        self.chatlog.yview(tk.END)

root = ChatGui()
root.mainloop()