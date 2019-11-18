#!/bin/python3
#by Qzacy

import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder
from phonenumbers import timezone
import sys
import subprocess
import requests
import json
import time

def lscan(uNumber):
    subprocess.call('clear')
    print('Running local scan...')
    time.sleep(1.5)

    FormattedPhoneNumber = "+" + uNumber

    try:
        PhoneNumberObject = phonenumbers.parse(FormattedPhoneNumber, None)
    except Exception as e:
        if e == '':
            print('Error, invalid phone number.')
            sys.exit()
        else:    
            print('Error,', e)
            sys.exit()
    else:
        if not phonenumbers.is_valid_number(PhoneNumberObject):
            return False

        numberCountryCode = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.INTERNATIONAL).split(' ')[0]
        localNumber = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.E164).replace(numberCountryCode, '')
        internationalNumber = phonenumbers.format_number(PhoneNumberObject, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        country = geocoder.country_name_for_number(PhoneNumberObject, "en")
        location = geocoder.description_for_number(PhoneNumberObject, "en")
        carrierName = carrier.name_for_number(PhoneNumberObject, 'en')

        
        print('International format: {}'.format(internationalNumber))
        print('Local format: {}'.format(localNumber))
        print('Country: {} ({})'.format(country, numberCountryCode))
        print('City: {}'.format(location))
        print('Carrier: {}'.format(carrierName))
        for timezoneResult in timezone.time_zones_for_number(PhoneNumberObject):
            print('Timezone: {}'.format(timezoneResult))

        if phonenumbers.is_possible_number(PhoneNumberObject):
            print('Valid: True')
        else:
            print('Valid: False')


def nverifyScan(uNumber):
    subprocess.call('clear')
    print('Running NumVerify API scan...')
    time.sleep(1.5)
    api_key = ''
    r = requests.get('http://apilayer.net/api/validate?access_key=' + api_key + '&number=' + uNumber)
    resp = r.json()
    print('International format: ' + resp['international_format'])
    print('Local format: ' + resp['local_format'])
    print('Country name: ' + resp['country_name'])
    print('Country prefix: ' + resp['country_prefix'])
    print('Country code: ' + resp['country_code'])
    print('City: ' + resp['location'])
    print('Carrier: ' + resp['carrier'])
    print('Line type: ' + resp['line_type'])


if __name__ == '__main__':
    subprocess.call('clear')
    print ('Welcome to phoneSc, coded by Qzacy.')
    uNumber = input('Enter the phone number without "+": ')
    subprocess.call('clear')
    print ('Select the scan method for', uNumber, ':\n[1] LocalScan\n[2] NumVerify')
    scanSel = input('pSc > ')
    if scanSel == '1':
        lscan(uNumber)
    elif scanSel == '2':
        nverifyScan(uNumber)
    else:
        print('Please, enter a valid option... \nQuitting...')
        sys.exit()
