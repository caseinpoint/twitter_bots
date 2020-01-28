from random import randint
from time import sleep
from markov_chain import MarkovChain
chain = MarkovChain()
# chain.load_training('bin/chopra.bin')
chain.load_training('bin/new_testament.bin')

from twitter import OAuth, Twitter
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

tweets = twit.search.tweets(q=f'#jesuschrist', count=100, tweet_mode='extended', lang='en')
replies = 0

for t in tweets['statuses']:
	 # and t['in_reply_to_status_id'] is None
	if t['is_quote_status'] == False and len(t['entities']['user_mentions']) == 0:
		replies += 1
		print(f'tweet #{replies}\noriginal: {t["full_text"]}\n')

		tweet = chain.generate_tweet(append_tag='#newtestament')
		print(f'reply: {tweet}\n{"_"*64}\n')
		twit.statuses.update(status=tweet, in_reply_to_status_id=t['id'], auto_populate_reply_metadata='true')

		# if replies == 10:
		# 	break
		# else:
		sleep(randint(64,128))
