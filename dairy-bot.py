import datetime
import os
import hashlib
from collections import Counter

LOG_FILE = "mental_health_log.txt"
PASSWORD_FILE = "password.txt"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def set_password():
    password = input("🔐 Set a password for your diary: ")
    hashed = hash_password(password)
    with open(PASSWORD_FILE, "w") as f:
        f.write(hashed)
    print("✅ Password set successfully!\n")

def check_password():
    if not os.path.exists(PASSWORD_FILE):
        set_password()
    else:
        for _ in range(3):  # 3 attempts
            password = input("🔐 Enter your password: ")
            hashed = hash_password(password)
            with open(PASSWORD_FILE, "r") as f:
                stored_hash = f.read()
            if hashed == stored_hash:
                print("✅ Access granted!\n")
                return True
            else:
                print("❌ Incorrect password.")
        print("🔒 Too many failed attempts. Exiting.")
        exit()

def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def log_entry(name, mood, note):
    timestamp = get_timestamp()
    with open(LOG_FILE, "a") as file:
        file.write(f"{timestamp} - {name}'s Entry\n")
        file.write(f"Mood: {mood}\n")
        if note.strip():
            file.write(f"Note: {note}\n")
        file.write("-" * 40 + "\n")

def view_entries():
    print("\n📖 Previous Entries:\n")
    try:
        with open(LOG_FILE, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("No entries found yet.")

def mood_stats():
    try:
        with open(LOG_FILE, "r") as file:
            lines = file.readlines()
        moods = [line.split(": ")[1].strip().lower() for line in lines if line.startswith("Mood:")]
        mood_count = Counter(moods)

        print("\n📊 Mood Statistics:\n")
        for mood, count in mood_count.items():
            print(f"{mood.capitalize()}: {count} times")
    except FileNotFoundError:
        print("No data to analyze yet.")

def main():
    print("Welcome to the Mental Health Diary Bot!")
    check_password()
    name = input("What is your name? ").strip().capitalize()

    while True:
        print("\n📋 Menu:")
        print("1. Add new diary entry")
        print("2. View previous entries")
        print("3. View mood statistics")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            mood = input(f"Hi {name}, How are you feeling today? (e.g., happy, sad, anxious, nervous): ").strip().lower()
            note = input("Would you like to write anything else? It's okay if you don't! :) (Press Enter to skip): ")
            log_entry(name, mood, note)
            print(f"\nThank you {name}, your entry has been saved! ✅")
        elif choice == "2":
            view_entries()
        elif choice == "3":
            mood_stats()
        elif choice == "4":
            print(f"Goodbye, {name}! Stay mindful. You will be okay soon, Stay motivated and Keep Learning! 🌸")
            break
        else:
            print("Invalid input. Please choose from 1 to 4.")

if __name__ == "__main__":
    main()