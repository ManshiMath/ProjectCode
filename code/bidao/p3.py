def add1(large_integer_str):
    """
    Adds one to a very large integer represented as a string.

    :param large_integer_str: A string representation of a very large integer.
    :return: A string representation of the large integer after adding one.
    """
    # Convert the string to a list of digits for easy manipulation
    digits = list(large_integer_str)
    
    # Start adding from the least significant digit
    carry = 1
    for i in range(len(digits) - 1, -1, -1):
        sum = int(digits[i]) + carry
        carry = sum // 10  # Carry for the next iteration
        digits[i] = str(sum % 10)  # Update the current digit
        if carry == 0:
            break
    
    # If there is a carry left, add a new digit at the beginning
    if carry:
        digits.insert(0, '1')
    
    return ''.join(digits)


def div2(large_integer_str):
    """
    Divides a very large even integer represented as a string by 2.

    :param large_integer_str: A string representation of a very large even integer.
    :return: A string representation of the large integer after division by 2.
    """
    # Check if the number is even
    if int(large_integer_str) == 0:
        return large_integer_str
    #print(large_integer_str)
    # Perform the division
    remainder = 0
    result = []
    for digit in large_integer_str:
        # Calculate the new digit
        num = remainder * 10 + int(digit)
        result.append(str(num // 2))
        remainder = num % 2  # Remainder for the next iteration
    
    # Remove leading zeros if any
    result_str = ''.join(result).lstrip('0')
    return result_str if result_str else '0'

def sub1(large_integer_str):
    """
    Subtracts one from a very large integer represented as a string.

    :param large_integer_str: A string representation of a very large integer.
    :return: A string representation of the large integer after subtracting one.
    """
    # If the string is '0', it can't be decremented
    #print(large_integer_str)
    if large_integer_str == '0':
        raise ValueError("Cannot subtract one from zero.")

    digits = list(large_integer_str)
    
    # Start subtracting from the least significant digit
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] == '0':
            digits[i] = '9'  # Borrow from the next digit
        else:
            digits[i] = str(int(digits[i]) - 1)  # Subtract one
            break

    # If the first digit is '0', remove it (for cases like '1000' -> '999')
    if digits[0] == '0':
        digits.pop(0)

    return ''.join(digits)


def solution(n):
    # Your code here
    x = []
    while n != '1':
        if int(n[-1]) % 2:
            x.insert(0, 1)
            n = sub1(n)
        else:
            x.insert(0, 0)
        n = div2(n)
        # print(f"{n} {x}")
    x.insert(0, 1)
    #print(x)
    L = len(x)
    f = [[0, 0] for _ in range(L)]
    f[0][1] = 1
    for i in range(1, L):
        f[i][0] = (1 + f[i-1][0]) if x[i] == 0 else (2+min(f[i-1][0], f[i-1][1]))
        f[i][1] = (1 + f[i-1][1]) if x[i] else (2+min(f[i-1][0], f[i-1][1]))
    # import numpy as np
    # print(np.array(f))
    return f[L-1][0]
