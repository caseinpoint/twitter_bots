from csv import DictWriter
import re

SPLIT = re.compile('[“”"\s\d,.!?;:/—()[\]]')

w_count = 0
all_words = {}

read_name = 'quran.txt'

with open(file=read_name, mode='r') as read_file:
	line = read_file.readline()
	while len(line) > 0:
		line = filter(lambda s: len(s) > 0, SPLIT.split(line))
		line = [w.lower() for w in line]

		for word in line:
			w_count += 1
			if word not in all_words:
				all_words[word] = 1
			else:
				all_words[word] += 1

		line = read_file.readline()

all_words = sorted(all_words.items(), key=lambda w: w[1], reverse=False)

write_name = read_name.split('.')[0] + '_count.csv'
with open(file=write_name, mode='w', newline='') as write_file:
	field_names = ['Word', 'Count', 'Percentage', 'Total', 'Distinct']
	writer = DictWriter(write_file, fieldnames=field_names)
	writer.writeheader()

	first_row = True
	while len(all_words) > 0:
		word = all_words.pop()
		row = {
			'Word': word[0],
			'Count': word[1],
			'Percentage': word[1] / w_count * 100
		}
		if first_row == True:
			row['Total'] = w_count
			row['Distinct'] = len(all_words)
			first_row = False
		writer.writerow(row)

print(f'{read_name} -> {write_name}')
