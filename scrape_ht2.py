import re
from random import randint
from markov_chain import MarkovChain
from markov_algorithms import *

from twitter import OAuth, Twitter
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

query = '(#belief OR #beliefs OR #believe OR #IBelieve OR #WeBelieve OR #MyBeliefs OR #OurBeliefs OR #BeliefSystem OR #BeliefSystems)'
print(f'____query____:\n{query}')

EXCLUDE_WORDS = re.compile(r'#prolife|#chooselife|rape|raping|#trump|#maga|pedophile|#fakenews|nigger', re.I)
TEXT_ONLY = re.compile('[^A-Z0-9 .,+=!?&@_/#$%^*;:"\\\'()[\\]{}-]', re.I)
RETWEET = re.compile(r'\s?RT\s')
USER_NAME = re.compile(r'@\S+', re.I)
LINKS = re.compile(r'https?\S*', re.I)
AMPERSAND = re.compile(r'&amp;', re.I)
GT = re.compile(r'&gt;', re.I)
LT = re.compile(r'&lt;', re.I)
LONE_PUNCTUATION = re.compile(r'\s[^a-zA-Z0-9 ]\s')
TYPO_HASHTAGS = re.compile(r'\S+#\w+', re.I)
def fix_hashtag(matchobj):
	fix = matchobj.group(0).split('#')
	return ' #'.join(fix)
TYPO_PERIOD = re.compile(r'\w+\.\S+', re.I)
def fix_period(matchobj):
	fix = matchobj.group(0).split('.')
	return '. '.join(fix)
TYPO_QUESTION = re.compile(r'\w+\?\S+', re.I)
def fix_question(matchobj):
	fix = matchobj.group(0).split('?')
	return '? '.join(fix)
TYPO_EXCLAMATION = re.compile(r'\w+\!\S+', re.I)
def fix_exclamation(matchobj):
	fix = matchobj.group(0).split('!')
	return '! '.join(fix)

def clean_tweet(tweet):
	tweet = TEXT_ONLY.sub(' ', tweet)
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
	return tweet

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

chain = MarkovChain()

tweets = twit.search.tweets(q=query, count=100, lang='en', result_type='recent', tweet_mode='extended', include_entities=False)

for t in tweets['statuses']:
	if EXCLUDE_WORDS.search(t['full_text']) is None:
		tweet = clean_tweet(t['full_text'])
		chain.train(tweet)
for i in range(179):
	if 'next_results' not in tweets['search_metadata']:
		print(f'____search ended at i = {i+1}____')
		break
	next_id = re.split(r'\D+', tweets['search_metadata']['next_results'])[1]
	try:
		tweets = twit.search.tweets(q=query, count=100, lang='en', result_type='recent', tweet_mode='extended', include_entities=False, max_id=next_id)
	except Exception as e:
		print('____an error occurred____')
		print(f'____search ended at i = {i+1}____')
		break
	for t in tweets['statuses']:
		if EXCLUDE_WORDS.search(t['full_text']) is None:
			tweet = clean_tweet(t['full_text'])
			chain.train(tweet)
print(f'____len(chain.tree) = {len(chain.tree)}____')

print('____adjusting weights, this may take a moment____')
chain.bulk_adjust_weights(fitness_functions=[aw_mult(aw_favor_complexity, .001), aw_mult(dg_disfavor_consecutive_hashtags, .001)], iterations=len(chain.tree))
print('____done____')

chain.save_training('bin/twitter/beliefs.bin')

print('____sample tweet____:\n', chain.generate_tweet())
