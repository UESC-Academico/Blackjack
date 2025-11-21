import pygame
import sys
from enum import Enum

# Inicialização do Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Cores
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
CARD_WHITE = (240, 240, 240)
CARD_BORDER = (50, 50, 50)

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.width = 80
        self.height = 120
        
    def get_display_rank(self):
        """Retorna a representação visual do rank"""
        if self.rank == 1:
            return "A"
        elif self.rank == 11:
            return "J"
        elif self.rank == 12:
            return "Q"
        elif self.rank == 13:
            return "K"
        else:
            return str(self.rank)
    
    def get_color(self):
        """Retorna a cor do naipe"""
        if self.suit in [Suit.HEARTS, Suit.DIAMONDS]:
            return RED
        return BLACK
    
    def draw_suit_symbol(self, surface, x, y, size, color):
        """Desenha o símbolo do naipe graficamente"""
        if self.suit == Suit.HEARTS:
            # Desenha um coração
            pygame.draw.circle(surface, color, (x - size//4, y), size//3)
            pygame.draw.circle(surface, color, (x + size//4, y), size//3)
            points = [(x - size//2, y + size//6), (x, y + size), (x + size//2, y + size//6)]
            pygame.draw.polygon(surface, color, points)
        elif self.suit == Suit.DIAMONDS:
            # Desenha um diamante
            points = [(x, y - size//2), (x + size//2, y), (x, y + size//2), (x - size//2, y)]
            pygame.draw.polygon(surface, color, points)
        elif self.suit == Suit.CLUBS:
            # Desenha um trevo (três círculos e um triângulo)
            pygame.draw.circle(surface, color, (x, y - size//3), size//3)
            pygame.draw.circle(surface, color, (x - size//3, y + size//6), size//3)
            pygame.draw.circle(surface, color, (x + size//3, y + size//6), size//3)
            points = [(x - size//6, y + size//3), (x + size//6, y + size//3), (x, y + size//2)]
            pygame.draw.polygon(surface, color, points)
        elif self.suit == Suit.SPADES:
            # Desenha uma espada (círculo, triângulo invertido e haste)
            pygame.draw.circle(surface, color, (x, y + size//6), size//3)
            points = [(x, y - size//2), (x - size//2, y + size//6), (x + size//2, y + size//6)]
            pygame.draw.polygon(surface, color, points)
            points = [(x - size//6, y + size//4), (x + size//6, y + size//4), (x, y + size//2)]
            pygame.draw.polygon(surface, color, points)

    def draw(self, surface, x, y):
        """Desenha a carta na posição especificada"""
        # Desenha o fundo branco da carta
        pygame.draw.rect(surface, CARD_WHITE, (x, y, self.width, self.height))

        # Desenha a borda
        pygame.draw.rect(surface, CARD_BORDER, (x, y, self.width, self.height), 2)

        # Fonte para o rank
        font_large = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)

        color = self.get_color()
        rank_text = self.get_display_rank()

        # Desenha o rank no canto superior esquerdo
        rank_surface = font_large.render(rank_text, True, color)
        surface.blit(rank_surface, (x + 10, y + 10))

        # Desenha o naipe pequeno no canto superior esquerdo (abaixo do rank)
        self.draw_suit_symbol(surface, x + 20, y + 55, 12, color)

        # Desenha o naipe grande no centro
        self.draw_suit_symbol(surface, x + self.width // 2, y + self.height // 2, 24, color)

        # Desenha o rank no canto inferior direito (invertido)
        rank_surface_bottom = font_small.render(rank_text, True, color)
        surface.blit(rank_surface_bottom,
                    (x + self.width - 25, y + self.height - 35))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Blackjack")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Cria algumas cartas de exemplo
        self.cards = [
            Card(1, Suit.SPADES),      # Ás de Espadas
            Card(13, Suit.HEARTS),     # Rei de Copas
            Card(7, Suit.DIAMONDS),    # 7 de Ouros
            Card(10, Suit.CLUBS),      # 10 de Paus
        ]
        
    def handle_events(self):
        """Processa eventos do Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Atualiza a lógica do jogo"""
        pass
    
    def draw(self):
        """Desenha todos os elementos na tela"""
        # Fundo verde (mesa de blackjack)
        self.screen.fill(GREEN)
        
        # Título
        font_title = pygame.font.Font(None, 48)
        title = font_title.render("BLACKJACK", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Desenha as cartas em uma linha
        start_x = 150
        start_y = 250
        spacing = 120
        
        for i, card in enumerate(self.cards):
            card.draw(self.screen, start_x + i * spacing, start_y)
        
        # Instruções
        font_small = pygame.font.Font(None, 24)
        instruction = font_small.render("Pressione ESC para sair", True, WHITE)
        self.screen.blit(instruction, (10, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

