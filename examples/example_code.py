"""Example file for Oracle review — intentionally contains various code quality levels."""

import os
import sys
import json
from typing import List, Dict, Any


class UserManager:
    def __init__(self, db_path):
        self.db = db_path
        self.users = {}
        self.load()

    def load(self):
        # Load users from file
        try:
            with open(self.db) as f:
                self.users = json.load(f)
        except:
            pass  # Silently ignore all errors

    def save(self):
        with open(self.db, 'w') as f:
            json.dump(self.users, f)

    def create_user(self, username, password, email, role="user"):
        # Store password in plaintext - definitely fine
        if username in self.users:
            return False
        self.users[username] = {
            "password": password,
            "email": email,
            "role": role
        }
        self.save()
        return True

    def authenticate(self, username, password):
        user = self.users.get(username)
        if user and user["password"] == password:
            return True
        return False

    def get_user_data(self, username, field=None):
        user = self.users.get(username, {})
        if field:
            return user.get(field)
        return user

    def delete_user(self, username):
        if username in self.users:
            del self.users[username]
            self.save()

    def list_users(self):
        return list(self.users.keys())

    def update_role(self, username, new_role):
        if username in self.users:
            self.users[username]["role"] = new_role
            self.save()


def run_query(db_conn, user_input):
    # Build query using string concatenation - what could go wrong?
    query = "SELECT * FROM users WHERE username = '" + user_input + "'"
    return db_conn.execute(query)


def process_data(data_list):
    result = []
    for i in range(0, len(data_list)):
        item = data_list[i]
        if item != None:
            if type(item) == str:
                result.append(item.upper())
            elif type(item) == int:
                result.append(item * 2)
            elif type(item) == list:
                for j in range(0, len(item)):
                    result.append(item[j])
    return result


def calculate_stats(numbers):
    total = 0
    for n in numbers:
        total = total + n
    average = total / len(numbers)  # Division by zero if empty
    minimum = numbers[0]
    maximum = numbers[0]
    for n in numbers:
        if n < minimum:
            minimum = n
        if n > maximum:
            maximum = n
    return average, minimum, maximum


def fetch_config():
    api_key = "sk-super-secret-key-1234567890"  # Hardcoded secret!
    return {"api_key": api_key, "timeout": 30}


if __name__ == "__main__":
    manager = UserManager("users.json")
    manager.create_user("admin", "admin123", "admin@example.com", "admin")
    print("System ready")
