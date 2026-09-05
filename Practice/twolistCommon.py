a = [1,2,3,4,5]
b =[3,4,5,6,7]

c = []

for i in a:
    if i in b:
        c.append(i)

print(c)


# without using in 

a = [1,2,3,4,5]
b =[3,4,5,6,7]

com = []

for i in a:
    for j in b:
        if i == j:
            com.append(i)
print(com)
