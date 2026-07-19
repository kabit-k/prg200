print("=" * 50)
print("PASSWORD STRENGTH CHECKER")
print("=" * 50)

passwords = [
    "hello",
    "Hello123",
    "H3ll0@World",
    "12345678",
    "MyP@ss!"
]

special = "!@#$%^&*"

for password in passwords:

    print("\nPassword:", password)

    upper = False
    lower = False
    digit = False
    special_char = False

    for ch in password:

        if ch.isupper():
            upper = True

        elif ch.islower():
            lower = True

        elif ch.isdigit():
            digit = True

        elif ch in special:
            special_char = True

    if len(password) < 8:
        print("- Minimum 8 characters required")

    if not upper:
        print("- Missing uppercase letter")

    if not lower:
        print("- Missing lowercase letter")

    if not digit:
        print("- Missing digit")

    if not special_char:
        print("- Missing special character")

    if len(password) >= 8 and upper and lower and digit and special_char:
        print("Strong Password")
    else:
        print("Weak Password")