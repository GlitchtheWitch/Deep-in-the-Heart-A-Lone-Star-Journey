"""
DEEP IN THE HEART: A LONE STAR JOURNEY
---------------------------------------
Description: A text-based adventure game set in Texas, where
players navigate between cities and face various challenges.
"""
import random
import function_library

# PARALLEL LISTS
# San Antonio
SA_DESTINATIONS = ['Corpus Christi', 'Houston', 'Austin', 'Laredo']
SA_DISTANCES = [150, 200, 80, 160]
SA_NOTES = ['BEACH!', 'Gateway East', 'Keep it Weird', 'Dead End']
# Houston
HOU_DESTINATIONS = ['Galveston', 'San Antonio', 'Dallas']
HOU_DISTANCES = [50, 200, 240]
HOU_NOTES = ['BEACH!', 'Back West', 'Wrong Way']
# Austin
AUS_DESTINATIONS = ['San Antonio', 'Houston']
AUS_DISTANCES = [80, 165]
AUS_NOTES = ['Back Home', 'Space City']

# save game constant
SAVE_FILE = 'savegame.txt'

# Other Constants
MILES_PER_TURN = 50
MILES_MULTIPLIER = 10
HAZARD_CHANCE = 30


# Function to display destinations for a given city
def display_destinations(city):
    """
    Displays the destinations and distances for a given city.
    """
    if city == 'San Antonio':
        destinations = SA_DESTINATIONS
        distances = SA_DISTANCES
        notes = SA_NOTES
    elif city == 'Houston':
        destinations = HOU_DESTINATIONS
        distances = HOU_DISTANCES
        notes = HOU_NOTES
    elif city == 'Austin':
        destinations = AUS_DESTINATIONS
        distances = AUS_DISTANCES
        notes = AUS_NOTES
    else:
        print('No destinations available')
        return 0
    print('Where would you like to go?')
    for i in range(len(destinations)):
        print(f'{i + 1}. {destinations[i]} - {distances[i]}' +
              f' miles ({notes[i]})')
    return len(destinations)


# get destination choice function
def get_destination(city, choice):
    """
    Gets the destination and distance based on the city and user choice.
    """
    index = choice - 1
    if city == 'San Antonio':
        return SA_DESTINATIONS[index], SA_DISTANCES[index]
    elif city == 'Houston':
        return HOU_DESTINATIONS[index], HOU_DISTANCES[index]
    elif city == 'Austin':
        return AUS_DESTINATIONS[index], AUS_DISTANCES[index]
    else:
        return 'San Antonio', 0


# redirect function
def get_redirect(city, avoid):
    """
    Gets a random redirect destination and distance based on the city
    """
    if city == 'San Antonio':
        destinations = SA_DESTINATIONS.copy()
        distances = SA_DISTANCES.copy()
    elif city == 'Houston':
        destinations = HOU_DESTINATIONS.copy()
        distances = HOU_DISTANCES.copy()
    elif city == 'Austin':
        destinations = AUS_DESTINATIONS.copy()
        distances = AUS_DISTANCES.copy()

    # Remove the avoid destination if it exists
    if avoid in destinations:
        idx = destinations.index(avoid)
        destinations.remove(avoid)
        distances.pop(idx)
        redirect = random.randint(0, len(destinations) - 1)
    return destinations[redirect], distances[redirect]


# save game function
def save_game(player_name, current_city, total_miles, total_turns,
              hazards_faced, hazards_escaped, visited_cities, hazards_list):
    """
    Save game function.
    """
    with open(SAVE_FILE, 'w') as outfile:
        outfile.write(str(player_name) + '\n')
        outfile.write(str(current_city) + '\n')
        outfile.write(str(total_miles) + '\n')
        outfile.write(str(total_turns) + '\n')
        outfile.write(str(hazards_faced) + '\n')
        outfile.write(str(hazards_escaped) + '\n')

        # visited cities
        for city in visited_cities:
            outfile.write(city + '\n')

        # hazard seperator
        outfile.write('---HAZARDS---\n')

        # hazards
        for hazard in hazards_list:
            outfile.write(str(hazard) + '\n')


# load game function
def load_game():
    """Load game Function."""
    try:
        infile = open(SAVE_FILE, 'r')

        player_name = infile.readline().rstrip('\n')
        current_city = infile.readline().rstrip('\n')
        total_miles = int(infile.readline().rstrip('\n'))
        total_turns = int(infile.readline().rstrip('\n'))
        hazards_faced = int(infile.readline().rstrip('\n'))
        hazards_escaped = int(infile.readline().rstrip('\n'))

        # load visited cities
        visited_cities = []
        line = infile.readline().rstrip('\n')

        # hazards seperator
        while line != '---HAZARDS---':
            visited_cities.append(line)
            line = infile.readline().rstrip('\n')
        # load hazards
        hazards_list = []
        for line in infile:
            hazards_list.append(line.rstrip('\n'))

        infile.close()

        return (player_name, current_city, total_miles, total_turns,
                hazards_faced, hazards_escaped, visited_cities, hazards_list)
    except FileNotFoundError:
        return None


def main():
    """Main function."""
    # variables to track game state also to lazy to fix
    current_city = 'San Antonio'
    visited_cities = ['San Antonio']
    keep_playing = True
    games_played = 0
    session_miles = 0
    session_hazards = 0
    player_name = ''
    total_turns = int()
    distance = int()
    distance_remaining = int()
    total_miles = 0
    turn = 1
    hazards_faced = 0
    total_escaped = 0
    hazards_list = []

    # Welcome banner
    print()
    print('=' * 50)
    print('DEEP IN THE HEART: A LONE STAR JOURNEY')
    print('=' * 50)
    print()

    # Main menu
    print('1. New Game')
    print('2. Load Game')
    print('3. Exit')

    menu_choice = function_library.get_valid_int('Choose (1-3): ', 1, 3)

    if menu_choice == 3:
        print('Thanks for playing!')
        return
    elif menu_choice == 2:
        saved = load_game()
        if saved is None:
            print('No saved game found. Starting new game.')
            menu_choice = 1
        else:
            (player_name, current_city, total_miles, total_turns,
             hazards_faced, hazards_escaped,
             visited_cities, hazards_list) = saved
            total_escaped = hazards_escaped
            print(f'Welcome back, {player_name}!')
            print(f'Resuming from {current_city}...')

    if menu_choice == 1:
        player_name = input('What is your name, traveler? ')
        print(f'Welcome, {player_name}!')
        print(f'You are in {current_city}. Your goal: reach the beach!')
        print()

    while keep_playing:
        turn = 1
        session_miles += total_miles
        distance_remaining = distance

        # Display destinations and get choice
        num_destinations = display_destinations(current_city)
        choice = function_library.get_valid_int('Enter your choice ' +
                                                f'(1-{num_destinations}): ', 1,
                                                num_destinations)
        destination, distance = get_destination(current_city, choice)

        # redirect
        print()
        if destination in ['Corpus Christi', 'Galveston']:  # added force beach
            print('HEADS! Texas lets you through!')
        else:
            print()
            print('Uh oh will you be able to go there?')
            coin = function_library.flip_coin()

            # print('Uh oh will you be able to go there?')
            # coin = function_library.flip_coin()

            if coin == 'HEADS':
                print('You take the direct route to your destination.')
            else:
                print('TAILS! Texas has other plans...')
                destination, distance = get_redirect(current_city, destination)
                print(f'You\'re being redirected to {destination} '
                      f'({distance} miles)')

        print()
        print('=' * 50)
        print('LET THE JOURNEY BEGIN!')
        print('=' * 50)

        # trip while loop
        while distance_remaining > 0:
            print(f'--- Turn {turn} ---')
            print(f'Miles remaining: {distance_remaining}')
            roll = function_library.roll_d20()
            miles_this_turn = roll * MILES_MULTIPLIER
            distance_remaining -= miles_this_turn
            total_miles += miles_this_turn
            print(f'Rolling D20... You rolled a {roll}!')
            print(f'You travel {miles_this_turn} miles...' +
                  f'{distance_remaining} miles remaining.')
            turn += 1

            # Hazard check
            if function_library.check_percentage(HAZARD_CHANCE):
                hazards_faced += 1
                haz_num = random.randint(1, 3)
                escape = function_library.flip_coin()
                print('*** HAZARD! ***')
                if haz_num == 1:
                    print('Buc-ee\'s appears!')
                    hazards_list.append('Buc-ee\'s appears!')
                    print(f'{escape}!')
                    if escape == 'HEADS':
                        total_escaped += 1
                        print('You resist the beaver\'s call.')
                    else:
                        print('Lost 2 hours on beef jerky.')
                elif haz_num == 2:
                    print('Armadillo crossing!')
                    hazards_list.append('Armadillo crossing!')
                    print(f'{escape}!')
                    if escape == 'HEADS':
                        total_escaped += 1
                        print('It scurries across safely.')
                    else:
                        print('You swerved. Armadillo unbothered.')
                elif haz_num == 3:
                    print('Speed trap!')
                    hazards_list.append('Speed trap!')
                    print(f'{escape}!')
                    if escape == 'HEADS':
                        total_escaped += 1
                        print('You saw the cop in time.')
                    else:
                        print('Small town officer says howdy.')
                print()
        current_city = destination
        visited_cities.append(destination)

        # End of while loop message
        print(f'You made it to {destination}!')

        # trip report
        print()
        print('=' * 50)
        print("TRIP REPORT")
        print('=' * 50)
        print('Driver:', player_name)
        print('Final City:', destination)
        print()
        print('YOUR ROUTE:')
        for i in range(len(visited_cities)):
            print(f'{i + 1}. {visited_cities[i]}')
        print()
        print('HAZARDS ENCOUTERED:')
        if len(hazards_list) > 0:
            for i in range(len(hazards_list)):
                print(f'{i + 1}. {hazards_list[i]}')
        else:
            print('None - Lucky traveler!')
        print()
        print('STATISTICS:')
        print('Total Miles:', total_miles)
        print('Total Turns:', turn - 1)
        print('Hazards: ', total_escaped, '/', hazards_faced, ' escaped')
        print('=' * 50)
        print()

        games_played += 1
        session_hazards += hazards_faced
        total_turns += (turn - 1)

        # Play again or save prompt
        print()
        if destination == 'Corpus Christi' or destination == 'Galveston':
            keep_playing = False
        else:
            print('1. Continue Journey')
            print('2. Save and quit')

            option = function_library.get_valid_int('Choose (1-2): ', 1, 2)

            if option == 2:
                save_game(player_name, current_city, total_miles, total_turns,
                          hazards_faced, total_escaped,
                          visited_cities, hazards_list)
                print('Game saved!')
                keep_playing = False
            else:
                keep_playing = True

        # you made it message based on choice
        if destination == 'Corpus Christi' or destination == 'Galveston':
            print('CONGRATULATIONS! YOU REACHED THE BEACH!')
        elif destination == 'Houston':
            print('Galveston is only 50 more miles away')
        else:
            print('No beach here!')

    # Session Statistics + thanks for playing
    print()
    print('=' * 50)
    print('SESSION STATISTICS')
    print('=' * 50)
    print(f'Games Played: {games_played}')
    print(f'Totals Miles (All Games): {session_miles}')
    print(f'Total Hazards Faced: {session_hazards}')
    print(f'Thanks for playing, {player_name}!')
    print('=' * 50)


if __name__ == '__main__':
    main()
