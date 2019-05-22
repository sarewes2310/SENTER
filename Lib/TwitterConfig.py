from twython import Twython

"""
Fungsi untuk setting twitter API
"""
#Twitter Configuration
CONSUMER_KEY    = 'YOUR-CONSUMER-KEY'
CONSUMER_SECRET = 'YOUR-CONSUMER_SECRET-KEY'

# Access Configuration:
ACCESS_TOKEN  = 'YOUR-ACCESS_TOKEN'
ACCESS_SECRET = 'YOUR-ACCESS_SECRET'

def login():
    key = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    return key 
    