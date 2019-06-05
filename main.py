import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import requests
import startDB
import sqlite3

try:
	f = open('./data/sensor.db')
except FileNotFoundError:
	startDB.startDB()
f.close()
# Define o tipo de sensor
sensor = Adafruit_DHT.DHT11
#sensor = Adafruit_DHT.DHT22

GPIO.setmode(GPIO.BOARD)

# Define a GPIO conectada ao pino de dados do sensor
pino_sensor = 17
conn = sqlite3.connect('./data/sensor.db')
cursor = conn.cursor()
cursor.execute('''SELECT senid from sensor;''')
id = cursor.fetchone()
id = id[0]
conn.close()

while(1):
	# Efetua a leitura do sensor
	umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor)

	if umid is None:
		umid = 'NULL'
	if temp is None:
		temp ='NULL'
	data = {
	'sensorID':id,
	'sensorKind':['Umidade', 'Temperatura'],
	'value':[umid, temp]
	}
	# Envia mensagem para o servidor
	r = requests.post('http://3.86.120.246/data/addReading/',json=data)
	# Caso seja o primeiro envio, alterar as informacoes no bd
	if (id == 0):
		# Enquanto nao conseguir persistir no banco de dados, tente
		while(1):
			try:
				id = int(r.text)
				conn = sqlite3.connect('./data/sensor.db')
				cursor = conn.cursor()
				sqlCommand = 'UPDATE sensor SET senid = '+str(id)+ ' where senid=0;'
				cursor.execute(sqlCommand)
				conn.commit()
				conn.close()
				break
			except:
				pass
	time.sleep(60)
