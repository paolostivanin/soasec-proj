from eve import Eve
from eve.auth import TokenAuth
import random
import string


class RolesAuth(TokenAuth):
	def check_auth(self, token, allowed_roles, resource, method):
		accounts = app.data.driver.db['accounts']
		account = accounts.find_one({'token': token})
		if account and '_id' in account:
			self.set_request_auth_value(account['_id'])
		#if allowed_roles:
			#only retrieve a user if his roles match ``allowed_roles``
		#	lookup['roles'] = {'$in': allowed_roles}
		#	account = accounts.find_one(lookup)
		
		return account


def add_token(documents):
     # Don't use this in production:
     # You should at least make sure that the token is unique.
     for document in documents:
         document["token"] = (''.join(random.choice(string.ascii_uppercase)
                                      for x in range(10)))

if __name__ == '__main__':
     app = Eve(auth=RolesAuth)
     app.on_insert_accounts += add_token
     app.run()
