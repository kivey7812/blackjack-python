import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

game_on = True


class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


    def __str__(self):
        return self.rank + " of " + self.suit

class Deck():
    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.all_cards.append(card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        card = self.all_cards.pop()
        return card

    def __str__(self):
        for x in self.all_cards:
            print(str(x))
        return " "

class Hand():
    def __init__(self):
        self.hand= []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.hand.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    #CHANGE THIS
    def adjust_for_ace(self):
        while self.value > 21 and self.aces != 0:
            self.value -= 10
            self.aces -= 1

class Chips():

    def __init__(self, total, bet):
        self.total = total
        self.bet = bet

    def win_bet(self):
        self.total += self.bet
        return self.total


    def lose_bet(self):
        self.total -= self.bet
        return self.total

    def bet_returned(self):
        return self.total

    def __str__(self):
        return f"you now have {self.total} chips"

#functions of game play

def hit(deck, hand):
    hand.add_card(deck.deal_one())
    hand.adjust_for_ace()
    return hand

def hit_or_stand(deck, hand, chips):
    global game_on
    choice = input("Type 'H' to hit or 'S' to stand: ")
    if choice == 'H':
        hit(deck, hand)
        print("")
        last_card = hand.hand[-1]
        print(last_card)
        print(f"point value = {hand.value}")
        print("")
        if hand.value >21:
            print("Player busts!")
            print("")
        else:
            hit_or_stand(deck, hand, chips)
    elif choice == 'S':
        game_on = False
    else:
        print(f"Not an acceptable answer.")
        hit_or_stand(deck,hand, chips)
    return

def show_some(player, dealer):
    print("the dealer's visible card:")
    dealer_top_card = dealer.hand[1]
    print(f"   {dealer_top_card}")
    print("")
    print("Player's Cards:")
    for x in player.hand:
        print(f'  {x}')
    print(f"point value = {player.value}")
    print("")
    return

def show_all(player, dealer):
    print("Dealer's cards:")
    for x in dealer.hand:
        print(f'  {x}')
    print(f"point value = {dealer.value}")
    print("")
    print("Player's Cards:")
    for x in player.hand:
        print(f'  {x}')
    print(f"point value = {player.value}")
    print(" ")
    return

#winning scenarios
def player_busts(player, chips):
    print(f"Player hand's value = {player.value}. Player busts! Game over!")
    return chips.lose_bet()

def player_wins(player, chips):
    if player.value == 21:
        print(f"YAY! 21! Player wins!!")
        return chips.win_bet()
    else:
        print(f"Yay! player won!")
        return chips.win_bet()

def dealer_busts(chips):
    print("Dealer busts!! You win!")
    return chips.win_bet()

def dealer_wins(chips):
    print("Uh oh! You lose!! Dealer wins!")
    return chips.lose_bet()

def push(chips):
    print("Tie! Push! Your bet is returned to you")
    return chips.bet_returned()

def take_bet(total):
    #try exception handling
    while True:
        try:
            bet = int(input("How much do you want to bet?"))
        except ValueError:
            print("Sorry, you must enter an integer")
        else:
            if (total - bet) < 0:
                print(f"Uh oh! You only have {total} chips. Place a smaller bet.")
            else:
                break
    return bet

#Main
print("Let's play Blackjack!!!")
player_name = input(" What's your name? ")
print(f"Good luck, {player_name}!")
while True:
    try:
        player_total = int(input("How many chips are you playing with today? "))
        if player_total <= 0:
            raise ValueError
        break
    except ValueError:
        print("Please enter a positive integer!")


#game loops
while True:

    new_deck = Deck()
    new_deck.shuffle()

    dealer_hand = Hand()
    player_hand = Hand()
    for x in range(2):
        dealer_hand.add_card(new_deck.deal_one())
        player_hand.add_card(new_deck.deal_one())



    player_bet = take_bet(player_total)

    current_chips = Chips(player_total, player_bet)

    show_some(player_hand, dealer_hand)

    while game_on:

        hit_or_stand(new_deck, player_hand, current_chips)


        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_total = player_busts(player_hand, current_chips)
            game_on = False

        else:
            while dealer_hand.value < 17:
                hit(new_deck, dealer_hand)

            show_all(player_hand, dealer_hand)
            print("*"*10)

            if dealer_hand.value > 21:
                player_total = dealer_busts(current_chips)
                print(f"{player_name}'s hand = {player_hand.value} points")
                print(f"Dealer hand = {dealer_hand.value} points")
                game_on = False

            elif player_hand.value > dealer_hand.value:
                player_total = player_wins(player_hand, current_chips)
                print(f"{player_name}'s hand = {player_hand.value} points")
                print(f"Dealer's hand = {dealer_hand.value} points")
                game_on = False

            elif player_hand.value < dealer_hand.value:
                player_total = dealer_wins(current_chips)
                print(f"{player_name}'s hand = {player_hand.value} points")
                print(f"Dealer's hand = {dealer_hand.value} points")
                game_on = False

            else:
                player_total = push(current_chips)
                print(f"{player_name}'s hand = {player_hand.value} points")
                print(f"Dealer's hand = {dealer_hand.value} points")
                game_on = False

    print(current_chips)
    print("")
    print("Would you like to play again? Enter 'y' or 'n': ")
    new_game = input("")
    if new_game[0].lower() == 'y':
        game_on = True
        continue
    else:
        print("Thanks for playing!")
        break
