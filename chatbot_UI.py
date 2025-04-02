import tkinter as tk
import time
from tkinter import scrolledtext
from weather_chatbot import chat_bot

window = tk.Tk()
window.title("Weather Chatbot")

# Create a scrolled text widget
chat_history = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10, state=tk.DISABLED)
chat_history.grid(row=0, column=0, columnspan=2, sticky = "nsew")

# adjustable/expandable grid
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Entry box for user input with adjustable height
user_entry = tk.Text(window, height=2, wrap=tk.WORD)
user_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
window.grid_columnconfigure(0, weight=1)

def init_chat():
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"Weather_Bot 🌍: Hello! How can I assist you today?\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.yview(tk.END)

def typing_indicator():
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Weather_Bot 🌍 is typing...\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.yview(tk.END)
    window.update_idletasks()
def remove_typing_indicator():
    """Removes the last line (typing indicator) from the chat."""
    chat_history.config(state=tk.NORMAL)
    lines = chat_history.get("1.0", tk.END).split("\n")
    if lines[-2] == "Weather_Bot 🌍 is typing...":
        chat_history.delete("end-2l", "end-1l")  # Removes 'Weather_Bot is typing...'
    chat_history.config(state=tk.DISABLED)
def process_response(user_input):
    remove_typing_indicator()
        #update chat history
    response = chat_bot(user_input)  
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"Weather_Bot 🌍: {response}\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.yview(tk.END)
#handle button click event
def button_click(event = None):
    user_input = user_entry.get("1.0", tk.END).strip() #get user input from text entry field
    if user_input:
        user_entry.delete("1.0", tk.END) #clear text entry field
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"You 🙂: {user_input}\n")
        chat_history.config(state=tk.DISABLED)
        chat_history.yview(tk.END)
        
        typing_indicator()
        window.after(1000, lambda: process_response(user_input))  # Delay response processing

#creating a send button
button = tk.Button(window, text="Send", width=10, command=button_click)
button.grid(row=1, column=1)

window.bind('<Return>', lambda event: button_click())
window.bind("<Control-v>", lambda event: None)


init_chat()
window.mainloop()
