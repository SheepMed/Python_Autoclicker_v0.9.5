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
        self.hotkey = KeyCode(char='c')  # Hotkey to stop auto-clicking

        self.start_stop_key = KeyCode(char='a')
        self.stop_key = KeyCode(char='b')

        self.start_stop_button = tk.Button(self.root, text="Start Clicking", command=self.toggle_clicking)
        self.start_stop_button.pack(pady=10)

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

    def exit_program(self):
        self.running = False
        if self.auto_click_thread:
            self.auto_click_thread.join()
        self.listener.stop()
        self.root.destroy()

root = tk.Tk()
app = AutoClickerApp(root)
root.mainloop()
