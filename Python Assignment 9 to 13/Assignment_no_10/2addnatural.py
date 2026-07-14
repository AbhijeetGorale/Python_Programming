def sumnaturalnumber(n):
    return n * (n + 1) // 2

def main():
    n = int(input("Enter a number: "))
    print("Sum of natural numbers is:", sumnaturalnumber(n))

if __name__ == "__main__":
    main()