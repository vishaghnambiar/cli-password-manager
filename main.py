from cryptography.fernet import Fernet
import json
import os
import base64
import hashlib
import getpass
import random
import string

VAULT_FILE = "vault.json"


# ==============================
# 🔐 KEY GENERATION FROM MASTER PASSWORD
# ==============================
def generate_key(master_password):
    password_bytes = master_password.encode()
    hashed = hashlib.sha256(password_bytes).digest()
    key = base64.urlsafe_b64encode(hashed)
    return key


# ==============================
# 📂 LOAD / CREATE VAULT
# ==============================
def load_vault():
    if not os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "w") as file:
            json.dump({}, file)
        return {}

    try:
        with open(VAULT_FILE, "r") as file:
            content = file.read().strip()
            if not content:
                return {}
            return json.loads(content)

    except json.JSONDecodeError:
        print("⚠ Vault corrupted. Resetting...")
        return {}


def save_vault(data):
    with open(VAULT_FILE, "w") as file:
        json.dump(data, file, indent=4)


# ==============================
# 🔒 ENCRYPT / DECRYPT
# ==============================
def encrypt_password(fernet, password):
    return fernet.encrypt(password.encode()).decode()


def decrypt_password(fernet, encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()


# ==============================
# 🔑 AUTHENTICATION
# ==============================
def authenticate():
    master_password = getpass.getpass("Enter Master Password: ")
    key = generate_key(master_password)
    return Fernet(key)


# ==============================
# 🔐 PASSWORD GENERATOR
# ==============================
def generate_password(length=14):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


# ==============================
# ➕ ADD PASSWORD
# ==============================
def add_password(fernet, vault):
    site = input("Enter site name: ")
    username = input("Enter username: ")

    choice = input("Generate strong password? (y/n): ").lower()

    if choice == "y":
        password = generate_password()
        print(f"Generated Password: {password}")
    else:
        password = getpass.getpass("Enter password: ")

    encrypted = encrypt_password(fernet, password)

    vault[site] = {
        "username": username,
        "password": encrypted
    }

    save_vault(vault)
    print("✅ Password saved securely.")


# ==============================
# 🔍 VIEW PASSWORD
# ==============================
def view_password(fernet, vault):
    site = input("Enter site name: ")

    if site not in vault:
        print("❌ No record found.")
        return

    record = vault[site]
    decrypted = decrypt_password(fernet, record["password"])

    print(f"\nSite: {site}")
    print(f"Username: {record['username']}")
    print(f"Password: {decrypted}")


# ==============================
# 📋 LIST ALL SITES
# ==============================
def list_sites(vault):
    if not vault:
        print("No passwords stored.")
        return

    print("\nSaved Accounts:")
    for site in vault:
        print(f" - {site}")


# ==============================
# 🗑 DELETE ENTRY
# ==============================
def delete_password(vault):
    site = input("Enter site to delete: ")

    if site in vault:
        del vault[site]
        save_vault(vault)
        print("🗑 Entry deleted.")
    else:
        print("❌ Site not found.")


# ==============================
# 📜 MENU
# ==============================
def menu():
    print("\n==== Secure CLI Password Manager ====")
    print("1. Add Password")
    print("2. View Password")
    print("3. List Stored Sites")
    print("4. Delete Entry")
    print("5. Exit")


# ==============================
# 🚀 MAIN LOOP
# ==============================
def main():
    fernet = authenticate()
    vault = load_vault()

    while True:
        menu()
        choice = input("Choose option: ")

        if choice == "1":
            add_password(fernet, vault)

        elif choice == "2":
            view_password(fernet, vault)

        elif choice == "3":
            list_sites(vault)

        elif choice == "4":
            delete_password(vault)

        elif choice == "5":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
