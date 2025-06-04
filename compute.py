#cross reference elevations from dumped json

from colorama import init
from colorama import Fore, Style
init()
import json
import time
import objectpath
import requests
price_max = 350000
ids = []
def get_elevation(lat, lon):
    """Get elevation for latitude and longitude using Open Elevation API."""
    url = "https://api.open-elevation.com/api/v1/lookup"
    params = {"locations": f"{lat},{lon}"}
    response = requests.get(url, params=params)
    data = response.json()
    
    if data and "results" in data and len(data["results"]) > 0:
        elevation = data["results"][0]["elevation"]
        return elevation
    else:
        return None


def parse_lot_area(lot_area_string):
    if not lot_area_string:
        return None
    try:
        if "acres" in lot_area_string:
            # Convert acres to sqft if needed, assuming 1 acre = 43560 sqft
            value = float(lot_area_string.split()[0])
            return value * 43560  # Convert acres to square feet
        else:
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

        zid = item.get('zpid')
        if zid in ids:
            continue
        ids.append(zid)

        price_str = item.get('price', 'N/A')
        price = parse_price(price_str)

        if price < 150000:
            continue
        
        if price > 650000:
            continue
        
        if price <= 300000:
            price_color = Fore.GREEN
        elif price <= 500000:
            price_color = Fore.YELLOW
        else:
            price_color = Fore.RED

        status = item.get('statusText', 'N/A')
        if "Lot" in status:
            continue
        
        latlon = item.get('latLong')
        lat = float(latlon['latitude'])
        lon = float(latlon['longitude'])
        
        elevation = get_elevation(lat, lon)
        feet = float(elevation / 0.3048)

        if feet<3700.0:
            continue

        # Printing details with color coding
        print(price_color + f"Listing ID: {item.get('zpid', 'N/A')}")
        #print(f"Status: {status}")
        #print(f"Listing Type: {item.get('marketingStatusSimplifiedCd', 'N/A').replace('_', ' ').title()}")
        print(f"Price: {price_str}")
        #print(f"Address: {item.get('address', 'N/A')}")
        print(f"Beds: {item.get('beds', 'N/A')}, Baths: {item.get('baths', 'N/A')}, Area: {item.get('area', 'N/A')} sqft")
        #print(f"Days on Zillow: {item.get('hdpData', {}).get('homeInfo', {}).get('daysOnZillow', 'N/A')}")
        #print(f"Zestimate: ${item.get('hdpData', {}).get('homeInfo', {}).get('zestimate', 'N/A')}, Rent Zestimate: ${item.get('hdpData', {}).get('homeInfo', {}).get('rentZestimate', 'N/A')}")
        #print(f"Broker: {item.get('brokerName', 'N/A')}")
        print(f"Details URL: {item.get('detailUrl', 'N/A')}" + Style.RESET_ALL)
        #print(Fore.CYAN +f"LAT: {lat}")
        #print(f"LON: {lon}")
        print(Fore.CYAN+f"Elevation at {lat}, {lon}: {feet} feet")
        print(Style.RESET_ALL)
        print("\n" + "-" * 40 + "\n")


def parse(data):

	tree_obj = objectpath.Tree(data)
	result = tuple(tree_obj.execute('$..cat1..listResults'))
	_print_property_details(result)

json_str = open("out.json","r").read()
json_data = json.loads(json_str)
parse(json_data)
