import time, getpass, logging, json
from iqoptionapi.stable_api import IQ_Option

email, password = '',''
logging.disable(level=logging.CRITICAL)

def printSlowly(string):
	for i in range(len(string)):
		print(string[i], sep="", end="", flush=True)
		time.sleep(0.2)
	print()

def greeting():
	global email, password
	print("\n  Greetings, what is your name?")
	name = input("  Input > ").upper()

	def printName(name):
		print("\n  ********" + "*" * len(name))
		fullName = ("   Hello " + name)
		printSlowly(fullName)
		print("  ********" + "*" * len(name))

	if name == "MARK" or name == "MARK GACOKA":
		email = "gacokambui@gmail.com"
		password = "Dodomans@001"
		printName(name)
		confirmStatus()

	with open('creds.json', 'r+') as json_file:
		data = json.load(json_file)
		print("  Checking locally...\n", end="", flush=True)
		for p in data['creds']:
			if (p['name']) == str(name.upper()):
				print("  Found!")
				email = p['email']
				password = p['password']
				printName(name)
				confirmStatus()
			else:
				print("\n  Not known. Please enter your credentials...")
				email = input("  Email: ")
				password = getpass.getpass("  Password: ")
				data = {}
				data['creds'] = []
				data['creds'].append({
					'name': name.upper(),
					'email': email,
					'password': password
				})

				with open('creds.json', 'a+') as filehandle:
					json.dump(data, filehandle)
				confirmStatus()

def confirmStatus():
	print("\n  Logging in with the credentials given", end="", flush=False)
	dots = [".",".","."]
	printSlowly(dots)
	try:
		api = IQ_Option(email.strip('\"'), password.strip('\"'))
	except:
		print("  Invalid Credentials")
		exit()

	time.sleep(1)
	print("  Logged in!\n")
	print("  Choose account mode: \n  1. PRACTICE ACCOUNT\n  2. REAL ACCOUNT\n  3. EXIT")
	mode = int(input("  Input > "))

	if mode == 1:
		api.change_balance("PRACTICE")
		print("\n  Account type set to [PRACTICE]")
	elif mode == 2:
		api.change_balance("REAL")
		print("\n  Account type set to [REAL]")
	elif mode == 3:
		print("\n  Exiting...")
		exit()
	else:
		while mode == 1 or mode == 2 or mode == 3:
			print("   Wrong [MODE]. Try again")

	print("  BALANCE: **", end="", flush=True)
	print(api.get_balance(), end="", flush=True)
	print("**")

if __name__ == '__main__':
	greeting()

