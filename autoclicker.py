import threading
import tkinter as tk
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import time

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")

        self.mouse = Controller()
        self.delay = 0.001
        self.button = Button.right
        self.running = False
        self.hotkey = KeyCode(char='c')  # Default hotkey

        self.start_stop_key = KeyCode(char='a')
        self.stop_key = KeyCode(char='b')

        self.start_stop_button = tk.Button(self.root, text="Start Clicking", command=self.toggle_clicking)
        self.start_stop_button.pack(pady=10)

        self.change_hotkey_button = tk.Button(self.root, text="Change Hotkey", command=self.change_hotkey)
        self.change_hotkey_button.pack(pady=5)

        self.hotkey_label = tk.Label(self.root, text="Hotkey: {}".format(self.hotkey.char))
        self.hotkey_label.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=5)

        self.listener = Listener(on_press=self.on_key_press)
        self.listener.start()

        self.clicking = False  # To keep track of the auto-clicking loop
        self.auto_click_thread = None  # Thread for auto-clicking

    def toggle_clicking(self):
        self.running = not self.running
        if self.running:
            self.start_stop_button.config(text="Stop Clicking")
            self.clicking = True
            self.auto_click_thread = threading.Thread(target=self.auto_click)
            self.auto_click_thread.start()
        else:
            self.start_stop_button.config(text="Start Clicking")
            self.clicking = False
            if self.auto_click_thread:
                self.auto_click_thread.join()
                self.auto_click_thread = None

    def auto_click(self):
        while self.clicking:
            self.mouse.click(self.button)
            time.sleep(self.delay)

    def on_key_press(self, key):
        if key == self.start_stop_key:
            self.toggle_clicking()
        elif key == self.stop_key:
            self.running = False
            self.clicking = False
            if self.auto_click_thread:
                self.auto_click_thread.join()
                self.auto_click_thread = None
        elif key == self.hotkey:
            if self.running:
                self.running = False
                self.clicking = False
                if self.auto_click_thread:
                    self.auto_click_thread.join()
                    self.auto_click_thread = None
                self.root.after(0, self.update_start_stop_button_text, "Start Clicking")

    def update_start_stop_button_text(self, text):
        self.start_stop_button.config(text=text)

    def change_hotkey(self):
        new_hotkey = self.get_new_hotkey()
        if new_hotkey:
            self.hotkey = new_hotkey
            self.hotkey_label.config(text="Hotkey: {}".format(self.hotkey.char))

    def get_new_hotkey(self):
        def on_new_hotkey_press(key):
            nonlocal new_key
            new_key = key
            listener.stop()

        new_key = None
        listener = Listener(on_press=on_new_hotkey_press)
        listener.start()

        while new_key is None:
            time.sleep(0.1)

        return new_key

    def exit_program(self):
        self.running = False
        if self.auto_click_thread:
            self.auto_click_thread.join()
        self.listener.stop()
        self.root.destroy()

root = tk.Tk()
app = AutoClickerApp(root)
root.mainloop()
#yeet
