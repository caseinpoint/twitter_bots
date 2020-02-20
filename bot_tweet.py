import datetime as dt
import random, time
from twitter import OAuth, Twitter

from markov_chain import MarkovChain
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

chain = MarkovChain()

print('*' * 22, 'tweeting at random intervals', '*' * 22)
num = 28
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
		category = 'christianity'
		chain.load_training('bin/twitter/jesusfreak.bin')
	elif i % 7 == 4:
		category = 'allgods'
		chain.load_training('bin/twitter/allgods.bin')
	elif i % 7 == 5:
		category = 'deepakchopra'
		chain.load_training('bin/chopra.bin')
	else:
		category = 'samharris'
		chain.load_training('bin/harris.bin')
	# else:
	# 	category = None
	# 	chain.load_training('bin/follow_me.bin')

	# if category is not None:
	tweet = chain.generate_tweet(append_tag=f'#MarkovChain.\n[Category: #{category}]')
	# else:
	# 	tweet = chain.generate_tweet(follow=True)
	print(f'-t: {tweet}')
	twit.statuses.update(status=tweet)

	if i < num - 1:
		delay = random.randint(1024,2048)
		delta = dt.timedelta(seconds=delay)
		when = dt.datetime.now(tz=dt.timezone(dt.timedelta(hours=-8))) + delta
		print(f'_d: {delay} seconds (next tweet at {when.strftime("%H:%M:%S")})\n')
		time.sleep(delay)
