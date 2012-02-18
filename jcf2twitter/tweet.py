#!/usr/bin/env python

import twitter
import tweetauth

user = tweetauth.u_id
t_dict = tweetauth.auth_dict

api = twitter.Api(
    consumer_key = t_dict['consumer_key'],
    consumer_secret = t_dict['consumer_secret'],
    access_token_key = t_dict['access_token_key'],
    access_token_secret = t_dict['access_token_secret'],
    )

status = api.PostUpdate('hoge')
print status.text
