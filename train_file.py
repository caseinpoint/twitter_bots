from markov_chain import MarkovChain
from markov_algorithms import *

chain = MarkovChain()

chain.train_on_file('training_txt/metahuman.txt')
chain.train_on_file('training_txt/youaretheuniverse.txt')
chain.train_on_file('training_txt/chopra_tweets.txt')
# chain.train_on_file('training_txt/new_testament.csv')

print('len(chain.tree):', len(chain.tree))

chain.bulk_adjust_wieghts(fitness_functions=[aw_mult(aw_favor_complexity, .001), aw_mult(aw_favor_punctuation, .001), aw_mult(aw_favor_consonants, .1), aw_mult(aw_favor_alliterations, .01)], iterations=len(chain.tree))


chain.save_training('bin/chopra.bin')
# chain.save_training('bin/new_testament.bin')

for i in range(10):
	print(chain.generate_tweet(append_tag='#newtestament'), '\n')
