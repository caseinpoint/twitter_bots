user = 'JerryFalwellJr'
# user = 'GOPLeader' # on deck
print(f'spamming screen_name: {user}\nscraping...')

from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET
from markov_algorithms import *
from markov_chain import MarkovChain
from random import randint
import re
from time import sleep
from twitter import OAuth, Twitter

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

# USER_NAME = re.compile(r'@\S+', re.I)
LINKS = re.compile(r'https?\S*', re.I)
AMPERSAND = re.compile(r'&amp;', re.I)
GT = re.compile(r'&gt;', re.I)
LT = re.compile(r'&lt;', re.I)

chain = MarkovChain()

tweets = twit.statuses.user_timeline(screen_name=user, count=200, tweet_mode='extended', trim_user=True, include_rts=False)

for i in range(36):
	try:
		tweets += twit.statuses.user_timeline(screen_name=user, count=200, tweet_mode='extended', trim_user=True, include_rts=False, max_id=tweets[-1]['id']-1)
	except Exception as e:
		print(f'scraping stopped at i={i+1}')
		break
print(f'# of tweets: {len(tweets)}')

for t in tweets:
	# if 'retweeted_status' in t:
	# 	continue
	# tweet = USER_NAME.sub(' ', t['full_text'])
	tweet = LINKS.sub(' ', t['full_text'])
	tweet = AMPERSAND.sub('&', tweet)
	tweet = GT.sub('>', tweet)
	tweet = LT.sub('<', tweet)
	chain.train(tweet)
print(f'length of chain: {len(chain.tree)}\n')

# chain.bulk_adjust_weights(fitness_functions=[aw_mult(aw_favor_complexity, .001), aw_mult(aw_favor_punctuation, .00015), aw_mult(aw_favor_alternating_complexity, .1)], iterations=len(chain.tree))
chain.save_training(f'bin/twitter/{user}.bin')

tweets = [tweets[i] for i in range(100)]
tweets.reverse()

print(f'{"—"*64}\n')
replies = 0
for t in tweets:
	replies += 1
	print(f'___tweet #{replies}___\n')
	print(f'___original tweet:___\n{t["full_text"]}\n')

	words = sorted(re.split(r'[^a-zA-Z#]', t['full_text']), key=lambda w: len(w), reverse=True)
	begin = None
	for w in words:
		if len(w) > 0 and w.lower() in chain.tree:
			begin = w.lower()
			break
		elif len(w) == 0:
			break

	reply = chain.generate_tweet(start_with=begin, append_tag='\n#YourWordFrequencies')
	print(f'___reply:___\n{reply}\n')

	try:
		twit.statuses.update(status=reply, in_reply_to_status_id=t['id'], auto_populate_reply_metadata='true')
	except Exception as e:
		replies -= 1
		print(f'{"!"*32}error{"!"*32}\n{e}\n')

	print(f'{"—"*64}\n')
	sleep(randint(2,8))
