import tkinter as tk
import time

class TypingEffectApp:
    def __init__(self, root, text, delay=0.1):
        self.root = root
        self.text = text
        self.delay = delay

        self.label = tk.Label(root, text="", font=("Courier", 16), width=50, height=10, anchor="nw", justify="left")
        self.label.pack(padx=20, pady=20)
        
        self.index = 0
        self.update_text()

    def update_text(self):
        if self.index < len(self.text):
            # Add one character at a time
            self.label.config(text=self.text[:self.index+1])
            self.index += 1
            # Call this method again after the delay
            self.root.after(int(self.delay * 1000), self.update_text)

def main():
    root = tk.Tk()
    root.title("Typing Effect GUI")

    text = "Initializing system... \nTARS online. \nHow can I assist you?"

    app = TypingEffectApp(root, text)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
