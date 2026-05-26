import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import getpass

# FILES ========================================
#creates the text files if they dont exist
userFile = "bankusers.txt" #store registered accounts
tranSactions = "Transactions.txt" #store transaction records (deposit/withdrawal)

try:
    open(userFile, "x").close()
except FileExistsError:
    pass # no need to create file if already existing

try:
    open(tranSactions, "x").close()
except FileExistsError:
    pass # no need to create file if already existing

# PALETTE FOR GUI ========================================
BG          = "#640D14" #background color mainly
BG2         = "#AD2831" #entry fields and frames
PEARL       = "#F3E6BD" #text color
GOLD        = "#D8973C" # titles and accents
BTN_LIGHT   = "#F3E6BD" #light button bg
BTN_DARK    = "#AD2831" #dark button bg
FG_DARK     = "#640D14" # dark text for light buttons

FONT        = "Palatino Linotype" #consistent font for all text in the GUI
FONT_TITLE  = (FONT, 20, "bold")
FONT_SUB    = (FONT, 10, "italic")
FONT_LABEL  = (FONT, 11, "bold")
FONT_BTN    = (FONT, 12, "bold")
FONT_BTN_SM = (FONT, 10, "bold")
FONT_ENTRY  = (FONT, 11)

# =GOLBAL VARIABLES ========================================
# Tracks the currently logged-in user throughout the session
currentUser = {"first": "", "last": ""}

# IMPORTANT PARTS ======================================================
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def valPass(password): # Validates password, must contain at least 8 characters, 1 uppercase letter, 1 number, and 1 special character
    if len(password) <= 8:
        return "Password must be at least 8 characters."
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase letter."
    if not any(not c.isalnum() for c in password):
        return "Password must contain at least one special character."
    if not any(c.isdigit() for c in password):
        return "Password must have atleast one number."
    return None #means all password passes all checks

def togglePass(entry, btn):
    
    # Works for both normal and readonly entries
    current_show = entry.cget("show")
    state = entry.cget("state")
    if state == "readonly":
        entry.config(state="normal")
        entry.config(show="" if current_show == "*" else "*") #this is for showing/hiding password for privacy
        btn.config(text="Hide" if current_show == "*" else "Show")
        entry.config(state="readonly")
    else:
        entry.config(show="" if current_show == "*" else "*")
        btn.config(text="Hide" if current_show == "*" else "Show")


def show_frame(frame): #since we use multiple windows/frames, this function will help us navigate through them by raising infront the one we are currently using
    frame.tkraise()

def divider(parent):
    tk.Frame(parent, bg=GOLD, height=1).pack(fill="x", padx=30, pady=(4, 12)) #Creates a thin gold horizontal line used as a separator.

def make_entry(parent, show=""): #Creates a styled text input box with your color theme already applied.
    e = tk.Entry(parent, font=FONT_ENTRY, bg=BG2, fg=PEARL,
                insertbackground=PEARL, relief="flat",
                highlightthickness=0, highlightbackground=GOLD,
                highlightcolor=GOLD, show=show)
    return e

def header(parent, title): #Creates the title + gold divider line combo that appears at the top of every screen
    tk.Label(parent, text=title, font=FONT_TITLE,
            bg=BG, fg=GOLD, justify="center").pack(pady=(28, 4))
    divider(parent)


# TO CLEAR FOR ALL WINDOWS ================================
def clear_register(): 
    #clears all fields in the regis screen
    entry_reg_first.delete(0, tk.END)
    entry_reg_last.delete(0, tk.END)
    entry_reg_pass.delete(0, tk.END)
    entry_reg_pass.config(show="*")
    btn_show_reg.config(text="Show")

def clear_login():
    # clears all fields in the login screen
    entry_login_first.delete(0, tk.END)
    entry_login_last.delete(0, tk.END)
    entry_login_pass.delete(0, tk.END)
    entry_login_pass.config(show="*")
    btn_show_login.config(text="Show")

def clear_deposit():
    #clears deposit amount field
    entry_deposit.delete(0, tk.END)

def clear_withdraw():
    #clears withdraw amount field
    entry_withdraw.delete(0, tk.END)

def clear_delete():
    # clears password field and hides coonfirmation password in delete account screen
    entry_del_pass.delete(0, tk.END)
    confirm_frame.pack_forget()


# navigation functions =======================================================================

def go_login():
    clear_login() #clear fields b4 showing
    show_frame(frame_login)

def go_register():
    clear_register()
    show_frame(frame_register)

def go_dashboard():
    show_frame(frame_dashboard)

def go_deposit():
    clear_deposit()
    show_frame(frame_deposit)

def go_withdraw():
    clear_withdraw()
    show_frame(frame_withdraw)

def go_profile():
    openProfile() #loads current data before showing

def go_delete():
    clear_delete()
    show_frame(frame_delete)



#REGISTER =======================================================================

def register(): #handles account creation
    

    firstName = entry_reg_first.get().strip()
    lastName = entry_reg_last.get().strip()
    passWord = entry_reg_pass.get().strip()


    #check if not numbers or symbols
    if not firstName.replace(" ","").isalpha():
        messagebox.showerror("Error", "First name must not include characters or numbers")
        return
    
    if not lastName.replace(" ","").isalpha():
        messagebox.showerror("Error", "Last name must not include characters or numbers")
        return
    
    #cehck if all fields are filled
    if not firstName or not lastName or not passWord:
        messagebox.showerror("Error", "All fields are required.")
        return
    
    # check if user already has an account
    try:
        with open(userFile, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    if parts[0] == firstName and parts[1] == lastName and parts[2] == passWord:
                        messagebox.showinfo("Info", "You already have an account. Please proceed to log in.")
                        return
    except FileNotFoundError:
        pass

        #validate pass
    err = valPass(passWord) #match ba ang password?
    if err:
        messagebox.showerror("Invalid Password", err)
        return

    else:
    #save new user to file
        with open(userFile, "a") as file: #save the user info in the txt file
            file.write(f"{firstName},{lastName},{passWord}\n")
        
        messagebox.showinfo("Info", f"Registration successful. Welcome, {firstName} {lastName}!")
        clear_register()
        go_login()


# LOG IN =======================================================================
def logIn():
    #handles user login by checking the credentials against the stored accounts in the text file
    firstName = entry_login_first.get().strip().title()
    lastName = entry_login_last.get().strip().title()
    password = entry_login_pass.get().strip()

#check if all fields are filled
    if not firstName or not lastName or not password:
        messagebox.showerror("Error", "All fields are required.")
        return

    try:
        with open(userFile, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 3 and parts[0] == firstName and parts[1] == lastName: #if name matched, check password
                    if parts[2] == password:
                        currentUser["first"] = firstName
                        currentUser["last"] = lastName
                        clear_login()
                        openDashboard()
                        return
                    else:
                        messagebox.showerror("Error", "Incorrect password.")
                        return
    except FileNotFoundError:
        pass

        #if no match, show error
    messagebox.showerror("Error", "You don't have an account.")

#LOG OUT ===============================================

def logOut():
    # clears the current user session and returns log in screen
    currentUser["first"] = ""
    currentUser["last"] = ""
    go_login()
    messagebox.showinfo("Logged Out", "Log Out successful.")


# DASHBOARD OPEN =========================
def openDashboard():
    #welcomes user by name and shows dashboard
    lbl_welcome.config(text=f"Welcome, {currentUser['first']} {currentUser['last']}!")
    show_frame(frame_dashboard)

# DEPOSIT =======================================================================
def deposit():
    # handles depositing money into user's account
    amount_str = entry_deposit.get().strip().replace(",", "")
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError #rejects zero or negatives
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive number.")
        return

    saveTransac("deposit", amount) #save to transactions file
    clear_deposit()
    messagebox.showinfo("Success", f"Deposited ₱{amount:,.2f} successfully.")

# WITHDRAW MONEY========================================================================
def withdraw():
    #withdrawing money from users account
    amount_str = entry_withdraw.get().strip().replace(",", "")
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError #rejects zero or negatives
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive number.")
        return

# prevent withdrawal if balance is not enough
    current_balance = getBal()
    if amount > current_balance:
        messagebox.showerror("Error", "Insufficient funds.")
        return
    
    #ask user to confirm before proceessing
    if messagebox.askyesno("Confirm", f"Withdraw ₱{amount:,.2f}?"):
        saveTransac("withdrawal", amount)
        clear_withdraw()
        messagebox.showinfo("Success", f"Withdrew ₱{amount:,.2f} successfully.")


# WITHDRAWAL RECORD =======================================================================

def withdrawalRecord():
    #loads and dislays withdrawal records in the withdrawal record screen, if no records found, shows a message instead
    for w in frame_wr_list.winfo_children():
        w.destroy() #clear previous records before loading

    #filter ONLY WITHDRAWAL records from all transaction records
    records = [(t, a, d) for t, a, d in getTransactions() if t == "withdrawal"]
    if not records: #if walay withdrawal records, show message
        tk.Label(frame_wr_list, text="No withdrawal records found.",
                font=FONT_LABEL, bg=BG2, fg=PEARL).pack(pady=10)
    else: #display each withdrawal record as a row with amount and date
        for _, amt, date in records:
            row = tk.Frame(frame_wr_list, bg=BG2)
            row.pack(fill="x", padx=6, pady=2)
            tk.Label(row, text=f"₱{amt:,.2f}", font=FONT_ENTRY,
                    bg=BG2, fg=PEARL, width=14, anchor="w").pack(side="left", padx=6)
            tk.Label(row, text=date, font=FONT_ENTRY,
                    bg=BG2, fg=GOLD, anchor="e").pack(side="right", padx=6)

# TRANSACTION RECORD =======================================================================

def loadTxRecords(): #loads and displays all transactions (both deposit and withdrawal)
    for w in frame_tx_list.winfo_children():
        w.destroy() #clear previous records before loading

    records = getTransactions()
    
    if not records:
        tk.Label(frame_tx_list, text="No transaction records found.",
                font=FONT_LABEL, bg=BG2, fg=PEARL).pack(pady=10)
    
    else: #display each transaction record as a row with type, amount, and date. Deposits in green, withdrawals in red
        for tx, amt, date in records:
            row = tk.Frame(frame_tx_list, bg=BG2)
            row.pack(fill="x", padx=6, pady=2)
            color = "#6fcf97" if tx == "deposit" else "#eb5757"
            tk.Label(row, text=tx.upper(), font=FONT_BTN_SM,
                    bg=BG2, fg=color, width=10, anchor="w").pack(side="left", padx=6)
            tk.Label(row, text=f"₱{amt:,.2f}", font=FONT_ENTRY,
                    bg=BG2, fg=PEARL, width=12).pack(side="left")
            tk.Label(row, text=date, font=FONT_ENTRY,
                    bg=BG2, fg=GOLD, anchor="e").pack(side="right", padx=6)

# USER PROFILE ========================================================
def openProfile(): # loads current user info and password
    lbl_prof_first.config(text=currentUser["first"])
    lbl_prof_last.config(text=currentUser["last"])

    # Reset to hidden and reset button label
    entry_prof_pass.config(state="normal")
    entry_prof_pass.delete(0, tk.END)
    entry_prof_pass.config(show="*")
    btn_show_prof.config(text="Show")

    #find and load the user's password from the userFile
    try:
        with open(userFile, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if (len(parts) >= 3 and parts[0] == currentUser["first"]
                        and parts[1] == currentUser["last"]):
                    entry_prof_pass.insert(0, parts[2])
                    break

    except FileNotFoundError:
        pass
    entry_prof_pass.config(state="readonly")
    show_frame(frame_profile)

# GET BALANCE =======================================================================
def getBal(): # calculates current alance by summing deposits and subtracting withdrwals
    first = currentUser["first"]
    last = currentUser["last"]
    balance = 0.0

    try: 
        with open(tranSactions, "r") as file:
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

# SAVE TRANSACTION =======================================================================

def saveTransac(tx_type, amount): #SAVE TRANSACTION TO FILE 
    # format: firstName, lastName, transactionType, amount, dateTime 
    with open(tranSactions, "a") as f:
        f.write(f"{currentUser['first']},{currentUser['last']},{tx_type},{amount},{now()}\n")


# TRANSACTION RECORDS =======================================================================
def getTransactions():
    #reads and returnsall transactions for the current user from the file
    first, last = currentUser["first"], currentUser["last"]
    records = []
    try:
        with open(tranSactions, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 5 and parts[0] == first and parts[1] == last:
                    records.append((parts[2], float(parts[3]), parts[4]))
    except FileNotFoundError:
        pass
    return records


#DELETE ACCOUNT =======================================================================

def deleteAccount():
    #delete current user profile
    confirm_pass = entry_del_pass.get().strip()
    first, last  = currentUser["first"], currentUser["last"]

    matched = False
    lines   = []

    # read all users 
    try:
        with open(userFile, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        pass

    #keeps all users exept the one being deleted
    new_lines = []
    for line in lines:
        parts = line.strip().split(",")
        if (len(parts) >= 3 and parts[0] == first
                and parts[1] == last and parts[2] == confirm_pass):
            matched = True
        else:
            new_lines.append(line)

    #stops if password didn't match the user record
    if not matched:
        messagebox.showerror("Error", "Incorrect password.")
        return

    # also deletes all transactions of deleted user
    with open(userFile, "w") as f:
        f.writelines(new_lines)

    try:
        with open(tranSactions, "r") as f:
            tx_lines = f.readlines()
        with open(tranSactions, "w") as f:
            for line in tx_lines:
                parts = line.strip().split(",")
                if not (len(parts) >= 2 and parts[0] == first and parts[1] == last):
                    f.write(line)
    except FileNotFoundError:
        pass

        #clear session and return to login
    currentUser["first"] = ""
    currentUser["last"]  = ""
    clear_delete()
    go_login()
    messagebox.showinfo("Deleted", "Your account has been deleted.")

# ══════════════════════════════════════════════════════════════════════════════
# ROOT WINDOW
# ══════════════════════════════════════════════════════════════════════════════
root = tk.Tk()
root.title("Bangko Central ng USTP")
root.geometry("420x600")
root.resizable(False, False)
root.configure(bg=BG)

container = tk.Frame(root, bg=BG)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

def make_frame():
    f = tk.Frame(container, bg=BG)
    f.grid(row=0, column=0, sticky="nsew")
    return f

# ══════════════════════════════════════════════════════════════════════════════
# FRAME: LOGIN
# ══════════════════════════════════════════════════════════════════════════════
frame_login = make_frame()

tk.Label(frame_login, text="BANGKO CENTRAL\nNG USTP",
        font=(FONT, 22, "bold"), bg=BG, fg=GOLD,
        justify="center").pack(pady=(36, 2))
tk.Label(frame_login, text="Digital Banking Portal",
        font=FONT_SUB, bg=BG, fg=PEARL).pack()
divider(frame_login)

tk.Label(frame_login, text="First Name", font=FONT_LABEL, bg=BG, fg=PEARL).pack(anchor="w", padx=30)
entry_login_first = make_entry(frame_login)
entry_login_first.pack(fill="x", padx=30, ipady=6, pady=(2, 10))

tk.Label(frame_login, text="Last Name", font=FONT_LABEL, bg=BG, fg=PEARL).pack(anchor="w", padx=30)
entry_login_last = make_entry(frame_login)
entry_login_last.pack(fill="x", padx=30, ipady=6, pady=(2, 10))

tk.Label(frame_login, text="Password", font=FONT_LABEL, bg=BG, fg=PEARL).pack(anchor="w", padx=30)
pass_row_login = tk.Frame(frame_login, bg=BG)
pass_row_login.pack(fill="x", padx=30, pady=(2, 4))
entry_login_pass = make_entry(pass_row_login, show="*")
entry_login_pass.pack(side="left", fill="x", expand=True, ipady=6)
btn_show_login = tk.Button(pass_row_login, text="Show", font=FONT_BTN_SM,
                        bg=BG2, fg=PEARL, relief="flat", cursor="hand2",
                        command=lambda: togglePass(entry_login_pass, btn_show_login))
btn_show_login.pack(side="left", padx=(4, 0), ipady=6, ipadx=4)

tk.Frame(frame_login, bg=BG, height=10).pack()
tk.Button(frame_login, text="LOG IN", font=FONT_BTN,
        bg=BTN_DARK, fg=PEARL, relief="flat",
        activebackground="#8B1A20", activeforeground=PEARL,
        cursor="hand2", command=logIn).pack(fill="x", padx=30, ipady=8)
tk.Frame(frame_login, bg=BG, height=6).pack()
tk.Button(frame_login, text="CREATE ACCOUNT", font=FONT_BTN,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, activeforeground=FG_DARK,
        cursor="hand2",
        command=go_register).pack(fill="x", padx=30, ipady=8)

# ══════════════════════════════════════════════════════════════════════════════
# FRAME: REGISTER
# ══════════════════════════════════════════════════════════════════════════════
frame_register = make_frame()

tk.Label(frame_register, text="BANGKO CENTRAL\nNG USTP",
        font=(FONT, 22, "bold"), bg=BG, fg=GOLD,
        justify="center").pack(pady=(36, 2))
tk.Label(frame_register, text="Digital Banking Portal",
        font=FONT_SUB, bg=BG, fg=PEARL).pack()
divider(frame_register)
tk.Label(frame_register, text="OPEN ACCOUNT",
        font=FONT_TITLE, bg=BG, fg=PEARL).pack(pady=(0, 8))

tk.Label(frame_register, text="First Name", font=FONT_LABEL, bg=BG, fg=PEARL).pack(anchor="w", padx=30)
entry_reg_first = make_entry(frame_register)
entry_reg_first.pack(fill="x", padx=30, ipady=6, pady=(2, 10))

tk.Label(frame_register, text="Last Name", font=FONT_LABEL, bg=BG, fg=PEARL).pack(anchor="w", padx=30)
entry_reg_last = make_entry(frame_register)
entry_reg_last.pack(fill="x", padx=30, ipady=6, pady=(2, 10))

tk.Label(frame_register, text="Password", font=FONT_LABEL, bg=BG, fg=PEARL).pack(anchor="w", padx=30)
pass_row_reg = tk.Frame(frame_register, bg=BG)
pass_row_reg.pack(fill="x", padx=30, pady=(2, 4))
entry_reg_pass = make_entry(pass_row_reg, show="*")
entry_reg_pass.pack(side="left", fill="x", expand=True, ipady=6)
btn_show_reg = tk.Button(pass_row_reg, text="Show", font=FONT_BTN_SM,
                        bg=BG2, fg=PEARL, relief="flat", cursor="hand2",
                        command=lambda: togglePass(entry_reg_pass, btn_show_reg))
btn_show_reg.pack(side="left", padx=(4, 0), ipady=6, ipadx=4)

tk.Label(frame_register,
        text="Min 8 chars • 1 uppercase • 1 number • 1 special character",
        font=(FONT, 8, "italic"), bg=BG, fg=GOLD, wraplength=340).pack(padx=30, anchor="w")

tk.Frame(frame_register, bg=BG, height=10).pack()
tk.Button(frame_register, text="REGISTER", font=FONT_BTN,
        bg=BTN_DARK, fg=PEARL, relief="flat",
        activebackground="#8B1A20", cursor="hand2",
        command=register).pack(fill="x", padx=30, ipady=8)
tk.Frame(frame_register, bg=BG, height=6).pack()
tk.Button(frame_register, text="BACK TO LOG IN", font=FONT_BTN,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=go_login).pack(fill="x", padx=30, ipady=8)

# ══════════════════════════════════════════════════════════════════════════════
# FRAME: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
frame_dashboard = make_frame() #WINDOW FOR DASHBOARD, FROM HERE USER CAN NAVIGATE TO OTHER SCREENS

tk.Button(frame_dashboard, text="USER PROFILE", font=FONT_BTN_SM,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=go_profile).pack(anchor="ne", padx=8, pady=8)

lbl_welcome = tk.Label(frame_dashboard, text="Welcome, User!",
                        font=(FONT, 18, "bold"), bg=BG, fg=GOLD)
lbl_welcome.pack(pady=(4, 2))
divider(frame_dashboard)

tk.Label(frame_dashboard, text="What would you like to do?",
        font=FONT_LABEL, bg=BG, fg=PEARL).pack(pady=(0, 16))

# ── Dashboard menu buttons ───────────────────────────────────────────────────
tk.Button(frame_dashboard, text="DEPOSIT", font=FONT_BTN,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2", #ACTEIVE BACKGROUND KAY ANG BG SA BUTTON PAG I HOVER OVER ANG CURSOR
        command=go_deposit).pack(fill="x", padx=30, pady=(0, 8), ipady=8)

tk.Button(frame_dashboard, text="WITHDRAW", font=FONT_BTN,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2", #ACTEIVE BACKGROUND KAY ANG BG SA BUTTON PAG I HOVER OVER ANG CURSOR
        command=go_withdraw).pack(fill="x", padx=30, pady=(0, 8), ipady=8)

tk.Button(frame_dashboard, text="CHECK BALANCE", font=FONT_BTN,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2", #ACTEIVE BACKGROUND KAY ANG BG SA BUTTON PAG I HOVER OVER ANG CURSOR
        command=lambda: show_balance_frame()).pack(fill="x", padx=30, pady=(0, 8), ipady=8) #internal padding, inside widget

tk.Button(frame_dashboard, text="CHECK WITHDRAWAL RECORDS", font=FONT_BTN,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=lambda: (withdrawalRecord(), show_frame(frame_wr))
        ).pack(fill="x", padx=30, pady=(0, 8), ipady=8)

tk.Button(frame_dashboard, text="CHECK TRANSACTION RECORDS", font=FONT_BTN,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=lambda: (loadTxRecords(), show_frame(frame_tx))
        ).pack(fill="x", padx=30, pady=(0, 8), ipady=8)

# ══════════════════════════════════════════════════════════════════════════════
# FRAME: DEPOSIT
# ══════════════════════════════════════════════════════════════════════════════
frame_deposit = make_frame()

tk.Button(frame_deposit, text="USER PROFILE", font=FONT_BTN_SM,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=go_profile).pack(anchor="ne", padx=8, pady=8)
header(frame_deposit, "DEPOSIT")

tk.Label(frame_deposit, text="Enter amount to deposit:",
        font=FONT_LABEL, bg=BG, fg=PEARL).pack(anchor="w", padx=30, pady=(20, 4))
entry_deposit = make_entry(frame_deposit)
entry_deposit.pack(fill="x", padx=30, ipady=10)

tk.Frame(frame_deposit, bg=BG, height=10).pack()
tk.Button(frame_deposit, text="DEPOSIT", font=FONT_BTN,
        bg=BTN_DARK, fg=PEARL, relief="flat",
        activebackground="#8B1A20", cursor="hand2",
        command=deposit).pack(fill="x", padx=30, ipady=8)

tk.Frame(frame_deposit, bg=BG).pack(expand=True)
tk.Button(frame_deposit, text="back to main menu", font=FONT_BTN_SM,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=lambda: (clear_deposit(), go_dashboard())).pack(
            anchor="sw", padx=8, pady=8)

# ══════════════════════════════════════════════════════════════════════════════
# FRAME: WITHDRAW
# ══════════════════════════════════════════════════════════════════════════════
frame_withdraw = make_frame()

tk.Button(frame_withdraw, text="USER PROFILE", font=FONT_BTN_SM,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=go_profile).pack(anchor="ne", padx=8, pady=8)
header(frame_withdraw, "WITHDRAW")

tk.Label(frame_withdraw, text="Enter amount to withdraw:",
        font=FONT_LABEL, bg=BG, fg=PEARL).pack(anchor="w", padx=30, pady=(20, 4))
entry_withdraw = make_entry(frame_withdraw)
entry_withdraw.pack(fill="x", padx=30, ipady=10)

tk.Frame(frame_withdraw, bg=BG, height=10).pack()
tk.Button(frame_withdraw, text="WITHDRAW", font=FONT_BTN,
        bg=BTN_DARK, fg=PEARL, relief="flat",
        activebackground="#8B1A20", cursor="hand2",
        command=withdraw).pack(fill="x", padx=30, ipady=8)

tk.Frame(frame_withdraw, bg=BG).pack(expand=True)
tk.Button(frame_withdraw, text="back to main menu", font=FONT_BTN_SM,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=lambda: (clear_withdraw(), go_dashboard())).pack(
            anchor="sw", padx=8, pady=8)

# ══════════════════════════════════════════════════════════════════════════════
# FRAME: CHECK BALANCE
# ══════════════════════════════════════════════════════════════════════════════
frame_balance = make_frame()

tk.Button(frame_balance, text="USER PROFILE", font=FONT_BTN_SM,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=go_profile).pack(anchor="ne", padx=8, pady=8)
header(frame_balance, "CHECK BALANCE")

tk.Frame(frame_balance, bg=BG, height=40).pack()
tk.Label(frame_balance, text="YOUR CURRENT BALANCE IS:",
        font=FONT_LABEL, bg=BG, fg=PEARL).pack()
tk.Frame(frame_balance, bg=BG, height=10).pack()

def show_balance_frame():
    lbl_bal_display.config(text=f"₱ {getBal():,.2f}")
    show_frame(frame_balance)

lbl_bal_display = tk.Label(frame_balance, text="₱ 0.00",
                            font=(FONT, 30, "bold"), bg=BG2, fg=PEARL,
                            relief="flat", padx=20, pady=16)
lbl_bal_display.pack(fill="x", padx=30)

tk.Frame(frame_balance, bg=BG).pack(expand=True)
tk.Button(frame_balance, text="back to main menu", font=FONT_BTN_SM,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=go_dashboard).pack(anchor="sw", padx=8, pady=8)

# ══════════════════════════════════════════════════════════════════════════════
# FRAME: WITHDRAWAL RECORDS
# ══════════════════════════════════════════════════════════════════════════════
frame_wr = make_frame()

tk.Button(frame_wr, text="USER PROFILE", font=FONT_BTN_SM,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=go_profile).pack(anchor="ne", padx=8, pady=8)
header(frame_wr, "WITHDRAWAL\nRECORDS")

tk.Label(frame_wr, text="WITHDRAWAL RECORDS:",
        font=FONT_LABEL, bg=BG, fg=PEARL).pack(anchor="w", padx=30, pady=(0, 4))

wr_canvas_frame = tk.Frame(frame_wr, bg=BG2, relief="flat")
wr_canvas_frame.pack(fill="both", expand=True, padx=30, pady=(0, 8))

frame_wr_list = tk.Frame(wr_canvas_frame, bg=BG2)
frame_wr_list.pack(fill="both", expand=True, pady=4)

tk.Button(frame_wr, text="back to main menu", font=FONT_BTN_SM,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=go_dashboard).pack(anchor="sw", padx=8, pady=8)

# ══════════════════════════════════════════════════════════════════════════════
# FRAME: TRANSACTION RECORDS
# ══════════════════════════════════════════════════════════════════════════════
frame_tx = make_frame()

tk.Button(frame_tx, text="USER PROFILE", font=FONT_BTN_SM,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=go_profile).pack(anchor="ne", padx=8, pady=8)
header(frame_tx, "TRANSACTION\nRECORDS")

tk.Label(frame_tx, text="TRANSACTION RECORDS:",
        font=FONT_LABEL, bg=BG, fg=PEARL).pack(anchor="w", padx=30, pady=(0, 4))

tx_canvas_frame = tk.Frame(frame_tx, bg=BG2, relief="flat")
tx_canvas_frame.pack(fill="both", expand=True, padx=30, pady=(0, 8))

frame_tx_list = tk.Frame(tx_canvas_frame, bg=BG2)
frame_tx_list.pack(fill="both", expand=True, pady=4)

tk.Button(frame_tx, text="back to main menu", font=FONT_BTN_SM,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=go_dashboard).pack(anchor="sw", padx=8, pady=8)

# ══════════════════════════════════════════════════════════════════════════════
# FRAME: USER PROFILE
# ══════════════════════════════════════════════════════════════════════════════
frame_profile = make_frame()

header(frame_profile, "USER PROFILE")

info_frame = tk.Frame(frame_profile, bg=BG)
info_frame.pack(fill="x", padx=30, pady=8)

tk.Label(info_frame, text="FIRST NAME:", font=FONT_LABEL, bg=BG, fg=PEARL).grid(row=0, column=0, sticky="w", pady=4)
lbl_prof_first = tk.Label(info_frame, text="", font=FONT_ENTRY, bg=BG, fg=GOLD)
lbl_prof_first.grid(row=0, column=1, sticky="w", padx=10)

tk.Label(info_frame, text="LAST NAME:", font=FONT_LABEL, bg=BG, fg=PEARL).grid(row=1, column=0, sticky="w", pady=4)
lbl_prof_last = tk.Label(info_frame, text="", font=FONT_ENTRY, bg=BG, fg=GOLD)
lbl_prof_last.grid(row=1, column=1, sticky="w", padx=10)

tk.Label(info_frame, text="PASSWORD:", font=FONT_LABEL, bg=BG, fg=PEARL).grid(row=2, column=0, sticky="w", pady=4)
prof_pass_row = tk.Frame(info_frame, bg=BG)
prof_pass_row.grid(row=2, column=1, sticky="w", padx=10)
entry_prof_pass = make_entry(prof_pass_row, show="*")
entry_prof_pass.config(state="readonly", readonlybackground=BG2, fg=PEARL)
entry_prof_pass.pack(side="left", ipady=4, ipadx=6)
btn_show_prof = tk.Button(prof_pass_row, text="Show", font=FONT_BTN_SM,
                        bg=BG2, fg=PEARL, relief="flat", cursor="hand2",
                        command=lambda: togglePass(entry_prof_pass, btn_show_prof))
btn_show_prof.pack(side="left", padx=(4, 0), ipady=4, ipadx=4)

tk.Frame(frame_profile, bg=BG).pack(expand=True)

tk.Button(frame_profile, text="Log Out", font=FONT_BTN,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=lambda: (
            messagebox.askyesno("Log Out", "Are you sure you want to log out?") and logOut()
        )).pack(fill="x", padx=30, ipady=8, pady=(0, 8))

tk.Button(frame_profile, text="Delete Account", font=FONT_BTN,
        bg=BTN_DARK, fg=PEARL, relief="flat",
        activebackground="#8B1A20", cursor="hand2",
        command=go_delete).pack(fill="x", padx=30, ipady=8)

tk.Frame(frame_profile, bg=BG, height=8).pack()
tk.Button(frame_profile, text="back to main menu", font=FONT_BTN_SM,
        bg=BG2, fg=PEARL, relief="flat",
        activebackground="#8B1A20", cursor="hand2",
        command=go_dashboard).pack(anchor="sw", padx=8, pady=8)

# ══════════════════════════════════════════════════════════════════════════════
# FRAME: DELETE ACCOUNT
# ══════════════════════════════════════════════════════════════════════════════
frame_delete = make_frame()

header(frame_delete, "DELETE ACCOUNT")

tk.Label(frame_delete, text="Are you sure you want to\nDelete Account?",
        font=FONT_LABEL, bg=BG, fg=PEARL, justify="center").pack(pady=(20, 16))

yes_no_row = tk.Frame(frame_delete, bg=BG)
yes_no_row.pack()

def on_yes_delete():
    confirm_frame.pack(fill="x", padx=30, pady=12)

tk.Button(yes_no_row, text="YES", font=FONT_BTN,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=on_yes_delete).pack(side="left", padx=10, ipadx=20, ipady=6)
tk.Button(yes_no_row, text="NO", font=FONT_BTN,
        bg=BTN_LIGHT, fg=FG_DARK, relief="flat",
        activebackground=GOLD, cursor="hand2",
        command=lambda: show_frame(frame_profile)).pack(side="left", padx=10, ipadx=20, ipady=6)

confirm_frame = tk.Frame(frame_delete, bg=BG)
tk.Label(confirm_frame, text="ENTER PASSWORD TO CONTINUE:",
        font=FONT_LABEL, bg=BG, fg=PEARL).pack(anchor="w")
entry_del_pass = make_entry(confirm_frame, show="*")
entry_del_pass.pack(fill="x", ipady=8, pady=(4, 8))
tk.Button(confirm_frame, text="CONFIRM DELETE", font=FONT_BTN,
        bg=BTN_DARK, fg=PEARL, relief="flat",
        activebackground="#8B1A20", cursor="hand2",
        command=deleteAccount).pack(fill="x", ipady=6)

tk.Frame(frame_delete, bg=BG).pack(expand=True)
tk.Button(frame_delete, text="BACK", font=FONT_BTN_SM,
        bg=BTN_DARK, fg=PEARL, relief="flat",
        activebackground="#8B1A20", cursor="hand2",
        command=lambda: show_frame(frame_profile)).pack(anchor="sw", padx=8, pady=8)

# ══════════════════════════════════════════════════════════════════════════════
show_frame(frame_login)
root.mainloop()



