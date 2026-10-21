"""
Function Library
GlitchtheWitch Personal Toolkit.
"""
import random


def flip_coin():
    """
    simulates flipping a coin and returns either heads or tails
    """

    if random.randint(0, 1) == 0:
        return 'HEADS'
    else:
        return 'TAILS'


def roll_d20():
    """
    simulates rolling a 20-sided die and returns a number between 1 and 20
    """

    return random.randint(1, 20)


def check_percentage(chance):
    """
    simulates a percentage chance and returns True if the chance is successful
    and False if it is not
    """

    return random.randint(1, 100) <= chance


# VALIDATION FUNCTIONS (Added in Lab 2.3)
def get_valid_int(prompt, min_value, max_value):
    """
    Prompts the user for an integer input and validates that it is within the
    specified range.
    """
    while True:
        try:
            value = input(prompt).strip()

            if value == '':
                print("ERROR: Invalid input. Please enter a number.")
                continue

            value = int(value)

            if min_value <= value <= max_value:
                return value
            else:
                print(f"ERROR: Enter a number between {min_value}"
                      f" and {max_value}.")
        except ValueError:
            print("ERROR: Invalid input. Please enter a number.")
        except EOFError:
            print("\nNo input provided. Exiting.")
            raise


def get_yes_no(prompt):
    """
    prompts the user for a yes/no response and validates the input
    """
    answer = input(prompt).strip().upper()

    while answer not in ['Y', 'N']:
        print("ERROR: Please enter 'y' or 'n'.")
        answer = input(prompt).strip().upper()

    return answer == 'Y'


def save_list_to_file(filename, data_list):
    """
    This function saves a list of data to a file, with each item on a new line.
    """
    with open(filename, 'w') as outfile:
        for item in data_list:
            outfile.write(str(item) + '\n')


def load_list_from_file(filename):
    """
    Loads a list of data from a file, where each line in the file is an
    item in the list.
    """
    result = []
    try:
        with open(filename, 'r') as infile:
            line = infile.readline()

            while line != '':
                result.append(line.rstrip('\n'))
                line = infile.readline()
    except FileNotFoundError:
        pass

    return result


def file_exists(filename):
    """
    Checks if file exists
    """
    try:
        with open(filename, 'r'):
            return True
    except FileNotFoundError:
        return False


def enter_to_continue(prompt):
    """
    Pause the game and wait for the player to press Enter.
    """
    input(f'  {prompt}')
