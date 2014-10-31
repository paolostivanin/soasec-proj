#!/usr/bin/python

import requests
import sys
import json
import base64

requests.packages.urllib3.disable_warnings()

VERSION = "1.0-alpha1"
METHODS = ['GET','POST','PATCH','DELETE']


def is_json(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


def run_interactive(mode):
    if(mode == 0):
        h = input("Host (with port and endpoint): ")
        m = input("Method: ")
        if h[-8:] != 'accounts':
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
        
        if h[-8:] != 'accounts':
            if m == 'PATCH' or m == 'DELETE':
                etag = input("Type _etag field: ")
                header = {'content-type':'application/json', 'If-Match': etag, 'Authorization': a}
            else:
                header = {'content-type':'application/json','Authorization': a}
        else:
            header = {'content-type':'application/json'}
        
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
		
		
    else:
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
            run_interactive(0)
        elif(sys.argv[2] == '--ws'):
            run_interactive(1)
            
