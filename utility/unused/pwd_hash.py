import bcrypt

password = 'paolo'

pwd_hash = bcrypt.hashpw(password, bcrypt.gensalt(10))
#hashed = ''

print(pwd_hash)
'''if bcrypt.hashpw(password, hashed) == hashed:
	print("It matches")
else:
	print("No matches :(")
'''
