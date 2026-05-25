import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import getpass

# ── FILES ──────────────────────────────────────────────────────────────
USERS_FILE = "Banker.txt"
TRANSACTIONS_FILE = "Transactions.txt"

try:
    open(USERS_FILE, "x").close()
except FileExistsError:
    pass

try:
    open(TRANSACTIONS_FILE, "x").close()
except FileExistsError:
    pass

# ── GLOBALS ────────────────────────────────────────────────────────────
current_user = {"first": "", "last": ""}


# ── UTILS ──────────────────────────────────────────────────────────────
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if not any(c.isupper() for c in password):
        return "Password must have at least 1 uppercase letter."
    if not any(not c.isalnum() for c in password):
        return "Password must have at least 1 special character."
    return None


def get_balance():
    first = current_user["first"]
    last = current_user["last"]
    balance = 0.0
    try:
        with open(TRANSACTIONS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4 and parts[0] == first and parts[1] == last:
                    tx_type = parts[2]
                    amount = float(parts[3])
                    if tx_type == "deposit":
                        balance += amount
                    elif tx_type == "withdrawal":
                        balance -= amount
    except FileNotFoundError:
        pass
    return balance


def save_transaction(tx_type, amount):
    with open(TRANSACTIONS_FILE, "a") as f:
        f.write(f"{current_user['first']},{current_user['last']},{tx_type},{amount},{now()}\n")


def toggle_password(entry, btn):
    if entry.cget("show") == "*":
        entry.config(show="")
        btn.config(text="Hide")
    else:
        entry.config(show="*")
        btn.config(text="Show")


def show_frame(frame):
    frame.tkraise()


# ── REGISTER ───────────────────────────────────────────────────────────
def register():
    first = entry_reg_first.get().strip()
    last = entry_reg_last.get().strip()
    password = entry_reg_pass.get()

    if not first or not last or not password:
        messagebox.showerror("Error", "All fields are required.")
        return

    err = validate_password(password)
    if err:
        messagebox.showerror("Invalid Password", err)
        return

    try:
        with open(USERS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2 and parts[0] == first and parts[1] == last:
                    messagebox.showinfo("Info", "Account already exists. Please log in.")
                    return
    except FileNotFoundError:
        pass

    with open(USERS_FILE, "a") as f:
        f.write(f"{first},{last},{password}\n")

    messagebox.showinfo("Success", f"Account created! Welcome, {first} {last}.")
    entry_reg_first.delete(0, tk.END)
    entry_reg_last.delete(0, tk.END)
    entry_reg_pass.delete(0, tk.END)
    show_frame(frame_login)


# ── LOG IN ─────────────────────────────────────────────────────────────
def log_in():
    first = entry_login_first.get().strip().title()
    last = entry_login_last.get().strip().title()
    password = entry_login_pass.get()

    if not first or not last or not password:
        messagebox.showerror("Error", "All fields are required.")
        return

    try:
        with open(USERS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 3 and parts[0] == first and parts[1] == last and parts[2] == password:
                    current_user["first"] = first
                    current_user["last"] = last
                    entry_login_first.delete(0, tk.END)
                    entry_login_last.delete(0, tk.END)
                    entry_login_pass.delete(0, tk.END)
                    open_dashboard()
                    return
    except FileNotFoundError:
        pass

    messagebox.showerror("Error", "Invalid credentials. Try again.")


# ── LOG OUT ────────────────────────────────────────────────────────────
def log_out():
    current_user["first"] = ""
    current_user["last"] = ""
    show_frame(frame_login)


# ── DASHBOARD ──────────────────────────────────────────────────────────
def open_dashboard():
    lbl_welcome.config(text=f"Welcome, {current_user['first']} {current_user['last']}!")
    refresh_balance()
    show_frame(frame_dashboard)


def refresh_balance():
    bal = get_balance()
    lbl_balance.config(text=f"Balance: ₱{bal:,.2f}")


# ── DEPOSIT ────────────────────────────────────────────────────────────
def deposit():
    raw = entry_deposit.get().strip()
    try:
        amount = float(raw)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount greater than 0.")
        return

    save_transaction("deposit", amount)
    entry_deposit.delete(0, tk.END)
    messagebox.showinfo("Success", f"Deposited ₱{amount:,.2f} successfully.")
    refresh_balance()


# ── WITHDRAW ───────────────────────────────────────────────────────────
def withdraw():
    raw = entry_withdraw.get().strip()
    try:
        amount = float(raw)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount greater than 0.")
        return

    balance = get_balance()
    if amount > balance:
        messagebox.showerror("Error", f"Insufficient balance.\nCurrent balance: ₱{balance:,.2f}")
        return

    save_transaction("withdrawal", amount)
    entry_withdraw.delete(0, tk.END)
    messagebox.showinfo("Success", f"Withdrawn ₱{amount:,.2f} successfully.")
    refresh_balance()


# ── TRANSACTION HISTORY ────────────────────────────────────────────────
def check_history():
    first = current_user["first"]
    last = current_user["last"]
    records = []

    try:
        with open(TRANSACTIONS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 5 and parts[0] == first and parts[1] == last:
                    records.append(parts)
    except FileNotFoundError:
        pass

    win = tk.Toplevel(root)
    win.title("Transaction History")
    win.geometry("420x350")
    win.config(bg="#f5f0e8")

    tk.Label(win, text="Transaction History", font=("Georgia", 14, "bold"), bg="#f5f0e8").pack(pady=12)

    frame = tk.Frame(win, bg="#f5f0e8")
    frame.pack(fill="both", expand=True, padx=16, pady=4)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Courier", 11), bg="#fffdf7", bd=0, relief="flat")
    listbox.pack(fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    if not records:
        listbox.insert(tk.END, "  No transactions yet.")
    else:
        for r in reversed(records):
            tx_type = r[2].capitalize()
            amount = float(r[3])
            date = r[4]
            sign = "+" if r[2] == "deposit" else "-"
            listbox.insert(tk.END, f"  {tx_type:12} {sign}₱{amount:>10,.2f}   {date}")


# ── WITHDRAWAL RECORDS ─────────────────────────────────────────────────
def check_withdrawals():
    first = current_user["first"]
    last = current_user["last"]
    records = []

    try:
        with open(TRANSACTIONS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 5 and parts[0] == first and parts[1] == last and parts[2] == "withdrawal":
                    records.append(parts)
    except FileNotFoundError:
        pass

    win = tk.Toplevel(root)
    win.title("Withdrawal Records")
    win.geometry("420x300")
    win.config(bg="#f5f0e8")

    tk.Label(win, text="Withdrawal Records", font=("Georgia", 14, "bold"), bg="#f5f0e8").pack(pady=12)

    frame = tk.Frame(win, bg="#f5f0e8")
    frame.pack(fill="both", expand=True, padx=16, pady=4)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Courier", 11), bg="#fffdf7", bd=0, relief="flat")
    listbox.pack(fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    if not records:
        listbox.insert(tk.END, "  No withdrawals yet.")
    else:
        for r in reversed(records):
            amount = float(r[3])
            date = r[4]
            listbox.insert(tk.END, f"  Withdrawal   -₱{amount:>10,.2f}   {date}")


# ── ROOT WINDOW ────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Bangko Central ng Pilipinas")
root.geometry("400x480")
root.config(bg="#f5f0e8")
root.resizable(False, False)

container = tk.Frame(root, bg="#f5f0e8")
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# ── FRAMES ─────────────────────────────────────────────────────────────
frame_login = tk.Frame(container, bg="#f5f0e8")
frame_register = tk.Frame(container, bg="#f5f0e8")
frame_dashboard = tk.Frame(container, bg="#f5f0e8")

for frame in (frame_login, frame_register, frame_dashboard):
    frame.grid(row=0, column=0, sticky="nsew")

FONT_TITLE = ("Palatino Linotype", 16, "bold")
FONT_LABEL = ("Palatino Linotype", 10)
FONT_ENTRY = ("Palatino Linotype", 11)
FONT_BTN   = ("Palatino Linotype", 10, "bold")
BG = "#f5f0e8"
CARD = "#fffdf7"
GOLD = "#c9a84c"
DARK = "#1a1a2e"

# ── LOGIN FRAME ────────────────────────────────────────────────────────
tk.Label(frame_login, text="Bangko Central\nng Pilipinas", font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=(30, 4))
tk.Label(frame_login, text="DIGITAL BANKING PORTAL", font=("Georgia", 8), bg=BG, fg=GOLD).pack()
tk.Frame(frame_login, height=1, bg="#e0d8c8").pack(fill="x", padx=30, pady=14)

tk.Label(frame_login, text="First Name", font=FONT_LABEL, bg=BG).pack(anchor="w", padx=40)
entry_login_first = tk.Entry(frame_login, font=FONT_ENTRY, bg=CARD, relief="flat", bd=4)
entry_login_first.pack(fill="x", padx=40, pady=(2, 10))

tk.Label(frame_login, text="Last Name", font=FONT_LABEL, bg=BG).pack(anchor="w", padx=40)
entry_login_last = tk.Entry(frame_login, font=FONT_ENTRY, bg=CARD, relief="flat", bd=4)
entry_login_last.pack(fill="x", padx=40, pady=(2, 10))

tk.Label(frame_login, text="Password", font=FONT_LABEL, bg=BG).pack(anchor="w", padx=40)
pass_frame_login = tk.Frame(frame_login, bg=BG)
pass_frame_login.pack(fill="x", padx=40, pady=(2, 16))
entry_login_pass = tk.Entry(pass_frame_login, font=FONT_ENTRY, bg=CARD, relief="flat", bd=4, show="*")
entry_login_pass.pack(side="left", fill="x", expand=True)
tk.Button(pass_frame_login, text="Show", font=("Georgia", 8), bg=BG, bd=0,
          command=lambda: toggle_password(entry_login_pass, btn_toggle_login)).pack(side="left", padx=4)
btn_toggle_login = pass_frame_login.winfo_children()[-1]

tk.Button(frame_login, text="Log In", font=FONT_BTN, bg=DARK, fg="white", relief="flat",
          padx=10, pady=8, command=log_in).pack(fill="x", padx=40, pady=(0, 8))
tk.Button(frame_login, text="Create Account", font=FONT_BTN, bg=CARD, fg=DARK, relief="flat",
          padx=10, pady=8, command=lambda: show_frame(frame_register)).pack(fill="x", padx=40)

# ── REGISTER FRAME ─────────────────────────────────────────────────────
tk.Label(frame_register, text="Create Account", font=FONT_TITLE, bg=BG, fg=DARK).pack(pady=(30, 4))
tk.Label(frame_register, text="BANGKO CENTRAL NG PILIPINAS", font=("Georgia", 8), bg=BG, fg=GOLD).pack()
tk.Frame(frame_register, height=1, bg="#e0d8c8").pack(fill="x", padx=30, pady=14)

tk.Label(frame_register, text="First Name", font=FONT_LABEL, bg=BG).pack(anchor="w", padx=40)
entry_reg_first = tk.Entry(frame_register, font=FONT_ENTRY, bg=CARD, relief="flat", bd=4)
entry_reg_first.pack(fill="x", padx=40, pady=(2, 10))

tk.Label(frame_register, text="Last Name", font=FONT_LABEL, bg=BG).pack(anchor="w", padx=40)
entry_reg_last = tk.Entry(frame_register, font=FONT_ENTRY, bg=CARD, relief="flat", bd=4)
entry_reg_last.pack(fill="x", padx=40, pady=(2, 10))









tk.Label(frame_register, text="Password", font=FONT_LABEL, bg=BG).pack(anchor="w", padx=40)
pass_frame_reg = tk.Frame(frame_register, bg=BG)
pass_frame_reg.pack(fill="x", padx=40, pady=(2, 16))
entry_reg_pass = tk.Entry(pass_frame_reg, font=FONT_ENTRY, bg=CARD, relief="flat", bd=4, show="*")
entry_reg_pass.pack(side="left", fill="x", expand=True)
tk.Button(pass_frame_reg, text="Show", font=("Georgia", 8), bg=BG, bd=0,
          command=lambda: toggle_password(entry_reg_pass, btn_toggle_reg)).pack(side="left", padx=4)
btn_toggle_reg = pass_frame_reg.winfo_children()[-1]

tk.Button(frame_register, text="Register", font=FONT_BTN, bg=DARK, fg="white", relief="flat",
          padx=10, pady=8, command=register).pack(fill="x", padx=40, pady=(0, 8))
tk.Button(frame_register, text="Back to Login", font=FONT_BTN, bg=CARD, fg=DARK, relief="flat",
          padx=10, pady=8, command=lambda: show_frame(frame_login)).pack(fill="x", padx=40)

# ── DASHBOARD FRAME ────────────────────────────────────────────────────
dash_top = tk.Frame(frame_dashboard, bg=DARK)
dash_top.pack(fill="x")

lbl_welcome = tk.Label(dash_top, text="Welcome!", font=("Georgia", 13, "bold"), bg=DARK, fg="white")
lbl_welcome.pack(side="left", padx=20, pady=16)

tk.Button(dash_top, text="Log Out", font=("Georgia", 9), bg=DARK, fg=GOLD, bd=0, relief="flat",
          command=log_out).pack(side="right", padx=20)

lbl_balance = tk.Label(frame_dashboard, text="Balance: ₱0.00", font=("Georgia", 18, "bold"), bg=BG, fg=DARK)
lbl_balance.pack(pady=20)

tk.Frame(frame_dashboard, height=1, bg="#e0d8c8").pack(fill="x", padx=20, pady=4)

# deposit section
tk.Label(frame_dashboard, text="Deposit", font=FONT_LABEL, bg=BG).pack(anchor="w", padx=30)
dep_row = tk.Frame(frame_dashboard, bg=BG)
dep_row.pack(fill="x", padx=30, pady=(2, 10))
entry_deposit = tk.Entry(dep_row, font=FONT_ENTRY, bg=CARD, relief="flat", bd=4)
entry_deposit.pack(side="left", fill="x", expand=True)
tk.Button(dep_row, text="Deposit", font=FONT_BTN, bg=GOLD, fg="white", relief="flat",
          padx=10, command=deposit).pack(side="left", padx=(6, 0))

# withdraw section
tk.Label(frame_dashboard, text="Withdraw", font=FONT_LABEL, bg=BG).pack(anchor="w", padx=30)
wit_row = tk.Frame(frame_dashboard, bg=BG)
wit_row.pack(fill="x", padx=30, pady=(2, 16))
entry_withdraw = tk.Entry(wit_row, font=FONT_ENTRY, bg=CARD, relief="flat", bd=4)
entry_withdraw.pack(side="left", fill="x", expand=True)
tk.Button(wit_row, text="Withdraw", font=FONT_BTN, bg="#c0392b", fg="white", relief="flat",
          padx=10, command=withdraw).pack(side="left", padx=(6, 0))

tk.Frame(frame_dashboard, height=1, bg="#e0d8c8").pack(fill="x", padx=20, pady=4)

btn_row = tk.Frame(frame_dashboard, bg=BG)
btn_row.pack(fill="x", padx=30, pady=12)
tk.Button(btn_row, text="Transaction History", font=FONT_BTN, bg=CARD, fg=DARK, relief="flat",
          padx=8, pady=8, command=check_history).pack(side="left", expand=True, fill="x", padx=(0, 6))
tk.Button(btn_row, text="Withdrawal Records", font=FONT_BTN, bg=CARD, fg=DARK, relief="flat",
          padx=8, pady=8, command=check_withdrawals).pack(side="left", expand=True, fill="x")

# ── START ──────────────────────────────────────────────────────────────
show_frame(frame_login)
root.mainloop()