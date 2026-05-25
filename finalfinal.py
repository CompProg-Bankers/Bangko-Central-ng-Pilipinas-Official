import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import getpass

# FILES ========================================

userFile = "bankusers.txt"
tranSactions = "Transactions.txt"

try:
    open(userFile, "x").close()
except FileExistsError:
    pass

try:
    open(tranSactions, "x").close()
except FileExistsError:
    pass

# =GOLBAL VARIABLES ========================================

currentUser = {"first": "", "last": ""}

# IMPORTANT PARTS ======================================================
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def valPass(password):
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase letter."
    if not any(not c.isalnum() for c in password):
        return "Password must contain at least one special character."
    if not any(c.isdigit() for c in password):
        return "Password must have atleast one number."
    return None

# GET BALANCE =======================================================================
def getBal():
    first = currentUser["first"]
    last = currentUser["last"]
    balance = 0.0

    try: 
        with open(userFile, "r") as file:
            for line in file: 
                parts = line.strip().split(",")
                if len(parts) >= 4 and parts[0] == first and parts[1] == last:
                    tx_type = parts[2]
                    amount = float(parts[3])
                    if tx_type == "deposit":
                        balance += amount
                    elif tx_type == "withdrawal":
                        balance -= amount
    except FileNotFoundError:
        pass
    return balance

def saveTransac(tx_type, amount):
    with open(tranSactions, "a") as file: 
        file.write(f"{currentUser['first']},{currentUser['last']},: {tx_type},{amount},{now()}\n")


def togglePass(entry, btn):
    if entry.cget("show") == "":
        entry.config(show="*")
        btn.config(text="Show")
    else:
        entry.config(show="")
        btn.config(text="Hide")

def show_frame(frame):
    frame.tkraise()



#REGISTER =======================================================================

def register(): #create acc niiiiii
    
    firstName = entry_reg_first.get().strip()
    lastName = entry_reg_last.get().strip()
    passWord = entry_reg_pass.get().strip()

    if not firstName or not lastName or not passWord:
        messagebox.showerror("Error", "All fields are required.")
        return
    # check if NA REGISTER NA
    try:
        with open("Banker.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    if parts[0] == firstName and parts[1] == lastName:
                        messagebox.info("Info", "You already have an account. Please proceed to log in.")
                        return
    except FileNotFoundError:
        pass

    while True:
        messagebox.showinfo("Info", "Password must be at least 8 characters long, contain at least one uppercase letter, and one special character.")
        password = entry_reg_pass.get().strip()
        if valPass(password):
            break
        messagebox.showerror("Error", "Invalid password. Try Again.")
        

    with open("Banker.txt", "a") as file:
        file.write(f"{firstName},{lastName},{password}\n")
    messagebox.showinfo("Info", f"Registration successful. Welcome, {firstName} {lastName}!")

    entry_reg_first.delete(0, tk.END)
    entry_reg_last.delete(0, tk.END)
    entry_reg_pass.delete(0, tk.END)
    show_frame(frame_login)


# LOG IN =======================================================================
def logIn():
    firstName = entry_login_first.get().strip().title()
    lastName = entry_login_last.get().strip().title()
    password = entry_login_pass.get().strip()

    if not firstName or not lastName or not password:
        messagebox.info("ERROR", "All fields are required.")
        return


    try:
        with open(userFile, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 3 and parts[0] == firstName and parts [1] == lastName and parts[2] == password:
                    currentUser["first"] = firstName
                    currentUser["last"] = lastName
                    entry_login_first.delete(0, tk.END)
                    entry_login_last.delete(0, tk.END)
                    entry_login_pass.delete(0, tk.END)
                    openDashboard()
                    return
    except FileNotFoundError:
        pass    

    messagebox.info("Error" "Invalid credentials. Try Again.")


#LOG OUT ===========================

def logOut():
    currentUser["first"] = ""
    currentUser["last"] = ""
    messagebox.showinfo("Info", "You have been logged out.")
    show_frame(frame_login)

# DASHBOARD OPEN =========================
def openDashboard():
    lbl_welcome.config(text=f"Welcome, {currentUser['first']} {currentUser['last']}!")
    refreshBal()
    show_frame(frame_dashboard)

def refreshBal():
    bal = getBal()
    lbl_balance.config(text=f"Balance: ₱{bal:.2f}")

# DEPOSIT =======================================================================
def deposit():
    amount_str = entry_deposit.get().strip()
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive number.")
        return

    saveTransac("deposit", amount)
    entry_deposit.delete(0, tk.END)
    messagebox.showinfo("Success", f"Deposited ₱{amount:.2f} successfully.")
    refreshBal()

# WITHDRAWAL RECORD =======================================================================
def withdrawalRecord():
    amount = entry_withdraw.get().strip()
    try:
        with open("bank.txt", "r") as file:
            found = False

            print("\nWITHDRAWAL Records - ")

            for line in file:
                if "Withdraw" in line:
                    print(line.strip())
                    found = True

            if not found:
                print("No withdrawal records found.")

    except FileNotFoundError:
        print("No withdrawal records found.")

# Withdraw Money========================================================================
def withdraw():
    amount_str = entry_withdraw.get().strip()
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive number.")
        return

    current_balance = getBal()
    if amount > current_balance:
        messagebox.showerror("Error", "Insufficient funds.")
        return

    saveTransac("withdrawal", amount)
    entry_withdraw.delete(0, tk.END)
    messagebox.showinfo("Success", f"Withdrew ₱{amount:.2f} successfully.")
    refreshBal()






# START OF GUI  HERE =======================================
# ROOT WINDOW ================================================
root = tk.Tk()
root.title("BANGKO CENTRAL \nNG USTP", font="Palatino Linotype", bg="#f3e6bd", fg="#640d14").pack(pady=(30,4))
root.geometry("400x480")
root.config(bg="#f3e6bd")
root.resizable(False, False)

container = tk.Frame(root, bg="#f3e6bd")
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

#FOR GUI REFERENCES AND FRAME  ======================================================

frame_login = tk.Frame(container, bg="#f3e6bd")
frame_register = tk.Frame(container, bg="#f3e6bd")
frame_dashboard = tk.Frame(container, bg="#f3e6bd")

for frame in (frame_login, frame_register, frame_dashboard):
    frame.grid(row=0, column=0, sticky="nsew")
FONT_TITLE = ("Palatino Linotype", 16, "bold")
FONT_LABEL = ("Palatino Linotype", 10)
FONT_ENTRY = ("Palatino Linotype", 11)
FONT_BTN   = ("Palatino Linotype", 10, "bold")
FONT_INPUT = ("Palatino Linotype", 10)

BG = "#f3e6bd"
GOLD = "#d89783"
cottonCandy = "#fd9bb7"
brownRed = "#ad2831"
blackCherry = "#640d14"



# REGISTER GUI ==========================================

tk.Label(frame_register, text="OPEN ACCOUNT", fot=FONT_TITLE, bg=BG, fg=blackCherry).pack(pady=(30, 4))
tk.Label(frame_register, text="BANGKO CENTRAL NG PILIPINAS", font=("Georgia", 8), bg=BG, fg=GOLD).pack()
tk.Frame(frame_register, height=1, bg=BG).pack(fill="x", padx=30, pady=14)

tk.Label(frame_register, text="First Name", font=FONT_LABEL, bg=BG).pack(panchor="w", padx=40)
entry_reg_first= tk.Entry(frame_register, font=FONT_ENTRY, bg=GOLD, relief="flat", bd=4) 
entry_reg_first.pack(fill="x", padx=40, pady=(2, 10))

tk.Label(frame_register, text="Last Name", font=FONT_LABEL, bg=BG).pack(panchor="w", padx=40)
entry_reg_last = tk.Entry(frame_register, font=FONT_ENTRY, bg=GOLD, relief="flat", bd=4)
entry_reg_last.pack(fill="x", padx=40, pady=(2, 10))

tk.Label(frame_register, text="Password", font=FONT_LABEL, bg=BG).pack(anchor="w",padx=40)
pass_frame_reg = tk.Frame(frame_register, bg=BG)
pass_frame_reg.pack(fill="x", padx=40, pady=(2, 16))
entry_reg_pass = tk.Entry(pass_frame_reg, font=FONT_ENTRY, bg=GOLD, relief="flat", bd=4, show="*")
entry_reg_pass.pack(side="left", fill="x", expand=True)
tk.Button(pass_frame_reg, text="Show", font=("Palatino Linotype", 8), bg=BG, bd=0,
          command=lambda: togglePass(entry_reg_pass, btn_toggle_reg)).pack(side="left", padx=4)
btn_toggle_reg = pass_frame_reg.winfo_children()[-1]

tk.Button(frame_register, text="Register", font=FONT_BTN, bg=blackCherry, fg=BG, relief="flat", padx=10, pady=8, command=register).pack(fill="x", padx=40, pady=(0, 8))
tk.Button(frame_register, text="Back to Login", font=FONT_BTN, bg=blackCherry, fg=BG, relief="flat", padx=10, pady=8, command=lambda: show_frame(frame_login)).pack(fill="x", padx=40)


#LOGIN ====================================================
tk.Label(frame_register, text="Digital Banking Portal", fot=FONT_TITLE, bg=BG, fg=blackCherry).pack(pady=(30, 4))
tk.Label(frame_register, text="BANGKO CENTRAL NG USTP", font=("Georgia", 8), bg=BG, fg=GOLD).pack()
tk.Frame(frame_register, height=1, bg=BG).pack(fill="x", padx=30, pady=14)

tk.Label(frame_register, text="First Name", font=FONT_LABEL, bg=BG).pack(panchor="w", padx=40)
entry_login_first= tk.Entry(frame_register, font=FONT_ENTRY, bg=GOLD, relief="flat", bd=4) 
entry_login_first.pack(fill="x", padx=40, pady=(2, 10))

tk.Label(frame_register, text="Last Name", font=FONT_LABEL, bg=BG).pack(panchor="w", padx=40)
entry_login_last = tk.Entry(frame_register, font=FONT_ENTRY, bg=GOLD, relief="flat", bd=4)
entry_login_last.pack(fill="x", padx=40, pady=(2, 10))

tk.Label(frame_login, text="Password", font=FONT_LABEL, bg=BG).pack(anchor="w", padx=40)
pass_frame_login = tk.Frame(frame_login, bg=BG)
pass_frame_login.pack(fill="x", padx=40, pady=(2, 16))
entry_login_pass = tk.Entry(pass_frame_login, font=FONT_ENTRY, bg=GOLD, relief="flat", bd=4, show="*")
entry_login_pass.pack(side="left", fill="x", expand=True)
tk.Button(pass_frame_login, text="Show", font=("Georgia", 8), bg=BG, bd=0,
          command=lambda: togglePass(entry_login_pass, btn_toggle_login)).pack(side="left", padx=4)
btn_toggle_login = pass_frame_login.winfo_children()[-1]

tk.Button(frame_login, text="Log In", font=FONT_BTN, bg=blackCherry, fg="white", relief="flat",
          padx=10, pady=8, command=logIn).pack(fill="x", padx=40, pady=(0, 8))
tk.Button(frame_login, text="Create Account", font=FONT_BTN, bg=GOLD, fg=blackCherry, relief="flat",
          padx=10, pady=8, command=lambda: show_frame(frame_register)).pack(fill="x", padx=40)

# DASHBOARD FOR ACCOUNTS ====================================
dash_top = tk.Frame(frame_dashboard, bg= blackCherry)
dash_top.pack(fill="x")

lbl_welcome = tk.Label(dash_top, text = f"Welcome, {currentUser['first']} {currentUser['last']}!", font=FONT_TITLE, bg=blackCherry, fg=BG)
lbl_welcome.pack(side = "left", padx=20, pady=16)

