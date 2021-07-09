from random import *
import time

class Card():
    color = None
    number = None
    action = None

    def __init__(self, c, n, a):
        self.color = c
        self.number = n
        self.action = a

    def matches(self, other):
        return self.color == other.color or (self.number == other.number and self.number != None) or (self.action == other.action and self.action != None)
     
    def __str__(self):
        return f'{self.color}{self.action or self.number}'

    def __repr__(self):
        return self.__str__()
        
class Deck():
    #cards = ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'rrev', 'rskp', 'r+2', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'brev', 'bskp', 'b+2', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9', 'yrev', 'yskp', 'y+2', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'grev', 'gskp', 'g+2', 'w+4', 'w+4', 'w+0', 'w+0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'rrev', 'rskp', 'r+2', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'brev', 'bskp', 'b+2', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9', 'yrev', 'yskp', 'y+2', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'grev', 'gskp', 'g+2', 'w+4', 'w+4', 'w+0', 'w+0']
    cards = []

    def __init__(self):
        for i in range(2):
            for color in ['r', 'g', 'b', 'y']:
                for num in range(1, 10):
                    self.cards.append(Card(color, num, None))
                for ac in ['+2', 'skip', 'reverse']:
                    self.cards.append(Card(color, None, ac))
            for i in range(2):
                self.cards.append(Card("Wild", None, "+4"))
                self.cards.append(Card("Wild", None, "+0"))
        for color in ['r', 'g', 'b', 'y']:
            self.cards.append(Card(color, 0, None))

    def draw(self, n):
        c = []
        for i in range(n):
            play = choice(self.cards)
            self.cards.remove(play)
            c.append(play)
        return c

class Player():
    hand = []
    name = None

    def __init__ (self, deck, name):
        self.hand = deck.draw(7)
        self.name = name

deck = Deck()

players = []
numofplayers = int(input('Number of players: '))
for i in range(numofplayers):
    players.append(Player(deck, f'Player {i+1}'))

# define discard pile, and initialize it
disPile = deck.draw(1)
def topDisPile():
    return disPile[len(disPile) - 1]
while topDisPile().action != None:
    disPile.extend(deck.draw(1))

# UNO game here

turn = 0
dir = +1

def next():
    global turn
    nextturn = turn + dir
    if nextturn >= len(players):
        nextturn = 0
    elif nextturn < 0:
        nextturn = len(players) - 1
    return nextturn

wildcolor = None

while True:
    print('\n' * 20)  # clear screen
    
    p = players[turn]  # p is the current player

    # print info like hand, discard pile, etc.
    print(p.name)
    print(p.hand)
    print(f'Discard Pile: {topDisPile()}')
    if wildcolor != None:
        print(f'Color: {wildcolor}')
    for x in players:
        if len(x.hand) == 1:
            print(f'{x.name} Has UNO tarjeta (card) left')


    # which card do they want to play?
    selection = int(input(f'Pick a card to play (1-{len(p.hand)}, or 0 to skip turn): '))
    if len(p.hand) >= selection and selection >= 0:
        card = p.hand[selection - 1]
        if card.matches(topDisPile()) or card.color == wildcolor or card.color == "Wild":
            if card.color != 'Wild':  # reset wildcolor
                wildcolor = None
            
            # what kind of card was played?
            if card.action == 'skip':
                turn = next()
            elif card.action == '+2':
                players[next()].hand.extend(deck.draw(2))
            elif card.action == 'reverse':
                dir = dir * -1
            elif card.action == '+0':
                wildcolor = input('Pick a color to change the game to! (r, g, b, y): ')
            elif card.action == "+4":
                wildcolor = input('Pick a color to change the game to! (r, g, b, y): ')
                players[next()].hand.extend(deck.draw(4))
            
            # move card from hand to disacrd pile
            p.hand.remove(card)
            disPile.append(card)
        elif selection == 0:  # skip turn
            p.hand.extend(deck.draw(2))
        else:  # illegal card
            print('You lose because you cheated or made a mistake but im just going to assume you cheated because its funnner so yeah you lose')
            exit()
    
    if len(p.hand) == 1:
        print('UNO')
    elif len(p.hand) == 0:
        print(f'{p.name} WINS!!!  ' *1000 )
        break
    time.sleep(2.5)


    turn = next()  # move to next turn

