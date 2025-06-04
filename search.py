#search zillow + interactivly dump

from colorama import init
from colorama import Fore, Style
init()
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import objectpath

price_max = 350000

def parse_lot_area(lot_area_string):
    if not lot_area_string:
        return None
    try:
        if "acres" in lot_area_string:
            # Convert acres to sqft if needed, assuming 1 acre = 43560 sqft
            value = float(lot_area_string.split()[0])
            return value * 43560  # Convert acres to square feet
        else:
            # Assume the value is already in sqft
            return float(lot_area_string.replace(",", "").split()[0])
    except ValueError:
        return None

def parse_price(price_str):
    if price_str.startswith('$'):
        price_str = price_str[1:]
    price_str = price_str.replace(',', '')
    try:
        return int(price_str)
    except ValueError:
        return None

def _print_property_details(data):
    for item in data:
        price_str = item.get('price', 'N/A')
        price = parse_price(price_str)
        if price is None or price > price_max:
            continue  # Skip this item if price is over limit or not parseable

        # Determine color based on price
        if price <= 300000:
            price_color = Fore.GREEN
        elif price <= 350000:
            price_color = Fore.YELLOW
        else:
            price_color = Fore.RED

        # Additional color coding based on home type or lot size
        home_type = item.get('homeType', 'N/A')
        color = price_color  # Default to price color
        if home_type == "LOT":
            color = Fore.CYAN
        elif home_type != "LOT" and price <= 350000:
            color = price_color  # Use specific color for homes in price range

        # Printing details with color coding
        print(color + f"Listing ID: {item.get('zpid', 'N/A')}")
        print(f"Status: {item.get('statusText', 'N/A')}")
        print(f"Listing Type: {item.get('marketingStatusSimplifiedCd', 'N/A').replace('_', ' ').title()}")
        print(f"Price: {price_str}")
        print(f"Address: {item.get('address', 'N/A')}")
        print(f"Beds: {item.get('beds', 'N/A')}, Baths: {item.get('baths', 'N/A')}, Area: {item.get('area', 'N/A')} sqft")
        print(f"Days on Zillow: {item.get('hdpData', {}).get('homeInfo', {}).get('daysOnZillow', 'N/A')}")
        print(f"Zestimate: ${item.get('hdpData', {}).get('homeInfo', {}).get('zestimate', 'N/A')}, Rent Zestimate: ${item.get('hdpData', {}).get('homeInfo', {}).get('rentZestimate', 'N/A')}")
        print(f"Broker: {item.get('brokerName', 'N/A')}")
        print(f"Details URL: {item.get('detailUrl', 'N/A')}" + Style.RESET_ALL)
        print("\n" + "-" * 40 + "\n")

def print_property_details(data):
    for item in data:
        price_str = item.get('price', 'N/A')
        price = parse_price(price_str)
        unformatted_price = item.get("unformattedPrice","N/A")
        if price is None or price > price_max:
            continue  # Skip this item if price is over limit or not parseable
        
        raw_status = item.get('rawHomeStatusCd','N/A')

        zpid = item.get('zpid', 'N/A')
        status = item.get('statusText', 'N/A')
        address = item.get('address', 'N/A')
        beds = item.get('beds', 'N/A')
        baths = item.get('baths', 'N/A')
        area = f"{item.get('area', 'N/A')} sqft"
        detail_url = item.get('detailUrl', 'N/A')
        listing_type = item.get('marketingStatusSimplifiedCd', 'N/A').replace('_', ' ').title()
        days_on_zillow = item.get('hdpData', {}).get('homeInfo', {}).get('daysOnZillow', 'N/A')
        zestimate = item.get('hdpData', {}).get('homeInfo', {}).get('zestimate', 'N/A')
        rent_zestimate = item.get('hdpData', {}).get('homeInfo', {}).get('rentZestimate', 'N/A')
        broker_name = item.get('brokerName', 'N/A')
        
        print(f"Listing ID: {zpid}")
        print(f"Status: {status}")
        print(f"Listing Type: {listing_type}")
        print(f"Price: {price_str}")
        print(f"UnformattedPrice: {unformatted_price}")
        print(f"Address: {address}")
        print(f"Beds: {beds}, Baths: {baths}, Area: {area}")
        print(f"Days on Zillow: {days_on_zillow}")
        print(f"Zestimate: ${zestimate}, Rent Zestimate: ${rent_zestimate}")
        print(f"Broker: {broker_name}")
        print(f"Details URL: {detail_url}")

        print("\n" + "-" * 40 + "\n")

def parse(data):
	print("parse...")
	tree_obj = objectpath.Tree(data)
	result = tuple(tree_obj.execute('$..cat1..listResults'))
	print_property_details(result)


options = webdriver.ChromeOptions()

# ???
#options.add_argument('--headless')
#options.add_argument('--disable-webgl')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
options.add_experimental_option("useAutomationExtension", False) 
browser = webdriver.Chrome(options=options)
browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
 
#yucca valley?
zillow_url = '''https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-116.74432410437376%2C%22east%22%3A-115.94094886023314%2C%22south%22%3A33.88203887220748%2C%22north%22%3A34.347058088601294%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22price%22%3A%7B%22max%22%3A600000%7D%2C%22mp%22%3A%7B%22max%22%3A3030%7D%7D%2C%22isEntirePlaceForRent%22%3Atrue%2C%22isRoomForRent%22%3Afalse%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%2C%22pagination%22%3A%7B%7D%7D'''
browser.get(zillow_url)
time.sleep(12) # might need to be longer  

script_tag = browser.find_elements(By.XPATH, '//*[@id="__NEXT_DATA__"]')
json_str = script_tag[0].get_attribute('innerHTML').replace('\u2192', '')

# save our results
out_json = open("out.json","w")
out_json.write(json_str)
json_data = json.loads(json_str)
parse(json_data)

browser.quit()