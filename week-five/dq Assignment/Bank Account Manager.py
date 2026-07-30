class BankAccount:
    def __init__(self, name, account_number, balance=0):
        self.name = name
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print(f"{self.name}: Insufficient funds")

    def get_balance(self):
        print(f"Name: {self.name}")
        print(f"Balance: NPR {self.balance}")
        print()


accounts = [
    ("Ramesh Thapa", "A001", 5000),
    ("Sunita Karki", "A002", 0),
    ("Bikash Rai", "A003", 12000),
]

bank_accounts = []

for name, acc_no, balance in accounts:
    bank_accounts.append(BankAccount(name, acc_no, balance))

# Operations
for account in bank_accounts:
    if account.account_number == "A002":
        account.deposit(3000)

    elif account.account_number == "A003":
        account.withdraw(15000)

    elif account.account_number == "A001":
        account.withdraw(2000)

# Final balances
for account in bank_accounts:
    account.get_balance()