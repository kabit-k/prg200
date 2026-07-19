print("=" * 50)
print("STUDENT ENROLLMENT PROFILE")
print("=" * 50)

def build_profile(name, **details):

    print("Student Name:", name)

    for key, value in details.items():
        print(key, ":", value)


build_profile(
    "Siri",
    Age=20,
    Program="BSc Computing",
    Semester=3,
    Portfolio="www.portfolio.com"
)