# rai_twitter_bot

## What?
This is simple python based twitter bot that tracks retweets for a particular message and if the retweeters have a xrb address in the profiles will send them some mrai for the retweet. It will work until it reaches a maxiumum number of retweets and then will stop.
For examples see: [https://twitter.com/xrb_giveaway]

## HowTo

0. You need a raiblocks node running to interface and send the funds
1. `$ pip install python-twitter`
2. `$ pip install pycurl`
3. Copy settings.example.py to settings.py and edit the tokens, keys, secrets, wallet and account fields. You will need to go to and sign up with a twitter dev account
4. Change the actual_tweet variable to what you want to tweet
5. Run the retweet_pay.py script
