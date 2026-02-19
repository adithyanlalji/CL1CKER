import threading
import time
import tkinter as tk
from tkinter import messagebox

try:
    from pynput.mouse import Controller as MouseController, Button
    from pynput import keyboard
except ImportError:
    raise ImportError("Please install pynput (pip install pynput) to run this script.")


class AutoClickerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Insane 100 CPS Autoclicker")
        self.mouse = MouseController()

        # state
        self.running_left = False
        self.running_right = False
        self.thread_left = None
        self.thread_right = None

        # default keybinds
        self.key_left = 'f6'
        self.key_right = 'f7'

        self.build_ui()
        self.listener = keyboard.Listener(on_press=self.on_key)
        self.listener.start()

    def build_ui(self):
        # crazy colored frame & title for insane UI
        frame = tk.Frame(self.master, padx=10, pady=10, bg="#222")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="🔥 Insane Autoclicker Settings 🔥", fg="#ff4081", bg="#222", font=("Comic Sans MS", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        tk.Label(frame, text="Template CPS (fixed at 100):", fg="#eee", bg="#222", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        tk.Label(frame, text="100", fg="#0f0", bg="#222", font=("Arial", 12, "bold")).grid(row=1, column=1, sticky="w")

        # left clicker keybind
        tk.Label(frame, text="Left click toggle key:", fg="#eee", bg="#222").grid(row=2, column=0, sticky="w")
        self.left_key_entry = tk.Entry(frame, width=10)
        self.left_key_entry.insert(0, self.key_left)
        self.left_key_entry.grid(row=2, column=1, sticky="w")

        # right clicker keybind
        tk.Label(frame, text="Right click toggle key (optional):", fg="#eee", bg="#222").grid(row=3, column=0, sticky="w")
        self.right_key_entry = tk.Entry(frame, width=10)
        self.right_key_entry.insert(0, self.key_right)
        self.right_key_entry.grid(row=3, column=1, sticky="w")

        tk.Button(frame, text="Apply Keybinds", command=self.apply_keybinds, bg="#ff4081", fg="#fff").grid(row=4, column=0, columnspan=2, pady=(5, 10))

        self.status_label = tk.Label(frame, text="Status: Stopped", fg="red", bg="#222", font=("Arial", 12, "bold"))
        self.status_label.grid(row=5, column=0, columnspan=2)

        tk.Label(frame, text="Instructions:", fg="#eee", bg="#222").grid(row=6, column=0, sticky="nw", pady=(10,0))
        tk.Label(frame, text="Press the configured keys (left/right) to toggle the respective autoclicker.\nLeft-clicker uses 100 CPS; Right is optional.", fg="#ccc", bg="#222").grid(row=6, column=1, sticky="w", pady=(10,0))

    def apply_keybinds(self):
        left = self.left_key_entry.get().strip().lower()
        right = self.right_key_entry.get().strip().lower()

        if left == right and left:
            messagebox.showerror("Keybind Error", "Left and right keybinds cannot be the same.")
            return
        self.key_left = left
        self.key_right = right
        messagebox.showinfo("Keybinds Applied", f"Left -> {self.key_left}\nRight -> {self.key_right}")

    def on_key(self, key):
        try:
            k = key.char
        except AttributeError:
            k = key.name
        if k == self.key_left:
            self.toggle_left()
        elif k == self.key_right:
            self.toggle_right()

    def toggle_left(self):
        if self.running_left:
            self.running_left = False
            self.status_update()
        else:
            self.running_left = True
            self.thread_left = threading.Thread(target=self.click_loop, args=(Button.left, lambda: self.running_left))
            self.thread_left.daemon = True
            self.thread_left.start()
            self.status_update()

    def toggle_right(self):
        if self.key_right == "":
            return
        if self.running_right:
            self.running_right = False
            self.status_update()
        else:
            self.running_right = True
            self.thread_right = threading.Thread(target=self.click_loop, args=(Button.right, lambda: self.running_right))
            self.thread_right.daemon = True
            self.thread_right.start()
            self.status_update()

    def click_loop(self, button, should_run):
        # 100 clicks per second -> interval 0.01
        interval = 1.0 / 100.0
        while should_run():
            self.mouse.click(button)
            time.sleep(interval)

    def status_update(self):
        parts = []
        if self.running_left:
            parts.append("Left=ON")
        if self.running_right:
            parts.append("Right=ON")
        if not parts:
            self.status_label.config(text="Status: Stopped", fg="red")
        else:
            self.status_label.config(text="Status: " + ",".join(parts), fg="green")

    def on_closing(self):
        self.running_left = False
        self.running_right = False
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()