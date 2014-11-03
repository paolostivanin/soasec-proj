import os
from http.cookiejar import LWPCookieJar
import requests
requests.packages.urllib3.disable_warnings()

USER='admin@admin'
REALM='testr'
PASSWD='test'
COOKIE_PATH='/tmp/cookiejar'

SERIAL=''
USER_TK=''
SESSION_ID=''


def get_session_id(name):
    file = open(name,'r')
    line = file.readline()
    line = file.readline()
    tk1 = line.split("=")
    tk2 = tk1[1]
    tk3 = tk2.split('"')[2]
    session_id = tk3.split("\\")[0]
    file.close()
    print(session_id)


s = requests.Session()
s.cookies = LWPCookieJar(COOKIE_PATH)
if not os.path.exists(COOKIE_PATH):
    # Create a new cookies file and set our Session's cookies
    s.cookies.save()
    r = s.post('https://localhost:5001/account/dologin?login=' + USER + '&realm=' + REALM + '&password=' + PASSWD, verify=False)
    print("LOGIN: " + r.status_code)
else:
    # Load saved cookies from the file and use them in a request
    s.cookies.load(ignore_discard=True)
    SESSION_ID = get_session_id(COOKIE_PATH)
    #le prime 3 (init, assign, enable) le devo fare *solo* se è la prima volta
    r = s.get('https://localhost:5001/admin/init?serial=' + SERIAL + '&type=hmac&description=api_gen&genkey=1&hashlib=sha1&otplen=6&session=' + SESSION_ID, verify=False)
    r = s.get('https://localhost:5001/admin/assign?serial=' + SERIAL + '&user=' + USER_TK + '&session=' + SESSION_ID, verify=False)
    r = s.get('https://localhost:5001/admin/enable?serial=' + SERIAL + '&user=' + USER_TK + '&session=' + SESSION_ID, verify=False)
    
    r = s.get('https://localhost:5001/gettoken/getotp?serial=' + SERIAL + '&session=' + SESSION_ID, verify=False)
    print(r.status_code)
    print(r.text)

# Save the session's cookies back to the file
s.cookies.save(ignore_discard=True)
