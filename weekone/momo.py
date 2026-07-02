
cost_per_plate = float(input("Enter cost price per plate (Rs): "))
selling_per_plate = float(input("Enter selling price per plate (Rs): "))
plates_sold = int(input("Enter number of plates sold: "))

total_revenue = selling_per_plate * plates_sold
total_cost = cost_per_plate * plates_sold
total_profit = total_revenue - total_cost

profit_margin = (total_profit / total_revenue) * 100
profit_margin = round(profit_margin, 2)
print("\n" + "="*45)
print("MOMO SHOP PROFIT REPORT")
print("="*45)

print(f"Cost per plate: Rs {cost_per_plate:,.2f}")
print(f"Selling price per plate: Rs {selling_per_plate:,.2f}")
print(f"Plates sold: {plates_sold}")
print("-"*45)
print(f"Total Revenue: Rs {total_revenue:,.2f}")
print(f"Total Cost: Rs {total_cost:,.2f}")
print(f"Total Profit: Rs {total_profit:,.2f}")
print(f"Profit Margin: {profit_margin}%")
print("-"*45)

if total_profit > 0:
    print(" STATUS: PROFIT! Business is doing well.")
    if profit_margin > 20:
        print(" Excellent profit margin! Keep up the good work!")
    elif profit_margin > 10:
        print(" Good profit margin. You're doing well.")
    else:
        print(" Small profit margin. Consider reducing costs or increasing prices.")
elif total_profit < 0:
    loss_amount = abs(total_profit)
    print(" STATUS: LOSS! Business is losing money.")
    print(f" You are losing Rs {loss_amount:,.2f}")
    print(" Suggestions:")
    print("   - Increase selling price")
    print("   - Reduce cost price (buy ingredients cheaper)")
    print("   - Sell more plates to cover fixed costs")
else:
    print(" STATUS: BREAKING EVEN! No profit, no loss.")
    print(" Suggestions:")
    print("   - Increase prices slightly")
    print("   - Find ways to reduce costs")

print("="*45)