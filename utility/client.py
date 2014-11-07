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
    
    
def run_interactive():
    h = input("Host (with port and endpoint): ")
    m = input("Method: ")
    m = m.upper()
    if(m not in METHODS):
        sys.exit("[!] Unknown method. You have to choose one between: " + str(METHODS))
    
    if m != 'POST' or (m == 'POST' and h[-8:] != 'accounts'):
        a = input("Auth token: ")
        a = base64.b64encode((a + ":").encode())
        a = a.decode()
        a = 'Basic ' + a
      
    if m != 'GET' and m != 'DELETE':
        c = input("JSON data: ")
        if not is_json(c):
            sys.exit("[!] Given data is not in JSON format")
    else:
        c = '{}'
    
    if h[-8:] == 'accounts' and m == 'POST':
        pass
    else:
        hmac_header = compute_hmac(c)
    
    if h[-8:] != 'accounts':
        if m == 'PATCH' or m == 'DELETE':
            etag = input("Type _etag field: ")
            header = {'content-type':'application/json', 'If-Match': etag, 'Authorization': a, 'Content-HMAC': hmac_header}
        else:
            header = {'content-type':'application/json','Authorization': a, 'Content-HMAC': hmac_header}
    elif h[-8:] == 'accounts' and m != 'POST':
        header = {'Authorization': a, 'content-type':'application/json', 'Content-HMAC': hmac_header}
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
		

def run_from_argv():
    h = sys.argv[1]
    m = upper(sys.argv[2])
    if(m not in METHODS):
        sys.exit("[!] Unknown method. You have to choose one between: " + str(METHODS))
    
    tk = sys.argv[3]
    if tk != 'none':
        a = base64.b64encode((tk + ":").encode())
        a = a.decode()
        a = 'Basic ' + a
        
    c = sys.argv[4]
    if not is_json(c):
        sys.exit("[!] Given data is not in JSON format")
        
    if sys.argv[5] != 'none':
        hmac_header = compute_hmac(c)
    
    # DA CAMBIARE, DEVE ESSERE SGRONDATO DA CLI E NON INTERATTIVAMENTE
    if sys.argv[6] != 'none':
        etag = sys.argv[6]
        if m == 'PATCH' or m == 'DELETE':
            header = {'content-type':'application/json', 'If-Match': etag, 'Authorization': a, 'Content-HMAC': hmac_header}
        
    else:
        if h[-8:] == 'accounts' and m == 'POST':
            header = {'content-type':'application/json'}
        else:
            header = {'content-type':'application/json','Authorization': a, 'Content-HMAC': hmac_header}

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


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        sys.exit('Usage: python ' + sys.argv[0] + ' [-h]|[-v]|[-i]')
        
    if(sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print("Usage:\npython " + sys.argv[0] + " <host> <method> <token> <JSON data> <secret key> <etag>\nWrite 'none' if you don't want to use a specific field")
    elif(sys.argv[1] == '-v' or sys.argv[1] == '--version'):
        print("PyClient v" + VERSION)
    elif(sys.argv[1] == '-i' or sys.argv[1] == '--interactive'):
        run_interactive()
    else:
        #<1:host>,<2:method>,<3:token>,<4:json>,<5:secret_key>,<6:etag>
        if len(sys.argv) >= 3 or len(sys.rgv) <= 7:
            run_from_argv()
