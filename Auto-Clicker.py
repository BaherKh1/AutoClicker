# Import necessary libraries
import customtkinter as ctk
from tkinter import messagebox
from pynput.mouse import Button, Controller
from pynput import keyboard
import time
import threading

# Set appearance mode and default color theme for Custom Tkinter
ctk.set_appearance_mode("System")  # Can be "System", "Dark", "Light"
ctk.set_default_color_theme("blue") # Can be "blue", "green", "dark-blue"

# Initialize mouse controller
mouse = Controller()

# Global variables for controlling the autoclicker
running = False
click_thread = None # To hold the reference to the clicking thread
keyboard_listener = None # To hold the reference to the keyboard listener

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
        # Start the clicker thread
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

            if current_click_type == "single":
                mouse.click(Button.left)
            elif current_click_type == "double":
                mouse.click(Button.left, 2) # 2 for double click
            time.sleep(current_interval)
        except ValueError:
            # If interval is invalid, stop clicking and show error
            stop_clicking()
            messagebox.showerror("Error", "Invalid interval value. Please enter a number.")
            break # Exit the clicking loop
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
        # Toggle autoclicker with 's' hotkey
        if key.char == 's':
            if not running:
                start_clicking()
            else:
                stop_clicking()
    except AttributeError:
        # Handle special keys, if needed (e.g., F1, F2)
        pass

def on_closing():
    """
    Handles the window closing event.
    """
    global running, keyboard_listener
    if running:
        stop_clicking()
    if keyboard_listener:
        keyboard_listener.stop() # Stop the pynput listener
    root.destroy()

# --- GUI Setup ---
root = ctk.CTk()
root.title("Python Autoclicker")
root.geometry("450x350")
root.resizable(False, False) # Make window not resizable

# Variables for GUI elements
click_type_var = ctk.StringVar(value="single")
interval_var = ctk.DoubleVar(value=1.0) # Use DoubleVar for float input

# Frame for settings
settings_frame = ctk.CTkFrame(root, corner_radius=10)
settings_frame.pack(pady=20, padx=20, fill="x", expand=True)

# Click Type Selection
click_type_label = ctk.CTkLabel(settings_frame, text="Click Type:")
click_type_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

click_type_radio_single = ctk.CTkRadioButton(settings_frame, text="Single", variable=click_type_var, value="single")
click_type_radio_single.grid(row=0, column=1, padx=10, pady=10, sticky="w")

click_type_radio_double = ctk.CTkRadioButton(settings_frame, text="Double", variable=click_type_var, value="double")
click_type_radio_double.grid(row=0, column=2, padx=10, pady=10, sticky="w")

# Interval Input
interval_label = ctk.CTkLabel(settings_frame, text="Interval (seconds):")
interval_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

interval_entry = ctk.CTkEntry(settings_frame, textvariable=interval_var, width=150)
interval_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

# Control Buttons Frame
control_frame = ctk.CTkFrame(root, corner_radius=10)
control_frame.pack(pady=10, padx=20, fill="x", expand=True)

start_button = ctk.CTkButton(control_frame, text="Start (s)", command=start_clicking, fg_color="green", hover_color="#229a54")
start_button.pack(side="left", padx=10, pady=10, expand=True)

stop_button = ctk.CTkButton(control_frame, text="Stop (s)", command=stop_clicking, state="disabled", fg_color="red", hover_color="#a53123")
stop_button.pack(side="left", padx=10, pady=10, expand=True)

exit_button = ctk.CTkButton(control_frame, text="Exit", command=on_closing, fg_color="gray", hover_color="#6c7a7b")
exit_button.pack(side="left", padx=10, pady=10, expand=True)

# Status Label
status_label = ctk.CTkLabel(root, text="Status: Stopped", text_color="red", font=ctk.CTkFont(size=16, weight="bold"))
status_label.pack(pady=10)

# Hotkey Info
hotkey_info_label = ctk.CTkLabel(root, text="Hotkey: Press 's' to toggle Start/Stop", text_color="gray", font=ctk.CTkFont(size=10, slant="italic"))
hotkey_info_label.pack(pady=5)

# Initialize keyboard listener in a non-blocking way
keyboard_listener = keyboard.Listener(on_press=on_hotkey_press)
keyboard_listener.start() # Start the listener thread

# Handle window closing
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Custom Tkinter event loop
root.mainloop()
