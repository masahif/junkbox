#!/usr/bin/env python

import time
from pyquery import PyQuery as pq

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

#status = api.PostUpdate('hoge')
#print status.text


def fetch_jcf(last_id):
    jcf = pq(url="http://jcf.or.jp/?cat=7067")
    queue = []
    
    for e in jcf.find(".post"):
        e1 = pq(e)
        tmp = e1.attr["id"]
        if len(tmp) > 5 and tmp.startswith("post-"):
            postid = int(tmp[5:])
            if postid > last_id:
                queue.insert(0, e1)

    for e in queue:
        print e.attr["id"]
        t = "#jcf %s %s %s" % (e(".content").text(), e(".title").text(), e(".date").text().replace(" ", ""))

        status = api.PostUpdate(t)
        print status.text

        last_id = int(e.attr["id"][5:])
        
    return last_id

        

if __name__ == "__main__":
    f = open("data.txt")
    tmp = f.read()
    f.close()

    if len(tmp):
        last_id = int(tmp)
    else:
        last_id = 0
    
    while(True):
        last_id = fetch_jcf(last_id)
        f = open("data.txt", "w")
        f.write(str(last_id))
        f.close()
        print "-- %d -- " % last_id
        time.sleep(5)
