from input_parser import InputParser
from polynomial import Polynomial

class GaloisFieldCalculator:
    def __init__(self, p):
        self.p = p

    def add(self, x, y):
        """
        Accepts Polynomial x and y and returns
        Polynomial z as sum
        """
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
        """
        Accepts Polynomial x, y and returns
        Polynomial as difference
        """
        return self.add(x,y)

    def multiply(self, x, y):
        """
        Accepts Polynomial x, y
        and returns Polynomial product
        """
        sums = []
        x_coeffs = x.coeffs[::-1]
        y_coeffs = y.coeffs[::-1]

        for y_digit in range(len(y_coeffs)):
            prod_list = [
                0 for i in range(y_digit)
            ]

            for x_digit in range(len(x_coeffs)):
                b_x = bin(x_coeffs[x_digit])[2:]
                b_y = bin(y_coeffs[y_digit])[2:]
                prod = self._gf_multiply(b_x, b_y)
                prod_list.insert(0, int(prod, 2))

            sums.append(Polynomial())
            sums[-1].import_coeffs(prod_list)

        Sum = sums[0]
        
        for i in range(1, len(sums)):
            Sum = self.add(Sum, sums[i])

        return Sum

    def divide(self, x, y):
        """
        Accepts Polynomial x, y
        returns Polynomial quotient and remainder
        """
        x_coeffs = x.coeffs
        y_coeffs = y.coeffs

        remainder = x_coeffs

        num_len = len(x_coeffs)
        den_len = len(y_coeffs)

        quotient = []

        den = [i for i in y_coeffs]
        while num_len >= den_len:
            diff = num_len - den_len

            den = den[:den_len]
            den += [0 for i in range(diff)]

            # print "%20s, %20s" %(remainder, den)
            # print len(den), len(remainder)

            if len(den) <= len(remainder):
                b_rem = bin(remainder[0])[2:]
                b_den = bin(den[0])[2:]
                
                q = int(self._gf_divide(b_rem, b_den), 2)
                quotient.append(q)
                
                Q = Polynomial()
                Q.import_coeffs([q])

                D = Polynomial()
                D.import_coeffs(den)

                D = self.multiply(D, Q)
                R = Polynomial()
                R.import_coeffs(remainder)

                remainder = self.subtract(R,D).coeffs
            else:
                quotient.append(0)

            num_len -= 1

        # print quotient, remainder

        Q = Polynomial()
        R = Polynomial()

        Q.import_coeffs(quotient)
        R.import_coeffs(remainder)

        return (Q,R)

    
    def _gf_divide(self, x, y):
        """
        Accepts x as numerator, y as denominator. Binary format
        Calls inverse of y and then multiplies
        Returns binary format
        """
        return self._gf_multiply(x, self._gf_inverse(y))

    def _gf_reduce(self, x):
        """
        Accepts binary x of format "0000"
        and reduces it using the irreducible polynomial
        Returns binary format
        """
        return self._binary_divide(x, self.p.b_coeffs)[1]

    def _gf_inverse(self, x):
        t = bin(0)[2:]
        r = self.p.b_coeffs
        new_t = bin(1)[2:]
        new_r = x

        while int(new_r,2) != 0:
            quotient, remainder = self._binary_divide(r, new_r)
            r, new_r = new_r, remainder
            d = self._gf_multiply(quotient, new_t)
            t, new_t = new_t, bin(int(t,2) ^ int(d,2))[2:]

        if int(r,2) > 1:
            raise Exception("{} is not invertible".format(x))

        return t

    def _gf_multiply(self, x, y):
        """
        Accepts binary strings x,y of format "00101010"
        Returns binary string
        """
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

        product = self._gf_reduce(sum_string)

        return product

    def _binary_divide(self, x, y):
        """
        Accepts x and y as binary and performs
        long division with modulo 2.
        Returns binary quotient and remainder
        """
        remainder = x

        # print "num: {}, den: {}".format(x,y)
            
        num_len = len(x)
        den_len = len(y)

        quotient = ""

        # print "%20s, %20s, %20s" % ("num/remainder", "den", "quotient")
        while num_len >= den_len:
            diff = num_len - den_len
            remainder = "0"*(num_len - len(remainder)) + remainder

            den = y + "0"*diff

            # print "%20s, %20s, %20s" % (remainder, den, quotient)
            if remainder[0] == "1":
                remainder = bin(int(remainder, 2) ^ int(den, 2))[2:]
                quotient += "1"
            else:
                remainder = remainder[1:]
                quotient += "0"

            num_len -= 1

        if not quotient:
            quotient = "0"

        # print "q: {}, r:{}".format(quotient, remainder)
        return (quotient, remainder)
        

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
        
        print "Sum of {} and {}".format(A, B)
        print Sum

        Difference = Calculator.subtract(A, B)
        
        print "Difference of {} and {}".format(A, B)
        print Difference 

        Product = Calculator.multiply(A,B)

        print "Product of {} and {}".format(A, B)
        print Product 

        Quotient, Remainder = Calculator.divide(A,B)

        print "Quotient and Remainder of {} and {}".format(A, B)
        print Quotient, "and", Remainder

        # print Calculator._gf_divide("111", "100")
