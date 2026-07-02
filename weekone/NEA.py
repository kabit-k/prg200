
previous_reading = float(input("Enter previous meter reading (kWh): "))
current_reading = float(input("Enter current meter reading (kWh): "))
per_unit_rate = float(input("Enter per-unit rate (Rs per kWh): "))
service_charge = float(input("Enter fixed monthly service/meter charge (Rs): "))

units_consumed = current_reading - previous_reading

energy_cost = units_consumed * per_unit_rate

total_bill = energy_cost + service_charge

total_bill = round(total_bill, 2)

print("\n" + "="*40)
print("NEA ELECTRICITY BILL ESTIMATE")
print("="*40)
print(f"Previous reading: {previous_reading:,.2f} kWh")
print(f"Current reading: {current_reading:,.2f} kWh")
print(f"Units consumed: {units_consumed:,.2f} kWh")
print(f"Energy cost ({per_unit_rate} Rs/kWh): Rs {energy_cost:,.2f}")
print(f"Service charge: Rs {service_charge:,.2f}")
print("-"*40)
print(f"TOTAL BILL: Rs {total_bill:,.2f}")
print("="*40)