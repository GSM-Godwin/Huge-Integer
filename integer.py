class HugeInteger:
    def __init__(self, value="0"):
        # Initialize the HugeInteger with an array of 40 zeros.
        self.digits = [0] * 40
        # Parse the input string to populate the digits array.
        self.parse(value)

    def parse(self, value):
        """
        Parse a string into the HugeInteger array.
        Each character of the string is converted into an integer and stored in the array.
        """
        if len(value) > 40:
            # Raise an error if the input string exceeds 40 digits.
            raise ValueError("Value exceeds 40 digits.")
        for i, char in enumerate(value.zfill(40)):
            # Pad the string with leading zeros to ensure 40 digits.
            if not char.isdigit():
                # Confirm that the input contains only numeric characters.
                raise ValueError("Value must only contain digits.")
            self.digits[i] = int(char)

    def __str__(self):
        """
        Convert the HugeInteger to a string by joining its digits.
        Strip leading zeros for proper formatting and return "0" if all digits are zero.
        """
        return ''.join(map(str, self.digits)).lstrip('0') or '0'

    def isEqualTo(self, other):
        # Check if the digits array of this object matches another HugeInteger.
        return self.digits == other.digits

    def isNotEqualTo(self, other):
        # Return the negation of the isEqualTo method.
        return not self.isEqualTo(other)

    def isGreaterThan(self, other):
        # Compare the digits arrays to check if this object is greater.
        return self.digits > other.digits

    def isLessThan(self, other):
        # Compare the digits arrays to check if this object is lesser.
        return self.digits < other.digits

    def isGreaterThanOrEqualTo(self, other):
        # Check if the HugeInteger is greater than or equal to another HugeInteger.
        return self.digits >= other.digits

    def isLessThanOrEqualTo(self, other):
        # Check if the HugeInteger is less than or equal to another HugeInteger.
        return self.digits <= other.digits

    def isZero(self):
        # Check if all elements in the digits array are zero.
        return all(digit == 0 for digit in self.digits)

    def add(self, other):
        """
        Add two HugeInteger objects and return the result.
        Handles carry over for each digit and raises an error if there is an overflow.
        """
        result = HugeInteger()
        carry = 0
        for i in range(39, -1, -1):
            temp_sum = self.digits[i] + other.digits[i] + carry
            result.digits[i] = temp_sum % 10
            carry = temp_sum // 10
        if carry > 0:
            raise OverflowError("Addition overflow: result exceeds 40 digits.")
        return result

    def subtract(self, other):
        """
        Subtract one HugeInteger from another.
        Ensures non-negative results by raising an error if the minuend is smaller.
        """
        if self.isLessThan(other):
            raise ValueError("Cannot subtract a larger number from a smaller one.")
        result = HugeInteger()
        borrow = 0
        for i in range(39, -1, -1):
            temp_diff = self.digits[i] - other.digits[i] - borrow
            if temp_diff < 0:
                temp_diff += 10
                borrow = 1
            else:
                borrow = 0
            result.digits[i] = temp_diff
        return result

    def multiply(self, other):
        """
        Multiply two HugeInteger objects.
        Uses a temporary array for intermediate results and checks for overflow.
        """
        result = HugeInteger()
        temp_result = [0] * 80  # Array to hold up to 80 digits during multiplication.
        for i in range(39, -1, -1):
            carry = 0
            for j in range(39, -1, -1):
                temp_product = self.digits[i] * other.digits[j] + temp_result[i + j + 1] + carry
                temp_result[i + j + 1] = temp_product % 10
                carry = temp_product // 10
            temp_result[i] += carry
        if any(temp_result[:40]):
            raise OverflowError("Multiplication overflow: result exceeds 40 digits.")
        result.digits = temp_result[40:]  # Copy the last 40 digits to the result.
        return result

    def divide(self, other):
        """
        Divide this HugeInteger by another.
        Implements long division and returns the quotient as a HugeInteger.
        """
        if other.isZero():
            raise ZeroDivisionError("Cannot divide by zero.")
        result = HugeInteger()
        remainder = HugeInteger()
        for digit in self.digits:
            remainder.digits = remainder.digits[1:] + [digit]
            count = 0
            while remainder.isGreaterThanOrEqualTo(other):
                remainder = remainder.subtract(other)
                count += 1
            result.digits = result.digits[1:] + [count]
        return result

    def remainder(self, other):
        """
        Compute the remainder when this HugeInteger is divided by another.
        """
        if other.isZero():
            raise ZeroDivisionError("Cannot divide by zero.")
        remainder = HugeInteger()
        for digit in self.digits:
            remainder.digits = remainder.digits[1:] + [digit]
            while remainder.isGreaterThanOrEqualTo(other):
                remainder = remainder.subtract(other)
        return remainder

# Example Usage
num1 = HugeInteger("1234567890123456789012345678901234567890")
num2 = HugeInteger("987654321098765432109876543210987654321")

print("num1:", num1)  # Display the first HugeInteger.
print("num2:", num2)  # Display the second HugeInteger.

sum_result = num1.add(num2)  # Add num1 and num2.
print("Sum:", sum_result)

diff_result = num1.subtract(num2)  # Subtract num2 from num1.
print("Difference:", diff_result)
