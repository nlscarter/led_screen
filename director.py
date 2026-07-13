import tkinter as tk

root = tk.Tk()
root.title("LED Screen")

label = tk.Label(
    root,
    text="Hello, World!",
    font=("Arial", 48),
    padx=40,
    pady=40
)

label.pack(expand=True)

root.mainloop()