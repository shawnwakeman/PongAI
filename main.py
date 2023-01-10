import random



def get_number(min1, max1):
    return str(random.randrange(min1, max1 + 1))

# Generates a combination based on the number of digits parameter
def next_combo_number(number_of_digits):
    digits = ''
    for _ in range(number_of_digits):
        digits += get_number(0,9)
        digits += " "


    return digits


# creates a list of combinations based defined by the number of
# digits per item and the total number of combinations
def get_combinations_list(number_of_digits, number_of_combinations):
    list_of_combinations = []
    for _ in range(number_of_combinations):
        list_of_combinations.append(next_combo_number(number_of_digits))
    return list_of_combinations

# Shows all of the required data to the user this includes desired number combinations,
# number of digits per combo, and the the actual combinations
def show_info(list_of_combinations, number_of_combinations, number_of_digits):
    print('\n---------------------------------------------------')
    print('List Of Combinations:')
    print('---------------------------------------------------')
    for i,v in enumerate(list_of_combinations):
        print(f'Combination Number {i+1} is {v}')
    print('---------------------------------------------------')
    print(f'{number_of_combinations} random combinations where generated.')

# gets the number of dials desired while checking for errors
def get_number_of_dials():
        number_of_digits = int(input("\nhow many digits per combination: "))
        if number_of_digits < 1:
            raise ValueError
        return number_of_digits

#  gets the number of combinations to generate while checking for errors
def get_how_many_to_list():
        number_of_combinations = int(input("how many combinations do you want: "))
        if number_of_combinations <= 2:
            raise ValueError
        return number_of_combinations



# function runs all of the necessary code
def run():
    try:
        number_of_combinations = get_how_many_to_list()
        number_of_digits = get_number_of_dials()
    except ValueError:
        print("Please enter a positive whole number.")
        print("combination number must over 3.")
        run()
    else:
        # Generate the list of combinations
        list_of_combinations = get_combinations_list(number_of_digits, number_of_combinations)
        # Show the combinations and other information to the user
        show_info(list_of_combinations, number_of_combinations, number_of_digits)

run()
