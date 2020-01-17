from datetime import datetime
import random, time
from twitter import OAuth, Twitter

from markov_chain import MarkovChain
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

chain = MarkovChain()

print('*' * 22, 'tweeting at random intervals', '*' * 22)
num = 7
for i in range(num):
	print('~i:', i)
	if i % 7 == 0:
		category = 'newage'
		chain.load_training('bin/twitter/newage.bin')
	elif i % 7 == 1:
		category = 'allgods'
		chain.load_training('bin/twitter/allgods.bin')
	elif i % 7 == 2:
		category = 'newagers'
		chain.load_training('bin/twitter/newagers.bin')
	elif i % 7 == 3:
		category = 'churches'
		chain.load_training('bin/twitter/churches.bin')
	elif i % 7 == 4:
		category = 'newtestament'
		chain.load_training('bin/new_testament.bin')
	elif i % 7 == 5:
		category = 'deepakchopra'
		chain.load_training('bin/chopra.bin')
	else:
		category = None
		chain.load_training('bin/follow_me.bin')

	if category is not None:
		tweet = chain.generate_tweet(append_tag=f'Category: #{category}')
	else:
		tweet = chain.generate_tweet(follow=True)
	print(f'-t: {tweet}')
	twit.statuses.update(status=tweet)

	if i < num - 1:
		delay = random.randint(256,512)
		print(f'_d: {delay} seconds\n')
		time.sleep(delay)
