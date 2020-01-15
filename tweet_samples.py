from markov_chain import MarkovChain
test_chain = MarkovChain()
test_chain.load_training('bin/twitter/trending.bin')
print(f'len(test_chain.tree): {len(test_chain.tree)}\n')
for i in range(32):
	print(test_chain.generate_tweet(append_tag='Category: #trending'), '\n')
