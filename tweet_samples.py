from math import sqrt
from random import random
from markov_chain import MarkovChain

test_chain = MarkovChain()
# test_chain.load_training('bin/twitter/newagers.bin')
test_chain.load_training('bin/new_testament.bin')

print(f'{"_"*20} len(test_chain.tree): {len(test_chain.tree)} {"_"*20}\n')
for i in range(18):
	print(test_chain.generate_tweet(append_tag='Category: #newtestament', rand=lambda x: random() * sqrt(2) * x), '\n')
