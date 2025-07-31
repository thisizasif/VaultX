# =============================================
# VaultX - Secure Password Manager (v1.0)
# Developed by thisizasif
# =============================================

import os
from cryptography.fernet import Fernet
from pyfiglet import figlet_format

VERSION = "v1.0"
AUTHOR = "thisizasif"

def banner():
    print(figlet_format("Vault.X", font="slant"))
    print(f"🔐 Version: {VERSION}")
    print(f"👨‍💻 Developed by {AUTHOR}")
    print("=" * 50)

def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

fernet = load_key()

def add_entry():
    site = input("🌐 Website/App: ")
    username = input("👤 Username: ")
    password = input("🔒 Password: ")
    entry = f"{site} | {username} | {password}\n"
    encrypted = fernet.encrypt(entry.encode())

    with open("vault.dat", "ab") as file:
        file.write(encrypted + b"\n")
    print("✅ Entry saved to VaultX.\n")

def view_entries():
    try:
        with open("vault.dat", "rb") as file:
            for line in file:
                decrypted = fernet.decrypt(line.strip())
                print("🔑", decrypted.decode())
    except FileNotFoundError:
        print("⚠️ No saved entries found.")

def search_entry():
    keyword = input("🔍 Enter website/app name or username to search: ").lower()
    found = False
    try:
        with open("vault.dat", "rb") as file:
            for line in file:
                decrypted = fernet.decrypt(line.strip()).decode()
                if keyword in decrypted.lower():
                    print(f"🔑 Found: {decrypted}")
                    found = True
        if not found:
            print("❌ No match found.")
    except FileNotFoundError:
        print("⚠️ No entries found.")

def menu():
    banner()
    while True:
        print("\n1️⃣  Add New Entry")
        print("2️⃣  View All Entries")
        print("3️⃣  Search Vault")
        print("4️⃣  Exit")
        choice = input("➡️ Enter choice: ")

        if choice == '1':
            add_entry()
        elif choice == '2':
            view_entries()
        elif choice == '3':
            search_entry()
        elif choice == '4':
            print("👋 Exiting VaultX. Stay safe.")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    menu()
