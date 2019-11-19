import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from phonenumbers import timezone
import sys
import os
import requests
import json
from time import sleep

cdir = os.path.dirname(os.path.realpath(__file__))
banner = """
 __i
|---| phoneSc      v0.0.2
|[_]| The phone numbers',   
|:::| scanner.   
|:::|    
`\   \ by Qzacy.   
  \_=_\ Use 'help' to show the options. 
"""
pschelp = """
>>> Scan commands
py                       Python Scan (using phonenumbers lib)
nv                       Numverify Scan*
antd                     Antideo Scan
verp                     Veriphone Scan*

'*' requires the api_key.

>>> API options
add [nv|verp]            Add an API
check                    Check all the apis.

>>> Misc
clear
restart
credits
"""

def trm():
    try:
        cmd = input("pSc #> ")
        cmd = cmd.lower()
        if cmd == "help" or cmd == "h" or cmd == "-h" or cmd == "--help":
            print(pschelp)
            trm()
        elif cmd == "py":
            lscan(unumber)
        elif cmd == "nv":
            nvscan(unumber)
        elif cmd == "antd":
            antdscan(unumber)
        elif cmd == "verp":
            verpscan(unumber)
        elif cmd == "add":
            print("Error, this requires another value: [nv|verp]")
            trm()
        elif cmd == "add nv":
            name = "numv"
            add(name)
        elif cmd == "add verp":
            name = "verp"
            add(name)
        elif cmd == "check":
            check()
        elif cmd == "clear":
            os.system("clear")
            trm()
        elif cmd == "restart":
            print("Restarting...")
            sleep(0.5)
            os.system("clear")
            os.system("python3 " + cdir + "/psc.py " + unumber)
        elif cmd == "exit":
            sys.exit()
        elif cmd == "credits":
            print("Coded by Qzacy.\nAPIs used: Numverify, Veriphone.\n\nContacts:\nGithub: https://github.com/Qzacy\nMail: qzacycoder@protonmail.com")
            trm()        
        else:
            print("Please enter a valid option.")
            trm()
    except KeyboardInterrupt as e:
        e = "Interrupt"
        print("\nFound: '" + e + "', next time use 'exit'.")
        sys.exit()
    except Exception as e:
        print("\nError: '+" + str(e) + "', write me for help.")
        input("Press [ENTER] to restart...")
        print("Restarting...")
        sleep(0.5)
        os.system("clear")
        os.system("python3 " + cdir + "/psc.py " + unumber)
    
def add(name):
    if name == "numv":
        f = cdir + "/setup/nvapi.txt" 
    elif name == "verp":
        f = cdir + "/setup/verpapi.txt"
    key = input("Enter the key: ")
    try:
        f = open(f, "w")
        f.write(key)
        print("Writing the file...")
        sleep(0.5)
        f.close()
        print("Successfully wrote.")
        trm()
    except Exception as e:
        print("Error '" + str(e) + "' while writing the file,\ncheck 'README.md' to set the api_key manually.")

def check():
    print("Checking...\n")
    sleep(0.2)
    nvfile = open(cdir + "/setup/nvapi.txt", "r")
    nvkey = nvfile.readline()
    nvr = requests.get("http://apilayer.net/api/validate?access_key=" + nvkey + "&number=" + unumber)
    nvstatus = nvr.status_code
    verpfile = open(cdir + "/setup/verpapi.txt", "r")
    verpkey = verpfile.readline()
    verpr = requests.get("https://api.veriphone.io/v2/verify?phone=" + unumber + "&key=" + verpkey)
    verpstatus = verpr.status_code
    print("Numverify response: " + str(nvstatus))
    print("Veriphone responde: " + str(verpstatus))
    trm()

def lscan(unumber):
    print("Scanning [" + unumber + "] using *Python Scan*    phoneSc - by Qzacy")
    sleep(0.5)
    try:
        numberObj = phonenumbers.parse(unumber, None)
    except Exception as err:
        print("\n\nError: " + err)
        trm()
    else:
        if not phonenumbers.is_valid_number(numberObj):
            return False    
        iNum = phonenumbers.format_number(numberObj, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        cCode = phonenumbers.format_number(numberObj, phonenumbers.PhoneNumberFormat.INTERNATIONAL).split(' ')[0]
        lNum = phonenumbers.format_number(numberObj, phonenumbers.PhoneNumberFormat.E164).replace(cCode, '')
        country = geocoder.country_name_for_number(numberObj, "en")
        city = geocoder.description_for_number(numberObj, "en")
        nCarrier = carrier.name_for_number(numberObj, "en")
        timezones = str(timezone.time_zones_for_number(numberObj))
        if iNum == "":
            iNum = "/"
        if lNum == "":
            lNum = "/"
        if country == "":
            country = "/"
        if cCode == "":
            cCode = "/"
        if city == "":
            city = "/"
        if nCarrier == "":
            nCarrier = "/"
        if timezones == "":
            timezones = "/"
        
        print("\nInternational format: {}".format(iNum))
        print("Local format: {}".format(lNum))
        print("Country: {}".format(country))
        print("Country Code: {}".format(cCode))
        print("City: {}".format(city))
        print("Carrier: {}".format(nCarrier))
        print("Timezones: {}\n".format(timezones))

        trm()


def nvscan(unumber):
    if os.stat(cdir + "/setup/nvapi.txt").st_size == 0:
        print("Error, no-key found.")
        trm()
    print("Scanning [" + unumber + "] using *Numverify Scan*    phoneSc - by Qzacy")
    sleep(0.5)
    api_file = open(cdir + "/setup/nvapi.txt", "r")
    api_key = api_file.readline()
    r = requests.get("http://apilayer.net/api/validate?access_key=" + api_key + "&number=" + unumber)
    resp = r.json()
    if resp["international_format"] == "":
        resp["international_format"] = "/"
    if resp["local_format"] == "":
        resp["local_format"] = "/"
    if resp["country_name"] == "":
        resp["country_name"] = "/"
    if resp["country_prefix"] == "":
        resp["country_prefix"] = "/"
    if resp["country_code"] == "":
        resp["country_code"] = "/"
    if resp["location"] == "":
        resp["location"] = "/"
    if resp["carrier"] == "":
        resp["carrier"] = "/"
    if resp["line_type"] == "":
        resp["line_type"] = "/"

    print("\nInternational format: " + resp["international_format"])
    print("Local format: " + resp["local_format"])
    print("Country name: " + resp["country_name"])
    print("Country prefix: " + resp["country_prefix"])
    print("Country code: " + resp["country_code"])
    print("City: " + resp["location"])
    print("Carrier: " + resp["carrier"])
    print("Line type: " + resp["line_type"] + "\n")
   
    trm()

def antdscan(unumber):
    print("Scanning [" + unumber + "] using *Antideo Scan*    phoneSc - by Qzacy")
    sleep(0.5)
    r = requests.get("api.antideo.com/phone/" + unumber)
    resp = r.json()
    if resp["formats"]["international"] == "":
        resp["formats"]["international"] = "/"
    if resp["formats"]["national"] == "":
        resp["formats"]["national"] = "/"
    if resp["location"] == "":
        resp["location"] = "/"
    if resp["type"] == "":
        resp["type"] = "/"
    if resp["timezones"] == "":
        resp["timezones"] = "/"
    
    print("\nInternational format: " + resp["formats"]["international"])
    print("Local format: " + resp["formats"]["national"])
    print("City: " + resp["location"])
    print("Line type: " + resp["type"])
    print("Timezone: " + str(resp["timezones"]) + "\n")
  
    trm()

def verpscan(unumber):
    if os.stat(cdir + "/setup/verpapi.txt").st_size == 0:
        print("Error, no-key found.")
        trm()
    print("Scanning [" + unumber + "] using *Veriphone Scan*    phoneSc - by Qzacy")
    sleep(0.5)
    api_file = open(cdir + "/setup/verpapi.txt", "r")
    api_key = api_file.readline()
    r = requests.get("https://api.veriphone.io/v2/verify?phone=" + unumber + "&key=" + api_key)
    resp = r.json()
    if resp["international_number"] == "":
        resp["international_number"] = "/"
    if resp["local_number"] == "":
        resp["local_number"] = "/"
    if resp["country"] == "":
        resp["country"] = "/"
    if resp["country_prefix"] == "":
        resp["country_prefix"] = "/"
    if resp["country_code"] == "":
        resp["country_code"] = "/"
    if resp["phone_region"] == "":
        resp["phone_region"] = "/"
    if resp["carrier"] == "":
        resp["carrier"] = "/"
    if resp["phone_type"] == "":
        resp["phone_type"] = "/"

    print("\nInternational format: " + resp["international_number"])
    print("Local format: " + resp["local_number"])
    print("Country name: " + resp["country"])
    print("Country prefix: " + resp["country_prefix"])
    print("Country code: " + resp["country_code"])
    print("Region: " + resp["phone_region"])
    print("Carrier: " + resp["carrier"])
    print("Line type: " + resp["phone_type"] + "\n")
   
    trm()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nUsage: python3 psc.py [phonenumber]")
        sys.exit()
    unumber = sys.argv[1]
    if  not unumber.startswith("+"):
        print("Please enter the full number.")
        sys.exit()
    if len(sys.argv[1]) < 12:
        print("Please enter the full number.")
        sys.exit()
    print("Starting...")
    sleep(1)
    os.system("clear")
    print(banner)
    trm()
    
    

