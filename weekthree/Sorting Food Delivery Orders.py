print("=" * 50)
print("SORTING FOOD DELIVERY ORDERS")
print("=" * 50)

orders = [
    ("ORD101", 30),
    ("ORD102", 15),
    ("ORD103", 45),
    ("ORD104", 10),
    ("ORD105", 25)
]

orders.sort(key=lambda order: order[1])

print("Orders sorted by delivery time:\n")

for order in orders:
    print(order)