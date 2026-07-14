marks = int(input("Enter your marks: "))

if marks >= 75:
    grade = "Distinction"
else:
    if marks >= 60:
        grade = "First Class"
    else:
        if marks >= 50:
            grade = "Second Class"
        else:
            grade = "Fail"

print("Your grade is:", grade)
