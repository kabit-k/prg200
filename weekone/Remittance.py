
usd_amount = float(input("Enter amount in USD sent: "))
exchange_rate = float(input("Enter current exchange rate (USD to NPR): "))
fee_percentage = float(input("Enter service fee percentage (e.g., 2 for 2%): "))

fee_amount = usd_amount * (fee_percentage / 100)

amount_after_fee = usd_amount - fee_amount

npr_amount = amount_after_fee * exchange_rate

print("\n" + "="*40)
print("REMITTANCE DETAILS")
print("="*40)
print(f"Amount sent (USD): ${usd_amount:.2f}")
print(f"Exchange rate: 1 USD = {exchange_rate:.2f} NPR")
print(f"Service fee: {fee_percentage}% = ${fee_amount:.2f}")
print(f"Amount after fee: ${amount_after_fee:.2f}")
print(f"Final amount received: NPR {npr_amount:,.2f}")
print("="*40)