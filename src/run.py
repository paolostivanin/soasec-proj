from eve import Eve
from eve.auth import TokenAuth
from hashlib import sha1
from datetime import datetime, timezone
from flask import request, abort
import json, base64, string
import random, bcrypt, hmac
from pymongo import MongoClient 


'''
    - VALUTARE SE CONVERTIRE WEB SERVER IN CALLBACK
'''

class RolesAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        accounts = app.data.driver.db['accounts']
        account = accounts.find_one({'token': token})
        if account and '_id' in account:
            self.set_request_auth_value(account['_id'])

        if not check_token_validity(account['tokendate']):
            return

        return account
        

def gen_token_hash_pwd(documents):
	for document in documents:
		document["token"] = (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)))
		document["tokendate"] = datetime.now(timezone.utc)
		document["password"] = bcrypt.hashpw(document["password"], bcrypt.gensalt(10))
		document["secret_key"] = (''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32)))
		

def check_token_validity(d1):
    d2 = datetime.now(timezone.utc)
    s = (d2-d1).seconds + (d2-d1).days * 86400
    m = round(s/60)
    #If token is older than a day (1440 minutes) => ERR(401)
    if m >= 1440:
        return False
    else:
        return True


def get_seckey_from_token(token):
    c = MongoClient()
    db = c.apitest
    myco = db["accounts"]
    sec_key = myco.find_one({"token": token})["secret_key"]
    c.close()
    return sec_key
    
    
def methods_callback(resource, request, payload):
    orig_hmac = request.headers.get('Content-HMAC')
    tmp_tk = request.headers.get('Authorization')
    b64_tk = tmp_tk.split(' ')[1]
    real_tk = base64.b64decode(b64_tk).decode()
    real_tk = real_tk.split(":")[0]
    secret_key = get_seckey_from_token(real_tk)
    key = bytes(secret_key, encoding='utf-8')
    msg = request.data
    if len(msg) == 0:
        msg = '{}'.encode()
    hm = hmac.new(key, msg, sha1).digest()
    computed_hmac = base64.b64encode(hm).decode()
    if orig_hmac != computed_hmac:
        abort(401)

				
if __name__ == '__main__':
    app = Eve(auth=RolesAuth)
    app.on_insert_accounts += gen_token_hash_pwd
    app.on_pre_POST_vms += methods_callback
    app.on_pre_GET += methods_callback
    app.on_pre_PATCH += methods_callback
    app.on_pre_DELETE += methods_callback
    app.run()
