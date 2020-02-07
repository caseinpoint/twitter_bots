from random import randint
from re import split
from time import sleep
from markov_chain import MarkovChain
chain = MarkovChain()
# chain.load_training('bin/chopra.bin')
chain.load_training('bin/new_testament.bin')

from twitter import OAuth, Twitter
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

query = '#rosary' # next:
print(f'{"*"*32} _query_: {query} {"*"*32}\n')

def reply(tweet):
	s_words = sorted(split(r'\W', tweet['full_text']), key=lambda w: len(w), reverse=True)
	begin = None
	for word in s_words:
		if len(word) > 0 and word.lower() in chain.tree:
			begin = word.lower()
			break
		elif len(word) == 0:
			break
	r_tweet = chain.generate_tweet(start_with=begin, append_tag=None, follow=False)
	print(f'_reply_: {r_tweet}\n')

	try:
		twit.statuses.update(status=r_tweet, in_reply_to_status_id=tweet['id'], auto_populate_reply_metadata='true')
	except Exception as e:
		print(f'{"!"*32}error{"!"*32}\n{e}\n')

	print(f'{"—"*64}\n')

tweets = twit.search.tweets(q=query, count=100, tweet_mode='extended', lang='en')
replies = 0

for t in tweets['statuses']:
	if t['is_quote_status'] == False and len(t['entities']['user_mentions']) == 0:
		replies += 1
		print(f'tweet #{replies} [id: {t["id"]}]\n_original_: {t["full_text"]}')
		print(f'_user_: {t["user"]["name"]} (@{t["user"]["screen_name"]}) [id: {t["user"]["id"]}]\n')

		reply(t)

		sleep(randint(64,128))

for i in range(3):
	if 'next_results' not in tweets['search_metadata']:
		break
	next_id = split(r'\D+', tweets['search_metadata']['next_results'])[1]
	print(f'\n{"*"*32} searching again ({i+1}) {"*"*32}')
	print(f'{"*"*32} _query_: {query} {"*"*32}\n')
	tweets = twit.search.tweets(q=query, count=100, tweet_mode='extended', max_id=next_id, lang='en')
	for t in tweets['statuses']:
		if t['is_quote_status'] == False and len(t['entities']['user_mentions']) == 0:
			replies += 1
			print(f'tweet #{replies} [id: {t["id"]}]\n_original_: {t["full_text"]}')
			print(f'_user_: {t["user"]["name"]} (@{t["user"]["screen_name"]}) [id: {t["user"]["id"]}]\n')

			reply(t)

			sleep(randint(64,128))
