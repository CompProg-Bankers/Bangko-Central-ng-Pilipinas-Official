import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import getpass

#CREATE FILE =======================================================================
try:
    with open("Banker.txt", "x") as file:
        print("File created successfully.")
except FileExistsError:
    print("File already exists.")


currentUser = {"firstName": None, "lastName": None}


# DATE AND VALIDATE PASSWORD =======================================================================
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validatePassword(password): #para naay twist and password para ers erss
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(not c.isalnum() for c in password):
        return False
    return True

# SIGN UP/REGISTER =======================================================================

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
        if validatePassword(password):
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

    with open("Banker.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                if firstName == parts[0] and lastName == parts[1] and password == parts[2]:
                    messagebox.info("INFO" "Login successful. Welcome back, {firstName} {lastName}!")
                    return True

    messagebox.info("INFO" "Invalid credentials. Try Again.")
    return False

## SIGN OUT --------
def signOut():
    global is_logged_in

    if is_logged_in == True:
        is_logged_in = False
        print("\nYou have successfully signed out.")
    else:
        print("\nNo user is currently logged in.")

#DEPOSIT MONEY ===========================================
def depositMoney():

    raw = entry_deposit.get().strip()

    try:
        amount = float(raw)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount grater than 0.")
        return
    with open("bank.txt", "a") as file:
        file.write(f"Deposit: {amount} on ({now})\n")
    messagebox.info("INFO" "Deposit: {amount} on ({date})")

    save_transaction("deposit", amount)
    entry_deposit.delete(0, tk.END)
    messagebox.showinfo("Success", f"Deposited ₱{amount:,.2f} successfully.")
    refresh_balance()


#CHECK BALANCE =============================================
def check_balance():
    
    Name = float(input("Enter Account Name to verify: "))
    with open("bank.txt","a")as file:
        file.write(f"Check balance: {Name} on ({now}) \n")
    print(f"Check balance: {Name} on ({now})")
    

# WITHDRAWAL RECORDS 
def withdrawalRecords():
    try:
        with open("bank.txt", "r") as file:
            found = False

            print("\nWITHDRAWAL RECORDS - ")

            for line in file:
                if "Withdraw" in line:
                    print(line.strip())
                    found = True

            if not found:
                print("No withdrawal records found.")

    except FileNotFoundError:
        print("No withdrawal records found.")


# DISPLAY TRANSACTION HISTORY
def displayTransactionHistory():
    try:
        with open("bank.txt", "r") as file:
            records = file.readlines()

            if not records:
                print("No transaction history found.")
                return

            print("\nTRANSACTION HISTORY - ")

            for record in records:
                print(record.strip())

    except FileNotFoundError:
        print("No transaction history found.")

#FOR GUI REFERENCES AND FRAME  ======================================================

frame_login = tk.Frame(container, bg=BG)
frame_register = tk.Frame(container, bg=BG)
frame_dashboard = tk.Frame(container, bg=BG)

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

# ROOT WINDOW ================================================
root = tk.Tk()
root.title("BANGKO CENTRAL \nNG USTP", font=FONT_TITLE, bg=BG, fg=blackCherry).pack(pady=(30,4))
root.geometry("400x480")
root.config(bg=BG)
root.resizable(False, False)

container = tk.Frame(root, bg=BG)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

#REGISTER ========================================================================

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
          command=lambda: toggle_password(entry_reg_pass, btn_toggle_reg)).pack(side="left", padx=4)
btn_toggle_reg = pass_frame_reg.winfo_children()[-1]

tk.Button(frame_register, text="Register", font=FONT_BTN, bg=blackCherry, fg=BG, relief="flat", padx=10, pady=8, command=register).pack(fill="x", padx=40, pady=(0, 8))
tk.Button(frame_register, text="Back to Login", font=FONT_BTN, bg=blackCherry, fg=BG, relief="flat", padx=10, pady=8, command=lambda: show_frame(frame_login)).pack(fill="x", padx=40)

#LOG IN ========================================================================

tk.Label(frame_register, text="Digital Banking Portal", fot=FONT_TITLE, bg=BG, fg=blackCherry).pack(pady=(30, 4))
tk.Label(frame_register, text="BANGKO CENTRAL NG USTP", font=("Georgia", 8), bg=BG, fg=GOLD).pack()
tk.Frame(frame_register, height=1, bg=BG).pack(fill="x", padx=30, pady=14)

tk.Label(frame_register, text="First Name", font=FONT_LABEL, bg=BG).pack(panchor="w", padx=40)
entry_reg_first= tk.Entry(frame_register, font=FONT_ENTRY, bg=GOLD, relief="flat", bd=4) 
entry_reg_first.pack(fill="x", padx=40, pady=(2, 10))

tk.Label(frame_register, text="Last Name", font=FONT_LABEL, bg=BG).pack(panchor="w", padx=40)
entry_reg_last = tk.Entry(frame_register, font=FONT_ENTRY, bg=GOLD, relief="flat", bd=4)
entry_reg_last.pack(fill="x", padx=40, pady=(2, 10))

tk.Label(frame_login, text="Password", font=FONT_LABEL, bg=BG).pack(anchor="w", padx=40)
pass_frame_login = tk.Frame(frame_login, bg=BG)
pass_frame_login.pack(fill="x", padx=40, pady=(2, 16))
entry_login_pass = tk.Entry(pass_frame_login, font=FONT_ENTRY, bg=CARD, relief="flat", bd=4, show="*")
entry_login_pass.pack(side="left", fill="x", expand=True)
tk.Button(pass_frame_login, text="Show", font=("Georgia", 8), bg=BG, bd=0,
          command=lambda: toggle_password(entry_login_pass, btn_toggle_login)).pack(side="left", padx=4)
btn_toggle_login = pass_frame_login.winfo_children()[-1]

tk.Button(frame_login, text="Log In", font=FONT_BTN, bg=DARK, fg="white", relief="flat",
          padx=10, pady=8, command=logIn).pack(fill="x", padx=40, pady=(0, 8))
tk.Button(frame_login, text="Create Account", font=FONT_BTN, bg=GOLD, fg=blackCherry, relief="flat",
          padx=10, pady=8, command=lambda: show_frame(frame_register)).pack(fill="x", padx=40)



#DASHBOARD UPON OPENING ACCOUNT ACCOUNT ========================================================================










# START ======================================
show_frame(frame_login)
root.mainloop()