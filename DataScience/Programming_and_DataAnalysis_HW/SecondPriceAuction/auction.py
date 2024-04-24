"""The Second-Price Auction program models an ad auction. where bidders
compete to show a user their ad, which results in a reward if the
user clicks it. The objective is to finish the game with as high a
balance as possible. It contains 2 modules: auction_lastname.py (this
module) and bidder_lastname.py

auction_lastname.py: This is the main program which contains the User
and Auction classes. It initializes and runs the online auction from 
the Auction class, which has the following rules:
1. User is chosen with equal probability in each round
2. Bidders place bids and the winner shows the User their ad.
3. User may/may not click the ad and winning Bidder observes this.
4. Winning Bidder's balance is increased by 1 only if the User
clicked and decreased by the winning price regardless.

It imports numpy and functions (excluding magic functions) include:
User: `show_ad`
Auction: `execute_round`
"""


import numpy as np


class User:
    """Class representing a user with a secret probability of clicking
    an ad.
    """

    def __init__(self):
        """Generating a probability between 0 and 1 from a uniform
        distribution."""
        self.__probability = np.random.uniform()

    def __str__(self):
        """User object with secret probability"""
        return ("User object with secret probability: " + 
                str(self.__probability ))

    def __repr__(self):
        """User object with a secret likelihood of clicking on an ad"""
        return str(self)

    def show_ad(self):
        """Returns True to represent the user clicking on an ad or
        False otherwise
        """
        return np.random.choice([True, False],
                    p = [self.__probability, 1-self.__probability])

class Auction:
    """Class representing an online second-price ad auction"""

    def __init__(self, users, bidders):
        """Initializing user, bidders, and a dictionary to store 
        balances for each bidder in the auction. There are num_users
        Users, numbered from 0 to num_users - 1. The number 
        corresponding to a user is its user_id. 
        """
        #Create a list of these user_ids to access in the auction.
        self.users = users
        self.user_id_list = np.arange(0,len(self.users))
        self.bidders = bidders 
        self.balances = {bidder: 0 for bidder in self.bidders}

    def __str__(self):
        """Return auction object with users and qualified bidders"""
        return ("Auction object with" + str(self.users) + "users and "
                 + str(self.bidders))

    def __repr__(self):
        """Return auction object with users and qualified bidders"""
        return str(self)

    def execute_round(self):
        """Executes a single auction round with the following steps:
            - random user selection
            - bids from every qualified bidder in the auction
            - selection of winning bidder based on maximum bid
            - selection of actual price (second-highest bid)
            - show ad to user and find out whether or not they click
            - notify winning bidder of price and user outcome and
            update their balance
            - notify losing bidders of winning price
            """
        # Set max_bid, winning Bidder (winner), and winning price
        max_bid = 0
        winner = None
        winning_price = 0

        # Select a user at random
        rand_user_id = np.random.choice(self.user_id_list)

        # For each Bidder, provide the randomly selected User ID to
        # make a bid (non-negative $ amount). If the Bidder's
        # balance goes below $ -1000, then the Bidder will be
        # disqualified from the Auction and further bidding. Add
        # all elligble bids and elligible bidders to an array.
        # Bidders don't know eachothers' bids.
        final_bids = np.array([])
        final_bidders = np.array([])
        for bidder in self.bidders:
            if self.balances[bidder] < -1000:
                self.bidders.remove(bidder)
            else:
                bid = bidder.bid(rand_user_id)
                if bid >= 0:
                    final_bids = np.append(final_bids, bid)
                    final_bidders = np.append(final_bidders, bidder)

        # If there are one or more Bidders with valid bids, have
        # auction. If not, skip auction and notify Bidders below
        if len(final_bids) > 0:

            # If only 1 Bidder submitted a valid bid, they win
            # and their bid is the max_bid and the winning_price.
            if len(final_bids) == 1:
                max_bid = final_bids[0]
                winner = final_bidders[0]
                final_bids = []
                winning_price = max_bid
            else:
                # Sort the bids array and identify ties.
                bids_sort = np.sort(final_bids)
                bids_sort_idx = np.argsort(final_bids)
                ties = bids_sort_idx[bids_sort == bids_sort[-1]]

                # In case of a tie, select one of the max Bidders at
                # random with equal probability, set the max_bid value
                # as the winning_price, and remove the winner's max_bid
                # from the bids array.
                if len(ties) > 1:
                    max_bidder_idx = np.random.choice(ties)
                    max_bid =  final_bids[max_bidder_idx]
                    winner = final_bidders[max_bidder_idx]
                    final_bids = np.delete(final_bids, max_bidder_idx)
                    winning_price = max_bid

                # If no tie, set the highest bid as max_bid and the
                # corresponding Bidder as winner. Remove the max bid
                # from the bids array and assign the second highest
                # bid to winning_price.
                else:
                    max_bidder_idx = bids_sort_idx[-1]
                    max_bid = bids_sort[-1]
                    winner = final_bidders[max_bidder_idx]
                    final_bids = np.delete(final_bids, max_bidder_idx)
                    winning_price = bids_sort[-2]

        # Show the winning bidder's ad to the selected User.
        clicked = self.users[rand_user_id].show_ad()

        # Notify each Bidder of the auction results.
        for bidder in self.bidders:

            # If the bidder is a winner, notify them they won,
            # the price and if the user clicked. If user clicked,
            # increase winner's balance by 1. Regardless decrease
            # winner's balance by the winning price.
            if bidder == winner:
                bidder.notify(True, winning_price, clicked)
                if clicked:
                    self.balances[bidder] += 1
                self.balances[bidder] -= winning_price

            # If bidder is not the winner, notify they did not win and
            # the winning price.
            else:
                bidder.notify(False, winning_price, None)