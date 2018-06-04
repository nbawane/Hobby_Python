#TO get prices of all the cryptos from all exchanges

import requests
import threading
import json
#********************Tickers**********************#

COINDELTA = r'https://coindelta.com/api/v1/public/getticker/'
COINSECURE = r'https://api.coinsecure.in/v1/exchange/ticker'
KOINEX = r'https://koinex.in/api/ticker'
ZEBPAY = 'https://www.zebapi.com/api/v1/market/ticker-new/{}/inr'   #zebpay has individual API for each currency,need to use format to construct API
UNOCOIN = r'https://www.unocoin.com/api/v1/general/prices'
BUYUCOIN = r'https://www.buyucoin.com/api/v1.2/currency/markets'#ETH,XRP end of extension
ETHEXINDIA = r'https://ethexindia.com/api/ticker'
POCKETBITS = 'https://pocketbits.in/api/ticker'
COINOME = r'https://www.coinome.com/api/v1/ticker.json'
BITBNS = r'https://bitbns.com/order/getTickerWithVolume/'
#**************TIcker ends**********************#

class Extractprice:
	def __init__(self):
		# self.allexchange = self.get_all_exchange()
		#default values
		self.universal_dict={'BTC': {'Sell': '0', 'Buy': '0'}, 'ETH': {'Sell':'0', 'Buy': '0'}, 'LTC': {'Sell': '0', 'Buy': '0'}, 'OMG': {'Sell': '0', 'Buy': '0'}, 'QTUM': {'Sell': '0', 'Buy': '0'}, 'XRP': {'Sell': '0', 'Buy': '0'}, 'BCH': {'Sell': '0', 'Buy': '0'}\
			} #'CLOAK': {'Sell': '838.00', 'Buy': '1100.00'}, 'CVC': {'Sell': '19.13', 'Buy': '24.29'}, 'DASH': {'Sell': '36972.00', 'Buy': '39433.00'}, 'DGB': {'Sell': '1.95', 'Buy': '2.26'}, 'DOGE': {'Sell': '0.25', 'Buy': '0.37'}, 'ETC': {'Sell': '1433.00', 'Buy': '1860.00'}, 'FCT': {'Sell': '1742.00', 'Buy': '2204.00'}, 'GNT': {'Sell': '26.39', 'Buy': '29.77'}, 'LSK': {'Sell': '976.00', 'Buy': '1224.00'}, 'NEO': {'Sell': '6028.00', 'Buy': '7684.00'}, 'NXT': {'Sell': '10.35', 'Buy': '14.36'}, 'PAY': {'Sell': '100.00', 'Buy': '132.00'}, 'PIVX': {'Sell': '330.00', 'Buy': '418.00'}, 'REP': {'Sell': '2599.00', 'Buy': '3250.00'}, 'SC': {'Sell': '1.04', 'Buy': '1.43'}, 'STEEM': {'Sell': '185.00', 'Buy': '237.00'}, 'STRAT': {'Sell': '414.00', 'Buy': '532.00'}, 'XEM': {'Sell': '18.77', 'Buy': '24.03'}, 'XMR': {'Sell': '20635.00', 'Buy': '24975.00'}, 'ZEC': {'Sell': '24450.50', 'Buy': '26147.06'}, 'MIOTA': {'Sell': '109.66', 'Buy': '109.66'}, 'TRX': {'Sell': '2.87', 'Buy': '2.87'}, 'AE': {'Sell': '144.95', 'Buy': '142.51'}, 'ZRX': {'Sell': '54.49', 'Buy': '54.01'}, 'REQ': {'Sell': '17.55', 'Buy': '17.50'}
							  #}
		# self.universal_dict = self.coindelta
	# 	pub.subscribe(self.get_connection_error,'ConnectionError')
	#
	# def get_connection_error(self):
	# 	#print('[ CoinsWatch ] I got connection error')
	# 	pub.sendMessage('ConErrScreen')
	# 	pub.unsubscribe(self.get_connection_error,'ConnectionError')

	def get_prices(self):
		'''

		:return:prices of all the currency from all the exchanges
		'''
		self.bitbns = {}
		self.coindelta = {}
		self.zebpay = {}
		self.coinome = {}
		self.coinsecure = {}
		self.koinex = {}
		self.pocketbits = {}
		self.buyucoin={}
		self.unocoin = {}

		coindeltathread = threading.Thread(target=self.get_coindelta_prices)
		zebpaythread = threading.Thread(target = self.get_zebpay_prices)
		coinomethread = threading.Thread(target=self.get_coinome_prices)
		coinsecurethread = threading.Thread(target=self.get_coinsecure_prices)
		koinexthread = threading.Thread(target=self.get_koinex_prices)
		pocketbitsthread = threading.Thread(target=self.get_pocketbits_prices)
		bitbnsthread = threading.Thread(target=self.get_bitbns_prices)
		unocointhread = threading.Thread(target=self.get_unocoin_prices)
		buyucointhread = threading.Thread(target=self.get_buyucoin_prices)

		coindeltathread.start()
		zebpaythread.start()
		coinomethread.start()
		coinsecurethread.start()
		koinexthread.start()
		pocketbitsthread.start()
		bitbnsthread.start()
		unocointhread.start()
		buyucointhread.start()

		coindeltathread.join()
		zebpaythread.join()
		coinomethread.join()
		coinsecurethread.join()
		koinexthread.join()
		pocketbitsthread.join()
		bitbnsthread.join()
		unocointhread.join()
		buyucointhread.join()
		#joining threads before all main thread executes
		#so as all threads finish fetching get_avg_prices starts
		self.universal_dict_updated = self.get_avg_prices(self.coindelta,self.zebpay,self.buyucoin,\
												self.coinome,self.coinsecure,self.unocoin,\
												  self.koinex,self.pocketbits,self.bitbns)    #this would contain avg of all the buy/sells of coins
		#print(self.universal_dict_updated)
		return self.universal_dict_updated

	def get_ethexindia_prices(self):
		'''
		discarded as of now
		:return:
		'''
		try:
			req1 = requests.get(ETHEXINDIA)
			#print(req1)
			if req1.status_code !=200:
				self.pocketbits = {}
				return
		except:
			# pub.sendMessage('ConnectionError')
			return
		data = req1.json()
		ethexindiadict = {}
		ethexindiadict['ETH'] = data['last_traded_price']
		return ethexindiadict

	def get_pocketbits_prices(self):
		#print('[ CoinsWatch ] op pocketbits')
		self.pocketbits = {}	#create empty dictionary to be pass to avg price calculation
		try:
			req1 = requests.get(POCKETBITS)	#requests for data
			#print('[ CoinsWatch ] pocketbits request %s'%req1)	###print current request status
			if req1.status_code !=200:	#check if request succeed
				#print('[ CoinsWatch ] pocketbits req status %s'%req1.status_code)	#if not #print status
				return self.pocketbits	#return
		except requests.exceptions.ConnectionError as e:
			# pub.sendMessage('ConnectionError')
			#print('[ CoinsWatch ] pocketbits %s'%e)
			return
		data = req1.json()
		#print('[ CoinsWatch ] pocketbits data %s'%data)
		pocketbitsdict = {}
		pocketbitsdict['BTC']={'Buy':data['buy'],'Sell':data['sell']}
		self.pocketbits=pocketbitsdict
		#print('[ CoinsWatch ] pocketbits %s'%pocketbitsdict)
		return pocketbitsdict

	def get_coinome_prices(self):
		#print('[ CoinsWatch ] op coinome')
		self.coinome = {}
		try:
			req1 = requests.get(COINOME)
			#print('[ CoinsWatch ] coinome request %s'%req1)
			if req1.status_code !=200:
				#print('[ CoinsWatch ] coinome req status %s' % req1.status_code)
				return self.coinome
		except Exception as e:
			# pub.sendMessage('ConnectionError')
			#print('[ CoinsWatch ] coinome %s'%e)
			return
		data = req1.json()


		#print('[ CoinsWatch ] coinome data %s' % data)
		coinomedict = {}
		for coin in data:
			cdata=data[coin]
			if coin.split('-')[1].lower()=='btc':
				continue
			coinomedict[coin.split('-')[0].upper()]={'Last':cdata['last'], 'Sell':cdata['lowest_ask'], 'Buy':cdata['highest_bid']}
		self.coinome = coinomedict
		#print('[ CoinsWatch ] coinome %s'%coinomedict)
		return coinomedict

	def get_buyucoin_prices(self):
		print('[ CoinsWatch ] op buyucoin')
		self.buyucoin = {}
		from kivy.utils import platform
		import json
		if platform == "android":
			from jnius import autoclass, cast
			print('hitting class')
			Test = autoclass('JavaUrlConnectionReader')
			print('hitting done')
			data1 = Test.getUrlContents('https://www.buyucoin.com/api/v1.2/currency/markets')
			#print('########################data %s  #######type %s' % (data1, type(data1)))
			buyudata = json.loads(data1)	#convert string to dict
			print('########################price extractor json data %s  #######type %s' % (buyudata, type(buyudata)))
			#data = buyudata['data']
		else:
			print("Non Android buyucoin")
			try:
				req1 = requests.get(BUYUCOIN)
				#print('[ CoinsWatch ] buyucoin req %s'%req1)
				if req1.status_code !=200:
					#print('[ CoinsWatch ] buyucoin req status %s' % req1.status_code)  # if not #print status
					return
			except Exception as e:
				# pub.sendMessage('ConnectionError')
				#print('[ CoinsWatch ] buyucoin %s'%e)
				return
			buyudata = req1.json()
		#print('[ CoinsWatch ] buyucoin data %s'%buyudata)
		buyucoinprice={}
		data = buyudata['data']
		coin = None
		for key in data:
			coin = str(key.split('_')[0].upper())
			if coin is None or coin not in buyucoinprice.keys():
				temp_coin = coin
				buyucoinprice[coin] = {}

				buyucoinprice[coin].update({'Sell': data[key]['ask']})
				buyucoinprice[coin].update({'Buy': data[key]['bid']})
		self.buyucoin = buyucoinprice
		print('[ CoinsWatch ] buyucoin %s'%self.buyucoin)
		return buyucoinprice

		# {'data': {'ark_inr': {'ask': 430.0, 'bid': 201.0, 'change': '0.73', 'high_24': '450.0000', 'last_trade': '430.0000', 'low_24': '201.0000', 'vol': 120.99554168}, 'bat_inr': {'ask': 28.0, 'bid': 27.0, 'change': '0.80', 'high_24': '27.0000', 'last_trade': '27.0000', 'low_24': '15.0000', 'vol': 14785.61923419}, 'bcc_inr': {'ask': 75000.0, 'bid': 60000.0, 'change': '0.00', 'high_24': '0.0000', 'last_trade': '0.0000', 'low_24': '0.0000', 'vol': 0.74235289}, 'btc_inr': {'ask': 650000.0, 'bid': 630000.0, 'change': '-0.15', 'high_24': '750000.0000', 'last_trade': '650000.0000', 'low_24': '650000.0000', 'vol': 4.54359035}, 'bts_inr': {'ask': 14.6, 'bid': 9.0, 'change': '-0.17', 'high_24': '17.0000', 'last_trade': '14.5000', 'low_24': '14.5000', 'vol': 38455.91054868}, 'cloak_inr': {'ask': 980.0, 'bid': 300.0, 'change': '0.00', 'high_24': '0.0000', 'last_trade': '0.0000', 'low_24': '0.0000', 'vol': 20.05982954}, 'cvc_inr': {'ask': 41.94, 'bid': 21.5, 'change': '-0.30', 'high_24': '43.0000', 'last_trade': '32.9500', 'low_24': '32.9500', 'vol': 5260.75119675}, 'dash_inr': {'ask': 35000.0, 'bid': 29000.0, 'change': '0.07', 'high_24': '29001.0000', 'last_trade': '28900.0000', 'low_24': '26900.0000', 'vol': 8.95286306}, 'dcn_inr': {'ask': 0.061, 'bid': 0.059, 'change': '-0.13', 'high_24': '0.0690', 'last_trade': '0.0610', 'low_24': '0.0500', 'vol': 5632921.3046025}, 'dgb_inr': {'ask': 2.45, 'bid': 2.0099, 'change': '-0.01', 'high_24': '2.4500', 'last_trade': '2.4300', 'low_24': '2.4300', 'vol': 99935.25015026}, 'doge_inr': {'ask': 0.369, 'bid': 0.26, 'change': '-0.00', 'high_24': '0.3700', 'last_trade': '0.3690', 'low_24': '0.3000', 'vol': 1103907.56928447}, 'etc_inr': {'ask': 2100.0, 'bid': 1000.0, 'change': '-1.30', 'high_24': '2299.0000', 'last_trade': '1000.0000', 'low_24': '1000.0000', 'vol': 55.15513759}, 'eth_inr': {'ask': 61450.0, 'bid': 47000.0, 'change': '0.06', 'high_24': '63000.0000', 'last_trade': '61500.0000', 'low_24': '58000.0000', 'vol': 5.99816716}, 'fct_inr': {'ask': 2369.0, 'bid': 852.0, 'change': '0.00', 'high_24': '0.0000', 'last_trade': '0.0000', 'low_24': '0.0000', 'vol': 32.99092895}, 'gnt_inr': {'ask': 27.0, 'bid': 23.21, 'change': '0.00', 'high_24': '23.2100', 'last_trade': '23.2100', 'low_24': '23.2100', 'vol': 5048.1617453}, 'lsk_inr': {'ask': 1298.0, 'bid': 600.0, 'change': '0.00', 'high_24': '0.0000', 'last_trade': '0.0000', 'low_24': '0.0000', 'vol': 41.78172792}, 'ltc_inr': {'ask': 10800.0, 'bid': 10700.0, 'change': '-0.12', 'high_24': '13900.0000', 'last_trade': '10800.0000', 'low_24': '10626.0000', 'vol': 70.7605844}, 'neo_inr': {'ask': 7800.0, 'bid': 5023.0, 'change': '0.20', 'high_24': '8000.0000', 'last_trade': '6000.0000', 'low_24': '5001.0000', 'vol': 14.22618999}, 'nxt_inr': {'ask': 15.2, 'bid': 14.4, 'change': '-0.06', 'high_24': '15.2000', 'last_trade': '14.4000', 'low_24': '14.4000', 'vol': 11282.67081922}, 'omg_inr': {'ask': 1050.0, 'bid': 571.0, 'change': '0.12', 'high_24': '1050.0000', 'last_trade': '571.0000', 'low_24': '510.0000', 'vol': 85.44756566}, 'pay_inr': {'ask': 168.0, 'bid': 98.0, 'change': '0.73', 'high_24': '168.0000', 'last_trade': '168.0000', 'low_24': '97.0000', 'vol': 1374.35617296}, 'pivx_inr': {'ask': 598.0, 'bid': 201.0, 'change': '0.32', 'high_24': '599.0000', 'last_trade': '599.0000', 'low_24': '454.0000', 'vol': 659.10091698}, 'qtum_inr': {'ask': 1407.0, 'bid': 1300.0, 'change': '-0.01', 'high_24': '1427.0000', 'last_trade': '1407.0000', 'low_24': '1407.0000', 'vol': 15.08515787}, 'rep_inr': {'ask': 13000.0, 'bid': 3200.0, 'change': '3.44', 'high_24': '14015.0000', 'last_trade': '14000.0000', 'low_24': '3153.0000', 'vol': 3.69469133}, 'sc_inr': {'ask': 1.84, 'bid': 1.43, 'change': '-0.02', 'high_24': '1.8900', 'last_trade': '1.8400', 'low_24': '1.4000', 'vol': 310966.14459882}, 'steem_inr': {'ask': 261.0, 'bid': 210.0, 'change': '0.30', 'high_24': '261.0000', 'last_trade': '261.0000', 'low_24': '200.0000', 'vol': 391.36347227}, 'strat_inr': {'ask': 460.0, 'bid': 300.0, 'change': '0.00', 'high_24': '0.0000', 'last_trade': '0.0000', 'low_24': '0.0000', 'vol': 36.7177564}, 'xem_inr': {'ask': 37.0, 'bid': 20.5, 'change': '0.50', 'high_24': '36.0000', 'last_trade': '36.0000', 'low_24': '24.0000', 'vol': 9216.51092249}, 'xmr_inr': {'ask': 29000.0, 'bid': 20997.0, 'change': '-0.38', 'high_24': '29000.0000', 'last_trade': '20997.0000', 'low_24': '20997.0000', 'vol': 5.76970064}, 'xrp_inr': {'ask': 57.0, 'bid': 55.0, 'change': '-0.04', 'high_24': '59.0000', 'last_trade': '57.0000', 'low_24': '55.0000', 'vol': 19125.69904052}, 'zec_inr': {'ask': 21950.0, 'bid': 16400.0, 'change': '0.05', 'high_24': '21950.0000', 'last_trade': '21950.0000', 'low_24': '21000.0000', 'vol': 34.8470821}}, 'success': 'True'}

	def get_coindelta_prices(self):
		'''
		This should have ask/bid pattern
		returns dictionary of coin and current price
		dictionary format :{COIN_NAME_IN_CAP : price in INR}
		'''

		#print('[ CoinsWatch ] op coindelta')
		self.coindelta = {}
		try:
			req1 = requests.get(COINDELTA)
			#print('[ CoinsWatch ] Coindelta request %s' % req1)  # #print current request status
			#print('[ CoinsWatch ] Coindelta %s'%req1)
			if req1.status_code !=200:
				#print('[ CoinsWatch ] coindelta req status %s' % req1.status_code)  # if not #print status
				return self.coindelta
		except Exception as e:
			# pub.sendMessage('ConnectionError')
			#print('[ CoinsWatch ] coindelta %s'%e)
			return
		data = req1.json()
		coindeltadict = {}
		for fields in data :
			if 'inr' in (fields['MarketName']):
				coindeltadict[(fields['MarketName'].split('-')[0]).upper()] = {'Last':fields['Last'],'Sell':fields['Ask'],'Buy':fields['Bid']}
		self.coindelta = coindeltadict
		#print('[ CoinsWatch ] coindelta '%coindeltadict)
		return coindeltadict
		# temp_list={}
		# temp_list = {'BTC': {'Last': 708004.02, 'Sell': 712396.9, 'Buy': 708501.0}, 'ETH': {'Last': 62898.0, 'Sell': 62898.0, 'Buy': 62640.0}, 'LTC': {'Last': 14898.0, 'Sell': 14850.0, 'Buy': 14800.0}, 'OMG': {'Last': 1175.0, 'Sell': 1175.0, 'Buy': 1174.0}, 'QTUM': {'Last': 2123.99, 'Sell': 2123.99, 'Buy': 2110.1}, 'XRP': {'Last': 75.72, 'Sell': 75.8, 'Buy': 75.79}, 'BCH': {'Last': 99697.99, 'Sell': 99697.99, 'Buy': 99202.0}}
		# return temp_list

	def get_zebpay_prices(self):
		#print('[ CoinsWatch ] op zebpay')
		self.zebpay = {}
		zebpaydict = {}
		coins = ['btc','ltc','xrp','bch','eth']
		for coin in coins:
			zebpayreq = ZEBPAY.format(coin)
			try:
				req1 = requests.get(zebpayreq)
				#print('[ CoinsWatch ] zebpay req %s'%req1)
				if req1.status_code != 200:
					#print('[ CoinsWatch ] zebpay req status %s' % req1.status_code)  # if not #print status
					return self.zebpay
			except Exception as e:
				# pub.sendMessage('ConnectionError')
				#print('[ CoinsWatch ] zebpay %s'%e)
				return
			data = req1.json()
			zebpaydict[data['virtualCurrency'].upper()]={'Sell':data['sell'],'Buy':data['buy']}
		self.zebpay = zebpaydict
		#print('[ CoinsWatch ] zebpay %s'%zebpaydict)
		return zebpaydict
		# temp_testing = {
		#                 'BTC':{'Sell':'900000','Buy':'899999'},\
		#                 'LTC':{'Sell':'14500','Buy':'17000'},\
		#                 'XRP':{'Sell':'30','Buy':'33'}
		#                }
		# return temp_testing

	def get_unocoin_prices(self):
		# The following Unocoin client id and secret only have access for prices
		self.client_id = "PXOHP8NOXL"
		self.client_secret = "1c1d44de-9323-491b-a01e-c1d021fc182a"
		self.URL = "https://www.unocoin.com/trade?all"
		self.prices_URL = "https://www.unocoin.com/api/v1/general/prices"
		self.auth_URL = "https://www.unocoin.com/oauth/token"
		self.title = "\033[94mUnocoin CryptoCurrency Rates\033[0m"
		self.supported_cryptos = {
			"BTC": "BitCoin"
		}
		unocoindict = {}

		def get_unocoin_access_token():
			"""Get Unocoin Access token"""
			payload = {
				"grant_type": "client_credentials",
				"access_lifetime": "30"
			}
			resp = requests.post(self.auth_URL, data=payload, auth=(self.client_id, self.client_secret))
			respj = resp.json()

			return respj['access_token']

		def get_unocoin_rates(crypto_curr='ALL'):
			print("\033[37mWait for it ...\033[0m")
			access_token = get_unocoin_access_token()
			if crypto_curr is None:
				crypto_curr = "ALL"
			try:
				authorization = "Bearer {}".format(access_token)
				headers = {
					"Content-Type": "application/json",
					"Authorization": authorization
				}
				response = requests.post(self.prices_URL, headers=headers)
			except Exception as e:
				print(response.status_code, response.text, type(e).__name__)
				return
			if response and response.status_code == 200:
				return response

		req1 = get_unocoin_rates()
		data = req1.json()
		unocoindict['BTC'] = {'Sell':data['sellbtc'], 'Buy':data['buybtc']}
		self.unocoin = unocoindict
		return unocoindict

	def get_koinex_prices(self):
		'''
		returns dictionary of coin and current price
		dictionary format :{COIN_NAME_IN_CAP : price in INR
		stats doesnot have all the coins hence sell and buy prices are kept same
		'''
		#print('[ CoinsWatch ] op koinex')
		self.koinex = {}
		try:
			req1 = requests.get(KOINEX)
			#print('[ CoinsWatch ] koinex request %s'%req1)	###print current request status
			#print(req1)
			if req1.status_code != 200:
				#print('[ CoinsWatch ] koinex req status %s'%req1.status_code)	#if not #print status
				return self.koinex
		except Exception as e:
			#print('[ CoinsWatch ] koinex %s'%e)
			return {}
		data = req1.json()
		#print('[ CoinsWatch ] koinex data %s'%data)
		koinexdict = data['prices']

		for coin in koinexdict:
			try:
				koinexstat = data['stats'][coin]
				koinexdict[coin]=({'Last':koinexdict[coin],'Sell':koinexstat['lowest_ask'],'Buy':koinexstat['highest_bid']})
			except KeyError:
				koinexdict[coin] = (
				{'Last': koinexdict[coin], 'Sell': koinexdict[coin], 'Buy':koinexdict[coin]})
		#print('[ CoinsWatch ] koinex %s'%koinexdict)
		self.koinex = koinexdict
		return koinexdict
		# return {'BTC': '691001.0', 'ETH': '62300.0', 'XRP': '75.05', 'BCH': '99500.0', 'LTC': '14550.0', 'MIOTA': 139.44, 'OMG': 1151.39, 'GNT': 30.62}

	def get_coinsecure_prices(self):
		'''
		returns dictionary of coin and current price
		dictionary format :{COIN_NAME_IN_CAP : price in INR}
		'''
		#print('[ CoinsWatch ] coinsecure')
		self.coinsecure = {}
		try:
			req1 = requests.get(COINSECURE)
			#print('[ CoinsWatch ] coinsecure request %s'%req1)	###print current request status
			if req1.status_code !=200:
				#print('[ CoinsWatch ] coinsecure req status %s'%req1.status_code)	#if not #print status
				return self.coinsecure
		except Exception as e:
			# pub.sendMessage('ConnectionError')
			#print('[ CoinsWatch ] coinsecure %s'%e)
			return
		data = req1.json()
		#print('[ CoinsWatch ] coinsecure data %s'%data)
		coinsecuredict = {}
		coinsecuredict['BTC'] = {'Last':data['message']['lastPrice']/100, 'Sell':data['message']['ask']/100, 'Buy':data['message']['bid']/100}
		#print('[ CoinsWatch ] coinsecure '%coinsecuredict)
		self.coinsecure = coinsecuredict
		return coinsecuredict

	def get_bitbns_prices(self):
		'''
		returns dictionary of coin and current price
		dictionary format :{COIN_NAME_IN_CAP : price in INR}
		'''

		self.bitbns = {}
		try:
			req1 = requests.get(BITBNS)
			#print('[ CoinsWatch ] coinsecure request %s'%req1)	###print current request status
			if req1.status_code !=200:
				#print('[ CoinsWatch ] coinsecure req status %s'%req1.status_code)	#if not #print status
				return self.bitbns
		except Exception as e:
			# pub.sendMessage('ConnectionError')
			#print('[ CoinsWatch ] coinsecure %s'%e)
			return
		data = req1.json()
		#print('[ CoinsWatch ] coinsecure data %s'%data)
		bitbnsdict = {}
		for coin in data:
			bitbnsdict[coin] = {'Sell': data[coin]['lowest_sell_bid'], 'Buy': data[coin]['highest_buy_bid']}
#		print('[ CoinsWatch ] bitbns '%bitbnsdict)
		self.bitbns = bitbnsdict
		return bitbnsdict


	def get_all_coins(self,*args):
		'''
		args:
		:return:list of all coins
		'''
		coindata = {}
		for coindict in args:
			#updating the dictionary of coins, as there can be only one key ill get unique key(coin)
			coindata.update(coindict)
		return coindata.keys()

	def merge_all_dicts(self,*args):
		'''
		accepts all the dictionaries as argument and returns a universal dictionary
		'''
		univ_dict = {}
		for i in args:
			univ_dict.update(i)
		return univ_dict

	def get_avg_prices(self,*coin_dicts):
		'''
		:param coin_dicts: dict of all exchanges
		:return: average price of a particular coin accross the exchange
		'''
		###print('[ CoinsWatch ] get_avg_prices')
		self.all_coins = self.get_all_coins(*coin_dicts)
		for coin in self.all_coins:
			sell = 0
			buy = 0
			coin_count = 0
			for coindata in coin_dicts:

				try:
					#to catch if a coin is present in particular exchange
					sell += float(coindata[coin]['Sell'])
					buy += float(coindata[coin]['Buy'])
					coin_count+=1   #number of exchanges in which the coin is available
				except (KeyError):
					pass

				except (TypeError):
					pass
				except:
					#print('coin %s'%coin)
					#print('coin average issue %s'%coindata[coin])
					pass

			try:
				avg_sell = "%.2f" % (float(sell)/coin_count ) #convert float result to 2 decimal
				avg_buy = "%.2f" % (float(buy)/coin_count)
				self.universal_dict[coin]={'Sell':avg_sell,'Buy':avg_buy}
			except ZeroDivisionError:
				pass
			if 'TST' in self.universal_dict.keys():
				del self.universal_dict['TST']
		return self.universal_dict


	def get_all_exchanges(self):
		'''
		:return: list of all exchanges
		'''
		return {'self.coindelta','self.koinex','self.unocoin','self.zebpay',\
				'self.coinsecure','self.coinome','self.pocketbits',\
				'self.ethxindia','self.bitbns','self.unocoin','self.buyucoin'}


	def get_exchange_data_for_coin(self,coin):
		'''
		coin: coin for which exchangevise data is needed
		:return:{'BTC':{'COINOME':700000,'COINDELTA':710000,....}}
		'''
		findict = {}
		exchanges = self.get_all_exchanges()
		for exchange in exchanges:
			try:
				findict[(exchange.split('.')[1]).upper()] = eval(exchange)[coin]
			except:
				pass
		return {coin:findict}

	def update_json_data(self):
		'''
		update the json file with average prices and coin prices in the exchanges
		'''
		#print('update json operation')
		average_data = self.get_prices()	#get all the average prices calculated
		# average_data[' ']={"Sell": " ", "Buy": " "}
		exchange_data = {}
		for coin in self.all_coins:
			exchange_data.update(self.get_exchange_data_for_coin(coin))
		jsondata = {'average':average_data,'exchange':exchange_data}
		if len(exchange_data)!=0:
			'''
			dont load json if data is not fetched
			'''
			with open('currencyrate.json','w') as cryptodata:
				json.dump(jsondata,cryptodata)
		threading.Timer(100, self.update_json_data).start()
		# #print('exchange data %s'%exchange_data)
		return average_data





if __name__ == '__main__':
	price = Extractprice()
	#print(price.get_prices())
	price.update_json_data()
