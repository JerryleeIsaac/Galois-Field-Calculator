from input_parser import InputParser
from polynomial import Polynomial

class GaloisFieldCalculator:
    def __init__(self, p):
        self.p = p

    def add(self, x, y):
        x_coeffs = x.coeffs[::-1]
        y_coeffs = y.coeffs[::-1]

        if x.degree > y.degree:
            for i in range(x.degree - y.degree):
                y_coeffs.append(0)
        elif y.degree > x.degree:
            for i in range(y.degree - x.degree):
                x_coeffs.append(0)

        z_coeff = []
        for i in range(0, x.degree + 1):
            z_coeff.insert(0, x_coeffs[i] ^ y_coeffs[i])

        z = Polynomial()

        z.import_coeffs(z_coeff)

        return z
            
    def subtract(self, x, y):
        return self.add(x,y)

    def multiply(self, x, y):
        pass

    def divide(self, x, y):
        pass
    
    def binary_multiply(self, x, y):
        b_sums = []
        by_coeffs = y[::-1]
        bx_coeffs = x[::-1]
            
        for by_digit in range(len(by_coeffs)):
            binary_string = ""

            binary_string += "0"*by_digit

            for bx_digit in range(len(bx_coeffs)):
                prod = bx_coeffs[bx_digit] * by_coeffs[by_digit]
                binary_string = prod + binary_string

            binary_string = "0"*(len(by_coeffs) - (by_digit + 1)) + binary_string
            b_sums.append(binary_string)

        sum_string = b_sums[0]

        for i in range(1, len(b_sums)):
            sum_string = bin(int(sum_string, 2) ^ int(b_sums[i], 2))[2:]
        

if __name__ == "__main__":
    cases = InputParser.read_inputs()

    for case in cases:
        polynomial_strings = InputParser.separate_polynomials(case)
        A_string = polynomial_strings[0]
        B_string = polynomial_strings[1]
        P_string = polynomial_strings[2]

        P = Polynomial(P_string, True)
        A = Polynomial(A_string, False, P.max_coeff)
        B = Polynomial(B_string, False, P.max_coeff)

        Calculator = GaloisFieldCalculator(P)
        
        Sum = Calculator.add(A, B)
        
        print "---------------------------------------------------"
        print "Sum of {} and {}".format(A, B)
        print "==================================================="
        print Sum
        print "---------------------------------------------------"

        Difference = Calculator.subtract(A, B)
        
        print "---------------------------------------------------"
        print "Difference of {} and {}".format(A, B)
        print "==================================================="
        print Difference 
        print "---------------------------------------------------"

        
        Product = Calculator.multiply(A,B)
        print "---------------------------------------------------"
        print "Product of {} and {}".format(A, B)
        print "==================================================="
        print Product 
        print "---------------------------------------------------"
