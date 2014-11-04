#!/usr/bin/python

import requests
import sys
import json, base64
import hmac
from hashlib import sha1

requests.packages.urllib3.disable_warnings()

VERSION = "1.0-alpha3"
METHODS = ['GET','POST','PATCH','DELETE']

'''
ToDo:
    - non interactive (tutto da argv)
'''


def is_json(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def compute_hmac(data):
    k = input("Secret Key: ")
    key = bytes(k, encoding='utf-8')
    msg = bytes(data, encoding='utf-8')
    hm = hmac.new(key, msg, sha1).digest()
    b64hm = base64.b64encode(hm).decode()    
    return b64hm
    
    
def run_interactive_api():
    h = input("Host (with port and endpoint): ")
    m = input("Method: ")
    
    if m != 'POST':
        a = input("Auth token: ")
        a = base64.b64encode((a + ":").encode())
        a = a.decode()
        a = 'Basic ' + a
      
    m = m.upper()
    if(m not in METHODS):
        sys.exit("[!] Unknown method. You have to choose one between: " + str(METHODS))
        
    if m != 'GET' and m != 'DELETE':
        c = input("JSON data: ")
        if not is_json(c):
            sys.exit("[!] Given data is not in JSON format")
    else:
        c = '{}'
        
    hmac_header = compute_hmac(c)
    
    if h[-8:] != 'accounts':
        if m == 'PATCH' or m == 'DELETE':
            etag = input("Type _etag field: ")
            header = {'content-type':'application/json', 'If-Match': etag, 'Authorization': a, 'Content-HMAC': hmac_header}
        else:
            header = {'content-type':'application/json','Authorization': a, 'Content-HMAC': hmac_header}
    else:
        header = {'Authorization': a, 'content-type':'application/json', 'Content-HMAC': hmac_header}
    
    try:
        if m == 'GET':
            r = requests.get(h, headers=header)
        elif m == 'POST':
            r = requests.post(h, data=c, headers=header)
        elif m == 'PATCH':
            r = requests.patch(h, data=c, headers=header)
        elif m == 'DELETE':
            r = requests.delete(h, headers=header)
    except requests.ConnectionError:
        sys.exit("[!] Connection error. The host " + h + " is either wrong or offline")
    else:
        if m == 'DELETE' and r.status_code == 200:
            print("200 DELETE OK")
        else:
            print(r.text)
		
		
def run_interactive_ws():
    h = input("Host: ")
    c = input("JSON data: ")

    if not is_json(c):
        sys.exit("You wrote wrong JSON data")        
    

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        sys.exit('Usage: python ' + sys.argv[0] + ' [-h]|[-v]|[-i]')
        
    if(sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print("Now a help will be printed")
    elif(sys.argv[1] == '-v' or sys.argv[1] == '--version'):
        print("PyClient v" + VERSION)
    elif(sys.argv[1] == '-i' or sys.argv[1] == '--interactive'):
        if(len(sys.argv) < 3):
            sys.exit("You must choose between '--api' or '--ws'")
        if(sys.argv[2] == '--api'):
            run_interactive_api()
        elif(sys.argv[2] == '--ws'):
            run_interactive_ws()
    elif(sys.argv[1] == '--api'):
        print("api")
    elif(sys.argv[1] == '--ws'):
        print("ws")
