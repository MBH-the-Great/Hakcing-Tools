import tkinter as tk
from tkinter import scrolledtext
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
import datetime

# --- Load model and tokenizer ---
model_name = "microsoft/DialoGPT-medium"  # You can replace with another local model for more freedom
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

chat_history_ids = None

# --- Logging setup ---
log_file = "chat_log.txt"
if os.path.exists(log_file):
    open(log_file, "w", encoding="utf-8").close()

def save_log(user_text, bot_text):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()}\nYou: {user_text}\nBot: {bot_text}\n\n")

# --- GUI setup ---
root = tk.Tk()
root.title("Unrestricted Chatbot")

# Chat display
chat_display = scrolledtext.ScrolledText(root, state='disabled', width=80, height=20, wrap='word')
chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Input box
user_input = tk.Entry(root, width=70)
user_input.grid(row=1, column=0, padx=10, pady=10)

# Send button
def send_message(event=None):
    global chat_history_ids

    text = user_input.get().strip()
    if text.lower() in ["exit", "quit", "bye"]:
        root.destroy()
        return

    if not text:
        return

    # Display user message
    chat_display.config(state='normal')
    chat_display.insert(tk.END, f"You: {text}\n")
    chat_display.config(state='disabled')
    chat_display.yview(tk.END)

    # Encode input
    new_input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    # Generate reply
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )
    bot_reply = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Display bot reply
    chat_display.config(state='normal')
    chat_display.insert(tk.END, f"Bot: {bot_reply}\n\n")
    chat_display.config(state='disabled')
    chat_display.yview(tk.END)

    # Save log
    save_log(text, bot_reply)
    user_input.delete(0, tk.END)

user_input.bind("<Return>", send_message)
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Start GUI loop
root.mainloop()
