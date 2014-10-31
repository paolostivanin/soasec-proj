from eve import Eve
#from eve.auth import HMACAuth
from eve.auth import TokenAuth
from hashlib import sha1
from datetime import datetime, timezone
#import hmac
import base64
import string
import random
import bcrypt


class RolesAuth(TokenAuth):
	def check_auth(self, token, allowed_roles, resource, method):
		accounts = app.data.driver.db['accounts']
		account = accounts.find_one({'token': token})
		if account and '_id' in account:
			self.set_request_auth_value(account['_id'])

		ret = check_token_validity(account['tokendate'])
		if ret == False:
			expired_token()
		
		return account


def gen_token_hash_pwd(documents):
	for document in documents:
		document["token"] = (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)))
		document["tokendate"] = datetime.now(timezone.utc)
		document["password"] = bcrypt.hashpw(document["password"], bcrypt.gensalt(10))
		

def check_token_validity(d1):
	d2 = datetime.now(timezone.utc)
	s = (d2-d1).seconds + (d2-d1).days * 86400
	m = round(s/60)
	#If token is older than a day (1440 minutes) => ERR(401)
	if m >= 1440:
		return False
			
				
if __name__ == '__main__':
	app = Eve(auth=RolesAuth)
	app.on_insert_accounts += gen_token_hash_pwd
	app.run()
	
	#DA CONTROLLARE!!!!!!!
	@app.errorhandler(401)
	def expired_token(err):
		return make_response("Token expired, please update it", 401)
