try:
    with open("Banker.txt", "x") as file:
        print("File created successfully.")
except FileExistsError:
    print("File already exists.")

# REGISTER =======================================================================
def register():
    with open("Banker.txt", "a") as file:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        file.write(f"{username},{password}\n")
    print("Registration successful.")

# LOGIN ==========================================================================

def logIn():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    with open("Banker.txt", "r") as file:
        for line in file:
            storedUsername, stored_password = line.strip().split(",")

            if username == storedUsername and password == stored_password:
                print("Login successful.")
                return 
            
    print("Invalid username or password.")
    return False


