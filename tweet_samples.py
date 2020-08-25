from math import sqrt
from random import random
from markov_chain import MarkovChain

test_chain = MarkovChain()
# file_name = './bin/chopra.bin'
# file_name = './bin/harris.bin'
# file_name = './bin/waking_meta.bin'
# file_name = './bin/new_testament.bin'
# file_name = './bin/quran.bin'
# file_name = './bin/quran_testament.bin'
file_name = './bin/atheists.bin'
# file_name = './bin/twitter/news.bin'
# file_name = './bin/coding.bin'
test_chain.load_training(file_name)

print(f'{"_"*16} file_name: "{file_name}" {"_"*16}')
print(f'{"_"*16} len(test_chain.tree): {len(test_chain.tree)} {"_"*16}\n')
for i in range(11):
	# print(test_chain.generate_tweet(start_with='finger', append_tag=None, append_verse=True, follow=False), '\n_\n')
	print(test_chain.generate_tweet(start_with='clowns', append_tag='#MarkovProcess', append_verse=False, follow=False), '\n_\n')

# that’s
