import Flight
from Flight import InitialLink, FindFlights
from time import sleep

t_f = True
iter = 0
previous_result = None  # Initialize the variable to store the previous result

print("Welcome to Cheap Flight Finder!")

#ask which travel destinations

vacances = []

dest = input("Enter a travel destination (Ex: Amérique du nord): ")
vacances.append(dest)
con = input("Do you wish to add another destination? (Yes/No): ")

while con.upper() == "YES":
    dest = input("Enter a travel destination (Ex: Amérique du nord): ")
    vacances.append(dest)
    con = input("Do you wish to add another destination? (Yes/No): ")


#ask which departure city
city = input("Enter a departure city (Ex: Montréal): ")

#ask which dates
date1 = input("Enter a departure date (Ex: 23 octobre): ")
date2 = input("Enter a return date (Ex: 29 octobre): ")

#enter the maximum price

price = input("Enter the maximum price you are willing to pay without the dollar sign (Ex: 500): ")

lien = InitialLink(vacances, city, [date1, date2])

while t_f:
    iter += 1
    print(iter)
    if iter == 2000:
        t_f = False
    else:
        current_result = FindFlights(lien, int(price))
        if len(current_result) == 0:
            print("No results found!")
        
        # Print only if the current result is different from the previous result
        if current_result != previous_result:
            if iter == 1:
                print(current_result)
            else:
                print("New result found!")
                print(current_result)
        
        # Update the previous result for the next iteration
        previous_result = current_result

        sleep(60)
