import openpyxl
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from openpyxl import Workbook, load_workbook
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

vacances = ["Caraibes", "Amérique du Nord"]

def FirstLink(ville, dates):
     
    first = []

     
    driver = webdriver.Chrome()

    driver.get("https://www.google.com/travel/flights?tcfs&ved=2ahUKEwi_5dndsrCBAxUmi8UCHZEWAosQ0I8EegQIAxAK&ictx=2")

    case = driver.find_elements(By.CLASS_NAME, "II2One")

    case[0].clear() # clear the cell
    case[0].send_keys(ville) # add departure city
    sleep(2)
    search_dep = driver.find_elements(By.CLASS_NAME, "CwL3Ec") # find the city button
    search_dep[0].click() # click the city button

    date2 = driver.find_elements(By.CLASS_NAME, "TP4Lpb ") # find the date button

    sleep(2)

    date2[0].click() # click the date button
    date2[0].send_keys(dates[0]) # click the date button
    date2[0].send_keys(Keys.ENTER) # click the date button
    date2[0].send_keys(Keys.ENTER) # click the date button

    sleep(2)

    date2[3].click() # click the date button
    date2[3].send_keys(dates[1]) # click the date button
    date2[3].send_keys(Keys.ENTER) # click the date button
    date2[3].send_keys(Keys.ENTER) # click the date button
                
    sleep(3)

    first = driver.current_url

    return first

def InitialLinks(link, dests):

    url_list = []

    for dest in dests:
        driver = webdriver.Chrome()

        driver.get(link)

        case = driver.find_elements(By.CLASS_NAME, "II2One")
        case[2].clear() # clear the cell
        case[2].send_keys(dest)
        sleep(1) 
        search_dep = driver.find_elements(By.CLASS_NAME, "CwL3Ec") # find the city button
        search_dep[0].click() # click the city button
        case[2].send_keys(Keys.ENTER)
        case[2].send_keys(Keys.ENTER)

        sleep(3)

        url_list += [[dest, driver.current_url]]

        driver.quit()

    return url_list

def FindFlights(url_list, aim):

    voyage = []
    for j in url_list:
            dest = j[0]
            link = j[1]
            driver = webdriver.Chrome()
            driver.get(link)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            try:
                main = WebDriverWait(driver, 30).until( EC.presence_of_all_elements_located((By.CLASS_NAME, "SD4Ugf")))   
                destinations = driver.find_elements(By.CLASS_NAME, "lPyEac")
                for z, destination in enumerate(destinations):
                    if z >= 0:
                        City = destination.find_element(By.CLASS_NAME, "W6bZuc")
                        Price = destination.find_element(By.CLASS_NAME, "QB2Jof")
                        
                        
                        price_with_non_numeric = Price.text
                        cleaned_price = ''.join(filter(str.isdigit, price_with_non_numeric))  # Remove non-numeric characters
                        prix = float(cleaned_price)

                        if dest == "Amérique du Nord":
                            if City.text == "Cancún" or City.text == "Miami" or City.text == "Honolulu":
                                if prix <= aim:
                                    voyage += [[City.text, prix]]

                        else:               
                            if prix <= aim:
                                voyage += [[City.text, prix]]
            except:
                pass
            
            finally:
                driver.quit()

    return voyage

def GetLinks(link, dests):
    new_dests = []
    for i in dests:
        new_dests += [i[0]]

    billets_url = []

    for dest in new_dests:
        driver = webdriver.Chrome()

        driver.get(link)

        case = driver.find_elements(By.CLASS_NAME, "II2One")
        case[2].clear() # clear the cell
        case[2].send_keys(dest)
        sleep(1) 
        search_dep = driver.find_elements(By.CLASS_NAME, "CwL3Ec") # find the city button
        search_dep[0].click() # click the city button
        case[2].send_keys(Keys.ENTER)
        case[2].send_keys(Keys.ENTER)

        sleep(3)

        billets_url += [[dest, driver.current_url]]

        driver.quit()

    return billets_url