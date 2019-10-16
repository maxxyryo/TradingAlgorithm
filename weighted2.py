#Dependancies
import logging, random, time, numpy, talib
from prettytable import PrettyTable
from iqoptionapi.stable_api import IQ_Option
from twilio.rest import Client

openAssets, actives, action, outcomes = [], '', '', []

#Login
api = IQ_Option("gacokambui@gmail.com", "Dodomans@001")
api.set_max_reconnect(5)
print("\nHello Mark. \nLogged in!")

#Set account
def setAccount():
	api.change_balance("REAL")
	print("\nAccount type set to [REAL]")
	print("Current balance is: ${:.2f}".format(api.get_balance()))

#Print available assets
def listOpenAssets():
	init_info = api.get_all_init()
	OP_code = api.get_all_ACTIVES_OPCODE()

	x = PrettyTable()
	x.field_names, x.padding_width = ["Asset", "Profit Percentage","Status"], 1
	binary_info = api.get_all_profit()
	for key, value in OP_code.items():
		try:
			if init_info["result"]["turbo"]["actives"][str(OP_code[key])]["enabled"] == True:
				profit_percentage = int(binary_info[key]["turbo"] * 100)
				if profit_percentage >= 80:
					openAssets.append(key)
					x.add_row([key, str(profit_percentage) + "%", "open"])
			else:
				pass

		except KeyError:
			continue
	print(x)
	return openAssets

#Get action whether buy or sell and asset
def getTradersMood():
	while True:
		random.shuffle(openAssets)
		actives = random.choice(openAssets)
		binary_info = api.get_all_profit()
		profit_percentage = int(binary_info[actives]["turbo"] * 100)
		if profit_percentage < 80:
			print("\nStarting a fresh. Asset percentages changed.")
			listOpenAssets()
			random.shuffle(openAssets)
			actives = random.choice(openAssets)
		else:
			print("Checking for correct assets...")
			break

	close, high, low, volume = [], [], [], []
	try:
		bars = api.get_candles(actives,15,1000,time.time())
	except:
		print("Could not get candles. Retrying...")
		bars = api.get_candles(actives,15,1000,time.time())
	for i in range(1000):
		close.append(bars[i]['close'])
		high.append(bars[i]['max'])
		low.append(bars[i]['min'])
		volume_float = float(bars[i]['volume'])
		volume.append(volume_float)

	close_array = numpy.array(close)
	high_array = numpy.array(high)
	low_array = numpy.array(low)
	closing_price = round(float(close[-1]), 7)
	volume_array = numpy.array(volume)

	rsi_indicator = talib.RSI(close_array, timeperiod=14)
	rsi = int(rsi_indicator[-1])

	macd_indicator, signal, hist = talib.MACD(close_array, fastperiod=12, slowperiod=26,signalperiod=9)
	macd = (macd_indicator[-1] *1000)
	signals = (signal[-1] * 1000)
	histogram = (hist[-1] * 1000)

	ema_indicator = talib.EMA(close_array, timeperiod=30)
	ema = round(float(ema_indicator[-1]), 2)

	psar1_indicator = talib.SAR(high_array, low_array, acceleration = 0.02, maximum =0.2)
	psar2_indicator = talib.SAR(high_array, low_array, acceleration = 0.04, maximum =0.2)
	psar1 = round(float(psar1_indicator[-1]), 7)
	psar2 = round(float(psar2_indicator[-1]), 7)

	chaikin_indicator = talib.ADOSC(high_array, low_array, close_array, volume_array, fastperiod=3, slowperiod=10)
	chaikin = round(chaikin_indicator[-1] * 1000, 2)

	ppo_indicator = talib.PPO(close_array, fastperiod=12, slowperiod=26, matype=0)
	ppo = round((ppo_indicator[-1] * 1000), 4)

#	lr_indicator = talib.LINEARREG(close_array, timeperiod=14)
#	lr = round(float(lr_indicator[-1]), 7)
#	api.start_mood_stream(actives)
#	traders_sentiment = int(api.get_traders_mood(actives)*100)

	macd_trade = macd > 0 and signals > 0 and histogram > 0

#	if ema < closing_price and rsi >= 55 and ppo < 0:
	if rsi >= 55 and ppo >= 0 and psar2 > psar1 and macd_trade == True:
		action = "call"
		print("\nTrying: " + actives + " Profit Percentage: " + str(profit_percentage) + "%")
#	elif ema > closing_price and rsi <=45 and ppo > 0:
	elif rsi <= 45 and ppo <= 0 and psar2 < psar1 and macd_trade == False:
		action = "put"
		print("\nTrying: " + actives + " Profit Percentage: " + str(profit_percentage) + "%")
	else:
#		action = random.choice(["call","put"])
#		print("Chosen at random")
		return getTradersMood()

#	api.stop_mood_stream(actives)
	return action, actives, profit_percentage, rsi, ppo, macd, chaikin, psar1, psar2

def get_expiration_time(t):
	exp = time.time()
	if (exp % 60) > 30:
		end = exp - (exp % 60) + 60*(t+1)
	else:
		end = exp - (exp % 60) + 60*(t)
	return end

#Method to buy the asset and get trade outcome
def buy(cash):
#	previous_active = []
	try:
		action, actives, profit_percentage, rsi, ppo, macd, chaikin, psar1, psar2 = getTradersMood()
	except:
		action, actives, profit_percentage, rsi, ppo, macd, chaikin, psar1, psar2 = getTradersMood()
	exptime = 2
#	previous_active.append(actives)
#	if actives == previous_active[-1]:
#		action, actives, profit_percentage, rsi, ppo, macd, chaikin, traders_sentiment = getTradersMood()
	while True:
		print("Attempting to buy asset")
		buy_id = api.buy(cash, actives, action, exptime, force_buy = False)
		if isinstance(buy_id, int):
			print("Buy ID Captured!")
			break
		else:
			time.sleep(1.5)

	print("\n--------------------")
	print("Asset: " + actives)
	print("Amount: $" + str(cash))
	print("RSI: " + str(rsi) + "%")
#	print("EMA: " + str(ema))
	print("PSar1: " + str(psar1) + " Psar2: " + str(psar2))
	print("PPO: " + str(ppo))
	print("MACD: " + str(macd))
#	print("Trader's Sentiment: " + str(traders_sentiment) + "%")
	print("Chaikin Oscillator: " + str(chaikin))
	print("Choice: " + action)
	print("--------------------")

	end_time = get_expiration_time(exptime)
	time_rem = round(end_time - time.time())
	for i in range(round(time_rem / 10)):
		print("Remaining time: ", end="", flush=True)
		print(str("{0:.2f} sec".format(time_rem)))
		time_rem -= 10
		time.sleep(10)

	print("Done!")
	time.sleep(2)
	try:
		outcome = api.check_win_v2(buy_id)
	except:
		print("Error at getting the outcome for the trade. Exiting...")
		outcome = api.check_win_v2(buy_id)
	print("Outcome: " + outcome)
	time.sleep(2)
	print("Balance: ${:.2f}".format(api.get_balance()))
	print("******************")
	return outcome

#The Martingale function controlling the trade amount
def onePercent(actives):
	global outcomes, action
	money, last_active = 1, ["active1"]
	starting_balance = int(api.get_balance())
	accountSid = 'ACd40fb677edaf206f6ac8f70cda89de08'
	authToken = '4426a8b9a4b1c2819611669ddcc5c80c'
	client = Client(accountSid, authToken)

	while True:
		if api.check_connect == "False":
			api.connect()
			time.sleep(5)
		if last_active[-1] == actives:
			print("Same previous asset... Changing.")
			getTradersMood()
		out_come = buy(money)
		outcomes.append(out_come)
		balance = api.get_balance()
		delta_balance = int(balance - starting_balance)
		print("Total gain/loss: $" + str(delta_balance))
		print(outcomes)

		if outcomes[-2:] == ['loose', 'loose']:
			print("2 Losses incurred. Waiting for 1 min...")
			time.sleep(60)
			print("Randomizing action")
			action = random.choice(["call", "put"])
		out_come
		last_active.append(actives)
		if delta_balance >= 2:
			print("Done! Profit at " + str(delta_balance))
			print("Sending message...")
			myMessage = client.messages.create(body="$2", from_='+12624574265', to='+254717270977')
			print("Sent message")
			exit()

if __name__ == '__main__':
	setAccount()
	listOpenAssets()
	onePercent(actives)
