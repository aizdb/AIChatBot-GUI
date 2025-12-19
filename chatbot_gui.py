# chatbot_gui.py
# AIChatBot Pro - GUI version with Tkinter

import re
from collections import deque
import tkinter as tk
from tkinter import scrolledtext

# --- NLU ---
class SimpleNLU:
    def __init__(self):
        self.patterns = {
            "greet": r"\b(hi|hello|hey|سلام)\b",
            "bye": r"\b(bye|goodbye|خداحافظ)\b",
            "calc": r"(\d+(?:\.\d+)?\s*[\+\-\*\/]\s*\d+(?:\.\d+)?)",
            "memory": r"\b(remember|notes|forget|list)\b"
        }

    def detect_intent(self, text):
        for intent, pattern in self.patterns.items():
            if re.search(pattern, text, re.I):
                return intent
        return "unknown"

# --- Memory ---
class Memory:
    def __init__(self, capacity=10):
        self.turns = deque(maxlen=capacity)
        self.notes = []

    def add_turn(self, role, text):
        self.turns.append({"role": role, "text": text})

    def add_note(self, note):
        self.notes.append(note)

    def list_notes(self):
        return self.notes

    def clear_notes(self):
        self.notes.clear()

# --- ChatBot ---
class ChatBot:
    def __init__(self):
        self.nlu = SimpleNLU()
        self.memory = Memory()

    def handle(self, user_text):
        self.memory.add_turn("user", user_text)
        intent = self.nlu.detect_intent(user_text)

        if intent == "greet":
            reply = "Hello! How can I help you?"
        elif intent == "bye":
            reply = "Goodbye!"
        elif intent == "calc":
            try:
                reply = f"Result: {eval(user_text, {'__builtins__': None}, {})}"
            except Exception:
                reply = "Invalid calculation."
        elif intent == "memory":
            if "remember" in user_text.lower():
                note = user_text.replace("remember", "").strip()
                self.memory.add_note(note)
                reply = "Got it, I’ll remember that."
            elif "list" in user_text.lower():
                notes = self.memory.list_notes()
                reply = "Notes:\n" + "\n".join(notes) if notes else "No notes yet."
            elif "forget" in user_text.lower():
                self.memory.clear_notes()
                reply = "All notes cleared."
            else:
                reply = "Memory commands: remember, list, forget."
        else:
            reply = "I didn’t understand. Try greeting, math, or notes."

        self.memory.add_turn("bot", reply)
        return reply

# --- GUI ---
def send_message(event=None):
    user_text = entry.get()
    if not user_text: return
    chat_window.insert(tk.END, f"You: {user_text}\n", "user")
    reply = bot.handle(user_text)
    chat_window.insert(tk.END, f"Bot: {reply}\n", "bot")
    entry.delete(0, tk.END)
    chat_window.see(tk.END)

def clear_chat():
    chat_window.delete("1.0", tk.END)

bot = ChatBot()

root = tk.Tk()
root.title("AIChatBot Pro")
root.configure(bg="#1e1e1e")

chat_window = scrolledtext.ScrolledText(root, width=70, height=20, bg="#252526", fg="#d4d4d4", font=("Consolas", 11))
chat_window.pack(padx=10, pady=10)
chat_window.tag_config("user", foreground="#569CD6")
chat_window.tag_config("bot", foreground="#6A9955")

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(padx=10, pady=10)

entry = tk.Entry(frame, width=50, font=("Consolas", 11))
entry.pack(side=tk.LEFT, padx=5)
entry.bind("<Return>", send_message)

send_btn = tk.Button(frame, text="Send", command=send_message, bg="#007ACC", fg="white")
send_btn.pack(side=tk.LEFT, padx=5)

clear_btn = tk.Button(frame, text="Clear Chat", command=clear_chat, bg="#D83B01", fg="white")
clear_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()
