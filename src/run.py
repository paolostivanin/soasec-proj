from eve import Eve
from eve.auth import TokenAuth
from hashlib import sha1
from datetime import datetime, timezone, timedelta
from flask import request, abort
from pymongo import MongoClient
from bson.objectid import ObjectId
import json, base64, string
import os, random, bcrypt, hmac
import pymysql
import requests
import hashlib


class RolesAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        accounts = app.data.driver.db['accounts']
        account = accounts.find_one({'token': token})
        if account and '_id' in account:
            self.set_request_auth_value(account['_id'])

        if not check_token_validity(account['tokendate']):
            abort(401, description="Token expired, please update it")

        return account
        

def check_token_validity(d1):
    d2 = datetime.now(timezone.utc)
    s = (d2-d1).seconds + (d2-d1).days * 86400
    m = round(s/60)
    #If token is older than a day (1440 minutes) => ERR(401)
    if m >= 1440:
        return False
    else:
        return True


def gen_token_hash_pwd(documents):
    for document in documents:
        username = document["username"]
        passwd = document["password"]
        if not is_user_inside_privacyidea_db(username):
            add_user_to_privacyidea_db(username, passwd)
            document["token"] = (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)))
            document["tokendate"] = datetime.now(timezone.utc)
            document["password"] = bcrypt.hashpw(document["password"], bcrypt.gensalt(10))
            document["secret_key"] = (''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32)))


def is_user_inside_privacyidea_db(u):
    c = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='paolo', db='wpdb')
    cur = c.cursor()
    res = cur.execute("SELECT username FROM newtable WHERE username=%s", (u))
    if res == 0:
        return False
    else:
        return True


def add_user_to_privacyidea_db(u, p):
	pb = p.encode('utf-8')
	salt = os.urandom(8)
	enc=  base64.b64encode(hashlib.sha1(pb + salt).digest() + salt)
	hashed_pwd = '{SSHA}' + enc.decode()
	c = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='paolo', db='wpdb')
	cur = c.cursor()
	cur.execute("INSERT INTO newtable(username, password) VALUES(%s, %s)", (u, hashed_pwd))
	c.commit()
	c.close()
    		

def add_userid_to_db(document):
    c = MongoClient()
    db = c.apitest
    myco = db["accounts"]
    for i in document:
        user_name = myco.find_one({"username": i['username']})["username"]
        to_add = i['_id']
        myco.update({'username': user_name},{'$set': {'user_id': ObjectId(to_add)}})
    c.close()

    
def delete_from_privacyidea_db(document):
	c = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='paolo', db='wpdb')
	cur = c.cursor()
	cur.execute("DELETE FROM newtable WHERE username=%s", (document["username"]))
	c.commit()
	c.close()    


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
        abort(401, description="Wrong HMAC")
        
        
def vms_post_callback(request):
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
        abort(401, description="Wrong HMAC")


def pre_accounts_patch_callback(request, lookup):
    data = request.json
    if 'username' and 'password' and 'otp' in data:
        u = data['username']
        p = data['password']
        o = data['otp']
        if not check_otp_auth(u, p, o):
            abort(401, description="Wrong OTP value")
        else:
            token = (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)))
            token_validity = datetime.now(timezone.utc) + timedelta(days=1)
            if not update_token(u, token, token_validity):
                abort(500, description="Failed to update token")
            else:
                pass
    else:
        abort(401, description="Missing username, password or otp")


def check_otp_auth(user, passwd, otp):
    req_link = "https://localhost:5001/validate/check?user=" + user + "&pass=" + passwd + otp
    print(req_link)
    r = requests.post(req_link, verify=False)
    parse = r.json()
    res = parse['result']['value']
    if res == False:
        return False
    else:
        return True


def update_token(username, tk, tk_val):
	c = MongoClient()
	db = c.apitest
	myco = db["accounts"]
	r = myco.update({'username': username},{'$set': {'token': tk, 'tokendate': tk_val}})
	ret = r['updatedExisting']
	if not ret:
		c.close()
		return False
	else:
		c.close()
		return True


def remove_from_patch(updates, original):
    if 'otp' and 'username' and 'password' in updates:
        del updates['otp']
        del updates['username']
        del updates['password']
    
   
if __name__ == '__main__':
    app = Eve(auth=RolesAuth)
    app.on_insert_accounts += gen_token_hash_pwd
    app.on_inserted_accounts += add_userid_to_db
    app.on_update_accounts += remove_from_patch
    app.on_delete_item_accounts += delete_from_privacyidea_db
    app.on_pre_POST_vms += vms_post_callback
    app.on_pre_GET += methods_callback
    app.on_pre_PATCH += methods_callback
    app.on_pre_PATCH_accounts += pre_accounts_patch_callback
    app.on_pre_DELETE += methods_callback
    app.run()
