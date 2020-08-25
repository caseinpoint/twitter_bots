from random import randint
from re import split
from time import sleep
from markov_chain import MarkovChain
chain = MarkovChain()

from twitter import OAuth, Twitter
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

# query = '(#starseed OR #crystalenergy OR #occult OR #oneness OR #energyhealing OR #wicca OR #astrology OR #reiki OR #chakras OR #divination OR #numerology OR #mindfulness)'
query = '(#jesusmatters OR #godisgreat OR #jesuschrist OR #godisgood OR #jesusheals OR #bibleverse OR #godislove OR #jesussaves OR #jesusisking)'
print(f'{"*"*16} _query_: {query} {"*"*16}\n')

replies = 0

def reply(tweet):
	global replies
	if replies % 4 == 0 or replies % 4 == 2:
		# chain.load_training('bin/waking_meta.bin')
		# print('_source_: waking_meta')
		# chain.load_training('bin/quran_testament.bin')
		# print('_source_: quran_testament')
		chain.load_training('bin/atheists.bin')
		print('_source_: atheists')
		verse = False
		tag = '#MarkovProcess'
	elif replies % 4 == 1:
		# chain.load_training('bin/chopra.bin')
		# print('_source_: chopra')
		chain.load_training('bin/new_testament.bin')
		print('_source_: new_testament')
		verse = True
		tag = None
	else:
		# chain.load_training('bin/harris.bin')
		# print('_source_: harris')
		chain.load_training('bin/quran.bin')
		print('_source_: quran')
		verse = True
		tag = None
	# r'[^a-zA-Z#]' or r'\W'
	t_words = sorted(split(r'[^a-zA-Z#]', tweet['full_text']), key=lambda w: len(w), reverse=True)
	begin = None
	for word in t_words:
		if len(word) > 0 and word.lower() in chain.tree:
			begin = word.lower()
			break
		elif len(word) == 0:
			break

	r_tweet = chain.generate_tweet(start_with=begin, append_verse=verse, append_tag=tag, follow=False)
	print(f'_reply_:\n{r_tweet}\n')

	try:
		twit.statuses.update(status=r_tweet, in_reply_to_status_id=tweet['id'], auto_populate_reply_metadata='true')
	except Exception as e:
		replies -= 1
		print(f'{"!"*32}error{"!"*32}\n{e}\n')

	print(f'{"—"*64}\n')

tweets = twit.search.tweets(q=query, count=100, tweet_mode='extended', lang='en', result_type='recent')

for t in tweets['statuses']:
	# if t['is_quote_status'] == False and
	if len(t['entities']['user_mentions']) < 16:
		replies += 1
		print(f'tweet #{replies} [id: {t["id"]}]\n_original_:\n{t["full_text"]}')
		print(f'_user_:\n{t["user"]["name"]} (@{t["user"]["screen_name"]}) [id: {t["user"]["id"]}]\n')

		reply(t)

		sleep(randint(32,256))

for i in range(9):
	if 'next_results' not in tweets['search_metadata']:
		break
	next_id = split(r'\D+', tweets['search_metadata']['next_results'])[1]
	print(f'\n{"*"*32} searching again ({i+1}) {"*"*32}')
	print(f'{"*"*16} _query_: {query} {"*"*16}\n')
	tweets = twit.search.tweets(q=query, count=100, tweet_mode='extended', lang='en', result_type='recent', max_id=next_id)
	for t in tweets['statuses']:
		# if t['is_quote_status'] == False and
		if len(t['entities']['user_mentions']) < 10:
			replies += 1
			print(f'tweet #{replies} [id: {t["id"]}]\n_original_:\n{t["full_text"]}')
			print(f'_user_:\n{t["user"]["name"]} (@{t["user"]["screen_name"]}) [id: {t["user"]["id"]}]\n')

			reply(t)

			sleep(randint(32,256))
