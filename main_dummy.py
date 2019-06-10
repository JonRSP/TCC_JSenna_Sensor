import sys
import time
import requests
import startDB
import sqlite3

arquivo = './data/sensor_dummy.db'
try:
    f = open(arquivo)
    f.close()
except FileNotFoundError:
    startDB.startDB(arquivo)


conn = sqlite3.connect(arquivo)
cursor = conn.cursor()
cursor.execute('''SELECT senid from sensor;''')
id = cursor.fetchone()
id = id[0]
conn.close()
url = 'http://'+str(sys.stdin.read().splitlines()[0])+':8000/data/addReading/'
while(1):
	# Efetua a leitura do sensor
    umid=78
    temp=27
    data = {'sensorID':id,'sensorKind':['Umidade', 'Temperatura'],'value':[umid, temp]}
	# Envia mensagem para o servidor
    # Monta a url com o primeiro argumento recebido
    r = requests.post(url,json=data)
	# Caso seja o primeiro envio, alterar as informacoes no bd
    if (id == 0):
		# Enquanto nao conseguir persistir no banco de dados, tente
        while(1):
            try:
                id = int(r.text)
                conn = sqlite3.connect(arquivo)
                cursor = conn.cursor()
                sqlCommand = 'UPDATE sensor SET senid = '+str(id)+ ' where senid=0;'
                cursor.execute(sqlCommand)
                conn.commit()
                conn.close()
                break
            except:
                pass
    time.sleep(60)
