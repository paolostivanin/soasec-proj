from eve import Eve
from eve.auth import HMACAuth
from hashlib import sha1
import hmac
import base64
import string
import random
import bcrypt


class HMACAuth(HMACAuth):
    def check_auth(self, userid, hmac_hash, headers, data, allowed_roles, resource, method):
	    accounts = app.data.driver.db['accounts']
	    user = accounts.find_one({'username': userid})
	    if user and '_id' in user:
		    secret_key = user['secret_key']
		    self.set_request_auth_value(user['_id'])
		    
	    # in this implementation we only hash request data, ignoring the headers.
	    hm = hmac.new(bytes(secret_key, encoding='utf-8'), data, sha1).digest()
	 
	    return user and base64.b64encode(hm).decode() == hmac_hash


def gen_secret_and_hash_pwd(documents):
	for document in documents:
		document["secret_key"] = (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)))
		document["password"] = bcrypt.hashpw(document["password"], bcrypt.gensalt(10))

	
if __name__ == '__main__':
	app = Eve(auth=HMACAuth)
	app.on_insert_accounts += gen_secret_and_hash_pwd
	app.run()
