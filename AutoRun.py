from Flight import InitialLinks, FindFlights, FirstLink, GetLinks, automail, message
from time import sleep

t_f = True
iter = 0
previous_result = None  # Initialize the variable to store the previous result

print("Welcome to Cheap Flight Finder!")

#ask which travel destinations

vacances = []
mail = []

dest = input("Enter a travel destination (Ex: Amérique du nord): ")
vacances.append(dest)
con = input("Do you wish to add another destination? (Yes/No): ")

while con.upper() == "YES":
    dest = input("Enter a travel destination (Ex: Amérique du nord): ")
    vacances.append(dest)
    con = input("Do you wish to add another destination? (Yes/No): ")


#enter which departure city
city = "ottawa"

#enter which dates
date1 = "20 janvier"
date2 = "27 janvier"

#enter the email adtresses
mail = ["parsa.homayouni@gmail.com"]

#enter the maximum price
price = 700

lien = FirstLink(city, [date1, date2])

links = InitialLinks(lien, vacances)

while t_f:
    iter += 1
    try:
        if iter == 2000:
            t_f = False
        else:
            current_result = FindFlights(links, int(price))
            if len(current_result) == 0:
                print("No results found!")
            
            # Print only if the current result is different from the previous result
            if current_result != previous_result:
                if iter == 1:
                    print(current_result)
                    mail_info = (GetLinks(lien, current_result))
                    automail(mail_info, current_result, mail)
                    print("email sent!")
                else:
                    print("New result found!")
                    print(current_result)
                    mail_info = (GetLinks(lien, current_result))
                    automail(mail_info, current_result, mail)
                    print("email sent!")
            
            # Update the previous result for the next iteration
            previous_result = current_result

            sleep(1800)
    except:
        pass
