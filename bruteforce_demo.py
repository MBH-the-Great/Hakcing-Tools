# stripped_bruteforce_demo.py
# =========================================
# Educational demo of brute force & dictionary 
# attack concepts in Python.
# 
# ⚠️ Disclaimer: This script is safe — it only 
# tests against a hardcoded demo password and 
# a small in-memory dictionary.
# =========================================

import itertools
import string

# Demo target password (in real attacks this is unknown)
TARGET_PASSWORD = "abc"

# Character set (letters + digits only for demo)
CHAR_SET = string.ascii_lowercase + string.digits

# --- Dictionary Attack ---
def dictionary_attack():
    print("\n[*] Starting dictionary attack (demo)...")
    demo_dict = ["123", "password", "abc", "qwerty"]  # very small fake dictionary
    
    for word in demo_dict:
        print(f"Trying: {word}")
        if word == TARGET_PASSWORD:
            print(f"[+] Password found (dictionary): {word}")
            return
    print("[!] Password not found in dictionary")

# --- Brute Force Attack ---
def brute_force_attack(max_length=3):
    print("\n[*] Starting brute force attack (demo)...")
    
    for length in range(1, max_length + 1):
        for combination in itertools.product(CHAR_SET, repeat=length):
            attempt = ''.join(combination)
            print(f"Trying: {attempt}")
            if attempt == TARGET_PASSWORD:
                print(f"[+] Password found (brute force): {attempt}")
                return
    print("[!] Password not found with brute force")

# --- Run demo ---
dictionary_attack()
brute_force_attack()
