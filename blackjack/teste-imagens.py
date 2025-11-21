import pygame
import os
import random

pygame.init()

# Tamanho da janela
WIDTH, HEIGHT = 1080, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teste de Cartas - Blackjack")

# Caminho base das cartas
cartas_path = "Cartas"

# Dicionário para armazenar imagens
cartas = {}

print(" Carregando cartas PNG...\n")

# Percorre todos os arquivos e subpastas
for root, dirs, files in os.walk(cartas_path):
    for file in files:
        if file.endswith(".png"):

            nome = file.replace(".png", "")  # Ex: "01_of_spades"

            caminho = os.path.join(root, file)

            try:
                print(f"Carregando: {nome}")

                img = pygame.image.load(caminho)
                img = pygame.transform.scale(img, (120, 180))

                cartas[nome] = img

            except Exception as e:
                print(f" Erro ao carregar {nome}: {e}")

print(f"\nTotal de cartas carregadas: {len(cartas)}")

# Carrega a imagem do fundo (verso da carta)
try:
    carta_fundo = pygame.image.load("Cartas/fundo.png")
    carta_fundo = pygame.transform.scale(carta_fundo, (120, 180))
    print("Carta de fundo (verso) carregada!")
except Exception as e:
    print(f" Erro ao carregar fundo.png: {e}")
    carta_fundo = None

# -----------------------------
#  NOVA PARTE: DISTRIBUIÇÃO
# -----------------------------

# Lista com os nomes das cartas disponíveis
todas_as_cartas = list(cartas.keys())

# Lista com cartas já distribuídas
cartas_em_jogo = []


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Quando apertar espaço → distribuir carta
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                if len(todas_as_cartas) > 0:
                    carta_escolhida = random.choice(todas_as_cartas)
                    todas_as_cartas.remove(carta_escolhida)
                    cartas_em_jogo.append(cartas[carta_escolhida])

                    print(f"→ Carta distribuída: {carta_escolhida}")
                else:
                    print("Não há mais cartas disponíveis!")


    # -------------------------
    #  Desenho visual
    # -------------------------
    screen.fill((0, 120, 0))  # Fundo de mesa verde

    # Desenha o "CAVA" (monte de cartas viradas) no centro superior
    if carta_fundo:
        cava_x = WIDTH // 2 - 60  # Centraliza
        cava_y = 150

        # Desenha várias cartas empilhadas para dar efeito de monte
        for i in range(5):
            offset = i * 2  # Pequeno deslocamento para dar efeito de pilha
            screen.blit(carta_fundo, (cava_x + offset, cava_y + offset))

        # Texto "CAVA" acima do monte
        font = pygame.font.Font(None, 36)
        texto_cava = font.render("CAVA", True, (255, 255, 255))
        texto_rect = texto_cava.get_rect(center=(WIDTH // 2, 100))
        screen.blit(texto_cava, texto_rect)

        # Contador de cartas restantes
        font_small = pygame.font.Font(None, 28)
        texto_contador = font_small.render(f"{len(todas_as_cartas)} cartas", True, (255, 255, 255))
        contador_rect = texto_contador.get_rect(center=(WIDTH // 2, cava_y + 200))
        screen.blit(texto_contador, contador_rect)

    # Instruções
    font_instrucao = pygame.font.Font(None, 24)
    instrucao = font_instrucao.render("Pressione ESPAÇO para distribuir carta", True, (255, 255, 255))
    screen.blit(instrucao, (20, HEIGHT - 40))

    #  Mostrar cartas distribuídas
    x_offset = 50
    y_position = 500

    for i, carta in enumerate(cartas_em_jogo):
        screen.blit(carta, (x_offset + i * 140, y_position))


    pygame.display.update()

pygame.quit()
