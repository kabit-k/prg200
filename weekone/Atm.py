correct_pin = "1234"
attempts = 0
max_attempts = 3

print("Insert your card.")
input("Press Enter to continue...")

while attempts < max_attempts:
    pin = input("Enter your PIN: ")

    if pin == correct_pin:
        print("PIN correct. Welcome!")
        break
    else:
        attempts += 1
        print("Wrong PIN!")

if attempts == max_attempts:
    print("You entered the wrong PIN 3 times.")
    print("Your card has been BLOCKED.")
else:
    print("You can now use ATM services.")
    