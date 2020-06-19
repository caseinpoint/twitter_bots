import re

from twitter import OAuth, Twitter
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

from markov_chain import MarkovChain
from markov_algorithms import *

EXCLUDE_WORDS = re.compile(r'#prolife|#chooselife|#rape|#raping|#trump|#maga|#pedophile|#fakenews|nigger', re.I)
TEXT_ONLY = re.compile('[^A-Z0-9 .,+=!?&@_/#$%^*;:\'"()[\\]{}-]', re.I)
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

# search_terms = ['rezaaslan', 'DrFrankTurek', 'RFupdates', 'ChristianDefORG', 'RaviZacharias', 'RamsdenMichael', 'LeeStrobel', 'DiscoveryInst1', 'BishopBarron', 'RTB_HRoss', 'RTB_official', 'alisteremcgrath', 'mRobLV']
# search_terms = ['FFRF', 'AmericanAtheist', 'SamHarrisOrg', 'VicedRhino', 'holykoolaid', 'paulogia0', 'magnabosco', 'Prophet_of_Zod', 'hemantmehta', 'telltaleatheist', 'DearMrAtheist', 'americnhumanist']
search_terms = ['npr', 'nprpolitics', 'MSNBC', 'MSNBC_Breaking', 'CNN', 'BBCWorld', 'BBCBreaking', 'MotherJones', 'thehill', 'MoveOn', 'NBCNews', 'NBCNewsNow', 'AJEnglish']
# search_terms = ['DeepakChopra', 'marwilliamson', 'goop', 'GwynethPaltrow', 'BabaRamDass', 'davidji_com', 'MindfulEveryday', 'DanielleLaPorte', 'PadraigOMorain', 'NativeAmWisdom', 'CrystalWind']
# search_terms = ['Pontifex', 'usccbfreedom', 'churchofengland', 'UMChurch', 'advmission', 'NABFellowship', 'Presbyterian', 'ELCA', 'UCC_Official']
# search_terms = ['realDonaldTrump', 'IvankaTrump', 'FLOTUS', 'DonaldJTrumpJr', 'EricTrump', 'TiffanyATrump', 'TeamTrump', 'Mike_Pence', 'VP', 'Scavino45', 'WomenforTrump']
# search_terms = ['MarkovChurch']

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=2)

chain = MarkovChain()

for user in search_terms:
	print(f'search_term: {user}')
	tweets = twit.statuses.user_timeline(screen_name=user, count=200, tweet_mode='extended', include_rts=False, trim_user=True)
	for t in tweets:
		if EXCLUDE_WORDS.search(t['full_text']) is None:
			tweet = TEXT_ONLY.sub(' ', t['full_text'])
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
		# chain.train(t['full_text'])
	print(f'len(chain.tree): {len(chain.tree)}')

chain.bulk_adjust_weights(fitness_functions=[aw_mult(aw_favor_complexity, .001), aw_mult(aw_favor_punctuation, .00015), aw_mult(aw_favor_alternating_complexity, .1)], iterations=len(chain.tree))

print('Sample tweet:', chain.generate_tweet())

# chain.save_training('bin/twitter/apologists.bin')
# chain.save_training('bin/twitter/atheists.bin')
chain.save_training('bin/twitter/news.bin')
# chain.save_training('bin/twitter/newagers.bin')
# chain.save_training('bin/twitter/churches.bin')
# chain.save_training('bin/twitter/trumpsterfire.bin')
# chain.save_training('bin/twitter/meta.bin')
