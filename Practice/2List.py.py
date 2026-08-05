# accept four student marks and display in sort manner

Marks = []

a = input("enter the mark of 1 student :")
Marks.append(a)

b = input("enter the mark of 2 student :")
Marks.append(b)

c = input("enter the mark of 3 student :")
Marks.append(c)

d = input("enter the mark of 4 student :")
Marks.append(d)

print(Marks)
Marks.sort()
print("sorted marks :",Marks)