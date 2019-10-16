#Dependancies
import logging, random, time, numpy, talib
from prettytable import PrettyTable
from iqoptionapi.stable_api import IQ_Option

logger = logging.getLogger()
logger.disabled = True
openAssets, actives = [], ''

#Login
api = IQ_Option("gacokambui@gmail.com", "Dodomans@001")
api.set_max_reconnect(5)
print("\nHello Mark. \nLogged in!")

#Set account
def setAccount():
	api.change_balance("PRACTICE")
	print("\nAccount type set to [PRACTICE]")
	print("Current balance is: ${:.2f}".format(api.get_balance()))

#Print available assets
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

#Get action whether buy or sell and asset
def getTradersMood():
	while True:
#		random.shuffle(openAssets)
		actives = random.choice(openAssets)
		api.start_mood_stream(actives)

		close, high, low = [], [], []
		bars = api.get_candles(actives,5,500,time.time())
		for i in range(500):
			close.append(bars[i]['close'])
			high.append(bars[i]['max'])
			low.append(bars[i]['min'])

		close_array = numpy.array(close)
		high_array = numpy.array(high)
		low_array = numpy.array(low)
		closing_price = round(float(close[-1]), 7)

		rsi_indicator = talib.RSI(close_array, timeperiod=14)
		rsi = int(rsi_indicator[-1])

		ema_indicator = talib.EMA(close_array, timeperiod=30)
		ema = round(float(ema_indicator[-1]), 2)

		psar1_indicator = talib.SAR(high_array, low_array, acceleration = 0.02, maximum = 0.2)
		psar2_indicator = talib.SAR(high_array, low_array, acceleration = 0.04, maximum = 0.2)
		psar1 = round(float(psar1_indicator[-1]), 7)
		psar2 = round(float(psar2_indicator[-1]), 7)

		ppo_indicator = talib.PPO(close_array, fastperiod=12, slowperiod=26, matype=0)
		ppo = float(ppo_indicator[-1])

		lr_indicator = talib.LINEARREG(close_array, timeperiod=14)
		lr = round(float(lr_indicator[-1]), 7)
		traders_sentiment = int(api.get_traders_mood(actives)*100)

#		weighted_action = 

		if ((rsi <= 25) and (traders_sentiment > 70)) and ((lr < closing_price) or (psar2 > psar1) or (ema < closing_price) or ppo > 0):
			action = "call"
			print("\nChosen: " + actives + "\nChoice: " + action)
			break
		elif ((rsi >= 75) and traders_sentiment < 30) and ((lr > closing_price) or (psar2 < psar1) or (ema > closing_price) or ppo <= 0):
			action = "put"
			print("\nChosen: " + actives + "\nChoice: " + action)
			break
		else:
			print()
			print(f'{"Asset: " + actives: <{14}}', end=' ')
			print(f'{"| Sentiment: " + str(traders_sentiment) + "%": <{18}}', end=' ')
			print(f'{"| LR: " + str(round(lr, 2)): <{12}}', end=' ')
			print(f'{"| RSI: " + str(rsi) + "%": <{8}}', end=' ')
#			print(f'{"| EMA: " + str(ema): <{15}}', end=' ')
#			print(f'{"| PSar1: " + str(round(psar1, 2)): <{19}}', end=' ')
			print(f'{"| PPO: " + str(round(ppo*1000, 2)): <{12}}', end=' ')
#			print(f'{"| PSar2: " + str(round(psar2, 2)): <{19}}', end=' ')
			print(f'{"| Not chosen |": <{8}}', end='')
			pass

	api.stop_mood_stream(actives)
	return action, actives, ema, rsi, psar1, psar2, ppo, traders_sentiment

def get_expiration_time(t):
	exp = time.time()
	if (exp % 60) > 30:
		end = exp - (exp % 60) + 60*(t+1)
	else:
		end = exp - (exp % 60) + 60*(t)
	return end

#Method to buy the asset and get trade outcome
def buy(cash):
	action, actives, ema, rsi, psar1, psar2, ppo, traders_sentiment = getTradersMood()
	exptime = 2
	buy_id = api.buy(cash, actives, action, exptime, force_buy = False)

	print("--------------------")
	print("Asset: " + actives)
	print("Amount: $" + str(cash))
	print("RSI: " + str(rsi))
	print("EMA: " + str(ema))
	print("PSar1: " + str(psar1) + " Psar2: " + str(psar2))
	print("PPO: " + str(ppo*1000))
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
	print("Outcome: " + outcome)
	time.sleep(2)
	print("Balance: ${:.2f}".format(api.get_balance()))
	print("******************")
	return outcome

#The Martingale function controlling the trade amount
def martingaleSystem(actives):
	money = 1
	outcomes = []
	while True:
		if api.check_connect == False:
			api.connect()
		try:
			out_come = buy(money)
			outcomes.append(out_come)
		except:
			out_come = buy(money)
			while out_come == None:
				print("Asset NOT Bought! Re-buing")
				out_come
				outcomes.append(out_come + "RE-BOUGHT")
		if out_come == "loose":
			money = money * 2.3
			money = round(money, 2)
			out_come
		elif out_come == "win":
			money = 1
			out_come
		else:
			out_come
		print(outcomes)

def onePercent():
	outcomes2 = []
	print("[1% Strategy] \n",sep=" ", end="", flush=True)
	while True:
		money = int(api.get_balance() * 0.01)
		outcome = buy(money)
		outcomes2.append(outcome)
		print(outcomes2)

if __name__ == '__main__':
	setAccount()
	listOpenAssets()
	martingaleSystem(actives)
#	onePercent()
