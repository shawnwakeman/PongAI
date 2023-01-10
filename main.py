import random

# generates a combination based on the number of digits parameter
DIGITS = '0123456789'

# Generates a combination based on the number of digits parameter
def generate_combination(number_of_digits):
    # Use the sample function to select a combination of digits
    return ''.join(random.sample(DIGITS, number_of_digits))


# creates a list of combinations based defined by the number of
# digits per item and the total number of combinations
def get_combinations_list(number_of_digits, number_of_combinations):
    list_of_combinations = []
    for _ in range(number_of_combinations):
        list_of_combinations.append(generate_combination(number_of_digits))
    return list_of_combinations

# Shows all of the required data to the user this includes desired number combinations,
# number of digits per combo, and the the actual combinations
def show_info(list_of_combinations, number_of_combinations, number_of_digits):
    print('\n---------------------------------------------------')
    print(f'Number of Combinations: {number_of_combinations}')
    print(f'Numbers Per Combination: {number_of_digits}')
    print('---------------------------------------------------')
    print('List Of Combinations:')
    print('---------------------------------------------------')
    for i,v in enumerate(list_of_combinations):
        print(f'Combination Number {i+1} is {v}')
    print('---------------------------------------------------')


# get the input from the user and set the data to working variables while checking for errors,
# next the function runs all of the necessary code
def run():
    try:
        number_of_combinations = int(input("how many combinations do you want: "))
        if number_of_combinations < 1:
            raise ValueError
        number_of_digits = int(input("\nhow many digits per combination: "))
        if number_of_digits < 1:
            raise ValueError
    except ValueError:
        print("Please enter a positive whole number.")
        run()
    else:
        # Generate the list of combinations
        list_of_combinations = get_combinations_list(number_of_digits, number_of_combinations)
        # Show the combinations and other information to the user
        show_info(list_of_combinations, number_of_combinations, number_of_digits)

run()
