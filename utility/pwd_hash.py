import bcrypt

password = 'paolo'

#pwd_hash = bcrypt.hashpw(password, bcrypt.gensalt(10))
hashed = '$2a$10$kiYIJnKZsCG5GKyxgaZEdeVgPW2J/n1sWWJx.iI9uzcJd0u.NPeEa'

#print(pwd_hash)
if bcrypt.hashpw(password, hashed) == hashed:
	print("It matches")
else:
	print("No matches :(")

