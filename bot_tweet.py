import datetime as dt
import os, random, time
from markov_chain import MarkovChain
from gtts import gTTS
from twitter import OAuth, Twitter
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

chain = MarkovChain()

def speak(text):
	speech = gTTS(text=text, lang='en', slow=False)
	speech.save('speech.mp3')
	os.system('mpg123 -q speech.mp3')

print('*' * 22, 'tweeting at random intervals', '*' * 22)
num = 32
for i in range(num):
	print('~i:', i)
	if i % 8 == 0:
		category = 'newtestament'
		chain.load_training('bin/new_testament.bin')
	elif i % 8 == 1:
		# category = 'christians'
		# chain.load_training('bin/twitter/jesusfreak.bin')
		category = 'apologists'
		chain.load_training('bin/twitter/apologists.bin')
	elif i % 8 == 2:
		category = 'quran'
		chain.load_training('bin/quran.bin')
	elif i % 8 == 3:
		# category = 'allgods'
		# chain.load_training('bin/twitter/allgods.bin')
		category = 'deepakchopra'
		chain.load_training('bin/chopra.bin')
	elif i % 8 == 4:
		category = 'samharris'
		chain.load_training('bin/harris.bin')
	elif i % 8 == 5:
		category = 'shakespeare'
		chain.load_training('bin/shakespeare.bin')
	elif i % 8 == 6:
		category = 'news'
		chain.load_training('bin/twitter/news.bin')
	else:
		category = 'atheists'
		# chain.load_training('bin/twitter/atheists.bin')
		chain.load_training('bin/atheists.bin')
		# category = 'programming'
		# chain.load_training('bin/programming.bin')

	# else:
	# 	category = None
	# 	chain.load_training('bin/follow_me.bin')

	# if category is not None:
	tweet = chain.generate_tweet(append_tag=f'#MarkovChain.\n\n[Category: #{category}]')
	# else:
	# 	tweet = chain.generate_tweet(follow=True)
	print(f'-t: {tweet}')
	twit.statuses.update(status=tweet)
	# speak(tweet)

	if i < num - 1:
		delay = random.randint(1024,2048)
		delta = dt.timedelta(seconds=delay)
		when = dt.datetime.now(tz=dt.timezone(dt.timedelta(hours=-7))) + delta
		delay_text = f'delay: {delay} seconds (next tweet at {when.strftime("%H:%M:%S")})'
		print(delay_text, '\n')
		# speak(delay_text)
		# time.sleep(delay - 12)
		time.sleep(delay)
