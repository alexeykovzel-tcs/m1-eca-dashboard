import json

"""
Fixes original data from 'p2000-tweets-orig.txt' into 'p2000-tweets.txt'

What changes:
1. Fixes image sources
2. Deletes test accounts
3. Deletes accounts with unconfirmed origin
"""


# As http://a0.twimg.com link is depreciated for twitter images and was replaced with http://pbs.twimg.com
def fix_image_source(txt):
    return txt.replace("http:\/\/a0.twimg.com", "http:\/\/pbs.twimg.com")


# deletes test accounts & accounts with unconfirmed origin and fixes image sources
def fix_data():
    fixed_tweets = []

    with open("p2000-tweets-orig.txt", "r") as file:

        # goes through each tweet in the original file
        for line in file.readlines():
            tweet = json.loads(fix_image_source(line))
            name = tweet['user']['name'].lower()
            confirmed_origin = False

            # We assume that account names with confirmed origin start with 112alarm or p2000
            if name.startswith("112alarm"):

                # As 112alarm icon in the original file is depreciated, we decided to substitute it for the modern account image of 112alarm.net
                tweet['user']['profile_image_url'] = "https://pbs.twimg.com/profile_images/1333135803824943105/eYD5osTP_400x400.jpg"
                confirmed_origin = True

            elif name.startswith("p2000"):
                confirmed_origin = True

            if confirmed_origin:
                fixed_tweets.append(json.dumps(tweet))

    with open("p2000-tweets.txt", "w") as file:
        file.write('\n'.join(fixed_tweets))
