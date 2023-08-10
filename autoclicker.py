import threading
import tkinter as tk
from tkinter import simpledialog
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import time

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")

        # Initialize controller, default values, and hotkey
        self.mouse = Controller()
        self.delay = 0.001
        self.button = Button.right
        self.hotkey = KeyCode(char='c')

        # Define keyboard keys
        self.start_stop_key = KeyCode(char='a')
        self.stop_key = KeyCode(char='b')

        # Create GUI components
        self.start_stop_button = tk.Button(self.root, text="Start Clicking", command=self.toggle_clicking)
        self.change_hotkey_button = tk.Button(self.root, text="Change Hotkey", command=self.change_hotkey)
        self.change_delay_button = tk.Button(self.root, text="Change Delay", command=self.change_delay)
        self.hotkey_label = tk.Label(self.root, text="Hotkey: {}".format(self.hotkey.char))
        self.delay_label = tk.Label(self.root, text="Current Delay: {}".format(self.delay))
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)

        # Place GUI components using grid layout
        self.start_stop_button.grid(row=0, column=0, pady=10)
        self.change_hotkey_button.grid(row=1, column=0, pady=5)
        self.change_delay_button.grid(row=2, column=0, pady=5)
        self.hotkey_label.grid(row=3, column=0, pady=5)
        self.delay_label.grid(row=4, column=0, pady=5)
        self.exit_button.grid(row=5, column=0, pady=5)

        # Create listener for hotkey
        self.listener = Listener(on_press=self.on_key_press)
        self.listener.start()

        # Auto-clicking state and thread
        self.clicking = False
        self.auto_click_thread = None


    def toggle_clicking(self):
        if self.auto_click_thread and self.auto_click_thread.is_alive():
            self.clicking = False
            self.auto_click_thread.join()
            self.start_stop_button.config(text="Start Clicking")
        else:
            self.clicking = True
            self.auto_click_thread = threading.Thread(target=self.auto_click)
            self.auto_click_thread.start()
            self.start_stop_button.config(text="Stop Clicking")

    def auto_click(self):
        while self.clicking:
            self.mouse.click(self.button)
            time.sleep(self.delay)

    def on_key_press(self, key):
        if key == self.hotkey:
            self.toggle_clicking()

    def change_hotkey(self):
        new_hotkey = self.get_new_hotkey()
        if new_hotkey:
            self.hotkey = new_hotkey
            self.hotkey_label.config(text="Hotkey: {}".format(self.hotkey.char))

    def get_new_hotkey(self):
        try:
            hotkey_str = simpledialog.askstring("Change Hotkey", "Enter new hotkey:")
            if hotkey_str:
                return KeyCode(char=hotkey_str)
            else:
                return None
        except ValueError:
            return None

    def change_delay(self):
        new_delay = self.get_new_delay()
        if new_delay is not None:
            self.delay = new_delay
            self.delay_label.config(text="Current Delay: {}".format(self.delay))

    def get_new_delay(self):
        try:
            new_delay = float(simpledialog.askstring("Change Delay", "Enter new delay (in seconds):"))
            return max(0, new_delay)  # Ensure delay is non-negative
        except (ValueError, TypeError):
            return None

    def exit_program(self):
        self.running = False
        if self.auto_click_thread:
            self.auto_click_thread.join()
        self.listener.stop()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
