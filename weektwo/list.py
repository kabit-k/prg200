marks = []
names = []

for i in range(3):
    n = input(f"Enter your name for student {i+1}: ")
    names.append(n)

    m = int(input(f"Enter your marks for student {i+1}: "))
    marks.append(m)

for i in range(3):
    if marks[i] >= 90:
        grade = "Distinction"
    elif marks[i] >= 75:
        grade = "First Division"
    elif marks[i] >= 60:
        grade = "Second Division"
    elif marks[i] >= 35:
        grade = "Third Division"
    else:
        grade = "Fail"

    print(f"The grade of student {names[i]} is: {grade}")