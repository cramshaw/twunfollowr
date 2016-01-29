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
        self.failed_follows = list()
        self.recently_followed = list()
        self.count = 0

    def make_auth(self):
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return auth

    def run(self):
        self.load_last_followed()
        self.get_current_followers()
        self.get_current_following()
        self.remove_useless()
        self.follow()
        self.save_changes()

    def get_current_followers(self):
        self.followers = self.api.followers_ids()
        print(self.followers)

    def get_current_following(self):
        self.following = self.api.friends_ids()
        print(self.following)

    def follow(self):
        try:
            for target in self.api.followers_ids(screen_name=self.target):
                if self.count < 75:
                    if target not in self.followers and target not in self.following and target not in self.recently_followed and target not in self.failed_follows and target != self.api.me().id:
                        print('Following', target)
                        self.api.create_friendship(target)
                        sleep(randint(0,50))
                        self.followed.append(target)
                        print("FOLLOWED", target)
                        self.count += 1
                        print(self.count)
            else:
                return
        except:
            print("rate limit hit, sleeping for 900 seconds", ctime())
            sleep(900)

    def save_changes(self):
        with open('follow.txt', 'wb') as fhand:
            pickle.dump(self.followed, fhand)
            print('saved follows')
        with open('failed_follows.txt', 'wb') as fhand:
            pickle.dump(self.failed_follows, fhand)
            print('saved failed follows')


    def load_last_followed(self):
        with open('follow.txt', 'rb') as fhand:
            self.recently_followed = pickle.load(fhand)
        with open('failed_follows.txt', 'rb') as fhand:
            self.failed_follows = pickle.load(fhand)

    def remove_useless(self):
        for user in self.recently_followed:
            if user not in self.followers:
                self.failed_follows.append(user)
                sleep(randint(0,30))
                try:
                    self.api.destroy_friendship(user)
                    print('unfollowed', user)
                except:
                    print(user, "couldn't be unfollowed - CHECK IT OUT")

if __name__ == "__main__":
    Followr("SkyBetChamp").run()