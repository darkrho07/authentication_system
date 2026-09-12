import csv
import hashlib
import time
from datetime import datetime

try:
	with open("database.csv","r"):
		pass
except FileNotFoundError:
	with open("database.csv","w",newline="") as f:
		r = csv.writer(f)
		first_row = ["id","username","password","lastlogin","registerdate","message"]
		r.writerow(first_row)

div = "----------------------------------------------------"

def write_msg(username):
	print(div)
	msg = input("Enter your message or 000 for exit: ").strip()

	if msg == "000":
		return
	with open("database.csv","r",newline="") as f:
		rows = list(csv.reader(f))

	for row in rows:
		if row and row[1] == username:
			row[5] = msg
			print("Message stored Successfully")
			break

	with open("database.csv","w",newline="") as f:
		writer = csv.writer(f)
		writer.writerows(rows)

def check_username(username):
	with open("database.csv","r") as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			if row and row[1] == username:
				return True
	return False

def hash_pass(password):
	return hashlib.sha256(password.encode()).hexdigest()

def login():
	dpass = ""
	msg = ""
	print(div)
	print("Login into your account or type 000 to get back")

	while True:
		uname = input("Enter your username: ").lower().strip()
		if uname == "000":
			return
		pword = input("Enter your password: ").strip()

		with open("database.csv","r") as f:
			reader = csv.reader(f)
			next(reader,None)

			for row in reader:
				if row[1] == uname:
					dpass = row[2]
					msg = row[5]
					break

		if not check_username(uname) or dpass != hash_pass(pword):
			print("Username or Password is incorrect")
			return

		login_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		with open("database.csv","r",newline="") as f:
			rows = list(csv.reader(f))

		for row in rows:
			if row and row[1] == uname:
				row[3] = login_date
				break

		with open("database.csv","w",newline="") as f:
			writer = csv.writer(f)
			writer.writerows(rows)

		print("Login Successful")

		if msg == "":
			print("You don't have any message yet")
			write_msg(uname)
		else:
			print("Your message:")
			print(msg)
		return
		
def sign_up():
	print(div)
	print("Create a new account or type 000 to get back")

	while True:
		uname = input("Enter username: ").lower().strip()

		if uname == "000":
			return
		elif check_username(uname):
			print("Username Already Exists")
		else:
			break

	while True:
		pword = input("Enter your password: ").strip()
		cpword = input("Confirm your password: ").strip()

		if pword != cpword:
			print("Your password doesn't match. Please try again")
		else:
			break

	hash_pword = hash_pass(pword)
	reg_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	uid = int(time.time())

	new_user = [uid,uname,hash_pword,"Never",reg_date,""]

	with open("database.csv","a",newline="") as f:
		writer = csv.writer(f)
		writer.writerow(new_user)

	print("Account created Successfully")
	write_msg(uname)

def start():
	print(div)
	print("Authentication System")
	print("1.Sign Up")
	print("2.Login")
	print("3.Exit")

	choice1 = 0

	try:
		choice1 = int(input("What you want to do(in number) : ").strip())
	except ValueError:
		print("Invalid Input!")

	if choice1 == 1:
		sign_up()
	elif choice1 == 2:
		login()
	elif choice1 == 3:
		print("Exit Successfully")
		raise SystemExit
	else:
		print("Not in the option!")

while True:
	start()