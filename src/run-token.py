from eve import Eve
from eve.auth import TokenAuth
import bcrypt

class RolesAuth(TokenAuth):
	def check_auth(self, token, allowed_roles, resource, method):
		accounts = app.data.driver.db['accounts']
		account = accounts.find_one({'token': token})
		if account and '_id' in account:
			self.set_request_auth_value(account['_id'])

		return account


def add_token(documents):
     # Don't use this in production:
     # You should at least make sure that the token is unique.
     for document in documents:
	     document["token"] = None
	     document["password"] = bcrypt.hashpw(document["password"], bcrypt.gensalt(16))


if __name__ == '__main__':
     app = Eve(auth=RolesAuth)
     app.on_insert_accounts += add_token
     app.run()
