from random import randint
from re import split
from time import sleep
from markov_chain import MarkovChain
chain = MarkovChain()
chain.load_training('bin/chopra.bin')
# chain.load_training('bin/new_testament.bin')

from twitter import OAuth, Twitter
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

query = '#wicca'
print(f'_query_: {query}\n')

tweets = twit.search.tweets(q=query, count=100, tweet_mode='extended', lang='en')
replies = 0

for t in tweets['statuses']:
	if t['is_quote_status'] == False and len(t['entities']['user_mentions']) == 0:
		replies += 1
		print(f'tweet #{replies}\n_original_: {t["full_text"]}')
		print(f'_user_: {t["user"]["name"]} (@{t["user"]["screen_name"]}) [id: {t["user"]["id"]}]\n')

		tweet = chain.generate_tweet(append_tag=None, follow=True)
		print(f'_reply_: {tweet}\n{"—"*64}\n')
		twit.statuses.update(status=tweet, in_reply_to_status_id=t['id'], auto_populate_reply_metadata='true')

		sleep(randint(32,64))

for i in range(4):
	if 'next_results' not in tweets['search_metadata']:
		break
	next_id = split(r'\D+', tweets['search_metadata']['next_results'])[1]
	print(f'\n{"*"*16} searching again ({i+1}) {"*"*16}\n')
	tweets = twit.search.tweets(q=query, count=100, tweet_mode='extended', max_id=next_id, lang='en')
	for t in tweets['statuses']:
		if t['is_quote_status'] == False and len(t['entities']['user_mentions']) == 0:
			replies += 1
			print(f'tweet #{replies}\n_original_: {t["full_text"]}\n')

			tweet = chain.generate_tweet(append_tag=None, follow=True)
			print(f'_reply_: {tweet}\n{"—"*64}\n')
			twit.statuses.update(status=tweet, in_reply_to_status_id=t['id'], auto_populate_reply_metadata='true')

			sleep(randint(32,64))
