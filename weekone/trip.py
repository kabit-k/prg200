
num_friends = int(input("How many friends went on the trek? "))

names = []
expenses = []

print("\n" + "="*40)
print("ENTER EACH PERSON'S EXPENSES")
print("="*40)

for i in range(num_friends):
    name = input(f"Enter name of friend {i+1}: ")
    amount = float(input(f"Enter total amount spent by {name} (Rs): "))
    names.append(name)
    expenses.append(amount)
    print("-"*30)

total_expenses = sum(expenses)
share_per_person = round(total_expenses / num_friends, 2)

print("\n" + "="*40)
print("TREK EXPENSE SUMMARY")
print("="*40)
print(f"Total friends: {num_friends}")
print(f"Total expenses: Rs {total_expenses:,.2f}")
print(f"Each person should pay: Rs {share_per_person:,.2f}")
print("="*40)

overpaid = [] 
underpaid = []
for i in range(num_friends):
    name = names[i]
    spent = expenses[i]
    difference = spent - share_per_person

    if difference > 0:
     
        overpaid.append({"name": name, "amount": round(difference, 2)})
    elif difference < 0:
       
        underpaid.append({"name": name, "amount": round(abs(difference), 2)})
    else:
     
        print(f"\n{name} spent exactly Rs {share_per_person:,.2f} - no payment needed!")

print("\n" + "="*40)
print("WHO PAYS WHOM?")
print("="*40)

while overpaid and underpaid:
    
    receiver = overpaid[0]
    payer = underpaid[0]
    transaction_amount = min(receiver["amount"], payer["amount"])
    print(f"{payer['name']} pays Rs {transaction_amount:,.2f} to {receiver['name']}")
    receiver["amount"] = round(receiver["amount"] - transaction_amount, 2)
    payer["amount"] = round(payer["amount"] - transaction_amount, 2)
    if receiver["amount"] == 0:
        overpaid.pop(0)
    if payer["amount"] == 0:
        underpaid.pop(0)

print("="*40)
print("\n All debts settled! Everyone pays their fair share.")