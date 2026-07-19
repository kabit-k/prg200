print("=" * 50)
print("NCELL DATA PACK RECHARGE")
print("=" * 50)

def recharge_cost(gb, validity_days=30):

    if gb == 1:
        price = 100
    elif gb == 5:
        price = 450
    elif gb == 10:
        price = 800
    elif gb == 20:
        price = 1500
    else:
        return "Data pack not available."

    return f"Price: NPR {price}\nValidity: {validity_days} days"


gb = int(input("Enter data pack (GB): "))

result = recharge_cost(gb)

print(result)