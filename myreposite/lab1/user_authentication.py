import hashlib

# Initial dictionary of users (login, hashed password, full name)
users = {
    "wulfiecs123": {
        "password": hashlib.md5("alex_under".encode()).hexdigest(),
        "full_name": "Lomov Anton"
    },
    "user456": {
        "password": hashlib.md5("petrenko".encode()).hexdigest(),
        "full_name": "Ivan Petrenko"
    }
}

def check_password(login, input_password):
    """Checks the user's entered password."""
    if login in users:
        hashed_input = hashlib.md5(input_password.encode()).hexdigest()
        if hashed_input == users[login]["password"]:
            print(f"Welcome, {users[login]['full_name']}! Login successful.")
        else:
            print("Incorrect password.")
    else:
        print("User not found.")

# User input
login = input("Enter login: ").strip()
password = input("Enter password: ").strip()

# Password check
check_password(login, password)


check_password(login, password)
