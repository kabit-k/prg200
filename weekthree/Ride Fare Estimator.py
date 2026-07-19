print("=" * 50)
print("RIDE FARE ESTIMATOR")
print("=" * 50)

def estimate_fare(distance_km, vehicle_type, surge=1.0):

    if vehicle_type.lower() == "bike":
        rate = 20

    elif vehicle_type.lower() == "car":
        rate = 40

    elif vehicle_type.lower() == "van":
        rate = 60

    else:
        return "Invalid vehicle type"

    fare = distance_km * rate * surge
    return fare


distance = float(input("Enter distance (km): "))
vehicle = input("Enter vehicle type (Bike/Car/Van): ")
surge = float(input("Enter surge multiplier (Default = 1.0): "))

result = estimate_fare(distance, vehicle, surge)

print("Estimated Fare: NPR", result)