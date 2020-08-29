from twitter import OAuth, Twitter
from credentials import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twit = Twitter(auth=oauth, retry=1)

followers = twit.followers.ids(user_id=1204948499005001728)
following = twit.friends.ids(user_id=1204948499005001728)
# maximum 5000 users, so if I ever have more than that many followers,
# I'll need to add consecutive searches.

to_follow = []
to_delete = []

for usr_id in followers['ids']:
	if usr_id not in following['ids']:
		to_follow.append(usr_id)

for usr_id in following['ids']:
	if usr_id not in followers['ids']:
		to_delete.append(usr_id)

print(f'to_follow ({len(to_follow)}):\n{to_follow}\n')
print(f'to_delete ({len(to_delete)}):\n{to_delete}\n')

print('following and deleting...')
for usr_id in to_follow:
	try:
		twit.friendships.create(user_id=usr_id)
	except Exception as e:
		print(e)

for usr_id in to_delete:
	try:
		twit.friendships.destroy(user_id=usr_id)
	except Exception as e:
		print(e)
print('done')
