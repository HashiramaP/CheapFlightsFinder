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


def InitialLink(dests, ville, dates):

    url_list = []

    driver = webdriver.Chrome()

    driver.get("https://www.google.com/travel/flights?tcfs&ved=2ahUKEwi_5dndsrCBAxUmi8UCHZEWAosQ0I8EegQIAxAK&ictx=2")

    for i, dest in enumerate(dests):
            if i == 0:

                case = driver.find_elements(By.CLASS_NAME, "II2One")

                case[0].clear() # clear the cell
                case[0].send_keys(ville) # add departure city
                sleep(2)
                search_dep = driver.find_elements(By.CLASS_NAME, "CwL3Ec") # find the city button
                search_dep[0].click() # click the city button


                case[2].send_keys(dest) # add arrival city
                sleep(1)
                search_ariv2 = driver.find_elements(By.CLASS_NAME, "CwL3Ec") # find the city button
                search_ariv2[0].click() # click the city button

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

                current_url = driver.current_url

                zizi = driver.find_elements(By.CLASS_NAME, "II2One")
                zizi[2].click() # click the date button
                zizi[2].send_keys(Keys.ENTER)
                zizi[2].send_keys(Keys.ENTER)

                sleep(10)

                url_list += [[dest, driver.current_url]]

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                driver.quit()

            if i >= 1:
                drive = webdriver.Chrome()
                drive.get(current_url)

                case = drive.find_elements(By.CLASS_NAME, "II2One")
                case[2].clear() # clear the cell
                case[2].send_keys(dest)
                sleep(1) 
                search_dep = drive.find_elements(By.CLASS_NAME, "CwL3Ec") # find the city button
                search_dep[0].click() # click the city button
                case[2].send_keys(Keys.ENTER)
                case[2].send_keys(Keys.ENTER)

                sleep(10)

                url_list += [[dest, drive.current_url]]

                drive.quit()

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

def GetLinks(url_list, fly1):
    links = []
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
                        for enum in fly1:
                            if City.text == enum[0]:
                                destination.click()
                                sleep(2)
                                #add the href to the list
                                li = driver.find_element(By.CLASS_NAME, "DvoDQ")
                                links += [[li.get_attribute("href")]]
                                driver.back()
            except:
                pass
    return links

lien = [['Caraibes', 'https://www.google.com/travel/explore?tfs=CBwQAxooEgoyMDIzLTEyLTI3agwIAxIIL20vMDUycDdyDAgEEggvbS8wMjYxbRooEgoyMDI0LTAxLTA1agwIBBIIL20vMDI2MW1yDAgDEggvbS8wNTJwN0ABSAFwAYIBCwj___________8BmAEBsgEEGAEgAQ&tfu=GgAqAggD'], ['Amérique du Nord', 'https://www.google.com/travel/explore?tfs=CBwQAxooEgoyMDIzLTEyLTI3agwIAxIIL20vMDUycDdyDAgEEggvbS8wNTlnNBooEgoyMDI0LTAxLTA1agwIBBIIL20vMDU5ZzRyDAgDEggvbS8wNTJwN0ABSAFwAYIBCwj___________8BmAEBsgEEGAEgAQ&tfu=GgAqAA']]

print(FindFlights(lien, 850))