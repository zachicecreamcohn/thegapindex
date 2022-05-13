# function to convert a moore color to hex
import csv
def mooreToHex(mooreCode):
    # open csv file (in static folder)
    with open(r'C:\Users\zwc12\Documents\Documents\WashU\Freshman S2\CSE 330\Module 7\flask and vue\benjamin-moore.csv', 'r') as csvfile:
        ## NOTE!!!! Change this path to the correct path on aws instance

        # loop through each row
        # if the second column matches the moore code, return the third column
        for row in csv.reader(csvfile, delimiter=';'):
            if row[1] == mooreCode:
                return row[2]


def hexToMoore(hexCode):
    # open csv file (in static folder)
    with open(r'C:\Users\zwc12\Documents\Documents\WashU\Freshman S2\CSE 330\Module 7\flask and vue\benjamin-moore.csv', 'r') as csvfile:
        ## NOTE!!!! Change this path to the correct path on aws instance

        # loop through each row
        # if the third column matches the hex code, return the second column
        for row in csv.reader(csvfile, delimiter=';'):
            if row[2] == hexCode:
                return row[1]
        return "Not Found"

# if this file is run as a script, tet
if __name__ == "__main__":
    print(hexToMoore("#DDAB87"))

