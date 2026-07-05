marks = float(input("Enter your marks (0-100): "))

if marks >= 80 and marks <= 100:
    grade = "Distinction"
elif marks >= 65 and marks < 80:
    grade = "First Division"
elif marks >= 50 and marks < 65:
    grade = "Second Division"
elif marks >= 40 and marks < 50:
    grade = "Third Division"
elif marks >= 0 and marks < 40:
    grade = "Fail"
else:
    grade = "Invalid marks"

print("Your grade is: {grade}")


