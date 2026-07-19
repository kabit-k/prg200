print("=" * 50)
print("TAXI FARE CALCULATOR")
print("=" * 50)

trips = [
    {"distance": 1.5, "hour": 14},
    {"distance": 5.0, "hour": 22},
    {"distance": 12.0, "hour": 3},
    {"distance": 8.5, "hour": 10},
    {"distance": 2.0, "hour": 23},
]

trip_no = 1

for trip in trips:

    distance = trip["distance"]
    hour = trip["hour"]

    fare = 150

    if distance > 2:

        if distance <= 10:
            fare = fare + (distance - 2) * 35

        else:
            fare = fare + (8 * 35)
            fare = fare + (distance - 10) * 28

    if hour >= 22 or hour < 5:
        fare = fare + (fare * 10 / 100)

    print("Trip", trip_no)
    print("Distance:", distance, "km")
    print("Hour:", hour)
    print("Fare: NPR", round(fare, 2))
    print("-" * 40)

    trip_no = trip_no + 1