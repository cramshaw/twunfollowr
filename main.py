import sys, os
import pickle

from time import sleep, ctime
from random import randint

import tweepy

TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']


class Followr:

    def __init__(self, target):
        self.target = target
        self.auth = self.make_auth()
        self.api = tweepy.API(self.auth)
        print(self.api.rate_limit_status())
        self.followers = list()
        self.following = list()
        self.followed = list()
        self.recently_followed = self.load_last_followed()
        self.count = 0

    def make_auth(self):
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return auth

    def run(self):
        self.remove_useless()
        self.get_current_followers()
        self.get_current_following()
        self.follow()
        self.save_changes()

    def get_current_followers(self):
        self.followers = self.api.followers_ids()

    def get_current_following(self):
        self.following = self.api.friends_ids()

    def follow(self):
        try:
            for target in self.api.followers_ids(screen_name=self.target):
                if self.count < 50:
                    if target not in self.followers and target not in self.following:
                        print('Following', target)
                        self.api.create_friendship(target)
                        sleep(randint(0,50))
                        self.followed.append(target)
                        print("FOLLOWED", target)
                        self.count += 1
            else:
                return
        except:
            print("rate limit hit, sleeping for 900 seconds", ctime())
            sleep(900)

    def save_changes(self):
        with open('follow.txt', 'wb') as fhand:
            pickle.dump(self.followed, fhand)
            print(self.followed)

    def load_last_followed(self):
        with open('follow.txt', 'rb') as fhand:
            x = pickle.load(fhand)
            print(x)
            return x

    def remove_useless(self):
        for user in self.recently_followed:
            if user not in self.followers:
                self.api.destroy_friendship(user)

if __name__ == "__main__":
    Followr("SkyBetChamp").run()