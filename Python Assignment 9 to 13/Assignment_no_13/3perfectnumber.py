def perfect (n):
    sum = 0  

    for i in range(1,n):
        if n % i == 0 :
            sum =sum +i

    return sum == n 


num = int (input("enter  number "))
if perfect(num):
    print("this is perfect no")

else:
    print("this is not perfect number")                