name = input("Enter your name: ")
marks = float(input("Enter your marks (0-100): "))

if 80 <= marks <= 100:
    grade = "Distinction"
elif 65 <= marks < 80:
    grade = "First Division"
elif 50 <= marks < 65:
    grade = "Second Division"
elif 40 <= marks < 50:
    grade = "Third Division"
elif 0 <= marks < 40:
    grade = "Fail"
else:
    grade = "Invalid marks"

print("Student Name:", name)
print("Marks:", marks)
print("Grade:", grade)