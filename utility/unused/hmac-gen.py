import hashlib
import hmac
import base64
from hashlib import sha1

userid = ""
secret_key = ""
payload = ''

key = bytes(secret_key, encoding='utf-8')
msg = bytes(payload, encoding='utf-8')

hm = hmac.new(key, msg, sha1).digest()

print("Authorization: " + userid + ":" + base64.b64encode(hm).decode())

