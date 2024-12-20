import tkinter as tk
from tkinter import messagebox
import time
import threading

# Store reminders in a list
reminders = []

# Event to signal thread termination
stop_event = threading.Event()

# Function to add a reminder
def add_reminder():
    reminder_text = reminder_text_entry.get()
    reminder_time = reminder_time_entry.get()

    if reminder_text and reminder_time:
        reminders.append({"text": reminder_text, "time": reminder_time})
        reminder_list.insert(tk.END, f"{reminder_text} at {reminder_time}")
        reminder_text_entry.delete(0, tk.END)
        reminder_time_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Reminder added: '{reminder_text}' at {reminder_time}")
    else:
        messagebox.showwarning("Warning", "Please fill in both fields.")

# Function to check and trigger reminders
def reminder_checker():
    while not stop_event.is_set():
        current_time = time.strftime("%H:%M")
        for reminder in reminders[:]:
            if reminder["time"] == current_time:
                messagebox.showinfo("Reminder", f"⏰ Reminder: {reminder['text']} at {reminder['time']}!")
                reminders.remove(reminder)
                reminder_list.delete(0, tk.END)
                for rem in reminders:
                    reminder_list.insert(tk.END, f"{rem['text']} at {rem['time']}")
        time.sleep(30)

# Function to view all reminders
def view_reminders():
    for reminder in reminders:
        messagebox.showinfo("Reminder", f"{reminder['text']} at {reminder['time']}")

# Initialize the GUI
root = tk.Tk()
root.title("Reminder App")
root.geometry("400x400")
root.configure(bg="#f4f4f9")

# Title label
title_label = tk.Label(root, text="Reminder App", font=("Arial", 20, "bold"), bg="#f4f4f9", fg="#333")
title_label.pack(pady=10)

# Input fields
input_frame = tk.Frame(root, bg="#f4f4f9")
input_frame.pack(pady=10)

reminder_text_label = tk.Label(input_frame, text="Reminder Text:", bg="#f4f4f9", fg="#333")
reminder_text_label.grid(row=0, column=0, padx=5, pady=5)
reminder_text_entry = tk.Entry(input_frame, width=30)
reminder_text_entry.grid(row=0, column=1, padx=5, pady=5)

reminder_time_label = tk.Label(input_frame, text="Time (HH:MM):", bg="#f4f4f9", fg="#333")
reminder_time_label.grid(row=1, column=0, padx=5, pady=5)
reminder_time_entry = tk.Entry(input_frame, width=30)
reminder_time_entry.grid(row=1, column=1, padx=5, pady=5)

# Buttons
button_frame = tk.Frame(root, bg="#f4f4f9")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Reminder", command=add_reminder, bg="#28a745", fg="white", width=15)
add_button.grid(row=0, column=0, padx=5, pady=5)

view_button = tk.Button(button_frame, text="View Reminders", command=view_reminders, bg="#28a745", fg="white", width=15)
view_button.grid(row=0, column=1, padx=5, pady=5)

# Reminder list
list_frame = tk.Frame(root, bg="#f4f4f9")
list_frame.pack(pady=10)

reminder_list = tk.Listbox(list_frame, width=50, height=10)
reminder_list.pack()

# Start reminder checker in a separate thread
checker_thread = threading.Thread(target=reminder_checker, daemon=True)
checker_thread.start()

# When the main window is closed, signal the thread to stop
def on_closing():
    stop_event.set()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()