import re

from twitter import OAuth, Twitter
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

from markov_chain import MarkovChain
from markov_algorithms import *

EXCLUDE_WORDS = re.compile(r'#prolife|#chooselife|#rape|#raping|#trump|#maga|#pedophile|#fakenews', re.I)
TEXT_ONLY = re.compile(r'[^A-Z0-9 .,+=!?&@_/#$%^*;:\'"()[\]{}-]', re.I)
RETWEET = re.compile(r'\s?RT\s')
USER_NAME = re.compile(r'@\S+', re.I)
LINKS = re.compile(r'https?://\S+', re.I)
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

search_terms = ['npr', 'nprpolitics', 'MSNBC', 'MSNBC_Breaking', 'CNN', 'BBCWorld', 'BBCBreaking', 'MotherJones', 'thehill', 'MoveOn', 'NBCNews', 'NBCNewsNow']
# search_terms = ['DeepakChopra', 'chopracenter', 'marwilliamson', 'goop', 'GwynethPaltrow', 'BabaRamDass', 'davidji_com', 'MindfulEveryday', 'DanielleLaPorte', 'PadraigOMorain']
# search_terms = ['DrFrankTurek', 'RFupdates', 'ChristianDefORG', 'RaviZacharias', 'RamsdenMichael', 'LeeStrobel', 'DiscoveryInst1', 'BishopBarron', 'RTB_HRoss', 'RTB_official', 'alisteremcgrath']
# search_terms = ['realDonaldTrump', 'IvankaTrump', 'FLOTUS', 'DonaldJTrumpJr', 'EricTrump', 'TiffanyATrump', 'TeamTrump', 'Mike_Pence', 'Scavino45', 'WomenforTrump']

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=2)

chain = MarkovChain()

for user in search_terms:
	print(f'search_term: {user}')
	tweets = twit.statuses.user_timeline(screen_name=user, count=200, tweet_mode='extended')
	for t in tweets:
		if EXCLUDE_WORDS.search(t['full_text']) is None:
			tweet = TEXT_ONLY.sub('', t['full_text'])
			tweet = RETWEET.sub('', tweet)
			tweet = USER_NAME.sub('', tweet)
			tweet = LINKS.sub('', tweet)
			tweet = TYPO_HASHTAGS.sub(fix_hashtag, tweet)
			tweet = TYPO_PERIOD.sub(fix_period, tweet)
			tweet = TYPO_QUESTION.sub(fix_question, tweet)
			tweet = TYPO_EXCLAMATION.sub(fix_exclamation, tweet)
			tweet = LONE_PUNCTUATION.sub('', tweet)
			tweet = AMPERSAND.sub('and', tweet)
			tweet = GT.sub('>', tweet)
			tweet = LT.sub('<', tweet)
			chain.train(tweet)
	print(f'len(chain.tree): {len(chain.tree)}')

chain.bulk_adjust_wieghts(fitness_functions=[aw_mult(aw_favor_complexity, .001), aw_mult(aw_favor_punctuation, .001), aw_mult(aw_favor_consonants, .1), aw_mult(aw_favor_alliterations, .01)], iterations=len(chain.tree))

print('Sample tweet:', chain.generate_tweet())

chain.save_training('bin/twitter/news.bin')
# chain.save_training('bin/twitter/newagers.bin')
# chain.save_training('bin/twitter/apologists.bin')
# chain.save_training('bin/twitter/trumpsterfire.bin')
