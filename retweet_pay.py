import settings

import twitter
import json
import time
import pycurl
from io import BytesIO

wallet = settings.wallet
giveaway_address = settings.account

def wallet_com(data):

	buffer = BytesIO()
	c = pycurl.Curl()
	c.setopt(c.URL, '127.0.0.1')
	c.setopt(c.PORT, 7076)
	c.setopt(c.POSTFIELDS, json.dumps(data))
	c.setopt(c.WRITEFUNCTION, buffer.write)

	output = c.perform()

	c.close()

	body = buffer.getvalue()
	parsed_json = json.loads(body.decode('iso-8859-1'))
	return parsed_json

api = twitter.Api(settings.consumer_key, settings.consumer_secret, settings.access_token_key, settings.access_token_secret)

if settings.old_tweet == 0:
	status = api.PostUpdate(settings.actual_tweet)

	print(status)
	json_status = json.loads(str(status))
	print(json_status['id'])
	giveaway_id = int(json_status['id'])

else:
	giveaway_id = settings.old_tweet

print(giveaway_id)

total_giveaway = settings.num_retweets
payout_volume = settings.volume
x = 0
users_data = []
users = []

while x < total_giveaway:
	#Check for any retweets
	results = api.GetRetweets(giveaway_id)
	#Scan through the retweets and check their descriptions to see if the have xrb addresses in the profiles/descriptions
	for replies in results:
		retweet_description = replies.user.description.split()
		for word in retweet_description:
			#Check for a xrb address (?64 long and does it start with xrb_)
			if (len(word) == 64) and (word[0:4] == 'xrb_'):
				retweet_user = replies.user.screen_name
				retweet_address = word
				#Check we haven't already paid out
				if retweet_user in users:
					z=1
				else:
					#Add them to the database
					temp_list = [retweet_user,retweet_address]
					print(temp_list)
					users.append(retweet_user)
					users_data.append(temp_list)
                                	#Transfer the mrai
					data = {'action' : 'mrai_to_raw', 'amount' : payout_volume}
					raw_withdraw = wallet_com(data)
					print(raw_withdraw['amount'])
					data = {'action' : 'send', 'wallet' : wallet, 'source' : giveaway_address, 'destination' : retweet_address, 'amount' : int(raw_withdraw['amount']) }
					print(data)
					parsed_json = wallet_com(data)
					print(parsed_json)
					#Update x so that eventually this while loop will end
					x = x + 1
					print(x)
					#payout_volume = payout_volume - 1

					#Send a DM with result
					reply_message = "Thanks for retweeting! Here is %iMrai https://raiblockscommunity.net/block/index.php?h=%s" % (payout_volume, str(parsed_json['block']))
					print(reply_message)
					data = api.PostDirectMessage(reply_message, screen_name=retweet_user)
					#print(data)
			#else:
				#TODO
				#send a DM suggesting that if they want a payout next time to add their
				# xrb address to their user description

	time.sleep(30)

print(users_data)

#Send a reply to your original message to announce that all the mrai is paid out
status = api.PostUpdate('All Mrai distributed - thanks for retweeting', in_reply_to_status_id=giveaway_id)

print(status)
