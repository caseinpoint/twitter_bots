from random import randint
from re import split
from time import sleep
from markov_chain import MarkovChain
chain = MarkovChain()
chain.load_training('bin/twitter/coding.bin')

from twitter import OAuth, Twitter
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

replies = 0
# query = '(#MarkovChain)'
query = '(#developer OR #algorithm OR #datastructures OR #python OR #java OR #golang OR #datascience OR #coding OR #opensource OR #sourcecode OR #machinelearning OR #programming)'
print(f'{"*"*16} _query_: {query} {"*"*16}\n')

def reply(tweet):
	global replies
	t_words = sorted(split(r'[^a-zA-Z]', tweet['full_text']), key=lambda w: len(w), reverse=True)
	begin = None
	for word in t_words:
		if len(word) > 0 and word.lower() in chain.tree:
			begin = word.lower()
			break
		elif len(word) == 0:
			break

	r_tweet = chain.generate_tweet(start_with=begin, append_tag='#MarkovChain.', follow=False)
	print(f'_reply_:\n{r_tweet}\n')

	try:
		twit.statuses.update(status=r_tweet, in_reply_to_status_id=tweet['id'], auto_populate_reply_metadata='true')
	except Exception as e:
		replies -= 1
		print(f'{"!"*32}error{"!"*32}\n{e}\n')

	print(f'{"—"*64}\n')

tweets = twit.search.tweets(q=query, count=100, tweet_mode='extended', lang='en')
for t in tweets['statuses']:
	if t['is_quote_status'] == False and t['user']['id'] != 1204948499005001728:
		replies += 1
		print(f'tweet #{replies} [id: {t["id"]}]\n_original_:\n{t["full_text"]}')
		print(f'_user_:\n{t["user"]["name"]} (@{t["user"]["screen_name"]}) [id: {t["user"]["id"]}]\n')

		reply(t)

		sleep(randint(64,128))

for i in range(4):
	if 'next_results' not in tweets['search_metadata']:
		break
	next_id = split(r'\D+', tweets['search_metadata']['next_results'])[1]
	print(f'\n{"*"*32} searching again ({i+1}) {"*"*32}')
	print(f'{"*"*16} _query_: {query} {"*"*16}\n')
	tweets = twit.search.tweets(q=query, count=100, tweet_mode='extended', max_id=next_id, lang='en')
	for t in tweets['statuses']:
		if t['is_quote_status'] == False and t['user']['id'] != 1204948499005001728:
			replies += 1
			print(f'tweet #{replies} [id: {t["id"]}]\n_original_:\n{t["full_text"]}')
			print(f'_user_:\n{t["user"]["name"]} (@{t["user"]["screen_name"]}) [id: {t["user"]["id"]}]\n')

			reply(t)

			sleep(randint(64,128))
