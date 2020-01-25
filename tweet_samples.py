from math import sqrt
from random import random
from markov_chain import MarkovChain

test_chain = MarkovChain()
# file_name = './bin/new_testament.bin'
file_name = './bin/twitter/trending.bin'
test_chain.load_training(file_name)

print(f'{"_"*20} file_name: {file_name} {"_"*20}')
print(f'{"_"*20} len(test_chain.tree): {len(test_chain.tree)} {"_"*20}\n')
for i in range(18):
	print(test_chain.generate_tweet(append_tag='Category: #trending', follow=False), '\n')
