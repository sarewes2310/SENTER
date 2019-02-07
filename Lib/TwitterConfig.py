
from twython import Twython
#Twitter Configuration
CONSUMER_KEY    = 'qXVo3PXRvaxRDinwEqluagyGB'
CONSUMER_SECRET = '8vkWXs30seGMJeJ21tg5SXXY0Lry9kdYhvJEGS3mYXIE6LHHpp'

# Access Configuration:
ACCESS_TOKEN  = '1707115609-D1axGwQkv2Mn2NOXd1sHqZbnQx0DqIJoHANI26V'
ACCESS_SECRET = 'liUdv7bkjUAWB347pl4oPfjhwlsHdzlAOn9fee6MoFhGL'


def login():

    key = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    return key 
    # Authentication and access using keys:
    ##auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    #auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    #api = tweepy.API(auth)
    #return api