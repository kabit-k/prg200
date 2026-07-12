
def convert_to_npr(dollar):
    rate = 138
    return dollar * rate

usd = float(input("Enter amount in USD: "))

result = convert_to_npr(usd)

print("NPR =", result)