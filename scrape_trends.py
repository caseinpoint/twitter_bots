import re
from twitter import OAuth, Twitter
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET
from markov_chain import MarkovChain
from markov_algorithms import *

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=2)

# print(twit.trends.closest(lat=37.7749, long=-122.4194))
# results = twit.trends.place(_id=1)[0]['trends'] # _id=1 for worldwide
results = twit.trends.place(_id=23424977)[0]['trends'] # _id=2487956 for US
# results = twit.trends.place(_id=2487956)[0]['trends'] # _id=2487956 for SF
trends = []
for r in results:
	if r['name'].startswith('#'):
		trends.append(r['name'])

print(trends, '\n')

EXCLUDE_WORDS = re.compile(r'#prolife|#chooselife|#rape|#raping|#trump|#maga|pedophile|#fakenews|nigger', re.I)
TEXT_ONLY = re.compile('[^A-Z0-9 .,+=!?&@_/#$%^*;:\'"()[\\]{}-]', re.I)
RETWEET = re.compile(r'\s?RT\s')
USER_NAME = re.compile(r'@\S+', re.I)
LINKS = re.compile(r'https?\S*', re.I)
AMPERSAND = re.compile(r'&amp;', re.I)
GT = re.compile(r'&gt;', re.I)
LT = re.compile(r'&lt;', re.I)
LONE_PUNCTUATION = re.compile(r'\s[^a-zA-Z0-9_]\s')
TYPO_HASHTAGS = re.compile(r'\w+#\w+', re.I)
def fix_hashtag(matchobj):
	fix = matchobj.group(0).split('#')
	return ' #'.join(fix)
TYPO_PERIOD = re.compile(r'\w+\.\w+', re.I)
def fix_period(matchobj):
	fix = matchobj.group(0).split('.')
	return '. '.join(fix)
TYPO_QUESTION = re.compile(r'\w+\?\w+', re.I)
def fix_question(matchobj):
	fix = matchobj.group(0).split('?')
	return '? '.join(fix)
TYPO_EXCLAMATION = re.compile(r'\w+\!\w+', re.I)
def fix_exclamation(matchobj):
	fix = matchobj.group(0).split('!')
	return '! '.join(fix)

chain = MarkovChain()

for trend in trends:
	print(f'trend: {trend}')
	tweets = twit.search.tweets(q=trend, count=100, tweet_mode='extended', lang='en')
	for t in tweets['statuses']:
		if EXCLUDE_WORDS.search(t['full_text']) is None:
			tweet = TEXT_ONLY.sub(' ', t['full_text'])
			tweet = RETWEET.sub(' ', tweet)
			tweet = USER_NAME.sub(' ', tweet)
			tweet = LINKS.sub(' ', tweet)
			tweet = TYPO_HASHTAGS.sub(fix_hashtag, tweet)
			tweet = TYPO_PERIOD.sub(fix_period, tweet)
			tweet = TYPO_QUESTION.sub(fix_question, tweet)
			tweet = TYPO_EXCLAMATION.sub(fix_exclamation, tweet)
			tweet = LONE_PUNCTUATION.sub(' ', tweet)
			tweet = AMPERSAND.sub('and', tweet)
			tweet = GT.sub('>', tweet)
			tweet = LT.sub('<', tweet)
			chain.train(tweet)
	for i in range(3):
		if 'next_results' not in tweets['search_metadata']:
			break
		next_id = re.split(r'\D+', tweets['search_metadata']['next_results'])[1]
		tweets = twit.search.tweets(q=trend, count=100, tweet_mode='extended', max_id=next_id, lang='en')
		for t in tweets['statuses']:
			if EXCLUDE_WORDS.search(t['full_text']) is None:
				tweet = TEXT_ONLY.sub(' ', t['full_text'])
				tweet = RETWEET.sub(' ', tweet)
				tweet = USER_NAME.sub(' ', tweet)
				tweet = LINKS.sub(' ', tweet)
				tweet = AMPERSAND.sub('and', tweet)
				tweet = TYPO_HASHTAGS.sub(fix_hashtag, tweet)
				tweet = TYPO_PERIOD.sub(fix_period, tweet)
				tweet = TYPO_QUESTION.sub(fix_question, tweet)
				tweet = TYPO_EXCLAMATION.sub(fix_exclamation, tweet)
				tweet = LONE_PUNCTUATION.sub(' ', tweet)
				tweet = GT.sub('>', tweet)
				tweet = LT.sub('<', tweet)
				chain.train(tweet)
	print(f'len(chain.tree): {len(chain.tree)}')

chain.bulk_adjust_weights(fitness_functions=[aw_mult(aw_favor_complexity, .001), aw_mult(aw_favor_punctuation, .00015), aw_mult(aw_favor_alternating_complexity, .1)], iterations=len(chain.tree))

chain.save_training('bin/twitter/trending.bin')

print(f'Sample tweet: {chain.generate_tweet(append_tag="Category: #trending")}')
