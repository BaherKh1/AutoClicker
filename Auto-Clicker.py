import customtkinter as ctk
from tkinter import messagebox
from pynput.mouse import Button, Controller
from pynput import keyboard
import time
import threading

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 

mouse = Controller()

running = False
click_thread = None 
keyboard_listener = None 

def start_clicking():
    """
    Starts the autoclicker thread.
    """
    global running, click_thread
    if not running:
        running = True
        status_label.configure(text="Status: Running...", text_color="green")
        start_button.configure(state="disabled")
        stop_button.configure(state="normal")

        click_thread = threading.Thread(target=clicker_task, daemon=True)
        click_thread.start()
        print("Autoclicker started!")

def stop_clicking():
    """
    Stops the autoclicker thread.
    """
    global running
    if running:
        running = False
        status_label.configure(text="Status: Stopped", text_color="red")
        start_button.configure(state="normal")
        stop_button.configure(state="disabled")
        print("Autoclicker stopped.")

def clicker_task():
    """
    This function runs in a separate thread and performs the clicks.
    """
    while running:
        try:
            current_interval = float(interval_entry.get())
            current_click_type = click_type_var.get()

            if current_interval <= 0:
                raise ValueError("Interval must be a positive number.")

            if current_click_type == "single":
                mouse.click(Button.left)
            elif current_click_type == "double":
                mouse.click(Button.left, 2) 
            time.sleep(current_interval)
        except ValueError as ve:

            stop_clicking()
            messagebox.showerror("Error", f"Invalid interval value: {ve}. Please enter a positive number.")
            break 
        except Exception as e:
            print(f"An error occurred during clicking: {e}")
            stop_clicking()
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            break

def on_hotkey_press(key):
    """
    This function handles hotkey presses to start/stop the autoclicker.
    """
    global running

    try:

        if key.char == 'e':
            if not running:
                start_clicking()
            else:
                stop_clicking()
    except AttributeError:

        pass

def on_closing():
    """
    Handles the window closing event.
    """
    global running, keyboard_listener
    if running:
        stop_clicking()
    if keyboard_listener:
        keyboard_listener.stop() 
    root.destroy()

root = ctk.CTk()
root.title("Autoclicker")
root.geometry("400x380") 
root.resizable(False, False) 

main_frame = ctk.CTkFrame(root, corner_radius=15)
main_frame.pack(pady=25, padx=25, fill="both", expand=True)

title_label = ctk.CTkLabel(main_frame, text="Python Autoclicker", font=ctk.CTkFont(size=24, weight="bold"))
title_label.pack(pady=(20, 10))

settings_frame = ctk.CTkFrame(main_frame, corner_radius=10)
settings_frame.pack(pady=10, padx=20, fill="x")
settings_frame.grid_columnconfigure((0, 1, 2), weight=1) 

click_type_label = ctk.CTkLabel(settings_frame, text="Click Type:", font=ctk.CTkFont(size=14))
click_type_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

click_type_var = ctk.StringVar(value="single") 
click_type_radio_single = ctk.CTkRadioButton(settings_frame, text="Single", variable=click_type_var, value="single")
click_type_radio_single.grid(row=0, column=1, padx=5, pady=10, sticky="w")

click_type_radio_double = ctk.CTkRadioButton(settings_frame, text="Double", variable=click_type_var, value="double")
click_type_radio_double.grid(row=0, column=2, padx=5, pady=10, sticky="w")

interval_label = ctk.CTkLabel(settings_frame, text="Interval (seconds):", font=ctk.CTkFont(size=14))
interval_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

interval_var = ctk.DoubleVar(value=1.0) 
interval_entry = ctk.CTkEntry(settings_frame, textvariable=interval_var, width=100, font=ctk.CTkFont(size=14))
interval_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

control_frame = ctk.CTkFrame(main_frame, corner_radius=10)
control_frame.pack(pady=15, padx=20, fill="x")
control_frame.grid_columnconfigure((0, 1, 2), weight=1) 

start_button = ctk.CTkButton(control_frame, text="Start", command=start_clicking, fg_color="green", hover_color="#229a54", font=ctk.CTkFont(size=16, weight="bold"))
start_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

stop_button = ctk.CTkButton(control_frame, text="Stop", command=stop_clicking, state="disabled", fg_color="red", hover_color="#a53123", font=ctk.CTkFont(size=16, weight="bold"))
stop_button.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

exit_button = ctk.CTkButton(control_frame, text="Exit", command=on_closing, fg_color="gray", hover_color="#6c7a7b", font=ctk.CTkFont(size=16, weight="bold"))
exit_button.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

status_label = ctk.CTkLabel(main_frame, text="Status: Stopped", text_color="red", font=ctk.CTkFont(size=16, weight="bold"))
status_label.pack(pady=10)

hotkey_info_label = ctk.CTkLabel(main_frame, text="Hotkey: Press 'E' to toggle Start/Stop", text_color="gray", font=ctk.CTkFont(size=11, slant="italic"))
hotkey_info_label.pack(pady=5)

keyboard_listener = keyboard.Listener(on_press=on_hotkey_press)
keyboard_listener.start() 

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()