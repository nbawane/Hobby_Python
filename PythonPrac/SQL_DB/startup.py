import sqlite3
import priceextractor


conn = sqlite3.connect('exchange.db')
c = conn.cursor()
# conn.execute('''CREATE TABLE logs(time text, exchange_id int, coin_id int, buy_price real, sell_price real)''')
# conn.execute('''CREATE TABLE coins(coin_id int, coin_symb real, coin_name real)''')
# conn.execute('''CREATE TABLE exchanges(exchange_id int, exchange_name real)''')

price = priceextractor.Extractprice()
exchanges = price.get_all_exchanges()
for index,exchange in enumerate(exchanges):
	exchange = exchange.split('.')[-1]
	c.execute('''insert into exchanges values(?,?)''',(index,exchange))


c.execute('select * from exchanges')
print(c.fetchall())
conn.commit()
conn.close()