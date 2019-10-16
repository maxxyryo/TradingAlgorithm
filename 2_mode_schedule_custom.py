import time, random, math, logging, schedule
from iqoptionapi.stable_api import IQ_Option
from prettytable import PrettyTable
from datetime import datetime

logger = logging.getLogger()
logger.disabled = True

actives = ''
openAssets = []

print("***Hello Mark***")
print("\nLogging in...")
api = IQ_Option("gacokambui@gmail.com", "Dodomans@001")

api.set_max_reconnect(5)
connect = api.check_connect()
print(connect)

print("Logged in!")

def setAccount():
	api.change_balance("PRACTICE")
	print("\nAccount type set to [PRACTICE]")
	print("Current balance is: ${:.2f}".format(api.get_balance()))

def listOpenAssets():
	init_info = api.get_all_init()
	OP_code = api.get_all_ACTIVES_OPCODE()
	x = PrettyTable()
	x.field_names, x.padding_width = ["Asset","Status"], 4
	for key, value in OP_code.items():
		try:
			if init_info["result"]["turbo"]["actives"][str(OP_code[key])]["enabled"]==True:
				openAssets.append(key)
				x.add_row([key, "open"])
			else:
				pass
		except KeyError:
			continue
	print(x)

def getTradersMood():
	global actives
	api.start_mood_stream(actives)
	if int(api.get_traders_mood(actives)) > 0.70:
		action = "call"
	elif int(api.get_traders_mood(actives)) < 0.30:
		action = "put"
	else:
		random.choice(openAssets)

	api.stop_mood_stream(actives)
	return action

def get_expiration_time(t):
	exp = time.time()
	if (exp % 60) > 30:
		end = exp - (exp % 60) + 60*(t+1)
	else:
		end = exp - (exp % 60) + 60*(t)
	return end

def buy(cash):
	action = getTradersMood()
	exptime = 1
	print("\nBuying " + actives + " with choice: " + action + ". ", end="")
	try:
		buy_id = api.buy(cash, actives, action, exptime, force_buy = False)
		print("Bought asset")
		print("--------------------")
		print("Asset: " + actives)
		print("Amount: $" + str(cash))
		print("Trader's Sentiment: ", end="")
		print(api.get_traders_mood(actives))
		print("Choice: " + action)
		print("--------------------")
	except:
		while buy_id == None:
			buy_id = api.buy(cash, actives, action, exptime, force_buy = False)

	end_time = get_expiration_time(exptime)
	time_rem = round(end_time - time.time())
	for i in range(round(time_rem / 10)):
		print("Remaining time: ", end="", flush=True)
		print(str("{0:.2f} sec".format(time_rem)))
		time_rem -= 10
		time.sleep(10)
	ifTrue, none = api.get_betinfo(buy_id)

	if ifTrue == "False":
		print("No outcome")
	else:
		print("\nOutcome: ", end=' ')
	outcome = api.check_win_v2(buy_id)
	print(outcome)
	balance = int(api.get_balance())
	print("Balance: ${:.2f}".format(balance))
	print("******************")
	return outcome

def martingaleSystem():
	global actives, openAssets, balance
	money, balance = 1, int(api.get_balance())
	x = datetime.today()
	while x.hour != 16 and x.minute != 0:
		schedule.run_pending()
		if int(api.get_balance()) >= (balance +50):
			break
		out_come = buy(money)
		if out_come == "loose":
			money = money * 2.3
			out_come
		elif out_come == "win":
			money = 1
			out_come
		else:
			out_come

def onePercent():
	global actives, openAssets
	while True:
		random.shuffle(openAssets)
		actives = random.choice(openAssets)
		balance = int(api.get_balance())
		out_come = buy(balance * 0.01)

if __name__ == '__main__':
	setAccount()
	listOpenAssets()
	actives = random.choice(openAssets)
	getTradersMood()

	print("\nChoose the desired strategy.\n  1. Martingale Strategy\n  2. 1% strategy")
	strategy = int(input("  Input > "))

	try:
		if int(strategy) == 1:
			martingaleSystem()
		else:
			onePercent()
	except:
		print("Wrong option!")

	schedule.every().day.at("17:36").do(martingaleSystem())
