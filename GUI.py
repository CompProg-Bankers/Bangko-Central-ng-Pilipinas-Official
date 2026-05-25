# START OF GUI  HERE =======================================
# ROOT WINDOW ================================================
root = tk.Tk()
root.title("BANGKO CENTRAL \nNG USTP")
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

tk.Label(frame_register, text="OPEN ACCOUNT", font=FONT_TITLE, bg=BG, fg=blackCherry).pack(pady=(30, 4))
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

tk.Button(dash_top, text="Log Out", font=FONT_BTN, bg=blackCherry, fg=BG, relief="flat", padx=10, pady=8, command=logOut).pack(side="right", padx=20)
lbl_balance = tk.Label(frame_dashboard, text="Balance: ₱0.00", font=FONT_LABEL, bg=BG, fg=blackCherry)
lbl_balance.pack(pady=20)

tk.Frame(frame_dashboard, height=1, bg=BG).pack(fill="x", padx=20, pady=4)

# DEPOSIT MONEY ============================================
tk.Label(frame_dashboard, text="Deposit", font=FONT_LABEL,bg=BG).pack(anchor="w", padx=30)
dep_row = tk.Frame(frame_dashboard, bg=BG)
dep_row.pack(fill="x", padx=30, pady=(2, 10))
entry_deposit = tk.Entry(dep_row, font=FONT_ENTRY, bg=GOLD, relief="flat", bd=4)
entry_deposit.pack(side="left", fill="x", expand=True)
tk.Button(dep_row, text="Deposit", font=FONT_BTN, bg=GOLD, fg=BG, relief="flat", padx=10, pady=8, command=deposit).pack(side="left", padx=(6,0))

# WITHDRAWAL MONEY ============================================
tk.Label(frame_dashboard, text="Withdraw", font=FONT_LABEL, bg=BG).pack(anchor="w", padx=30)
wit_row = tk.Frame(frame_dashboard, bg=BG)
wit_row.pack(fill="x", padx=30, pady=(2, 16))
entry_withdraw = tk.Entry(wit_row, font=FONT_ENTRY, bg=cottonCandy, relief="flat", bd=4)
entry_withdraw.pack(side="left", fill="x", expand=True)
tk.Button(wit_row, text="Withdraw", font=FONT_BTN, bg=blackCherry, fg=BG, relief="flat",
          padx=10, command=withdraw).pack(side="left", padx=(6, 0))

tk.Frame(frame_dashboard, height=1, bg="#e0d8c8").pack(fill="x", padx=20, pady=4)

btn_row = tk.Frame(frame_dashboard, bg=BG)
btn_row.pack(fill="x", padx=30, pady=12)
tk.Button(btn_row, text="Transaction History", font=FONT_BTN, bg=CARD, fg=DARK, relief="flat",
          padx=8, pady=8, command=check_history).pack(side="left", expand=True, fill="x", padx=(0, 6))
tk.Button(btn_row, text="Withdrawal Records", font=FONT_BTN, bg=CARD, fg=DARK, relief="flat",
          padx=8, pady=8, command=check_withdrawals).pack(side="left", expand=True, fill="x")









show_frame(frame_login)
root.mainloop()



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

tk.Button(dash_top, text="Log Out", font=FONT_BTN, bg=blackCherry, fg=BG, relief="flat", padx=10, pady=8, command=logOut).pack(side="right", padx=20)
lbl_balance = 













show_frame(frame_login)
root.mainloop()
