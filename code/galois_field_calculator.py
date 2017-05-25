from input_parser import InputParser
from polynomial import Polynomial

class GaloisFieldCalculator:
    def __init__(self, p):
        self.p = p

    def detailed_add(self, x, y):
        """
        Verbose version of the add operation
        """
        z = self.add(x, y)

        x_coeffs = x.coeffs[::-1]
        y_coeffs = y.coeffs[::-1]
        xb_coeffs = x.b_coeffs[::-1]
        yb_coeffs = y.b_coeffs[::-1]

        if x.degree > y.degree:
            for i in range(x.degree - y.degree):
                y_coeffs.append(0)
                yb_coeffs.append("0")
        elif y.degree > x.degree:
            for i in range(y.degree - x.degree):
                x_coeffs.append(0)
                xb_coeffs.append("0")

        output_string_1 = "    "

        output_string_2 = "XOR "

        for a,b in zip(x_coeffs[::-1], y_coeffs[::-1]):
            longer = str(a)

            if len(str(b)) > len(str(a)):
                longer = str(b)

            pad = len(longer)
            
            output_string_1 += "%*s " %(pad, str(a))
            output_string_2 += "%*s " %(pad, str(b))

        print "-------------------------------------------------------------"
        print "Align all coefficients, removing the '+' symbol between terms"
        print "-------------------------------------------------------------"
        print "="*len(output_string_1)
        print output_string_1
        print output_string_2
        print "="*len(output_string_1)
        output_string_1 = "    "
        output_string_2 = "XOR "
        output_string_3 = "    "

        zb_coeffs = z.b_coeffs[::-1]

        if len(zb_coeffs) < len(xb_coeffs):
            for i in range(len(xb_coeffs) - len(zb_coeffs)):
                zb_coeffs.append("0")

        for a,b,c in zip(xb_coeffs[::-1], yb_coeffs[::-1], zb_coeffs[::-1]):
            longest = a

            if len(longest) < len(b):
                longest = b
            if len(longest) < len(c):
                longest = c

            a = "0"*(len(longest)-len(a)) + a
            b = "0"*(len(longest)-len(b)) + b
            c = "0"*(len(longest)-len(c)) + c

            output_string_1 += "%s " %str(a)
            output_string_2 += "%s " %str(b)
            output_string_3 += "%s " %str(c)

        output_string_3 += " ===> "
        for i in z.coeffs:
            output_string_3 += "%d " %i

        print "\n-------------------------------------------------------"
        print "Convert the numbers into binary and perform bitwise XOR"
        print "-------------------------------------------------------"
        print "="*len(output_string_1)
        print output_string_1
        print output_string_2
        print "_"*len(output_string_1)
        print output_string_3
        print "-------------------------------------------------------"

        return z

    def add(self, x, y):
        """
        Accepts Polynomial x and y and returns
        Polynomial z as sum
        """
        x_coeffs = x.coeffs[::-1]
        y_coeffs = y.coeffs[::-1]
        xb_coeffs = x.b_coeffs[::-1]
        yb_coeffs = y.b_coeffs[::-1]

        if x.degree > y.degree:
            for i in range(x.degree - y.degree):
                y_coeffs.append(0)
                yb_coeffs.append("0")
        elif y.degree > x.degree:
            for i in range(y.degree - x.degree):
                x_coeffs.append(0)
                xb_coeffs.append("0")

        z_coeff = []
        for i in range(0, len(x_coeffs)):
            z_coeff.insert(0, x_coeffs[i] ^ y_coeffs[i])

        z = Polynomial()

        z.import_coeffs(z_coeff)

        return z
            
    def detailed_subtract(self, x, y):
        """
        Verbose version of subtract operation
        """

        return self.detailed_add(x, y)

    def subtract(self, x, y):
        """
        Accepts Polynomial x, y and returns
        Polynomial as difference
        """
        return self.add(x,y)

    def detailed_multiply(self, x, y):
        z = self.multiply(x, y)

        x_coeffs = x.coeffs[::-1]
        y_coeffs = y.coeffs[::-1]
        xb_coeffs = x.b_coeffs[::-1]
        yb_coeffs = y.b_coeffs[::-1]

        output_string_1 = ""
        output_string_2 = ""
        output_string_3 = ""
        output_string_4 = ""

        longer = len(x_coeffs)
        if len(y_coeffs) > longer:
            longer = len(y_coeffs)

        for i in range(longer):
            a = ""
            b = ""
            c = ""
            d = ""
            if i < len(x_coeffs):
                a = str(x_coeffs[i])
                c = xb_coeffs[i]
            if i < len(y_coeffs):
                b = str(y_coeffs[i])
                d = xb_coeffs[i]
            
            l = len(a)
            if l < len(b):
                l = len(b)

            lb = len(c)
            if lb < len(d):
                lb = len(d)

            output_string_1 = "%*s " %(l, a) + output_string_1 
            output_string_2 = "%*s " %(l, b) + output_string_2 
            output_string_3 = "%*s " %(lb, c) + output_string_3 
            output_string_4 = "%*s " %(lb, d) + output_string_4 

        output_string_1 = "  " + output_string_1
        output_string_2 = "* " + output_string_2
        output_string_3 = "  " + output_string_3
        output_string_4 = "* " + output_string_4

        sum_rows = [
            i.b_coeffs[::-1] for i in self.multiply_partial_sums
        ]
        sum_rows.append(z.b_coeffs[::-1])
        os_rows = [
            "" for i in sum_rows
        ]

        longest = len(sum_rows[-1])

        for i in range(longest):
            mod = []
            for row in sum_rows:
                if i < len(row):
                    mod.append(row[i])
                else:
                    mod.append("")

            l = 0
            for j in mod:
                if l < len(j):
                    l = len(j)

            for j in range(len(sum_rows)):
                os_rows[j] = "0"*(l - len(mod[j])) + "%s " % mod[j] + os_rows[j]
        
        os_rows[-2] = "XOR " + os_rows[-2]
        longest = len(os_rows[-2])

        s = ""
        for i in z.coeffs:
            s += "%d " % i
        
        print "-------------------------------------------------------------"
        print "Align all coefficients, removing the '+' symbol between terms"
        print "-------------------------------------------------------------"
        print "="*len(output_string_1)
        print output_string_1
        print output_string_2
        print "="*len(output_string_1)
        print "\n-------------------------------------------------------------"
        print "Convert each coefficient to their GF(2^m) representation"
        print "Multiply using long (every coefficient of A with every)"
        print "coefficient of B) multplication and reduce using"
        print "{}".format(self.p.b_coeffs)
        print "After that, perform bitwise XOR to each element to get the"
        print "product"
        print "-------------------------------------------------------------"
        print "="*longest
        print "%*s" %(longest, output_string_3)
        print "%*s" %(longest, output_string_4)
        print "-"*longest
        for i in os_rows[:-1]:
            print "%*s" %(longest, i)
        print "_"*longest
        print "%*s" %(longest, os_rows[-1]), "==>", s
        

        return z

    def multiply(self, x, y):
        """
        Accepts Polynomial x, y
        and returns Polynomial product
        """
        self.multiply_partial_sums = []
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

            self.multiply_partial_sums.append(Polynomial())
            self.multiply_partial_sums[-1].import_coeffs(prod_list)

        Sum = self.multiply_partial_sums[0]
        
        for i in range(1, len(self.multiply_partial_sums)):
            Sum = self.add(Sum, self.multiply_partial_sums[i])

        return Sum

    def detailed_divide(self, x, y):
        q,r = self.divide(x, y)

        return (q,r)
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

    i = 0
    for case in cases:
        print "\n\n\nCase {}".format(i+1)
        i += 1

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

        print "Quotient {} and {}".format(A, B)
        print Quotient
        if Remainder.coeffs:
            print "Remainder:"
            print Remainder

        # print Calculator._gf_divide("111", "100")
