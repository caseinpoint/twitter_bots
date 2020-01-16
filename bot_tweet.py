from datetime import datetime
import random, time
from twitter import OAuth, Twitter

from markov_chain import MarkovChain
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

chain = MarkovChain()

print('*' * 22, 'tweeting at random intervals', '*' * 22)
num = 18 + 1 # +1 for range
for i in range(1,num):
	print('~i:', i)
	if i % 6 == 1:
		category = 'newage'
		chain.load_training('bin/twitter/newage.bin')
	elif i % 6 == 2:
		category = 'allgods'
		chain.load_training('bin/twitter/allgods.bin')
	elif i % 6 == 3:
		category = 'newagers'
		chain.load_training('bin/twitter/newagers.bin')
	elif i % 6 == 4:
		category = 'apologists'
		chain.load_training('bin/twitter/apologists.bin')
	elif i % 6 == 5:
		category = 'newtestament'
		chain.load_training('bin/new_testament.bin')
	else:
		category = 'deepakchopra'
		chain.load_training(f'bin/chopra.bin')

	tweet = chain.generate_tweet(append_tag=f'Category: #{category}')
	print(f'-t: {tweet}')
	twit.statuses.update(status=tweet)

	if i < num - 1:
		delay = random.randint(1024,2048)
		print(f'_d: {delay} seconds\n')
		time.sleep(delay)
