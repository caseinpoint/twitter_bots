import sqlite3
from sqlite3 import Error
from markov_chain import MarkovChain

chain = MarkovChain()

database = '/home/drue/Deployment/star_trek_club/star_trek_db.sqlite3'
connection = sqlite3.connect(database)
cursor = connection.cursor()

char_name = 'PICARD'

cursor.execute('SELECT id FROM characters WHERE name=?', (char_name,))
char_id = cursor.fetchone()[0]

cursor.execute('SELECT line FROM lines WHERE character_id=?', (char_id,))
for result in cursor.fetchall():
	chain.train(result[0].replace('...', '').replace('--', ''))

chain.save_training(f'bin/star_trek/{char_name}.bin')
