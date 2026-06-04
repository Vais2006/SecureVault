# main.py
from register_recovery import register_user_with_recovery
from login import authenticate_user
from database import create_database

def main_menu():
    """Main application menu"""
    create_database()

    while True:
        print("\n=== Offline MFA Authentication System ===")
        print("1. Register new user")
        print("2. Login")
        print("3. Exit")

        choice = input("Select option (1-3): ")

        if choice == "1":
            print("\n--- User Registration ---")
            username = input("Enter username: ")
            password = input("Enter password: ")
            recovery_phrase = input("Enter recovery phrase (remember this!): ")
            register_user_with_recovery(username, password, recovery_phrase)

        elif choice == "2":
            print("\n--- User Login ---")
            username = input("Enter username: ")
            password = input("Enter password: ")
            otp_code = input("Enter OTP from Google Authenticator: ")
            authenticate_user(username, password, otp_code)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option! Please try again.")


if __name__ == "__main__":
    main_menu()
