"""The Second-Price Auction program models an ad auction. where bidders
compete to show a user their ad, which results in a reward if the
user clicks it. The objective is to finish the game with as high a
balance as possible. It contains 2 modules: auction_lastname.py and
bidder_lastname.py (this module)

bidder_lastname.py: This module contains a Bidder class that represents
a bidder in the online auction. It implements a bidding algorithm using
the Epsilon-Greedy, multi-armed bandit strategy. Its purpose is to gain
the highest balance possible.

It imports numpy and functions (excluding magic functions) include:
`bid` and `notify`
"""


import numpy as np


class Bidder:
    """Class representing a bidder in an online second-price ad auction
    """

    def __init__(self, num_users, num_rounds):
        """Creates a bidder with attributes that track users' behavior
        and algorithm performance to refine bidding strategy. Takes
        number of users and number of auction rounds, sets epsilon to
        0.01 for the greedy bidder strategy, tracks balance to
        """
        self.num_rounds = num_rounds
        self.round_counter = 0
        self.num_users = num_users
        self.epsilon = 0.01

        # Track performance metrics to improve our bidding strategy.
        # Balance to ensure we stay above -$1000 cut off, the winning
        # price per round, how many times we won/lost the auction with
        # the given user, our rewards per user (the +1 if they
        # clicked), and our score per user (win ratio: click/win),
        # respectively to each metric below:
        self.__balance = 0
        self.price_history = np.array([0] * self.num_rounds,
                                       dtype = np.float64)
        self.win_per_user = np.array([0] * self.num_users, 
                                     dtype = np.float64)
        self.click_per_user = np.array([0] * self.num_users, 
                                     dtype = np.float64)
        self.score_per_user = np.array([0] * self.num_users, 
                                     dtype = np.float64)

        # Set the first price to a random value to begin auction, set
        # a max score variable to identify the max win/ratio so far,
        # a set of all the best possible users, current rounds's user id.
        self.price_history[0] = np.round(np.random.uniform(0,1), 3)
        self.max_score = 0
        self.best_users = set()
        self.user_id = None

    def __str__(self):
        """Return Bidder object with balance"""
        return "Bidder object with balance $" + str(self.__balance)

    def __repr__(self):
        """Return Bidder object with balance""" 
        return str(self)

    def bid(self, user_id):
        """Returns a non-negative bid amount in dollars rounded to 3
        decimal places. Takes the User's ID and performs these steps:
        1. Set upper limit for our bid based on previous winning price
        2. With the given user's performance either:
            a. With probability epsilon, we choose a random bid
            b. Bid the upper limit if they have good performance
            c. Bid 0/don't bid if they have bad performance
        """
        # Obtain the last winning price and set user id
        self.user_id = user_id
        upper_limit = np.round(np.sort(self.price_history)[-1], 3)

        # With probability epsilon, we choose a random bid. If that
        # bid causes you to go below $-1000 cut off, choose again
        if np.random.uniform() < self.epsilon:
            rand_bid = np.random.uniform(0, upper_limit)
            while self.__balance - rand_bid <= -1000:
                rand_bid = np.random.uniform(0, upper_limit)
            return np.round(np.random.uniform(0, upper_limit), 3)
        
        else:
            # If the upper limit bid causes us to go below $-1000 
            # cut off, then obtain the next highest bid by progressivly
            # dividing the upper limit by a value 2 to upper limit val.
            if self.__balance-upper_limit <= -1000:
                for i in np.arange(2,upper_limit):
                    if self.__balance-(upper_limit/i) > -1000:
                        upper_limit = np.round(upper_limit/i,3)

            # If user's score is equal to our max_score, add it
            # to bests_users list and bid upper limit. 
            if self.score_per_user[user_id] == self.max_score:
                self.best_users.add(user_id)
                return upper_limit
                      
            # If it's greater than max score, reset best users list
            # since this user is our new best, set new max score to
            # this user's score, and bid upper limit
            elif self.score_per_user[user_id] > self.max_score:
                self.best_users = {user_id}
                self.max_score = self.score_per_user[user_id]
                return upper_limit

            # If it's neither of above, but it's in best_users, bid
            # upper limit. Else if it's lower than max score, but not
            # the lowest score, bid randomly between 0 and upper limit.
            # Else if it is the lowest score, do not bid.
            elif user_id in self.best_users:
                return upper_limit
            else:
                if (self.score_per_user[user_id] !=
                    np.sort(self.score_per_user)[0]):
                    return np.round(np.random.uniform(0, upper_limit),)
                else:
                    return np.round(0,3)

    def notify(self, auction_winner, price, clicked):
        """Updates bidder attributes based on results from an
        auction round. Takes in these values:
        auction_winner: True == won, False == lost (boolean)
        price: Amount of second bid which winner pays (float)
        clicked: If Bidder won, Clicked == True/False, if
            bidder lost, Clicked will always be None.
        """
        # If user clicked, increase winner's balance by 1.
        # Regardless decrease winner's balance by winning price.
        if auction_winner:
            if clicked:
                self.click_per_user[self.user_id] += 1
                self.__balance += 1
            self.__balance -= np.round(price, 3)

        # Track metrics for our bidding strategy then reset user id
        self.win_per_user[self.user_id] += 1
        self.price_history = np.append(self.price_history, price)
        self.score_per_user[self.user_id] = self.click_per_user[self.user_id]\
                                            /self.win_per_user[self.user_id]
        self.user_id = None
        self.round_counter += 1