print("=" * 50)
print("EXAM SCORE AVERAGER")
print("=" * 50)

def average_score(*marks):

    average = sum(marks) / len(marks)
    return average


result = average_score(80, 75, 90, 88, 95)

print("Average Score:", result)