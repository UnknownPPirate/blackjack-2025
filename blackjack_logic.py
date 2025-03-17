import random

# Define cards and their values
cards = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}

# Function to deal a card
def deal_card():
    return random.choice(list(cards.keys()))

# Function to calculate the score of a hand
def calculate_score(hand):
    score = sum(cards[card] for card in hand)
    aces = hand.count('A')
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

# Function to determine the result of the game
def determine_result(player_score, dealer_score):
    if player_score > 21:
        return "Bust! You lost."
    elif dealer_score > 21 or player_score > dealer_score:
        return "You won!"
    elif player_score < dealer_score:
        return "You lost."
    else:
        return "It's a tie!"
