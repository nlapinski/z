import pyzill
import json
import time
import objectpath
import math

#use rotating residential proxies
# disabled for now #proxy_url = pyzill.parse_proxy("[proxy_ip or proxy_domain]","[proxy_port]","[proxy_username]","[proxy_password]")
proxy_url = None

#top 
ne_lat = 34.248512648489
ne_long = -118.01146348295566

#BTM
sw_lat = 34.016050882856305
sw_long = -118.41315110502597

pagination = 1
#pagination is for the list that you see at the right when searching
#you don't need to iterate over all the pages because zillow sends the whole data on mapresults at once on the first page
#however the maximum result zillow returns is 500, so if mapResults is 500
#try playing with the zoom or moving the coordinates, pagination won't help because you will always get at maximum 500 results
pagination = 1

price_max = 2400
distance_cutoff = .75

# transit_pos: [latitude, longitude]  # Station Name
transit_pos = [
    [34.017485, -118.496241,  "4th Street/ Santa Monica College "],
    [34.019065, -118.491020,  "17th Street/SMC "],
    [34.022145, -118.481688,  "Downtown Santa Monica "],

    [33.941591, -118.408529,  "Aviation/LAX "],
    [33.937519, -118.395956,  "Aviation/Century "],
    [33.930804, -118.357315,  "El Segundo "],
    [33.915627, -118.339927,  "Mariposa "],
    [33.905258, -118.337071,  "Downtown Inglewood "],
    [33.902873, -118.326158,  "Westchester/Veterans "],
    [33.898098, -118.303024,  "Fairview Heights "],
    [33.892041, -118.289089,  "Redondo Beach "],

    [33.961680, -118.361714,  "Hawthorne/Lennox "],
    [34.014783, -118.493365,  "26th Street/Bergamot "],
    [33.952018, -118.340720,  "Crenshaw/Imperial "],
    [33.951761, -118.333188,  "Florence/West "],
    [33.951728, -118.296397,  "Washington/Western "],
    [33.951684, -118.267244,  "Vermont/Athens "],

    [33.938783, -118.287013,  "Imperial/Wilmington "],
    [33.932655, -118.273546,  "Anaheim "],
    [33.925816, -118.261585,  "Compton "],
    [33.925110, -118.225692,  "Long Beach Blvd "],
    [33.918136, -118.200989,  "Del Amo "],
    [33.899028, -118.202926,  "Willowbrook/Rosa Parks "],
    [33.889327, -118.194856,  "Lakewood Blvd "],
    [33.877918, -118.190519,  "Del Amo "],

    [34.056219, -118.236502,  "Hollywood/Western "],
    [34.052167, -118.243568,  "Pershing Square "],
    [34.052268, -118.248900,  "Civic Center/Grand Park "],
    [34.056219, -118.247002,  "Union Station "],
    [34.059395, -118.245303,  "Chinatown "],

    [34.056825, -118.205032,  "Civic Center/Grand Park "],
    [34.052545, -118.244667,  "Pershing Square "],
    [34.045589, -118.256778,  "7th Street/Metro Center "],
    [34.039005, -118.267254,  "Westlake/MacArthur Park "],
    [34.035573, -118.269178,  "Wilshire/Vermont "],
    [34.059679, -118.309239,  "Hollywood/Highland "],
    [34.066904, -118.303792,  "Hollywood/Vine "],
    [34.076140, -118.360226,  "Vermont/Sunset "],
    [34.081185, -118.361629,  "Sunset/Vermont "],
    [34.092809, -118.328661,  "Hollywood/Western "],
    [34.147580, -118.144528,  "North Hollywood "],

    [34.011510, -118.492620,  "Expo/Bundy "],
    [34.009800, -118.495800,  "Expo/Westwood "],
    [34.007555, -118.502000,  "26th Street/Bergamot "],
    [34.007500, -118.509000,  "17th Street/SMC "],
    [34.021122, -118.393837,  "LATTC/USC "],
    [34.022960, -118.254231,  "Little Tokyo/Arts District "],

    [34.028620, -118.060740,  "Sierra Madre Villa "],
    [34.146240, -118.155940,  "Memorial Park (Pasadena) "],
    [34.145510, -118.164000,  "Lake (Pasadena) "],
    [34.133150, -118.161527,  "Allen (Pasadena) "],
    [34.123880, -118.155590,  "Memorial Park "],
    [34.147460, -118.145580,  "Lake (Pasadena) "],
    [34.148969, -118.162272,  "Allen (Pasadena) "],
    [34.133672, -118.142200,  "Fillmore (Pasadena) "],

    [34.148705, -118.085153,  "APU/Citrus College "],
    [34.096351, -118.105650,  "Arcadia "],
    [34.136467, -118.065768,  "Monrovia "],
    [34.145330, -118.066085,  "Duarte/City of Hope "],
    [34.150270, -118.121940,  "Irwindale "],
    [34.133020, -118.080280,  "Azusa Downtown "],
    [34.108290, -118.085690,  "San Gabriel/Fox "],

    [34.041820, -118.424780,  "7th Street/Metro Center "],
    [34.034016, -118.266201,  "Westlake/MacArthur Park "],
    [34.053236, -118.242637,  "Pershing Square "],
    [34.039472, -118.266155,  "7th Street/Metro Center "],
    [34.043018, -118.248766,  "Civic Center/Grand Park "],

    [33.946242, -118.351928,  "Redondo Beach "],
    [33.948553, -118.346402,  "Hawthorne/Lennox "],
    [33.915689, -118.342082,  "Mariposa "],
    [33.930557, -118.336408,  "Downtown Inglewood "],
    [33.905064, -118.281216,  "Fairview Heights "],
    [33.898117, -118.283436,  "Westchester/Veterans "],
    [33.937519, -118.395956,  "Aviation/Century "],
    [33.941591, -118.408529,  "Aviation/LAX "],

    [34.021122, -118.393837,  "LATTC/USC "],
    [34.019992, -118.284290,  "Vermont/Sunset "],
    [34.020159, -118.264742,  "Hollywood/Western "],
    [34.020254, -118.267571,  "Hollywood/Vine "],
    [34.052167, -118.243568,  "Pershing Square "],
    [34.048548, -118.256779,  "7th Street/Metro Center "],

    [34.095090, -118.131660,  "Sierra Madre Villa "],
    [34.044885, -118.250540,  "Union Station "],
    [34.033620, -118.244994,  "Civic Center/Grand Park "],
    [34.028610, -118.259138,  "Little Tokyo/Arts District "],
    [34.021122, -118.393837,  "LATTC/USC "],
    [34.009800, -118.495800,  "Expo/Westwood "],
    [34.011510, -118.492620,  "Expo/Bundy "],

    [34.063993, -118.358032,  "Hollywood/Highland "],
    [34.046656, -118.256780,  "7th Street/Metro Center "],
    [34.056219, -118.247002,  "Union Station "],
    [34.052173, -118.247103,  "Pershing Square "],
    [34.060260, -118.236790,  "Chinatown "],

    [34.046656, -118.256780,  "7th Street/Metro Center "],
    [34.041820, -118.424780,  "7th Street/Metro Center "],
    [34.021122, -118.393837,  "LATTC/USC "],
    [33.946242, -118.351928,  "Redondo Beach "],
    [33.951761, -118.333188,  "Florence/West "],

    [34.048548, -118.256779,  "7th Street/Metro Center "],
    [34.056219, -118.247002,  "Union Station "],
    [34.052545, -118.244667,  "Pershing Square "],
    [34.053236, -118.242637,  "Pershing Square "],
    [34.029001, -118.263695,  "Little Tokyo/Arts District "],

    [34.020254, -118.267571,  "Hollywood/Vine "],
    [34.014783, -118.493365,  "26th Street/Bergamot "],
    [33.941591, -118.408529,  "Aviation/LAX "],
    [33.937519, -118.395956,  "Aviation/Century "],
    [34.009800, -118.495800,  "Expo/Westwood "],

    [34.056219, -118.247002,  "Union Station "],
    [34.052545, -118.244667,  "Pershing Square "],
    [34.053236, -118.242637,  "Pershing Square "],
    [33.952018, -118.340720,  "Crenshaw/Imperial "],
    [33.932655, -118.273546,  "Anaheim "],

    [33.899028, -118.202926,  "Willowbrook/Rosa Parks "],
    [33.925816, -118.261585,  "Compton "],
    [33.918136, -118.200989,  "Del Amo "],
    [33.877918, -118.190519,  "Del Amo "],
    [33.889327, -118.194856,  "Lakewood Blvd "],

    [34.093000, -118.131950,  "Sierra Madre Villa "],
    [34.095090, -118.131660,  "Sierra Madre Villa "],
    [34.044885, -118.250540,  "Union Station "],
    [34.053236, -118.242637,  "Pershing Square "],
    [34.048548, -118.256779,  "7th Street/Metro Center "],

    [34.020254, -118.267571,  "Hollywood/Vine "],
    [34.052545, -118.244667,  "Pershing Square "],
]


results_rent = pyzill.for_rent(pagination, 
              search_value="",is_entire_place=False,is_room=True,
              min_beds=1,max_beds=None,
              min_bathrooms=None,max_bathrooms=None,
              min_price=10000,max_price=None,
              ne_lat=ne_lat,ne_long=ne_long,sw_lat=sw_lat,sw_long=sw_long,
              zoom_value=15,
              proxy_url=proxy_url)


def latlon_to_miles(lat1, lon1, lat2, lon2):

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    sin_dlat_half = math.sin(dlat / 2.0)
    sin_dlon_half = math.sin(dlon / 2.0)
    a = (
        sin_dlat_half * sin_dlat_half
        + math.cos(lat1_rad) * math.cos(lat2_rad) * sin_dlon_half * sin_dlon_half
    )
    c = 2.0 * math.asin(math.sqrt(a))

    earth_radius_miles = 3959.0
    return earth_radius_miles * c

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

def print_property_details(data):
    for item in data:
        #print(item)
        price_str = item.get('price', 'N/A').replace("/mo","")
        price = parse_price(price_str)
        #print(price_str)
        unformatted_price = item.get("unformattedPrice","N/A")
        if price is None or price > price_max:
            continue  # Skip this item if price is over limit or not parseable
        
        # raw_status = item.get('rawHomeStatusCd','N/A')

        zpid = item.get('zpid', 'N/A')
        status = item.get('statusText', 'N/A')
        address = item.get('address', 'N/A')
        beds = item.get('beds', 'N/A')
        baths = item.get('baths', 'N/A')
        area = f"{item.get('area', 'N/A')} sqft"
        detail_url = item.get('detailUrl', 'N/A')
        listing_type = item.get('marketingStatusSimplifiedCd', 'N/A').replace('_', ' ').title()
        #days_on_zillow = item.get('hdpData', {}).get('homeInfo', {}).get('daysOnZillow', 'N/A')
        # zestimate = item.get('hdpData', {}).get('homeInfo', {}).get('zestimate', 'N/A')
        # rent_zestimate = item.get('hdpData', {}).get('homeInfo', {}).get('rentZestimate', 'N/A')
        # broker_name = item.get('brokerName', 'N/A')
        lat = float(item.get('latLong').get("longitude"))
        lon = float(item.get('latLong').get("latitude"))
        
        p1 = [lon,lat]
        station = 'NA'

        min_d = 99999999999

        for p2 in transit_pos:
            d = latlon_to_miles(p1[0],p1[1], p2[0],p2[1] )
            if d < min_d:
                min_d = d
                station = p2[2]

        if min_d > distance_cutoff:
            continue             
        if beds > 1:
            continue

        print(f"Listing ID: {zpid}")
        print(f"Status: {status}")
        # print(f"Listing Type: {listing_type}")
        print(f"Price: {price_str}")
        print(f"UnformattedPrice: {unformatted_price}")
        print(f"Address: {address}")
        print(f"Beds: {beds}, Baths: {baths}, Area: {area}")
        # print(f"Days on Zillow: {days_on_zillow}")
        # print(f"Zestimate: ${zestimate}, Rent Zestimate: ${rent_zestimate}")
        # print(f"Broker: {broker_name}")
        print(f"LOC: ({lat},{lon})")
        print(f"Nearest transit: {format(min_d, '.2f')} miles")
        print(f"Station: {station}")
        print(f"Details URL: {detail_url}")

        print("\n" + "-" * 40 + "\n")

def parse2(data):
    print("parse...")
    #tree_obj = objectpath.Tree(data)
    #result = tuple(tree_obj.execute('$..cat1..listResults'))
    #print(result)
    print_property_details(data)

jsondata_rent = json.dumps(results_rent)

# parse2((results_rent))
#for l in results_rent:
    #print(l)
    #for j in results_rent['listResults']:
        #print(j)

parse2(results_rent['listResults']) 

# f = open("./jsondata_rent.json", "w")
# f.write(jsondata_rent)
# f.close()
