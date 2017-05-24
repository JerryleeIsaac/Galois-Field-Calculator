from input_error import InputError


class InputParser:
    @classmethod
    def read_inputs(cls, input_file="input.in"):
        """
        This function reads a given file and returns
        an array of the inputs.
        """
        examples = []

        with open(input_file, 'r') as fi:
            examples = fi.readlines()

        return examples

    @classmethod
    def separate_polynomials(cls, string_input=""):
        """
        Accepts a string with the format `a,b,c` where
        `a` has the format 'x x x x', where x is an integer.
        """
        
        string_input = string_input.strip('\n\r')
        polynomial_strings = string_input.split(',')

        for polynomial in polynomial_strings:
            cls._valid_characters_check(polynomial)

        return polynomial_strings

    @classmethod
    def _valid_characters_check(cls, x):
        """
        This function checks whether all inputs are of only
        valid characters
        """

        string = x.replace(" ","")

        if not string.isdigit():
            raise InputError(string, "contains invalid characters")
