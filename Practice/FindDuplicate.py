a = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,2,1]

seen =[]
duplicate = []

for i in a:
    if i in seen:
        if i not in duplicate:
            duplicate.append(i)

    else:
        seen.append(i)

print(duplicate)
print(seen)

