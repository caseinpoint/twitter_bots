from markov_chain import MarkovChain
from markov_algorithms import *

chain = MarkovChain()

chain.train_on_file(filename='training_txt/artofrprogramming.txt', verbose=True)
chain.train_on_file(filename='training_txt/thinklikeaprogrammer.txt', verbose=True)

print(f'len(chain.tree): {len(chain.tree)}\n')

print('Adjusting weights. This may take a while.\n_\n')
chain.bulk_adjust_weights(fitness_functions=[aw_mult(aw_favor_complexity, .001), aw_mult(aw_favor_punctuation, .00015), aw_mult(aw_favor_alternating_complexity, .1)], iterations=len(chain.tree))

chain.save_training('bin/programming.bin')
# chain.save_training('bin/follow_me.bin')

for i in range(8):
	print(chain.generate_tweet(append_tag=None, follow=True), '\n_\n')
