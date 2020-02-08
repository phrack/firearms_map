#!/usr/bin/env python3

import pandas as pd
import json
import math
import urllib.request
import urllib.parse

# This script tries to use the US Census geocoding API, but this service does not support a lot of businesses.
# As a fallback, MapQuest's geocoding API is used assuming an API key is specified.
MAP_QUEST_API_KEY='Hfd69ylv3AF2NwDvE9JePSKGBVBjjWp9'

def get_coordinates_for_address(address):
    encoded_address = urllib.parse.urlencode({'address' : address})
    r = urllib.request.urlopen('https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?{}&benchmark=9&format=json'.format(encoded_address))
    address_data = json.loads(r.read().decode('utf-8'))

    coords = {}
    if address_data['result']['addressMatches']:
        coords['lat'] = address_data['result']['addressMatches'][0]['coordinates']['y']
        coords['lon'] = address_data['result']['addressMatches'][0]['coordinates']['x']
    elif MAP_QUEST_API_KEY:
        encoded_address = urllib.parse.urlencode({'location' : address})
        r = urllib.request.urlopen('http://open.mapquestapi.com/geocoding/v1/address?key={}&{}'.format(MAP_QUEST_API_KEY, encoded_address))
        address_data = json.loads(r.read().decode('utf-8'))

        if address_data['results']:
            coords['lat'] = address_data['results'][0]['locations'][0]['latLng']['lat']
            coords['lon'] = address_data['results'][0]['locations'][0]['latLng']['lng']

    return coords

df = pd.read_excel('1219-ffl-list-pennsylvania-1_trimmed.xlsx', sheet_name="Sheet1")

with open('ffl-list-pennsylvania.json', 'w') as f:
    f.write('{"ffls":[')

    jsonRowTemplate = '{{"businessName":"{}","url":"{}","address":"{}","lat":"{}",' + \
                      '"lon":"{}","phone":"{}","status":"uncontacted"}}'

    count = 0;

    for i in df.index:
        address = '{}, {}, {} {}'.format(df['Premise Street'][i], df['Premise City'][i], 
                  df['Premise State'][i], df['Premise Zip Code'][i])
        
        coords = get_coordinates_for_address(address)
        if not coords:
            print('Could not get coordinates for: ' + address)
            continue

        business_name = ''
        if isinstance(df['Business Name'][i], float):
            business_name = df['License Name'][i]
        else:
            business_name = df['Business Name'][i]

        phone_number = ''
        if math.isnan(df['Voice Phone'][i]):
            print('No phone number for: ' + address)
            continue
        else:
            phone_number = str(int(df['Voice Phone'][i]))

        f.write(jsonRowTemplate.format(business_name, "", address, coords['lat'], 
                coords['lon'], phone_number))

        if i != df.index.size - 1:
            f.write(',')

        count+=1

        if count % 100 == 0:
            print('Processed ' + count + 'entries')

    f.write(']}')
