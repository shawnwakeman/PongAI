import random

# generates an individual based on the number of didgits previded
def generateCombination(numberOFDidgits):
    didgit = ""
    i = 0
    while i < numberOFDidgits:
        intermDidgit = random.randint(0,9)
        intermDidgit = str(intermDidgit)
        didgit += intermDidgit
        i += 1
    return didgit

# creates a list of combinations with the length of "numberOfDidgits" and "numberOfCombinations" combinations
def getCombinationsList(numberOfDidgits, numberOfCombinations):
    listOfCombinations = []
    i = 0
    while i <= numberOfCombinations:
        listOfCombinations.append(generateCombination(numberOfDidgits))
        i += 1
    return listOfCombinations

# shows all of the required data to the user this incudes desired number combinations, number of didgits per combo, and the the actuall combinations
def showInfo(listOfCombinations, numberOfCombinations, numberOfDidgits):
    print(f'\n---------------------------------------------------')
    print(f'Number of Combinations: {numberOfCombinations}')
    print(f'Numbers Per Combination: {numberOfDidgits}')
    print(f'---------------------------------------------------')
    print(f'List Of Combinations:')
    print(f'---------------------------------------------------')
    for i,v in enumerate(listOfCombinations):
        print(f'Combination Number {i+1} is {v}')
    print(f'---------------------------------------------------')


# get the input from the user and set the data to working variables while checking for errors, next the function runs all of the nessasary code
def run():
    valid = False
    try:
        numberOfCombinations = int(input("how many combinations do you want: "))
        numberOfDidgits = int(input("\nhow many didgits per combination: "))
        listOfCombinations = getCombinationsList(numberOfDidgits, numberOfCombinations)
        showInfo(listOfCombinations, numberOfCombinations, numberOfDidgits)
    except:
        print("Please enter a whole number.")
        run()

run()
