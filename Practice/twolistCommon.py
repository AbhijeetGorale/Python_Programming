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

def common(arr1,arr2):
    set1 = set (arr1)
    return list(set1.intersection(arr2))

print(common([1,2,3,4,5],[3,4,5,6,7]))
