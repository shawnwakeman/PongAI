import random

DIGITS = '1234567890'

# Generates a combination based on the number of digits parameter
def get_number():
    # Use the sample function to select a combination of digits
    return random.randrange(0,10)


def get_next_combo_number():
    list_of_combinations = []


def get_info():
    try:
        get_number_of_dials()
        get_how_many_to_list()
    except ValueError:
        print("Please enter a positive whole number.")
        get_info()

def get_number_of_dials():
        number_of_digits = int(input("\nhow many digits per combination: "))
        if number_of_digits < 1:
            raise ValueError
        return number_of_digits
def get_how_many_to_list():
        number_of_combinations = int(input("how many combinations do you want: "))
        if number_of_combinations < 1:
            raise ValueError
        return number_of_combinations

