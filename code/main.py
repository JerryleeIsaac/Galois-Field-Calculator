#!/usr/bin/python
from galois_field_calculator import GaloisFieldCalculator
from polynomial import Polynomial
from input_parser import InputParser

a_string = raw_input("Input A(x): ")
b_string = raw_input("Input B(x): ")
p_string = raw_input("Input P(x): ")

InputParser.valid_characters_check(a_string)
InputParser.valid_characters_check(b_string)
InputParser.valid_characters_check(p_string)

P = Polynomial(p_string, True)
A = Polynomial(a_string, False, P.max_coeff)
B = Polynomial(b_string, False, P.max_coeff)

print "Inputs Valid! Below are the polynomials inputted"

print "A(x) =", A
print "B(x) =", B
print "P(x) =", P

choice = -1

Calculator = GaloisFieldCalculator(P)

while choice != 0:
    print "\nWhat would you like to do?"
    menu = "[1] Add\n[2] Subtract\n[3] Multiply\n[4] Divide\n[0] Exit\nInput: "
    choice = raw_input(menu)

    print "\n\n"
    if choice == "1":
        print "A(x) =", A
        print "B(x) =", B
        print "A(x) + B(x) =", Calculator.add(A,B)
    elif choice == "2":
        print "A(x) =", A
        print "B(x) =", B
        print "A(x) - B(x) =", Calculator.subtract(A,B)
    elif choice == "3":
        print "A(x) =", A
        print "B(x) =", B
        print "A(x) * B(x) =", Calculator.multiply(A,B)
    elif choice == "4":
        print "A(x) =", A
        print "B(x) =", B
        quotient, remainder = Calculator.divide(A,B)
        print "A(x) / B(x) =", quotient
        print "Remainder =", remainder
    else:
        choice = 0
