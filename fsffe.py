#GUI NI AYAW NI HILABTI PLS KAY I INSERT PANI NAKO SA PIKAS I REPEAT AYAW  HILABTI KAMULO PAKO CODE ANI



import tkinter as tk
from tkinter import messagebox


def register():
    firstName = entry_first.get().strip()
    lastName = entry_last.get().strip()
    passWord = entry_password.get().strip()





root = tk.Tk()
root.title("Bangko Central ng Pilipinas")
root.geometry("400x300")
root.config(bg="#fbf4eb")

tk.Label(root, text="First Name ", font=("Courier New", 8)).pack()
entry_first = tk.Entry(root, bg="#fbd9eb", fg="#c43670", font=("Courier New", 8))
entry_first.pack()

tk.Label(root, text="Last Name ", font=("Courier New", 8)).pack()
entry_last = tk.Entry(root, bg="#fbd9eb", fg="#c43670", font=("Courier New", 8))
entry_last.pack()

tk.Label(root, text="Password ", font=("Courier New", 8)).pack()
entry_password = tk.Entry(root, bg="#fbd9eb", fg="#c43670", font=("Courier New", 8), show="*")
entry_password.pack()

def togglePass():
    if entry_password.cget("show") == "*":
        entry_password.config(show="")
    else:
        entry_password.config(show="*")
tk.Button(root, text="Show/Hide Password", command=togglePass, bg="#fbd9eb", fg="#c43670", font=("Courier New", 8)).pack()



register()
root.mainloop()