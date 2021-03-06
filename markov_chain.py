### Original code: https://medium.com/@G3Kappa/writing-a-weight-adjustable-markov-chain-based-text-generator-in-python-9bbde6437fb4

### Several additions and modifications have been made. Probably the largest addition is the generate_tweet() method.

import re, glob, pickle, random

from bible_books import ot_books, nt_books
ot_keys = list(ot_books)
nt_keys = list(nt_books)

class MarkovChain:
	def __init__(self):
		self.tree = dict()

	def train(self, text, factor=.1):
		words = filter(lambda s: len(s) > 0, re.split(r'[\s]', text))
		words = [w.lower() for w in words]

		for a, b in [(words[i], words[i+1]) for i in range(len(words) - 1)]:
			if a not in self.tree:
				self.tree[a] = dict()
			self.tree[a][b] = factor if b not in self.tree[a] else self.tree[a][b] + self.tree[a][b] * factor

	def train_on_file(self, filename, encodings=None, verbose=False):
		encodings = encodings if encodings is not None else ['utf-8', 'ISO-8859-1']
		ret = False
		for encoding in encodings:
			try:
				with open(filename, 'r', encoding=encoding) as f:
					self.train(f.read())
				if verbose:
					print(f'Successfully trained on "{filename}". [ENCODING: {encoding}]')
				ret = True
				break
			except UnicodeDecodeError:
				if verbose:
					print(f'Unable to decode "{filename}" for training. [ENCODING: {encoding}]')
		if verbose:
			print()
		return ret

	def bulk_train(self, path, verbose=False):
		i = 0
		for filename in glob.glob(path):
			if self.train_on_file(filename, verbose=verbose):
				i += 1
		if verbose:
			print(f'Successfully trained on {i} files')
		return i

	def save_training(self, file):
		with open(file, 'wb') as f:
			pickle.dump(self.tree, f)

	def load_training(self, file):
		with open(file, 'rb') as f:
			self.tree = pickle.load(f)

	def generate(self, start_with=None, max_len=0, rand=lambda x: random.random() * x, verbose=False):
		if len(self.tree) == 0:
			return
		word = start_with if start_with is not None else random.choice([key for key in self.tree])

		if verbose:
			print(f'Generating a sentence of max. {max_len} words, starting with "{word}":\n')

		yield word

		i = 1
		while max_len == 0 or i < max_len:
			i += 1
			if word not in self.tree:
				return
			dist = sorted([(w, rand(self.tree[word][w] / len(self.tree[word]))) for w in self.tree[word]], key=lambda k: 1-k[1])
			if len(dist) > 1:
				word = dist[1][0]
			else:
				word = dist[0][0]
			yield word

	### new addition ###
	def generate_verse(self):
		if random.randint(0, 1) == 0:
			key = random.choice(ot_keys)
			chapter = random.randint(1, ot_books[key])
		else:
			key = random.choice(nt_keys)
			chapter = random.randint(1, nt_books[key])
		verse = random.randint(1, 26)
		return f'[{key} {chapter}:{verse}]'

	### new addition ###
	def generate_tweet(self, start_with=None, rand=lambda x: x / random.random(), append_tag=None, append_verse=False, follow=False):
		if len(self.tree) == 0:
			return
		t_keys = [w for w in self.tree.keys()]
		if start_with is None or start_with not in t_keys:
			word = random.choice(t_keys)
		else:
			word = start_with

		tweet = [word]
		count_len = len(word)

		# first_word = True
		while count_len <= 200:
			if word not in self.tree:
				break
			### original randomizing: ###
			# dist = sorted([(w, rand(self.tree[word][w] / len(self.tree[word]))) for w in self.tree[word]], key=lambda k: 1-k[1])
			### new randomizing: ###
			dist = sorted([(w, rand(self.tree[word][w])) for w in self.tree[word]], key=lambda k: k[1])
			### more random equals more better ###

			# if first_word == True:
			# 	print(dist)
			# 	first_word = False

			prev_word = word
			word = dist[0][0]
			tries = 0
			while word in tweet and tries < 3:
				word = random.choice(dist)[0]
				tries += 1

			if word == 'i':
				tweet.append('I')
			elif prev_word.endswith('.') or prev_word.endswith('!') or prev_word.endswith('?'):
				tweet.append(word.capitalize())
			else:
				tweet.append(word)

			count_len += len(word) + 1 # plus one for space

			if count_len >= 70 and (word.endswith('.') or word.endswith('!') or word.endswith('?')):
				break

		tweet[0] = tweet[0].capitalize()

		if append_verse == True:
			tweet.append(self.generate_verse())

		if append_tag is not None:
			tweet.append(append_tag)

		if follow == True and '@MarkovChurch' not in tweet:
			tweet.append('\n\n#Follow @MarkovChurch')

		return ' '.join(tweet)

	def generate_sentence(self, start_with=None, rand=lambda x: random.random() * x, verbose=False):
		if len(self.tree) == 0:
			return
		word = start_with if start_with is not None else random.choice([key for key in self.tree])

		if verbose:
			print(f'Generating a sentence of max. {max_len} words, starting with "{word}":\n')

		yield word
		while True:
			if word not in self.tree:
				return
			elif word.endswith('.') or word.endswith('!') or word.endswith('?'):
				return
			dist = sorted([(w, rand(self.tree[word][w] / len(self.tree[word]))) for w in self.tree[word]], key=lambda k: 1-k[1])
			if len(dist) > 1:
				word = dist[1][0]
				# word = dist[random.randint(1,len(dist)-1)][0]
			else:
				word = dist[0][0]
			yield word

	def adjust_weights(self, max_len=2, f=lambda a, b: 0):
		pairs = [w for w in self.generate(max_len=max_len, rand=lambda r: random.random() * r)]
		pairs = [[pairs[i], None if i == len(pairs) - 1 else pairs[i + 1]] for i in range(len(pairs))][:-1]
		factors = [(f(*p) - 0.5) * 2 for p in pairs]
		for p, x in zip(pairs, factors):
			if x < -1 or x > 1:
				raise ValueError(x)
			# self.train(reduce(lambda a, b: f'{a} {b}', p), x)
			self.train(text=f'{p[0]} {p[1]}', factor=x)

	def bulk_adjust_weights(self, fitness_functions=None, iterations=1, pbar_len=14, verbose=False):
		if fitness_functions is None or len(fitness_functions) == 0:
			return

		for i in range(iterations):
			for ff in fitness_functions:
				self.adjust_weights(f=ff)
