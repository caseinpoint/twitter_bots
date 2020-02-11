import random, time
from twitter import OAuth, Twitter

from markov_chain import MarkovChain
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

chain = MarkovChain()

print('*' * 22, 'tweeting at random intervals', '*' * 22)
num = 21
for i in range(num):
	print('~i:', i)
	if i % 7 == 0:
		category = 'quran'
		chain.load_training('bin/quran.bin')
	elif i % 7 == 1:
		category = 'newtestament'
		chain.load_training('bin/new_testament.bin')
	elif i % 7 == 2:
		category = 'tao'
		chain.load_training('bin/tao.bin')
	elif i % 7 == 3:
		category = 'allgods'
		chain.load_training('bin/twitter/allgods.bin')
	elif i % 7 == 4:
		category = 'deepakchopra'
		chain.load_training('bin/chopra.bin')
	elif i % 7 == 5:
		category = 'samharris'
		chain.load_training('bin/harris.bin')
	else:
		category = None
		chain.load_training('bin/follow_me.bin')

	if category is not None:
		tweet = chain.generate_tweet(append_tag=f'#MarkovChain.\n[Category: #{category}]')
	else:
		tweet = chain.generate_tweet(follow=True)
	print(f'-t: {tweet}')
	twit.statuses.update(status=tweet)

	if i < num - 1:
		delay = random.randint(512,1024)
		print(f'_d: {delay} seconds\n')
		time.sleep(delay)
