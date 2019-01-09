import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import requests
import startDB
import sqlite3

try:
	f = open('sensor.db')
except FileNotFoundError:
	startDB.startDB()
f.close()
# Define o tipo de sensor
sensor = Adafruit_DHT.DHT11
#sensor = Adafruit_DHT.DHT22
 
GPIO.setmode(GPIO.BOARD)
 
# Define a GPIO conectada ao pino de dados do sensor
pino_sensor = 17
conn = sqlite3.connect('sensor.db')
cursor = conn.cursor()
cursor.execute('''SELECT senid from sensor;''')
id = cursor.fetchone()
id = id[0]
conn.close()

while(1):
	# Efetua a leitura do sensor
	try:
		umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor)
	# Caso leitura esteja ok, mostra os valores na tela
		if umid is None:
			umid = 'NULL'
		if temp is None:
			temp ='NULL'
		data = {
		'sensorID':id,
		'sensorKind':['Umidade', 'Temperatura'],
		'value':[umid, temp]
		}
#	print(data)
		r = requests.post('http://3.86.120.246/data/addReading/',json=data)

		if (id == 0):
			try:
				id = int(r.text)
				conn = sqlite3.connect('sensor.db')
				cursor = conn.cursor()
				sqlCommand = 'UPDATE sensor SET senid = '+str(id)+ ' where senid=0;'
				cursor.execute(sqlCommand)
				conn.commit()
				conn.close()
				#print(id)
			except:
				pass
		time.sleep(5)
	except:
		pass
