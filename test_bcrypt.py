import bcrypt

password = b"1234"

hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print(f'password: {password}')
print(f'hashed: {hashed}')

if bcrypt.checkpw(password, hashed):
    print("It matches!")
else:
    print("Didn't match")
