from markov_chain import MarkovChain
from markov_algorithms import *

chain = MarkovChain()

# chain.train_on_file(filename='training_txt/metahuman.txt', verbose=True)
# chain.train_on_file(filename='training_txt/youaretheuniverse.txt', verbose=True)
# chain.train_on_file(filename='training_txt/chopra_tweets.txt', verbose=True)
# chain.train_on_file(filename='training_txt/new_testament.csv', verbose=True)
chain.train_on_file(filename='training_txt/shakespeare.txt', verbose=True)
# chain.train_on_file(filename='training_txt/follow_me.txt', verbose=True)

print(f'len(chain.tree): {len(chain.tree)}\n')

pritn('Adjusting weights. This may take a while.\n')
chain.bulk_adjust_weights(fitness_functions=[aw_mult(aw_favor_complexity, .001), aw_mult(aw_favor_punctuation, .00015), aw_mult(aw_favor_alternating_complexity, .1)], iterations=len(chain.tree)//6)


# chain.save_training('bin/chopra.bin')
# chain.save_training('bin/new_testament.bin')
chain.save_training('bin/follow_me.bin')

for i in range(8):
	print(chain.generate_tweet(append_tag=None, follow=False), '\n_\n')
