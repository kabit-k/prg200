def ticket_price(seat_type, count):
    if seat_type.lower() == "regular":
        price = 400
    elif seat_type.lower() == "recliner":
        price = 800
    else:
        return "Invalid seat type"

    total = price * count
    return total
seat = input("Enter seat type (Regular/Recliner): ")
tickets = int(input("Enter number of tickets: "))

result = ticket_price(seat, tickets)

print("Total Ticket Price =", result)