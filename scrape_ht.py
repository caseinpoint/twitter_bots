# from datetime import datetime
import re

from twitter import OAuth, Twitter

from markov_chain import MarkovChain
from markov_algorithms import *
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

EXCLUDE_WORDS = re.compile(r'#prolife|#chooselife|rape|raping|#trump|#maga|pedophile|#fakenews|nigger', re.I)
TEXT_ONLY = re.compile('[^A-Z0-9 .,+=!?&@_/#$%^*;:"()[\]{}\'-]', re.I)
RETWEET = re.compile(r'\s?RT\s')
USER_NAME = re.compile(r'@\S+', re.I)
LINKS = re.compile(r'https?\S*', re.I)
AMPERSAND = re.compile(r'&amp;', re.I)
GT = re.compile(r'&gt;', re.I)
LT = re.compile(r'&lt;', re.I)
LONE_PUNCTUATION = re.compile(r'\s[^a-zA-Z0-9_]\s')
TYPO_HASHTAGS = re.compile(r'\S+#\w+', re.I)
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

chain = MarkovChain()

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=2)

search_terms = ['jesus', 'brahma', 'buddha', 'muhammad', 'dao', 'shinto', 'waheguru', 'shiva', 'yahweh', 'allah', 'vishnu', 'GuruNanak']
# 	*** train on old tweets before scraping newage ***
# chain.train_on_file('training_txt/williamson_tweets.txt')
# chain.train_on_file('training_txt/chopra_tweets.txt')
# print('old newage tweets:', len(chain.tree))
# search_terms = ['wicca', 'astral', 'zodiac', 'awakening', 'chakras', 'retrograde', 'aura', 'numerology', 'tarot', 'meditation', 'mindfulness']
# search_terms = ['follow', 'retweet', 'follow4follow', 'rt', 'like', 'f4f', 'followback']
# search_terms = ['psychedelics', 'cannabis', 'magicmushrooms ', 'dmt', 'lsd', 'psilocybin', 'ayahuasca', 'psychonaut', 'acid', 'peyote']
# search_terms = ['epistemology', 'ontology', 'atheism', 'humanism', 'godless', 'secularism', 'skeptic', 'athiest', 'humanist', 'antitheist', 'freedomfromreligion', 'secular', 'agnostic']
# search_terms = ['rpg', 'ttrpg', 'dnd', 'dnd5e', 'pathfinder', '13thage', 'tabletop', 'dungeonmaster', 'dungeonsanddragons', 'tabletoprpg']
# search_terms = ['algorithm', 'datastructures', 'python', 'java', 'golang', 'sql', 'cplusplus', 'csharp', 'kotlin', 'swift', 'machinelearning', 'artificialintelligence']

for term in search_terms:
	print('search_term:', term)
	tweets = twit.search.tweets(q=f'#{term}', count=100, tweet_mode='extended')
	for t in tweets['statuses']:
		if EXCLUDE_WORDS.search(t['full_text']) is None:
			tweet = clean_tweet(t['full_text'])
			chain.train(tweet)
		# else:
		# 	print('_bad tweet:_\t', t['full_text'])
	for i in range(4):
		if 'next_results' not in tweets['search_metadata']:
			break
		next_id = re.split(r'\D+', tweets['search_metadata']['next_results'])[1]
		tweets = twit.search.tweets(q=f'#{term}', count=100, tweet_mode='extended', max_id=next_id)
		for t in tweets['statuses']:
			if EXCLUDE_WORDS.search(t['full_text']) is None:
				tweet = clean_tweet(t['full_text'])
				chain.train(tweet)
			# else:
			# 	print('_bad tweet:_\t', t['full_text'])
	print('len(chain.tree):', len(chain.tree))

chain.bulk_adjust_wieghts(fitness_functions=[aw_mult(aw_favor_complexity, .001), aw_mult(aw_favor_punctuation, .00015), aw_mult(aw_favor_alternating_complexity, .1)], iterations=len(chain.tree))

chain.save_training('bin/twitter/allgods.bin')
# chain.save_training('bin/twitter/newage.bin')
# chain.save_training('bin/twitter/follow.bin')
# chain.save_training('bin/twitter/psychonaut.bin')
# chain.save_training('bin/twitter/reason.bin')
# chain.save_training('bin/twitter/dnd.bin')
# chain.save_training('bin/twitter/coding.bin')
print('Sample tweet:', chain.generate_tweet())
