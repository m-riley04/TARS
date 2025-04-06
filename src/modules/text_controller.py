# typing_gui.py
import tkinter as tk
import queue

def toggle_fullscreen(window: tk.Tk):
    """Toggle fullscreen mode."""
    is_fullscreen = window.attributes("-fullscreen")
    window.attributes("-fullscreen", not is_fullscreen)
    window.focus_set()

class TypingEffectApp:
    def __init__(self, root: tk.Tk, text_queue, delay=20):
        self.root = root
        self.text_queue = text_queue
        self.delay = delay  # in milliseconds
        self.font_size = 50
        
        # Label for listening indicator
        self.listeningLight = tk.Label(root, text="", font=("Courier", self.font_size, "bold"),
                                       fg="red", bg="black")

        # Main text label
        self.label = tk.Label(root, text="", font=("Courier", self.font_size, "bold"),
                              bg="black", fg="green", anchor="nw", justify="left",
                              wraplength=root.winfo_screenwidth())
        self.label.pack(padx=20, pady=20)
        self.listeningLight.pack(padx=20, pady=20)

        # Start in fullscreen and allow toggling with F11
        self.root.attributes("-fullscreen", True)
        root.bind("<F11>", lambda event: toggle_fullscreen(root))

        self.index = 0
        self.full_text = ""
        self.update_text()

    def update_text(self):
        # Check if there's new text to display
        try:
            while True:
                new_message = self.text_queue.get_nowait()
                # If the message indicates listening state, update the light.
                if isinstance(new_message, dict):
                    if "clear" in new_message and new_message["clear"]:
                        self.full_text = ""
                        self.index = 0
                        self.label.config(text=self.full_text)
                    # Check for listening indicator.
                    elif "listening" in new_message:
                        self.update_listening_light(new_message["listening"])
                # Otherwise, assume it's text to display.
                elif isinstance(new_message, str):
                    self.full_text += new_message + "\n"
        except queue.Empty:
            pass

        # Type out the text one character at a time.
        if self.index < len(self.full_text):
            self.index += 1
            self.label.config(text=self.full_text[:self.index])
        
        # Schedule the next update.
        self.root.after(self.delay, self.update_text)
        
    def update_listening_light(self, is_listening):
        """Update the listening light based on the listening state."""
        if is_listening:
            self.listeningLight.config(text="LISTENING", fg="red")
        else:
            self.listeningLight.config(text="", fg="black")

def run_gui(text_queue):
    root = tk.Tk()
    root.title("TARS Display")
    root.configure(background="black")
    app = TypingEffectApp(root, text_queue)
    root.mainloop()
