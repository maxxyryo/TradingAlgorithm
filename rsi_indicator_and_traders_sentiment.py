import time, random, math, logging, talib, numpy
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime

logger = logging.getLogger()
logger.disabled = True

actives, action = '', ''
openAssets = []

print("***Hello Mark***")
print("\nLogging in...")
api = IQ_Option("gacokambui@gmail.com", "Dodomans@001")

print("Logged in!")
api.set_max_reconnect(5)

def setAccount():
	api.change_balance("PRACTICE")
	print("\nAccount type set to [PRACTICE]")
	print("Current balance is: ${:.2f}".format(api.get_balance())+ "\n")

def listOpenAssets():
	init_info = api.get_all_init()
	OP_code = api.get_all_ACTIVES_OPCODE()
	for key, value in OP_code.items():
		try:
			if init_info["result"]["turbo"]["actives"][str(OP_code[key])]["enabled"]==True:
				openAssets.append(key)
				print(key + " open")
			else:
				pass
		except KeyError:
			continue

def getTradersMood():
	while True:
		random.shuffle(openAssets)
		actives = random.choice(openAssets)
		api.start_mood_stream(actives)

		close = []
		bars = api.get_candles(actives,5,500,time.time())
		for i in range(500):
			close.append(bars[i]['close'])

		close_array = numpy.array(close)
		real = talib.RSI(close_array, timeperiod=14)
		rsi = int(real[-1])
		traders_sentiment = int(api.get_traders_mood(actives)*100)

		if traders_sentiment >= 60 and rsi <= 20:
			action = "call"
			print("\nBuying " + actives + " with choice: " + action + ". Defined.")
			api.stop_mood_stream(actives)
			break
		elif traders_sentiment <= 40 and rsi >= 80:
			action = "put"
			print("\nBuying " + actives + " with choice: " + action + ". Defined")
			api.stop_mood_stream(actives)
			break
	return action, actives, rsi, traders_sentiment
#		action = random.choice(['call', 'put'])
#		print("\nBuying " + actives + " with choice: " + action + ". Guessing")

#Expiration time
def get_expiration_time(t):
	exp = time.time()
	if (exp % 60) > 30:
		end = exp - (exp % 60) + 60*(t+1)
	else:
		end = exp - (exp % 60) + 60*(t)
	return end

def buy(cash):
	action, actives, rsi, traders_sentiment = getTradersMood()
	exptime = 2

	buy_id = api.buy(cash, actives, action, exptime, force_buy = False)
	print("--------------------")
	print("Asset: " + actives)
	print("Amount: $" + str(cash))
	print("RSI: " + str(rsi))
	print("Trader's Sentiment: " + str(traders_sentiment) + "%")
	print("Choice: " + action)
	print("--------------------")

	end_time = get_expiration_time(exptime)
	time_rem = round(end_time - time.time())
	for i in range(round(time_rem / 10)):
		print("Remaining time: ", end="", flush=True)
		print(str("{0:.2f} sec".format(time_rem)))
		time_rem -= 10
		time.sleep(10)

	outcome = api.check_win_v2(buy_id)
	print("\nOutcome: " + outcome)
	print("Balance: ${:.2f}".format(api.get_balance()))
	print("******************")
	return outcome

def martingaleSystem(actives):
	global openAssets
	money = 1
	outcomes = []
#	y = datetime.today()
#	out_come = buy(money)
	while True:
		if api.check_connect == False:
			api.connect()
		try:
			out_come = buy(money)
			outcomes.append(out_come)
		except:
			while buy_id == None:
				print("Asset NOT Bought!")
				out_come
				outcomes.append(out_come)
		print(outcomes)

		if out_come == "loose":
			money = money * 2.3
			money = round(money, 2)
			out_come
		elif out_come == "win":
			money = 1
			out_come

		else:
			out_come

#def runProgram():
#	listOpenAssets()
#	getTradersMood()
#	martingaleSystem(actives)

if __name__ == '__main__':
	setAccount()
	listOpenAssets()
	martingaleSystem(actives)


#	runProgram()
#	x = datetime.today()
#	try:
#		schedule.every().day.at("14:40").do(runProgram)
#	except:
#		print("Program crashed... Retrying")
#	while True:
#		schedule.run_pending()
#		time.sleep(30)
#		if schedule.run_pending() == False:
#			runProgram()
#		if x.hour == 16 and x.minute == 00:
#			break
