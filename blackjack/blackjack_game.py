import pygame
import os
import sys
import time
from regras import *

# Inicialização do Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 1080, 1080
FPS = 60

# Cores
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (100, 149, 237)

# Mapeamento de nomes de arquivos para cartas
def get_card_filename(value, naipe):
    """Converte valor e naipe para nome do arquivo PNG"""
    naipe_map = {
        'Espadas': 'spades',
        'Copas': 'hearts',
        'Paus': 'clubs',
        'Ouros': 'diamonds'
    }
    
    value_map = {
        'A': '01',
        'J': 'Jack',
        'Q': 'Queen',
        'K': 'King'
    }
    
    naipe_folder = naipe_map.get(naipe, naipe.lower())
    
    if value in value_map:
        if value in ['J', 'Q', 'K']:
            filename = f"{value_map[value]}_of_{naipe_folder}_en.png"
        else:
            filename = f"{value_map[value]}_of_{naipe_folder}_01.png"
    else:
        filename = f"{value.zfill(2)}_of_{naipe_folder}.png"
    
    naipe_path_map = {
        'Espadas': 'Espadas',
        'Copas': 'Copas',
        'Paus': 'Paus',
        'Ouros': 'Ouros'
    }
    
    return f"Cartas/{naipe_path_map.get(naipe, naipe)}/{filename}"

class BlackjackGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Blackjack - 2 Jogadores")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Carrega imagens
        self.card_images = {}
        self.load_card_images()
        
        # Carrega carta de fundo
        try:
            self.card_back = pygame.image.load("Cartas/fundo.png")
            self.card_back = pygame.transform.scale(self.card_back, (120, 180))
        except:
            self.card_back = None
        
        # Estado do jogo
        self.PLAYERS = 2
        self.deck = createShuffledDeck(False)
        self.hands = createHands(self.deck, self.PLAYERS)
        self.current_player = 0
        self.game_state = "PLAYING"  # PLAYING, REVEAL, FINISHED

        # Debug: mostra as primeiras cartas
        print("\nCartas iniciais distribuídas:")
        for player_idx in range(self.PLAYERS):
            print(f"Jogador {player_idx + 1}:")
            for carta in self.hands[player_idx][0]:
                print(f"  - {carta.show_card()}")
        
        # Fontes
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
        
    def load_card_images(self):
        """Carrega todas as imagens de cartas PNG"""
        print("Carregando imagens de cartas...")
        for root, dirs, files in os.walk("Cartas"):
            for file in files:
                if file.endswith(".png") and file != "fundo.png":
                    path = os.path.join(root, file)
                    try:
                        img = pygame.image.load(path)
                        img = pygame.transform.scale(img, (120, 180))
                        self.card_images[file] = img
                    except Exception as e:
                        print(f"Erro ao carregar {file}: {e}")
        print(f" {len(self.card_images)} cartas carregadas!")
    
    def get_card_image(self, carta: card):
        """Retorna a imagem da carta"""
        if not carta.isRevealed():
            return self.card_back

        value = carta.getValue()
        naipe = carta.getNaipe()
        filename = get_card_filename(value, naipe)

        # Tenta encontrar a imagem pelo nome exato
        basename = os.path.basename(filename)
        if basename in self.card_images:
            return self.card_images[basename]

        # Se não encontrar, tenta buscar por valor
        for key in self.card_images.keys():
            if value.lower() in key.lower() and naipe.lower()[:3] in key.lower():
                return self.card_images[key]

        return self.card_back
    
    def handle_events(self):
        """Processa eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.game_state == "PLAYING":
                    self.deal_card()
                elif event.key == pygame.K_RETURN and self.game_state == "PLAYING":
                    self.pass_turn()
                elif event.key == pygame.K_s and self.game_state == "PLAYING":
                    self.try_split()
    
    def deal_card(self):
        """Distribui uma carta para o jogador atual"""
        if calculateFaceUp(self.hands[self.current_player]) < 21:
            dealCards(self.hands[self.current_player], self.deck)

    def pass_turn(self):
        """Passa a vez para o próximo jogador"""
        self.current_player += 1
        if self.current_player >= self.PLAYERS:
            print("\n⏳ Finalizando jogo e revelando cartas...")
            self.reveal_all_cards()
            # Força um redesenho imediato após revelar
            self.draw()
            pygame.display.flip()

    def try_split(self):
        """Tenta fazer split das cartas"""
        player_hand = self.hands[self.current_player]

        # Verifica se pode fazer split:
        # 1. Deve ter apenas uma mão (não pode split após split)
        # 2. A mão deve ter exatamente 2 cartas
        # 3. As duas cartas devem ter o mesmo valor
        if len(player_hand) == 1 and len(player_hand[0]) == 2:
            carta1 = player_hand[0][0].getValue()
            carta2 = player_hand[0][1].getValue()

            # Considera J, Q, K como iguais (todos valem 10)
            def normalize_value(val):
                if val in ['J', 'Q', 'K']:
                    return '10'
                return val

            if normalize_value(carta1) == normalize_value(carta2):
                splitCards(player_hand, self.deck)
                print(f"Split realizado! Jogador {self.current_player + 1} agora tem 2 mãos")
            else:
                print(f"Split não permitido: cartas diferentes ({carta1} e {carta2})")
        else:
            if len(player_hand) > 1:
                print("Split não permitido: já foi feito um split")
            else:
                print(f"Split não permitido: precisa ter exatamente 2 cartas (tem {len(player_hand[0])})")

    def reveal_all_cards(self):
        """Revela todas as cartas e calcula vencedor"""
        print("\nRevelando todas as cartas...")
        self.board = [[i, 0] for i in range(self.PLAYERS)]

        for index, hand in enumerate(self.hands):
            print(f"\nJogador {index + 1}:")
            for hand_idx, chance in enumerate(hand):
                # Força a revelação de todas as cartas
                for carta in chance:
                    if not carta.isRevealed():
                        carta.reveal_card()
                        print(f"  Revelando: {carta.show_card()}")

                points = revealCards(chance)
                self.board[index][1] += points - 21 if points < 21 else 21 - points
                print(f"  Mão {hand_idx + 1}: {points} pontos")

        self.board.sort(key=lambda x: -x[1])
        self.game_state = "FINISHED"
        print(f"\n🏆 Vencedor: Jogador {self.board[0][0] + 1}")
        print(f"Placar: {self.board}")

    def draw(self):
        """Desenha todos os elementos na tela"""
        self.screen.fill(GREEN)

        # Título com fundo
        title = self.font_large.render("♠ BLACKJACK ♥", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 40))
        # Fundo escuro para o título
        pygame.draw.rect(self.screen, BLACK, title_rect.inflate(40, 20), border_radius=10)
        self.screen.blit(title, title_rect)

        # Desenha o cava (monte de cartas) - mais bonito
        if self.card_back:
            cava_x = WIDTH - 250
            cava_y = 100

            # Fundo para o cava
            pygame.draw.rect(self.screen, (0, 80, 0), (cava_x - 20, cava_y - 40, 200, 280), border_radius=15)
            pygame.draw.rect(self.screen, YELLOW, (cava_x - 20, cava_y - 40, 200, 280), 3, border_radius=15)

            # Texto "CAVA"
            cava_text = self.font_medium.render("CAVA", True, YELLOW)
            self.screen.blit(cava_text, (cava_x + 20, cava_y - 30))

            # Pilha de cartas
            for i in range(5):
                offset = i * 3
                self.screen.blit(self.card_back, (cava_x + offset, cava_y + offset))

            # Contador de cartas
            counter = self.font_small.render(f"{len(self.deck)} cartas", True, WHITE)
            self.screen.blit(counter, (cava_x + 15, cava_y + 200))

        # Desenha as mãos dos jogadores - mais espaçadas
        y_positions = [150, 580]

        for player_idx in range(self.PLAYERS):
            y_pos = y_positions[player_idx]

            # Área do jogador com fundo
            player_area_height = 350
            pygame.draw.rect(self.screen, (0, 100, 0),
                           (20, y_pos - 80, WIDTH - 40, player_area_height),
                           border_radius=20)

            # Borda da área do jogador
            if self.game_state == "PLAYING" and player_idx == self.current_player:
                border_color = YELLOW
                border_width = 5
            else:
                border_color = (0, 150, 0)
                border_width = 3

            pygame.draw.rect(self.screen, border_color,
                           (20, y_pos - 80, WIDTH - 40, player_area_height),
                           border_width, border_radius=20)

            # Nome do jogador - ACIMA da área das cartas
            player_name = f"JOGADOR {player_idx + 1}"
            if self.game_state == "PLAYING" and player_idx == self.current_player:
                player_name += " ⭐ SUA VEZ ⭐"
                name_color = YELLOW
            else:
                name_color = WHITE

            name_text = self.font_large.render(player_name, True, name_color)
            self.screen.blit(name_text, (50, y_pos - 65))

            # Pontuação - ao lado do nome
            # Se o jogo terminou, calcula com todas as cartas reveladas
            if self.game_state == "FINISHED":
                points = 0
                for chance in self.hands[player_idx]:
                    for carta in chance:
                        if not carta.isRevealed():
                            carta.reveal_card()
                    points += revealCards(chance)
            else:
                points = calculateFaceUp(self.hands[player_idx])

            # Cor da pontuação baseada no valor
            if points > 21:
                points_color = RED
                points_status = "ESTOUROU!"
            elif points == 21:
                points_color = YELLOW
                points_status = "BLACKJACK!"
            else:
                points_color = WHITE
                points_status = ""

            points_text = self.font_large.render(f"Pontos: {points}", True, points_color)
            self.screen.blit(points_text, (WIDTH - 400, y_pos - 65))

            if points_status:
                status_text = self.font_medium.render(points_status, True, points_color)
                self.screen.blit(status_text, (WIDTH - 400, y_pos - 30))

            # Desenha as cartas - ABAIXO do nome
            x_offset = 50
            for hand_idx, hand in enumerate(self.hands[player_idx]):
                if len(self.hands[player_idx]) > 1:
                    # Mostra número da mão se houver split - ACIMA das cartas
                    hand_label = self.font_medium.render(f"Mão {hand_idx + 1}", True, YELLOW)
                    self.screen.blit(hand_label, (x_offset, y_pos + 10))
                    card_y = y_pos + 50
                else:
                    card_y = y_pos + 20

                for card_idx, carta in enumerate(hand):
                    card_x = x_offset + card_idx * 140

                    # Obtém a imagem da carta (revelada ou virada)
                    card_img = self.get_card_image(carta)

                    if card_img:
                        # Sombra da carta
                        shadow_rect = pygame.Rect(card_x + 5, card_y + 5, 120, 180)
                        pygame.draw.rect(self.screen, (0, 0, 0, 128), shadow_rect, border_radius=10)

                        # Carta
                        self.screen.blit(card_img, (card_x, card_y))
                    else:
                        # Fallback: desenha retângulo se não tiver imagem
                        if carta.isRevealed():
                            pygame.draw.rect(self.screen, WHITE, (card_x, card_y, 120, 180), border_radius=10)
                            pygame.draw.rect(self.screen, BLACK, (card_x, card_y, 120, 180), 2, border_radius=10)
                            value_text = self.font_medium.render(carta.getValue(), True, BLACK)
                            self.screen.blit(value_text, (card_x + 40, card_y + 70))
                        else:
                            pygame.draw.rect(self.screen, BLUE, (card_x, card_y, 120, 180), border_radius=10)
                            pygame.draw.rect(self.screen, BLACK, (card_x, card_y, 120, 180), 2, border_radius=10)

                x_offset += len(hand) * 140 + 80

        # Instruções - Painel no lado direito inferior
        if self.game_state == "PLAYING":
            # Fundo do painel de instruções - reposicionado
            panel_x = WIDTH - 450
            panel_y = HEIGHT - 200
            panel_rect = pygame.Rect(panel_x, panel_y, 420, 180)
            pygame.draw.rect(self.screen, (0, 0, 0, 200), panel_rect, border_radius=15)
            pygame.draw.rect(self.screen, YELLOW, panel_rect, 3, border_radius=15)

            # Título do painel
            title_text = self.font_medium.render("CONTROLES", True, YELLOW)
            self.screen.blit(title_text, (panel_x + 20, panel_y + 10))

            instructions = [
                ("ESPAÇO", "Pedir carta"),
                ("ENTER", "Passar vez"),
                ("S", "Split (2 iguais)"),
                ("ESC", "Sair")
            ]
            y = panel_y + 50
            for key, action in instructions:
                key_text = self.font_small.render(key, True, YELLOW)
                action_text = self.font_small.render(f"- {action}", True, WHITE)
                self.screen.blit(key_text, (panel_x + 20, y))
                self.screen.blit(action_text, (panel_x + 120, y))
                y += 30

        elif self.game_state == "FINISHED":
            # Painel de vencedor 
            panel_width = 800
            panel_height = 300
            panel_x = WIDTH // 2 - panel_width // 2
            panel_y = HEIGHT // 2 - panel_height // 2

            # Fundo do painel
            panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
            pygame.draw.rect(self.screen, (0, 50, 0), panel_rect, border_radius=20)
            pygame.draw.rect(self.screen, YELLOW, panel_rect, 5, border_radius=20)

            # Texto de vencedor
            winner_text = self.font_large.render(
                f"🏆 VENCEDOR: JOGADOR {self.board[0][0] + 1}! 🏆",
                True, YELLOW
            )
            winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
            self.screen.blit(winner_text, winner_rect)

            # Placar
            for idx, (player, score) in enumerate(self.board):
                score_text = self.font_medium.render(
                    f"Jogador {player + 1}: {score} pontos",
                    True, WHITE
                )
                self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20 + idx * 40))

            restart_text = self.font_small.render("Pressione ESC para sair", True, WHITE)
            self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 120))

        pygame.display.flip()

    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BlackjackGame()
    game.run()


