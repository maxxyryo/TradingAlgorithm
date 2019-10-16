from iqoptionapi.stable_api import IQ_Option
import  random, time, numpy, talib

api = IQ_Option("gacokambui@gmail.com", "Dodomans@001")
actives = "EURUSD"
print("Asset: " + actives)
while True:
	close, high, low, volume = [], [], [], []
	bars = api.get_candles(actives,5,500,time.time())

	for i in range(500):
		close.append(bars[i]['close'])
#		high.append(bars[i]['max'])
#		low.append(bars[i]['min'])
#		volume_float = float(bars[i]['volume'])
#		volume.append(volume_float)

	close_array = numpy.array(close)
#	high_array = numpy.array(high)
#	low_array = numpy.array(low)
#	volume_array = numpy.array(volume)
#
#	rsi_indicator = talib.RSI(close_array, timeperiod=14)
#	rsi = rsi_indicator[-1]
#
#	lr_indicator = talib.LINEARREG(close_array, timeperiod=14)
#	lr = lr_indicator[-1]
#
#	ppo_indicator = talib.PPO(close_array, fastperiod=12, slowperiod=26, matype=0)
#	ppo = ppo_indicator[-1]

#	ema_indicator = talib.EMA(close_array, timeperiod=30)
#	ema = round(float(ema_indicator[-1]), 5)

#	psar1_indicator = talib.SAR(high_array, low_array, acceleration = 0.02, maximum=0.2)
#	psar2_indicator = talib.SAR(high_array, low_array, acceleration = 0.04, maximum=0.2)
#	psar1 = round(float(psar1_indicator[-1]), 7)
#	psar2 = round(float(psar2_indicator[-1]), 7)

#	print("EMA: " + str(ema) + " Closing price: " + str(close[-1]) + " Diff: " + str((close[-1]-ema) * 1000000))
#	print("LR: " + str(lr) + " Closing price: " + str(close[-1]) + " Diff: " + str((lr-close[-1])*1000000))
#	print("PSAR1: " + str(psar1) + " PSAR2: " + str(psar2) + " Diff: " + str((psar2-psar1)*1000000))
#	print("PPO: " + str(ppo*1000) + " Closing price: " + str(close[-1]))

#	chaikin_indicator = talib.ADOSC(high_array, low_array, close_array, volume_array, fastperiod=3, slowperiod=10)
#	chaikin = chaikin_indicator[-1]
#	print(chaikin)

	macd_indicator, signal, hist = talib.MACD(close_array, fastperiod=12, slowperiod=26,signalperiod=9)
	print("MACD: " + str(macd_indicator[-1] * 1000))
	print("Signal: " + str(signal[-1]))
	print("Histogram: " + str(hist[-1]))

#	print(rsi)
#	time.sleep(5)

#buy_id = api.buy(1, actives, 'call', 1, force_buy = False)
#print(buy_id)
#g = api.get_betinfo(buy_id)
#print(g)
