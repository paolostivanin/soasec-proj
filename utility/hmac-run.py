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


class MyHMACAuth(HMACAuth):
	def check_auth(self, userid, hmac_hash, headers, data, allowed_roles, resource, method):
		accounts = app.data.driver.db['accounts']
		user = accounts.find_one({'username': userid})
		if user and '_id' in user:
			secret_key = user['secret_key']
			self.set_request_auth_value(user['_id'])
		
		# in this implementation we only hash request data, ignoring the headers.
		hm = hmac.new(bytes(secret_key, encoding='utf-8'), data, sha1).digest()
		
		return user and base64.b64encode(hm).decode() == hmac_hash
