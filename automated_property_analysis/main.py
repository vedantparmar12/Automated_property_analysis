import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


url = "https://appbrewery.github.io/Zillow-Clone/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Open the Google Form
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdaDyYk3YvpJkO3rLANXC5TdlV1aqBhCT6Gw9Wrlncr6t9B6g/viewform?usp=sf_link"
driver = webdriver.Chrome(options=chrome_options)
driver.get(form_url)

# Find all the listing elements
listings = soup.find_all("li", class_="ListItem-c11n-8-84-3-StyledListCardWrapper")

# Extract and clean the price and address for each listing
links = []
prices = []
addresses = []

for listing in listings:
    # Extract the href attribute from each listing element
    link = listing.find("a", class_="StyledPropertyCardDataArea-anchor")["href"]
    link_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field.send_keys(link)
    # links.append(link)

    # Extract and clean the price
    price_text = listing.find("span", class_="PropertyCardWrapper__StyledPriceLine").text
    clean_price = re.sub(r"[^$\d,]", "", price_text).strip()
    price_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field.send_keys(clean_price)
    # prices.append(clean_price)

    # Extract and clean the address
    address_text = listing.find("address").text
    clean_address = re.sub(r"[\n|]+", "", address_text).strip()
    address_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_field.send_keys(clean_address)
    # addresses.append(clean_address)

    # Submit the form
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    # Wait for the form to submit and reload
    time.sleep(2)

    # Reload the form for the next entry
    driver.get(form_url)
    time.sleep(2)

driver.quit()

print(len(links))
print(len(prices))
print(len(addresses))
#
print(prices)