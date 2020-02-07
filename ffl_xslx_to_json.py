import pandas as pd
import json
import urllib.request
import urllib.parse

def get_coordinates_for_address(address):
    encoded_address = urllib.parse.urlencode({'address' : address})
    r = urllib.request.urlopen('https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?{}&benchmark=9&format=json'.format(encoded_address))
    address_data = json.loads(r.read().decode('utf-8'))

    coords = {}
    coords['lat'] = address_data['result']['addressMatches'][0]['coordinates']['y']
    coords['lon'] = address_data['result']['addressMatches'][0]['coordinates']['x']

    return coords

df = pd.read_excel('1219-ffl-list-pennsylvania-1.xlsx', sheet_name="Sheet1")

with open('ffl-list-pennsylvania.json', 'w') as f:
    f.write('{"ffls":[')

    jsonRowTemplate = '{{"businessName":"{}","url":"{}","address":"{}","lat":"{}",' + \
                      '"long":"{}","phone":"{}","status":"uncontacted"}}'

    for i in df.index:
        address = '{}, {}, {} {}'.format(df['Premise Street'][i], df['Premise City'][i], 
                  df['Premise State'][i], df['Premise Zip Code'][i])
        coords = get_coordinates_for_address(address)
        f.write(jsonRowTemplate.format(df['Business Name'][i], "", address, coords['lat'], 
                coords['lon'], str(df['Voice Phone'][i])))

        if i != df.index.size - 1:
            f.write(',')

    f.write(']}')
