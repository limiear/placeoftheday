# -*- coding: utf-8 -*-

"""
Copyright 2014 Randal S. Olson

This file is part of the Twitter Follow Bot library.

The Twitter Follow Bot library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option) any
later version.

The Twitter Follow Bot library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with the Twitter
Follow Bot library. If not, see http://www.gnu.org/licenses/.
"""

from twitter_keys import *
from twitter import Twitter, OAuth, TwitterHTTPError
import os
import itertools
import random
import time

# put your tokens, keys, secrets, and Twitter handle in the following variables
TWITTER_HANDLE = "ellugardeldia"

# put the full path and file name of the file you want to store your "already followed"
# list in
ALREADY_FOLLOWED_FILE = "already-followed.csv"

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
            APP_KEY, APP_SECRET))


def search_tweets(q, count=100, result_type="recent"):
    """
        Returns a list of tweets matching a certain phrase (hashtag, word, etc.)
    """

    return t.search.tweets(q=q, result_type=result_type, count=count)


def auto_fav(q, count=100, result_type="recent"):
    """
        Favorites tweets that match a certain phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count, result_type)

    for tweet in result["statuses"]:
        try:
            # don't favorite your own tweets
            if tweet["user"]["screen_name"] == TWITTER_HANDLE:
                continue

            result = t.favorites.create(_id=tweet["id"])
            print("favorited: %s" % (result["text"].encode("utf-8")))

        # when you have already favorited a tweet, this error is thrown
        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))


def auto_rt(q, count=100, result_type="recent"):
    """
        Retweets tweets that match a certain phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count, result_type)

    for tweet in result["statuses"]:
        try:
            # don't retweet your own tweets
            if tweet["user"]["screen_name"] == TWITTER_HANDLE:
                continue

            result = t.statuses.retweet(id=tweet["id"])
            print("retweeted: %s" % (result["text"].encode("utf-8")))

        # when you have already retweeted a tweet, this error is thrown
        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))


def get_do_not_follow_list():
    """
        Returns list of users the bot has already followed.
    """

    # make sure the "already followed" file exists
    if not os.path.isfile(ALREADY_FOLLOWED_FILE):
        with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
            out_file.write("")

        # read in the list of user IDs that the bot has already followed in the
        # past
    do_not_follow = set()
    dnf_list = []
    with open(ALREADY_FOLLOWED_FILE) as in_file:
        for line in in_file:
            dnf_list.append(int(line))

    do_not_follow.update(set(dnf_list))
    del dnf_list

    return do_not_follow


def auto_follow(q, count=100, result_type="recent"):
    """
        Follows anyone who tweets about a specific phrase (hashtag, word, etc.)
    """

    result = search_tweets(q, count, result_type)
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    do_not_follow = get_do_not_follow_list()

    for tweet in result["statuses"]:
        try:
            if (tweet["user"]["screen_name"] != TWITTER_HANDLE and
                    tweet["user"]["id"] not in following and
                    tweet["user"]["id"] not in do_not_follow):

                t.friendships.create(user_id=tweet["user"]["id"], follow=False)
                following.update(set([tweet["user"]["id"]]))

                print("followed %s" % (tweet["user"]["screen_name"]))

        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))

            # quit on error unless it's because someone blocked me
            if "blocked" not in str(e).lower():
                quit()


def auto_follow_followers_for_user(user_screen_name, count=100):
    """
        Follows the followers of a user
    """
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers_for_user = set(t.followers.ids(screen_name=user_screen_name)["ids"][:count]);
    do_not_follow = get_do_not_follow_list()

    for user_id in followers_for_user:
        try:
            if (user_id not in following and
                user_id not in do_not_follow):

                t.friendships.create(user_id=user_id, follow=False)
                print("followed %s" % user_id)

        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))

def auto_follow_followers():
    """
        Follows back everyone who's followed you
    """

    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

    not_following_back = followers - following

    for user_id in not_following_back:
        try:
            t.friendships.create(user_id=user_id, follow=False)
        except Exception as e:
            print("error: %s" % (str(e)))


def auto_unfollow_nonfollowers():
    """
        Unfollows everyone who hasn't followed you back
    """

    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

    # put user IDs here that you want to keep following even if they don't
    # follow you back
    users_keep_following = set([])

    not_following_back = following - followers

    # make sure the "already followed" file exists
    if not os.path.isfile(ALREADY_FOLLOWED_FILE):
        with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
            out_file.write("")

    # update the "already followed" file with users who didn't follow back
    already_followed = set(not_following_back)
    af_list = []
    with open(ALREADY_FOLLOWED_FILE) as in_file:
        for line in in_file:
            af_list.append(int(line))

    already_followed.update(set(af_list))
    del af_list

    with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
        for val in already_followed:
            out_file.write(str(val) + "\n")

    for user_id in not_following_back:
        if user_id not in users_keep_following:
            t.friendships.destroy(user_id=user_id)
            print("unfollowed %d" % (user_id))


def auto_mute_following():
    """
        Mutes everyone that you are following
    """
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    muted = set(t.mutes.users.ids(screen_name=TWITTER_HANDLE)["ids"])

    not_muted = following - muted

    # put user IDs of people you do not want to mute here
    users_keep_unmuted = set([])

    # mute all
    for user_id in not_muted:
        if user_id not in users_keep_unmuted:
            t.mutes.users.create(user_id=user_id)
            print("muted %d" % (user_id))


def auto_unmute():
    """
        Unmutes everyone that you have muted
    """
    muted = set(t.mutes.users.ids(screen_name=TWITTER_HANDLE)["ids"])

    # put user IDs of people you want to remain muted here
    users_keep_muted = set([])

    # mute all
    for user_id in muted:
        if user_id not in users_keep_muted:
            t.mutes.users.destroy(user_id=user_id)
            print("unmuted %d" % (user_id))


def is_ascii(s):
        return all(ord(c) < 128 for c in s)


def is_contained(s, l):
    return any(map(lambda e: s in e and s != e, l))


def wait_and_auto_follow(count, trend):
    print "Waiting 4 minute for following %s trend..." % trend
    time.sleep(3 * 60)  # 30 min * 60 seconds
    return auto_follow(trend, count=count)


def distribute_follows_into_trends(count, trends):
    return map(lambda t: wait_and_auto_follow(count=count/len(trends),
                                              trend=t), trends)


def save_followers(amount):
    with open('lastcount.txt', 'w') as f:
        f.write(str(amount))


def load_followers():
    if not os.path.exists('lastcount.txt'):
        save_followers(0)
    with open('lastcount.txt', 'r') as f:
        count = f.read()
    return int(count)


def strategy():
    print "Summing last week results..."
    begin = load_followers()
    auto_rt("lugar", count=1)
    end = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])
    news = len(end) - begin
    save_followers(len(end))
    t.direct_messages.new(screen_name='ecolell',
                          text='%i new followers (%i).' % (news, len(end)))
    print "Projecting next week..."
    huge_group = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    auto_unfollow_nonfollowers()
    better_group = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    posible_group = len(huge_group) if len(huge_group) > 1000 else 1000
    posible_group = (posible_group - len(better_group)) * 1.01
    print "Selecting trends..."
    countries = ['Worldwide', 'Argentina', 'Brazil', 'Chile', 'Spain']
    """
                 'United States', 'Venezuela', 'United Kingdom',
                 'Dominican Republic', 'Ecuador', 'Panama']
    """
    countries = map(lambda i: countries[i],
                    random.sample(xrange(len(countries)), 3))
    places = map(lambda p: p[u'woeid'], filter(lambda p: p['name'] in countries,
                                               t.trends.available()))
    trends = map(lambda p: t.trends.place(_id = p), places)
    trends = map(lambda t: filter(lambda h: not h['promoted_content'],
                                  t[0]['trends']), trends)
    trends = map(lambda t: map(lambda h: h['name'], t), trends)
    trends = set(filter(is_ascii,
                        itertools.chain(*trends)))
    hights = filter(lambda t: is_contained(t, trends), trends)
    trends = list(trends - set(hights))
    selected = map(lambda i: trends[i], random.sample(xrange(len(trends)),
                                                      13 - len(hights)))
    try:
        #print "Following by high trends %i..." % int(posible_group)
        #distribute_follows_into_trends(int(posible_group), hights)
        print "Following by low trends %i..." % int(posible_group)
        distribute_follows_into_trends(int(posible_group), selected)
        auto_rt("lugar", count=1)
        print "Mutting followers..."
        auto_mute_following()
    except Exception:
        pass
    t.direct_messages.new(screen_name='ecolell',
        text='%i new followers (%i).' % (news, len(end)))
    t.direct_messages.new(screen_name='ecolell',
        text='HT: %s' % str(selected)[:170])


if __name__ == "__main__":
    try:
        strategy()
    except Exception, e:
        print e
