import time
import random

class Card(object):
    """Represents a standard playing card.

    Attributes:
      suit: integer 0-3
      rank: integer 1-13
    """

    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7", 
              "8", "9", "10", "Jack", "Queen", "King"]
    values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
             'Jack':10,'Queen': 10, 'King':10, 'Ace':11}

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank
        self.value = int(self.values[self.rank_names[self.rank]])
        
        
    def __str__(self):
        return '%s of %s' % (Card.rank_names[(self.rank)], Card.suit_names[self.suit])
                  

    def __repr__(self):
        return self.__str__()


class Deck(object):
    """Represents a deck of cards.

    Attributes:
      cards: list of Card objects.
    """
    
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def add_card(self, card):
        """Adds a card to the deck."""
        self.cards.append(card)

    def remove_card(self, card):
        """Removes a card from the deck."""
        self.cards.remove(card)

    def pop_card(self, i=-1):
        """Removes and returns a card from the deck.

        i: index of the card to pop; by default, pops the last card.
        """
        return self.cards.pop(i)

    def shuffle(self):
        """Shuffles the cards in this deck."""
        random.shuffle(self.cards)

    def sort(self):
        """Sorts the cards in ascending order."""
        self.cards.sort()

    def move_cards(self, hand, num):
        """Moves the given number of cards from the deck into the Hand.

        hand: destination Hand object
        num: integer number of cards to move
        """
        for i in range(num):
            hand.add_card(self.pop_card())

class Hand(Deck):
    """Represents a hand of playing cards."""
    
    def __init__(self, label=''):
        self.cards = []
        self.label = label

    def total_value(self):
        total = 0
        for card in self.cards:
            total += card.value
            if total == 21:
                return total
            elif total > 21:
                for card in self.cards:
                    if card.rank_names[card.rank] == 'Ace': 
                       card.value = 1
                       total -= 10
                       return total
        return total

def find_defining_class(obj, method_name):
    """Finds and returns the class object that will provide 
    the definition of method_name (as a string) if it is
    invoked on obj.

    obj: any python object
    method_name: string method name
    """
    for ty in type(obj).mro():
        if method_name in ty.__dict__:
            return ty
    return None


class Player(object):

    def __init__(self, bankroll=100):
        dealer = False
        self.hand = Hand()
        self.bankroll = bankroll
        self.deck = Deck()
        self.deck.shuffle()
        bet = self.bet()

    def hit(self):
        self.deck.move_cards(self.hand, 1)
        
    def doubledown(self):
        self.deck.move_cards(self.hand, 1)
        self.bankroll -= int(self.bet)
        self.bet = int(self.bet)*2
        
    def bet(self):
        print "Here is your bankroll. It currently has $%d in it" %self.bankroll
        is_valid_bet = False
        initial_bet= raw_input("How much would you like to bet?")
        
        while is_valid_bet == False:
            try:
                initial_bet = int(initial_bet)
            except:
                is_valid_bet = False
            if initial_bet <= self.bankroll:
                is_valid_bet = True
            else:
                initial_bet = raw_input("Please place a valid bet.")
                is_valid_bet = False
        print "Alright your current bet is $%s" %initial_bet
        initial_bet = int(initial_bet)
        self.bankroll = self.bankroll - initial_bet
        print "Your bankroll now has $%s in it." %self.bankroll
        print line
        time.sleep(1)
                
        
class Dealer(object):
    
    def __init__(self):
        dealer = True
        self.hand = Hand()
        self.deck = Deck()
        self.deck.shuffle()
        for card in self.hand.cards:
            if card.rank == 'Ace':
                if self.hand.total_value() <= 10:
                    card.value() == 11
                else:
                    card.value() == 1                                         

    def hit(self):
        if self.hand.total_value() <=16: 
            self.deck.move_cards(self.hand, 1)
        print line
        print "Here is the dealer's hand"
        print self.hand
        print self.hand.total_value()

class Blackjack(object):

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer = Dealer()
        self.player = Player()
        self.deck.move_cards(self.player.hand,2)
        self.deck.move_cards(self.dealer.hand, 2)

    def welcome(self):
        name = raw_input("What is your name?")
        name = name.capitalize()
        print "Welcome to the table, %s" % name

    def prompt_instructions(self):
        need_instructions = raw_input("Do you know how to play Blackjack? \
Respond with a 'yes' or 'no'.")
        instructions_response = False
        while instructions_response == False:
            if need_instructions == 'no':
                print instructions
                need_instructions = raw_input("Hit enter to continue")
                instructions_response = True
            elif need_instructions == 'yes':
                instructions_response = True
            else:
                need_instructions = raw_input("I didn't quite catch that. Can you repeat yourself?\
 Remember, I need a 'yes', or a 'no'.")
                instructions_response = False
        print ("Alright let's get started")
        print line
        
    def deal_cards(self):    
        print "Here is your hand."
        print self.player.hand
        print self.player.hand.total_value()
        print line
        time.sleep(2)
        print "Here is the dealer's hand."
        print self.dealer.hand
        print self.dealer.hand.total_value()
        print line
        enter = raw_input("Press enter when you're ready to continue.")
        print line
        
        
    def begin_game(self):
        first_play = raw_input( "What would you like to do? 'double down', 'stay', \
or 'hit' Respond with either the entire word, or 'd', 's', or 'h'")
        first_play_response = False
        while first_play_response == False:
            if first_play == 'double down' or first_play =='d':
                print 'doubled down'
                self.player.doubledown()
                print "Your bet is now",self.player.bet
                first_play_response = True
            elif first_play == 'stay' or first_play == 's':
                print 'Your hand will remain as is.'
                self.player.hand.total_value()
                first_play_response = True
            elif first_play == 'hit' or first_play == 'h':
                self.player.hit()
                self.player.hand.total_value()
                first_play_response = True
            else:
                first_play = raw_input("Respond with either the entire word, \
or a d, s, or h")
        print "Here is your current hand."
        print self.player.hand
        print self.player.hand.total_value()
        if self.player.hand.total_value() > 21:
            print "You bust!"

                                  
line = '-----------------------------------------------------------------------'        
instructions = "The dealer and each player get two cards. The dealer's first\
card faces up, the second faces down. Face cards each count as 10, Aces count\
as 1 or 11, all others count at face value. Any First 2 cards with an Ace with\
any 10, Jack, Queen, or King is a 'Blackjack.' If you have a Blackjack, the\
dealer pays you one-and-a-half times your bet - unless the dealer also has a\
Blackjack, in which case it's a 'push' and neither wins. If you don't have a\
Blackjack, you can ask the dealer to 'hit' you by using a scratching motion\
with your fingers on the table. You may draw as many cards as you like\
(one at a time), but if you go over 21, you 'bust' and lose. If you do not\
want to 'hit,' you may 'stand' by making a side-to-side waving motion with your\
hand. After all players are satisfied with their hands, the dealer will turn his\
or her down card face up and stand or draw as necessary."


"""it still asks what you want to do after you've already busted"""

def run_game():
    game = Blackjack()
    game.welcome()
    game.prompt_instructions()
    game.deal_cards()
    game.begin_game()
    game.dealer.hit()
    while True:
        if game.player.hand.total_value() == 21:
            return "YOU WIN YOU ROCK!"
        elif game.player.hand.total_value() > 21:
            return "Dealer wins, you lose."
        else:
            game.begin_game()
            
        game.dealer.hit()
        
        if game.dealer.hand.total_value() == 21 and game.player.hand.total_value() > 21:
            return "Dealer wins, you lose."
        elif game.dealer.hand.total_value() > 21:
            return "Dealer busted, so YOU WIN YOU ROCK!"
        elif game.player.hand.total_value() <= 21 and game.player.hand.total_value() > game.dealer.hand.total_value():
            return "YOU WIN YOU ROCK!"
        elif game.dealer.hand.total_value() == 21 == game.player.hand.total_value():
            return "Tie. Push game"
        
print run_game()
