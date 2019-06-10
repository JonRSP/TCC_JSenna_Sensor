#Utilizando banco de dados para armazenar uma informação simples como ID apenas para garantir as propriedades ACID
import sqlite3

def startDB( arquivo ):
	conn = sqlite3.connect(arquivo)

	cursor = conn.cursor()

	cursor.execute('''CREATE TABLE sensor(senid integer)''')
	cursor.execute("INSERT INTO sensor VALUES(0)")
	conn.commit()
	conn.close()
