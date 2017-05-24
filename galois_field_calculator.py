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
        for i in range(0, len(x_coeffs)):
            z_coeff.insert(0, x_coeffs[i] ^ y_coeffs[i])

        z = Polynomial()

        z.import_coeffs(z_coeff)

        return z
            
    def subtract(self, x, y):
        return self.add(x,y)

    def multiply(self, x, y):
        sums = []
        x_coeffs = x.b_coeffs[::-1]
        y_coeffs = y.b_coeffs[::-1]

        for y_digit in range(len(y_coeffs)):
            prod_list = [
                0 for i in range(y_digit)
            ]

            for x_digit in range(len(x_coeffs)):
                prod = self._binary_multiply(x_coeffs[x_digit], y_coeffs[y_digit])
                prod_list.insert(0, prod)

            sums.append(Polynomial())
            sums[-1].import_coeffs(prod_list)

        Sum = sums[0]
        
        for i in range(1, len(sums)):
            Sum = self.add(Sum, sums[i])

        return Sum

    def divide(self, x, y):
        pass
    
    def _binary_reduce(self, x):
        return self._binary_division(x, self.p.b_coeffs)[1]

    def _binary_division(self, x, y):
        remainder = x
            
        num_len = len(x)
        den_len = len(y)

        quotient = ""

        # print "%20s, %20s, %20s" % ("num/remainder", "den", "quotient")
        while num_len >= den_len:
            diff = num_len - den_len
            remainder = "0"*(num_len - len(remainder)) + remainder

            den = self.p.b_coeffs + "0"*diff

            if remainder[0] == "1":
                remainder = bin(int(remainder, 2) ^ int(den, 2))[2:]
                quotient += "1"
            else:
                remainder = remainder[1:]
                quotient += "0"

            num_len -= 1
            # print "%20s, %20s, %20s" % (remainder, den, quotient)

        if not quotient:
            quotient = "0"

        return (quotient, remainder)
        
    def _binary_multiply(self, x, y):
        b_sums = []
        by_coeffs = y[::-1]
        bx_coeffs = x[::-1]
            
        for by_digit in range(len(by_coeffs)):
            binary_string = "0"*by_digit

            for bx_digit in range(len(bx_coeffs)):
                prod = int(bx_coeffs[bx_digit]) * int(by_coeffs[by_digit])
                binary_string = str(prod) + binary_string

            # binary_string = "0"*(len(by_coeffs) - (by_digit + 1)) + binary_string
            b_sums.append(binary_string)

        sum_string = b_sums[0]

        for i in range(1, len(b_sums)):
            sum_string = bin(int(sum_string, 2) ^ int(b_sums[i], 2))[2:]
        # print b_sums
        # print sum_string

        product = int(self._binary_reduce(sum_string), 2)

        return product
        

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

        # P = Polynomial("1 1 1 0", True)
        # c = GaloisFieldCalculator(P)
