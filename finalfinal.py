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


#LOG OUT ===============================================

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

# WITHDRAW MONEY========================================================================
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
    
    if messagebox.askyesno("Confirm", f"Withdraw ₱{amount:.2f}?"):
        saveTransac("withdrawal", amount)
        entry_withdraw.delete(0, tk.END)
        messagebox.showinfo("Success", f"Withdrew ₱{amount:.2f} successfully.")
        refreshBal()

# WITHDRAWAL RECORD =======================================================================
def withdrawalRecord():
    amount = entry_withdraw.get().strip()
    try:
        with open(userFile, "r") as file:
            records = file.readlines()

            history = ""
            for record in records:
                parts = record.strip().split(",")
                if parts[0] == currentUser["first"] and parts[1] == currentUser["last"]:
                    if parts[2].lower() == "withdrawal":
                        history += f"Withdrawal - ₱{float(parts[3]):.2f}\n"

            if not history:
                messagebox.showinfo("Withdrawal Records", "No withdrawal records found.")
                return

            messagebox.showinfo("Withdrawal Records", history)

    except FileNotFoundError:
        messagebox.showinfo("Withdrawal Records", "No withdrawal records found.")

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
                    try:
                        amount = float(parts[3])
                        if tx_type == "deposit":
                            balance += amount
                        elif tx_type == "withdrawal":
                            balance -= amount
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return balance

#DISPLAY TRANSACTION HISTORY =======================================================================
def displayTransactionHistory():
    try:
        with open(userFile, "r") as file:
            records = file.readlines()
            if not records:
                messagebox.showinfo("Transaction History", "No transaction history found.")
                return
            history = ""

            for record in records:
                parts = record.strip().split(",")
                if parts[0] == currentUser["first"] and parts[1] == currentUser["last"]:
                    history += f"{parts[2].capitalize()} - ₱{float(parts[3]):.2f}\n"
            if not history:
                messagebox.showinfo("Transaction History", "No transaction history found.")
                return
            
            win = tk.Toplevel()
            win.title("Transaction History")
            text = tk.Text(win, width=40, height=15)
            text.insert(tk.END, history)
            text.config(state="disabled")
            text.pack(padx=10, pady=10)

    except FileNotFoundError:
        messagebox.showinfo("Transaction History", "No transaction history found.")

#DELETE ACCOUNT =======================================================================
def deleteAccount():
    if not currentUser["first"] or not currentUser["last"]:
        messagebox.showinfo("Info", "No user is currently logged in.")
        return

    if messagebox.askyesno("Confirm", "Are you sure you want to delete your account? This action cannot be undone."):
        try:
            with open(userFile, "r") as file:
                lines = file.readlines()
            with open(userFile, "w") as file:
                for line in lines:
                    parts = line.strip().split(",")
                    if not (parts[0] == currentUser["first"] and parts[1] == currentUser["last"]):
                        file.write(line)
            messagebox.showinfo("Info", "Your account has been deleted.")
            logOut()
        except FileNotFoundError:
            messagebox.showinfo("Info", "No user data found.")

#SIGN OUT =======================================================================
def signOut():
    if currentUser["first"] and currentUser["last"]:
        messagebox.showinfo("Info", f"Goodbye, {currentUser['first']} {currentUser['last']}!")
        logOut()
    else:
        messagebox.showinfo("Info", "No user is currently logged in.")





