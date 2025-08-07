# Import necessary libraries
import customtkinter as ctk
from tkinter import messagebox, PhotoImage # Import PhotoImage for .png icons
from pynput.mouse import Button, Controller
from pynput import keyboard
import time
import threading
import os # Import os module to handle file paths
import sys # Import sys module to check for PyInstaller environment

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

            if current_interval <= 0:
                raise ValueError("Interval must be a positive number.")

            if current_click_type == "single":
                mouse.click(Button.left)
            elif current_click_type == "double":
                mouse.click(Button.left, 2) # 2 for double click
            time.sleep(current_interval)
        except ValueError as ve:
            # If interval is invalid, stop clicking and show error
            stop_clicking()
            messagebox.showerror("Error", f"Invalid interval value: {ve}. Please enter a positive number.")
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
        if key.char == '²':
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
root.title("Autoclicker")
root.geometry("480x380") # Adjusted width for better layout
root.resizable(False, False) # Make window not resizable

# --- Set the application icon ---
# Function to get the correct path for bundled resources
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# IMPORTANT:
# 1. Place your icon file (e.g., 'autoclicker_icon.ico' or 'autoclicker_icon.png')
#    in the SAME directory as your Python script.
# 2. Use the resource_path function to get the correct path at runtime.

icon_filename_ico = "autoclicker_icon.ico"
icon_filename_png = "autoclicker_icon.png"

# Try loading .ico first
icon_path_ico = resource_path(icon_filename_ico)
if os.path.exists(icon_path_ico):
    try:
        root.iconbitmap(icon_path_ico)
    except ctk.TclError:
        print(f"Warning: Could not load .ico icon from {icon_path_ico}. Ensure it's a valid .ico file.")
else:
    print(f"Info: .ico icon file not found at {icon_path_ico}. Trying .png...")
    # Then try loading .png
    icon_path_png = resource_path(icon_filename_png)
    if os.path.exists(icon_path_png):
        try:
            icon_image = PhotoImage(file=icon_path_png)
            root.iconphoto(True, icon_image)
        except Exception as e:
            print(f"Warning: Could not load .png icon from {icon_path_png}. Error: {e}. Ensure Pillow is installed if it's a complex PNG.")
    else:
        print(f"Warning: No icon file found at {icon_filename_ico} or {icon_filename_png}. Using default icon.")


# Main frame to center content
main_frame = ctk.CTkFrame(root, corner_radius=15)
main_frame.pack(pady=25, padx=25, fill="both", expand=True)

# Title Label
title_label = ctk.CTkLabel(main_frame, text="Python Autoclicker", font=ctk.CTkFont(size=24, weight="bold"))
title_label.pack(pady=(20, 10))

# Settings Frame
settings_frame = ctk.CTkFrame(main_frame, corner_radius=10)
settings_frame.pack(pady=10, padx=20, fill="x")
settings_frame.grid_columnconfigure((0, 1, 2), weight=1) # Make columns expand evenly

# Click Type Selection
click_type_label = ctk.CTkLabel(settings_frame, text="Click Type:", font=ctk.CTkFont(size=14))
click_type_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

click_type_var = ctk.StringVar(value="single") # Initialize here
click_type_radio_single = ctk.CTkRadioButton(settings_frame, text="Single", variable=click_type_var, value="single")
click_type_radio_single.grid(row=0, column=1, padx=5, pady=10, sticky="w")

click_type_radio_double = ctk.CTkRadioButton(settings_frame, text="Double", variable=click_type_var, value="double")
click_type_radio_double.grid(row=0, column=2, padx=5, pady=10, sticky="w")

# Interval Input
interval_label = ctk.CTkLabel(settings_frame, text="Interval (seconds):", font=ctk.CTkFont(size=14))
interval_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

interval_var = ctk.DoubleVar(value=1.0) # Initialize here
interval_entry = ctk.CTkEntry(settings_frame, textvariable=interval_var, width=100, font=ctk.CTkFont(size=14))
interval_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

# Control Buttons Frame
control_frame = ctk.CTkFrame(main_frame, corner_radius=10)
control_frame.pack(pady=15, padx=20, fill="x")
control_frame.grid_columnconfigure((0, 1, 2), weight=1) # Make columns expand evenly

start_button = ctk.CTkButton(control_frame, text="Start", command=start_clicking, fg_color="green", hover_color="#229a54", font=ctk.CTkFont(size=16, weight="bold"))
start_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

stop_button = ctk.CTkButton(control_frame, text="Stop", command=stop_clicking, state="disabled", fg_color="red", hover_color="#a53123", font=ctk.CTkFont(size=16, weight="bold"))
stop_button.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

exit_button = ctk.CTkButton(control_frame, text="Exit", command=on_closing, fg_color="gray", hover_color="#6c7a7b", font=ctk.CTkFont(size=16, weight="bold"))
exit_button.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

# Status Label
status_label = ctk.CTkLabel(main_frame, text="Status: Stopped", text_color="red", font=ctk.CTkFont(size=16, weight="bold"))
status_label.pack(pady=10)

# Hotkey Info
hotkey_info_label = ctk.CTkLabel(main_frame, text="Hotkey: Press '²' to toggle Start/Stop", text_color="gray", font=ctk.CTkFont(size=12, slant="italic"))
hotkey_info_label.pack(pady=5)

# Initialize keyboard listener in a non-blocking way
keyboard_listener = keyboard.Listener(on_press=on_hotkey_press)
keyboard_listener.start() # Start the listener thread

# Handle window closing
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Custom Tkinter event loop
root.mainloop()
