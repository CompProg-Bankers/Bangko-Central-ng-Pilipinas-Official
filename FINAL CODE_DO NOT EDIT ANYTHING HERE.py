import tkinter as tk
from tkinter import messagebox
from datetime import datetime

now = datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")

# CREATE FILE
try:
    with open("Banker.txt", "x") as file:
        print("File created successfully.")
except FileExistsError:
    print("File already exists.")

# COLORS & FONT
BG = "#fbf4eb"
ENTRY_BG = "#fbd9eb"
FG = "#c43670"
FONT = ("Courier New", 9)
FONT_TITLE = ("Courier New", 13, "bold")

# SHARED STATE
logged_in_user = {"first": "", "last": ""}


# VALIDATE PASSWORD
def validatePassword(password):
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(not c.isalnum() for c in password):
        return False
    return True


# ==================== WINDOW 1: LOGIN / REGISTER ====================

def open_window1():
    win1 = tk.Tk()
    win1.title("Bangko Central ng Pilipinas")
    win1.geometry("420x340")
    win1.config(bg=BG)
    win1.resizable(False, False)

    tk.Label(win1, text="Bangko Central ng Pilipinas", font=FONT_TITLE, bg=BG, fg=FG).pack(pady=(18, 4))
    tk.Label(win1, text="─" * 44, bg=BG, fg="#e0b0c8", font=("Courier New", 8)).pack()

    # entries
    tk.Label(win1, text="First Name", font=FONT, bg=BG).pack(pady=(12, 1))
    e_first = tk.Entry(win1, bg=ENTRY_BG, fg=FG, font=FONT, width=28)
    e_first.pack()

    tk.Label(win1, text="Last Name", font=FONT, bg=BG).pack(pady=(6, 1))
    e_last = tk.Entry(win1, bg=ENTRY_BG, fg=FG, font=FONT, width=28)
    e_last.pack()

    tk.Label(win1, text="Password", font=FONT, bg=BG).pack(pady=(6, 1))
    e_pass = tk.Entry(win1, bg=ENTRY_BG, fg=FG, font=FONT, width=28, show="*")
    e_pass.pack()

    def togglePass():
        e_pass.config(show="" if e_pass.cget("show") == "*" else "*")

    tk.Button(win1, text="Show / Hide Password", command=togglePass,
              bg=ENTRY_BG, fg=FG, font=("Courier New", 7), relief="flat", cursor="hand2").pack(pady=(3, 0))

    tk.Label(win1, text="Password: 8+ chars, 1 uppercase, 1 special character",
             font=("Courier New", 6), bg=BG, fg="#999").pack()

    # REGISTER
    def do_register():
        first = e_first.get().strip().title()
        last = e_last.get().strip().title()
        password = e_pass.get()

        if not first or not last or not password:
            messagebox.showerror("Error", "Please fill in all fields.", parent=win1)
            return

        try:
            with open("Banker.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 2 and parts[0] == first and parts[1] == last:
                        messagebox.showerror("Error", "Account already exists. Please log in.", parent=win1)
                        return
        except FileNotFoundError:
            pass

        if not validatePassword(password):
            messagebox.showerror("Error", "Invalid password. Must be 8+ chars, 1 uppercase, 1 special character.", parent=win1)
            return

        with open("Banker.txt", "a") as f:
            f.write(f"{first},{last},{password},0\n")  # balance starts at 0

        messagebox.showinfo("Success", f"Registered successfully! Welcome, {first} {last}!", parent=win1)

    # LOGIN → goes to Window 2
    def do_login():
        first = e_first.get().strip().title()
        last = e_last.get().strip().title()
        password = e_pass.get()

        if not first or not last or not password:
            messagebox.showerror("Error", "Please fill in all fields.", parent=win1)
            return

        try:
            with open("Banker.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 3 and parts[0] == first and parts[1] == last and parts[2] == password:
                        logged_in_user["first"] = first
                        logged_in_user["last"] = last
                        messagebox.showinfo("Success", f"Welcome back, {first} {last}!", parent=win1)
                        win1.destroy()
                        open_window2()
                        return
        except FileNotFoundError:
            pass

        messagebox.showerror("Error", "Invalid credentials. Try again.", parent=win1)

    btn_frame = tk.Frame(win1, bg=BG)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="  Log In  ", command=do_login,
              bg=FG, fg="white", font=FONT, relief="flat", cursor="hand2", padx=6).grid(row=0, column=0, padx=6)
    tk.Button(btn_frame, text="  Register  ", command=do_register,
              bg=ENTRY_BG, fg=FG, font=FONT, relief="flat", cursor="hand2", padx=6).grid(row=0, column=1, padx=6)

    win1.mainloop()


# ==================== WINDOW 2: DETAILS ====================

def open_window2():
    win2 = tk.Tk()
    win2.title("Account Details")
    win2.geometry("420x300")
    win2.config(bg=BG)
    win2.resizable(False, False)

    first = logged_in_user["first"]
    last = logged_in_user["last"]

    tk.Label(win2, text="Account Details", font=FONT_TITLE, bg=BG, fg=FG).pack(pady=(18, 4))
    tk.Label(win2, text="─" * 44, bg=BG, fg="#e0b0c8", font=("Courier New", 8)).pack()

    info_frame = tk.Frame(win2, bg=BG)
    info_frame.pack(pady=14)

    def row(label, value):
        tk.Label(info_frame, text=f"{label:<14}", font=FONT, bg=BG, fg="#888", anchor="w").grid(
            row=row.n, column=0, sticky="w", padx=(20, 6), pady=3)
        tk.Label(info_frame, text=value, font=("Courier New", 9, "bold"), bg=BG, fg=FG, anchor="w").grid(
            row=row.n, column=1, sticky="w", pady=3)
        row.n += 1
    row.n = 0

    row("First Name :", first)
    row("Last Name  :", last)

    # Read balance from file
    balance = "0.00"
    try:
        with open("Banker.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 4 and parts[0] == first and parts[1] == last:
                    balance = parts[3]
    except FileNotFoundError:
        pass

    row("Balance    :", f"₱ {float(balance):,.2f}")

    def go_deposit():
        win2.destroy()
        open_window3()

    def go_logout():
        win2.destroy()
        open_window1()

    btn_frame = tk.Frame(win2, bg=BG)
    btn_frame.pack(pady=14)
    tk.Button(btn_frame, text="  Deposit  ", command=go_deposit,
              bg=FG, fg="white", font=FONT, relief="flat", cursor="hand2", padx=6).grid(row=0, column=0, padx=6)
    tk.Button(btn_frame, text="  Log Out  ", command=go_logout,
              bg=ENTRY_BG, fg=FG, font=FONT, relief="flat", cursor="hand2", padx=6).grid(row=0, column=1, padx=6)

    win2.mainloop()


# ==================== WINDOW 3: DEPOSIT ====================

def open_window3():
    win3 = tk.Tk()
    win3.title("Deposit")
    win3.geometry("420x320")
    win3.config(bg=BG)
    win3.resizable(False, False)

    first = logged_in_user["first"]
    last = logged_in_user["last"]

    tk.Label(win3, text="Deposit Money", font=FONT_TITLE, bg=BG, fg=FG).pack(pady=(18, 4))
    tk.Label(win3, text="─" * 44, bg=BG, fg="#e0b0c8", font=("Courier New", 8)).pack()

    # Read current balance
    lines = []
    current_balance = 0.0
    user_line_index = -1

    try:
        with open("Banker.txt", "r") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            parts = line.strip().split(",")
            if len(parts) >= 4 and parts[0] == first and parts[1] == last:
                current_balance = float(parts[3])
                user_line_index = i
    except FileNotFoundError:
        pass

    bal_var = tk.StringVar(value=f"₱ {current_balance:,.2f}")
    tk.Label(win3, text="Current Balance", font=FONT, bg=BG, fg="#888").pack(pady=(12, 0))
    tk.Label(win3, textvariable=bal_var, font=("Courier New", 14, "bold"), bg=BG, fg=FG).pack()

    tk.Label(win3, text="Amount to Deposit", font=FONT, bg=BG).pack(pady=(12, 1))
    e_amount = tk.Entry(win3, bg=ENTRY_BG, fg=FG, font=FONT, width=22)
    e_amount.pack()

    def do_deposit():
        nonlocal current_balance, user_line_index, lines
        raw = e_amount.get().strip()
        if not raw:
            messagebox.showerror("Error", "Please enter an amount.", parent=win3)
            return
        try:
            amount = float(raw)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive amount.", parent=win3)
            return

        current_balance += amount
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update balance in Banker.txt
        if user_line_index >= 0:
            parts = lines[user_line_index].strip().split(",")
            parts[3] = f"{current_balance:.2f}"
            lines[user_line_index] = ",".join(parts) + "\n"
            with open("Banker.txt", "w") as f:
                f.writelines(lines)

        # Log transaction
        with open("bank.txt", "a") as f:
            f.write(f"{first} {last} | Deposit: ₱{amount:,.2f} | Balance: ₱{current_balance:,.2f} | {now_str}\n")

        bal_var.set(f"₱ {current_balance:,.2f}")
        e_amount.delete(0, tk.END)
        messagebox.showinfo("Success", f"Deposited ₱{amount:,.2f}\nNew Balance: ₱{current_balance:,.2f}", parent=win3)

    def go_back():
        win3.destroy()
        open_window2()

    btn_frame = tk.Frame(win3, bg=BG)
    btn_frame.pack(pady=12)
    tk.Button(btn_frame, text="  Confirm Deposit  ", command=do_deposit,
              bg=FG, fg="white", font=FONT, relief="flat", cursor="hand2", padx=6).grid(row=0, column=0, padx=6)
    tk.Button(btn_frame, text="  Back  ", command=go_back,
              bg=ENTRY_BG, fg=FG, font=FONT, relief="flat", cursor="hand2", padx=6).grid(row=0, column=1, padx=6)

    win3.mainloop()


# ==================== START ====================
open_window1()