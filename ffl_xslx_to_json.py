#!/usr/bin/env python3

import pandas as pd
import json
import urllib.request
import urllib.parse

def get_coordinates_for_address(address):
    encoded_address = urllib.parse.urlencode({'address' : address})
    r = urllib.request.urlopen('https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?{}&benchmark=9&format=json'.format(encoded_address))
    address_data = json.loads(r.read().decode('utf-8'))

    coords = {}
    if address_data['result']['addressMatches']:
        coords['lat'] = address_data['result']['addressMatches'][0]['coordinates']['y']
        coords['lon'] = address_data['result']['addressMatches'][0]['coordinates']['x']

    return coords

df = pd.read_excel('1219-ffl-list-pennsylvania-1_trimmed.xlsx', sheet_name="Sheet1")

with open('ffl-list-pennsylvania.json', 'w') as f:
    f.write('{"ffls":[')

    jsonRowTemplate = '{{"businessName":"{}","url":"{}","address":"{}","lat":"{}",' + \
                      '"lon":"{}","phone":"{}","status":"uncontacted"}}'

    for i in df.index:
        address = '{}, {}, {} {}'.format(df['Premise Street'][i], df['Premise City'][i], 
                  df['Premise State'][i], df['Premise Zip Code'][i])
        
        coords = get_coordinates_for_address(address)
        if not coords:
            print('Could not get coordinates for: ' + address)
            continue

        business_name = df['Business Name'][i]
        if not business_name:
            business_name = df['License Name'][i]

        f.write(jsonRowTemplate.format(business_name, "", address, coords['lat'], 
                coords['lon'], str(int(df['Voice Phone'][i]))))

        if i != df.index.size - 1:
            f.write(',')

    f.write(']}')
