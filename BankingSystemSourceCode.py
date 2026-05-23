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
    
    firstName = entry_first.get().strip()
    lastName = input("Enter last name: ").strip()
       

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
        password = input("Enter password (8+ chars, 1 uppercase, 1 special char): ")
        if validatePassword(password):
            break
        print("Invalid password. Try Again")

    with open("Banker.txt", "a") as file:
        file.write(f"{firstName},{lastName},{password}\n")
    print(f"Registration successful. Welcome, {firstName} {lastName}!")


# LOG IN =======================================================================
def logIn():
    firstName = input("Enter first name: ").strip().title()
    lastName = input("Enter last name: ").strip().title()
    password = input("Enter your password: ")

    with open("Banker.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                if firstName == parts[0] and lastName == parts[1] and password == parts[2]:
                    print(f"Login successful. Welcome back, {firstName} {lastName}!")
                    return True

    print("Invalid credentials. Try Again.")
    return False


#DEPOSIT MONEY
def depositMoney():
    amount = float(input("Enter amount:    "))
    with open("bank.txt", "a") as file:
        file.write(f"Deposit: {amount} on ({date})\n")
    print(f"Deposit: {amount} on ({date})")



