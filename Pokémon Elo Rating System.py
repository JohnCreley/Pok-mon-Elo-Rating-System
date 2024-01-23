"""

Pokémon Elo Rating System
John Creley
12023/6/14/1:43:35 through

I need to specify # of wins, losses, & total plays b/c need # of draws extracted from all 3. It is important to edit the data
in the csv header in the event the .csv file is ever deleted.

menu is a 1x3 array determining the following values:
 - menu[1] = executive decision to make w/ data.
 - menu[2] = category of new game entered.
 - menu[3] = whether win/lose the game entered.

"""

# Imports.
import os
import csv
import pandas as pd
import numpy as np
from tabulate import tabulate
            
# Check if the file already exists. Create the file if not.
if (not os.path.isfile('BattleStats.csv') ):
    
    # If the file doesn't exist, create it and write a header.
    with open('BattleStats.csv', 'w', newline='') as csvfile:
        
        # Write your header here. (BE SURE TO UPDATE TABLE FREQUENTLY TO SAVE PROGRESS!)
        writer = csv.writer(csvfile)
        writer.writerows([["Statistic", "# of Wins", "# of Losses", "Total Plays", "Game ELO"],
            ["Total ELO", 0, 0, 0, 800], # The same for all topics, regardless of plays.
            ["Battle Royales", 0, 0, 0, 800],
            ["Derbies", 0, 0, 0, 800],
            ["Double Battles", 0, 0, 0, 800],
            ["Escape Rooms", 0, 0, 0, 800],
            ["Fashion Shows", 0, 0, 0, 800],
            ["Miscellaneous Battles", 0, 0, 0, 800],
            ["Single Battles", 0, 0, 0, 800],
            ["Team Quests", 0, 0, 0, 800],
            ["Tournaments", 0, 0, 0, 800]])
        
        print("\nBattleStats.csv file created successfully.\n")

# Input variables.
menu = [None] * 3
record = pd.read_csv('BattleStats.csv') # Read data in legible format to alter.
ID_Num = "456-789-012-345" # ID No. from game.


# Main program.
while True:

    # Main menu:
    menu[0] = int(input("""\nWhat would you like to do?
    1. Add New Game.
    2. Display Record.
    99. Exit\n\n""") )

    if menu[0] == 99: # Exit program.
        print("\nExiting program. Goodbye!\n")
        break
    
    elif menu[0] == 1: # Add New Game.
        menu[1] = int(input("""\nEnter what game was played:
    1. Battle Royales
    2. Derbies
    3. Double Battles
    4. Escape Rooms
    5. Fashion Shows
    6. Miscellaneous Battles
    7. Single Battles
    8. Team Quests
    9. Tournaments
    99. Exit\n\n""") )

        # Game menu:
        if menu[1] == 99:
            continue

        elif not 1 <= menu[1] <= 9:
            print("\nInvalid choice. Please enter a valid option.\n")

        else:
            OppELO = int(input("\nPlease enter the opponent's ELO:\n") )
            menu[2] = input("\nWin/lose/draw? (W/L/D)\n")

            E = 1 / (1 + 10 ** ( (OppELO - record.iloc[0,1]) / 400))

            # Input K variable depending on existing ELO score. (Harder to advance the higher the score.)
            if (int(record.iloc[menu[1],4]) >= 2000):
                K = 16
            elif (int(record.iloc[menu[1],4]) >= 1000):
                K = 32
            else:
                K = 64

            # Calculate new Elo.
            if menu[2] == 'W':
                record.iloc[menu[1],1:4] += np.array( [1,0,1] ) # Add your win & to # of games played.
                
                record.iloc[menu[1],4] = int(record.iloc[menu[1],4] + K * (1 - E) )

            elif menu[2] == 'L':
                record.iloc[menu[1],2:4] += np.array( [1,1] ) # Add your loss & to # of games played.
                record.iloc[menu[1],4] = int(record.iloc[menu[1],4] + K * (0 - E) )

            elif menu[2] == 'D':
                record.iloc[menu[1],3] += 1 # Only add to # of games played.
                record.iloc[menu[1],4] = int(record.iloc[menu[1],4] + K * (0.5 - E) )

            else:
                print("\nInvalid choice. Please enter a valid option.\n")
    
            # Calculate final average Elo summing all Elo averages.
            record.iloc[0,1:4] = np.sum(record.iloc[1:,1:4], axis = 0)
            record.iloc[0,4] = round(pd.Series(np.sum(record.iloc[1:,4]) / len(record.iloc[1:,4]) ) )

            # Write data to the .csv file.
            record.to_csv('BattleStats.csv', index = False)

    elif menu[0] == 2:
        print(tabulate(record.reset_index(), headers = 'keys', tablefmt = 'github', showindex = False) )
    
    else:
        print("\nInvalid choice. Please enter a valid option.\n")
