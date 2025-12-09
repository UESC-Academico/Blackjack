import random
import time

# Inicializa o gerador de números aleatórios com timestamp
random.seed(time.time())

def evaluateCardValue(card: str, handValue:int) -> int:
    extra = ['J', 'Q', 'K']
    if card in extra:
        return 10
    elif card == 'A':
        if (handValue + 11) <= 21:
            return 11
        return 1
    elif card.lower() == 'joker':
        if handValue < 21:
            return 21 - handValue
        return 0
    return int(card)

def createDeck(Joker: bool = True) -> list:
    naipes = ['Espadas', 'Copas', 'Diamantes', 'Ouros']
    values = ['A']
    for i in range (2, 11):
        values.append(str(i))
    values.extend(['J', 'Q', 'K'])
    deck = []
    for naipe in naipes:
        for value in values:
            deck.append((value, naipe))
    if Joker:
        deck.append(('Joker', 'Preto'))
        deck.append(('Joker', 'Vermelho'))
    return deck

def createShuffledDeck(Joker: bool = True) -> list:
    naipes = ['Espadas', 'Copas', 'Paus', 'Ouros']
    values = ['A']
    for i in range (2, 11):
        values.append(str(i))
    values.extend(['J', 'Q', 'K'])
    deck = []
    for naipe in naipes:
        for value in values:
            deck.append((value, naipe))
    if Joker:
        deck.append(('Joker', 'Preto'))
        deck.append(('Joker', 'Vermelho'))
    random.shuffle(deck)
    return deck

class card():
    def __init__(self, value_naipe: tuple, faceup = True):
        self.__value = value_naipe[0]
        self.__naipe = value_naipe[1]
        self.__faceup = faceup
    def show_card(self) -> str:
        if self.__faceup:
            return f'{self.__value} de {self.__naipe}'
        return f'Virada'
    def reveal_card(self) -> None:
        self.__faceup = True
    def isRevealed(self) -> bool:
        return self.__faceup
    def getValue(self) -> str:
        return self.__value
    def getNaipe(self) -> str:
        return self.__naipe

def createHands(deck: list, players: int ,start: int = 2) -> list[list[list[card]]]:
    player_hands:list[list[list]] = [[[]] for _ in range(players)]
    for i in range(start):
        for player in range(players):
            # OPÇÃO 2: Multiplayer - Todos têm primeira carta virada
            # Primeira carta virada (False), segunda revelada (True)
            if i == 0:
                carta_atual = card(deck.pop(0), False)  # Primeira carta: virada
            else:
                carta_atual = card(deck.pop(0), True)   # Segunda carta: revelada
            player_hands[player][0].append(carta_atual)
    return player_hands

def revealCards(player_hand: list[card]) -> int:
    points = 0
    for carta in player_hand:
        if not carta.isRevealed():
            carta.reveal_card()
        points += evaluateCardValue(carta.getValue(), points)
    return points

def calculateFaceUp(player_hand: list[list[card]]) -> int:
    points = [0 for _ in range(len(player_hand))]
    for chance in range(len(player_hand)):
        for cart in player_hand[chance]:
            if cart.isRevealed():
                points[chance] += evaluateCardValue(cart.getValue(), points[chance])
    return points

def dealCards(player_hand: list[list[card]], deck: list) -> None:
            for chance in player_hand:
                chance.append(card(deck.pop(0)))
                showHand(chance)

def splitCards(player_hand: list[list[card]], deck: list) -> None:
        # Remove a última carta da primeira mão e cria uma nova mão com ela
        carta_removida = player_hand[0].pop(-1)
        # Adiciona uma nova carta para cada mão
        #player_hand[0].append(card(deck.pop(0), True))  # Nova carta para primeira mão
        player_hand.append([card(deck.pop(0), False), carta_removida])  # Nova mão com carta removida + nova carta

def options(player_hand: list[list[card]], deck:list) -> None:
    while input("\nDeal? Y/N\n->")[0].lower() == "y" and calculateFaceUp(player_hand) < 21:
        dealCards(player_hand, deck)
        if len(player_hand) == 1 and len(player_hand[0]) == 3:
            if input("\nSplit? Y/N\n->")[0].lower() == "y":
                splitCards(player_hand, deck)
                for chance in player_hand:
                    showHand(chance)

def showHand(hand: list[card]):
    for cart in hand:
        print(cart.show_card(), end=", ")
    print("\b\b ")

def evalPoints(points: int) -> str:
    if points > 21:
        return f'Passou com {points}'
    elif points == 21:
        return f'BlackJack! Fez {points}!'
    return f'Abaixo com {points}'

# Código executável apenas quando rodar diretamente (modo texto)
if __name__ == "__main__":
    PLAYERS = 2
    deck = createShuffledDeck(False)
    hands = createHands(deck, PLAYERS)
    board = [[i, 0] for i in range(PLAYERS)]


    for i in range(PLAYERS):
        print(f"\nVez do jogador: {i + 1}")
        print(f"Mão do jogador {i + 1}: ", end=' ')
        for hand_count, chance in enumerate(hands[i]):
            print(f"Chance  {hand_count + 1}: ")
            showHand(chance)
        options(hands[i], deck)

    for index, hand in enumerate(hands):
        print(f"Mão(s) do jogador {index + 1}: ")
        for hand_count, chance in enumerate(hand):
            points = revealCards(chance)

            board[index][1] += points - 21 if points < 21 else 21 - points

            print(f'{evalPoints(points)}')
            print(f"Mão {hand_count + 1}: ", end=" ")
            showHand(chance)
            print()
        print()
    board.sort(key= lambda x: -x[1])
    print(board)
    print(f"Ganhador: Jogador {board[0][0] + 1}")