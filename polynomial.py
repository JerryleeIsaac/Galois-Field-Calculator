from input_error import InputError

class Polynomial:
    def __init__(self, x="", irreducible=False, max_coeff=7):
        self.irreducible = irreducible
        self.coeffs = self._clean(x)
        self.b_coeffs = [
            list(int(c) for c in bin(coeff)[2:]) for coeff in self.coeffs
        ]

        self.degree = len(self.coeffs) - 1
        if self.irreducible:
            self.max_coeff = 2^(self.degree) - 1
        else:
            self.max_coeff = max_coeff
        self._validity_check()


    def import_coeffs(self, x):
        self.coeffs = x
        self.b_coeffs = [
            bin(coeff)[2:] for coeff in self.coeffs
        ]

        self.degree = len(self.coeffs) - 1

    def _clean(self, x):
        """
        This function removes the initial zeroes in the string
        version of the polynomial as well as other characters
        """
        coeffs = []

        for s_coeff in x.split():
            coeff = int(s_coeff)
            if coeffs or coeff:
                coeffs.append(coeff)
        
        return coeffs

    def _validity_check(self):
        for coeff in self.coeffs:
            if coeff > self.max_coeff:
                raise InputError(coeff, "exceeds max value: {}".format(self.max_coeff))

    def __str__(self):
        string = ""

        for i, coeff in enumerate(self.coeffs):
            power = self.degree - i 

            string += "{}".format(coeff)

            if power > 0:
                string += "x"
            if power > 1:
                string += "^{}".format(power)

            if i != self.degree:
                string += " + "

        return string
