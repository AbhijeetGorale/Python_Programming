number = int(input("Enter the number :"))

orignal = number
reversed = 0

while number > 0 :
    num = number % 10
    reversed= reversed * 10 + num
    number = number // 10

print(reversed)

if orignal == reversed:
    {
        print("Palindrome")
    }
else:
    {
        print("number is not palindrome")
    }