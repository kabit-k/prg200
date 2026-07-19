purchase = float(input("Enter purchase amount (NPR): "))
member = input("Are you a loyalty member? (yes/no): ")

if purchase < 1000:
    discount = 0
elif purchase < 5000:
    discount = 5
elif purchase < 15000:
    discount = 10
else:
    discount = 20

discount_amount = purchase * discount / 100
final_amount = purchase - discount_amount

if member.lower() == "yes":
    loyalty_discount = final_amount * 5 / 100
    final_amount = final_amount - loyalty_discount
    print("Purchase Discount:", discount, "%")
    print("Loyalty Discount: 5%")
else:
    print("Purchase Discount:", discount, "%")

print("Final Payable Amount: NPR", final_amount)