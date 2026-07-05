salary = float(input("Enter monthly basic salary: "))

bonus = salary * 1

deduction_rate = 15
deduction = bonus * (deduction_rate / 100)

take_home = bonus - deduction

print("Monthly Basic Salary: Rs.", salary)
print("Dashain Bonus (1 month): Rs.", bonus)
print("Income Deduction (15%): Rs.", deduction)
print("Final Take-Home Bonus: Rs.", take_home)