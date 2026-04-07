#!/usr/bin/env python3
"""
Generate a bcrypt hash for a given password using passlib.
"""

from passlib.hash import bcrypt

def generate_hash(password: str) -> str:
    """
    Hash the provided password using bcrypt.
    """
    return bcrypt.hash(password)

if __name__ == "__main__":
    password = "Marcie!!!$$$"   # <-- your chosen password
    hashed = generate_hash(password)
    print("\nGenerated bcrypt hash:\n")
    print(hashed)
    print("\nUse this hash in your MySQL users table.\n")
