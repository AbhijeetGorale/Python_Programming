arr = [0, 1, 0, 2, 0, 3, 0, 4, 0, 5]

sor = []
for i in arr:
    if i != 0:
        sor.append(i)
        
for i in arr:
    if i == 0:
        sor.append(i)

print(sor)

print("----------------------------------")


def zero(arr):
    non_zero = [num for num in arr if num != 0 ]
    zero = len(arr) - len(non_zero)
    return non_zero+[0]*zero

print(zero([0,1,0,2,0,3,0,4,0,5]))

print("----------------------------------")

arr = [0, 1, 0, 2, 0, 3, 0, 4, 0, 5]

# Step 1: Count non-zero elements manually
non_zero = []
count_non_zero = 0
for i in arr:
    if i != 0:
        non_zero.append(i)
        count_non_zero += 1

# Step 2: Count zeros manually
count_zero = 0
for i in arr:
    if i == 0:
        count_zero += 1

# Step 3: Build final list
for i in range(count_zero):
    non_zero.append(0)

print(non_zero)

print("----------------------------------")

