weight = float(input("Enter your weight (kg): "))
height_cm = float(input("Enter your height (cm): "))

height_m = height_cm / 100

bmi = weight / (height_m ** 2)

print("Your BMI is:", round(bmi, 1))