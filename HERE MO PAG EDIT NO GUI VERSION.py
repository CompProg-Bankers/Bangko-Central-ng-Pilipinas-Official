from datetime import datetime #IMPORT DATE

now = datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")


#CREATE FILE =======================================================================
try:
    with open("Banker.txt", "x") as file:
        print("File created successfully.")
except FileExistsError:
    print("File already exists.")
    

# VALIDATE PASSWORD =======================================================================
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
    
    firstName = input("Enter your first name: ").strip()
    lastName = input("Enter your last name: ").strip()
    passWord = input("Enter your password: ").strip()

       

    # check if NA REGISTER NA
    try:
        with open("Banker.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    if parts[0] == firstName and parts[1] == lastName:
                        print("You already have an account. Please proceed to log in.")
                        return
    except FileNotFoundError:
        pass

    while True:
        print("Password must be at least 8 characters long, contain at least one uppercase letter, and one special character.")
        password = input("Enter your password: ").strip()
        if validatePassword(password):
            break
        print("Invalid password. Try Again.")

    with open("Banker.txt", "a") as file:
        file.write(f"{firstName},{lastName},{password}\n")
    print(f"Registration successful. Welcome, {firstName} {lastName}!")




# LOG IN =======================================================================
def logIn():
    firstName = input("Enter your first name: ").strip().title()
    lastName = input("Enter your last name: ").strip().title()
    password = input("Enter your password: ").strip()

    with open("Banker.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                if firstName == parts[0] and lastName == parts[1] and password == parts[2]:
                    print(f"Login successful. Welcome back, {firstName} {lastName}!")
                    return True

    print("Invalid credentials. Try Again.")
    return False

## SIGN OUT --------
def signOut():
    global is_logged_in

    if is_logged_in == True:
        is_logged_in = False
        print("\nYou have successfully signed out.")
    else:
        print("\nNo user is currently logged in.")

#DEPOSIT MONEY
def depositMoney():
    amount = float(input("Enter the amount to deposit: "))
    with open("bank.txt", "a") as file:
        file.write(f"Deposit: {amount} on ({date})\n")
    print(f"Deposit: {amount} on ({date})")


#CHECK BALANCE
def check_balance():
    Name = float(input("Enter Account Name to verify: "))
    with open("bank.txt","a")as file:
        file.write(f"Check balance: {Name} on ({date}) \n")
    print(f"Check balance: {Name} on ({date})")
    

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

