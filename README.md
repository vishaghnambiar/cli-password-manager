# 🔐 CLI Password Manager

A secure command-line password manager built with Python.

## Features
- AES-based encryption using Fernet
- Master password authentication
- Secure password generation
- Encrypted local storage
- Add, view, list, and delete credentials
- No plaintext password storage

## Tech Used
- Python
- Cryptography (Fernet)
- JSON Storage

## How It Works
The master password is converted into a secure encryption key using SHA-256.
All stored passwords are encrypted and cannot be accessed without the correct master password.

## Run Locally
pip install cryptography
python main.py
