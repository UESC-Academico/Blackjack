import sys
import pygame
import threading
import json
import socket
from network import Network
from regras import card
from blackjack_game import BlackjackGame

with open("hostlocator.txt", "r+") as hostlocator:
    IP = hostlocator.readline().replace('\n', '')
    PORT = hostlocator.readline().replace('\n', '')

class NetworkGame(BlackjackGame):
    def __init__(self, ip = IP, port = PORT):
        print(f'{ip}, {port}')
        # 1. Conexão TCP
        self.net = Network(ip, port)
        if not self.net.connect():
            print("\n[ERRO FATAL] Nao foi possivel conectar ao servidor.")
            print("Verifique IP e Porta.\n")
            sys.exit()
            
        # 2. Handshake com timeout
        # Evita que o programa trave se o IP estiver errado
        self.net.client.settimeout(5.0) 
        self.my_id = -1
        self.initial_state = None 
        
        try:
            buffer = ""
            # Loop síncrono esperando identificação
            while self.my_id == -1:
                chunk = self.net.client.recv(4096).decode('utf-8')
                if not chunk: raise Exception("Conexao fechada pelo servidor")
                
                buffer += chunk
                while "\n" in buffer:
                    msg_str, buffer = buffer.split("\n", 1)
                    if not msg_str.strip(): continue
                    
                    try:
                        data = json.loads(msg_str)
                        if data.get("type") == "WELCOME":
                            self.my_id = data["my_id"]
                        elif "hands" in data:
                            self.initial_state = data
                    except json.JSONDecodeError:
                        pass 

        except socket.timeout:
            print("\n[ERRO] Timeout. Servidor nao respondeu.")
            sys.exit()
        except Exception as e:
            print(f"\n[ERRO] Falha no Handshake: {e}")
            sys.exit()

        self.net.client.settimeout(None)

        # 3. Inicializa engine gráfica (Pygame)
        super().__init__()
        
        # Carrega estado inicial para evitar tela preta no começo
        if self.initial_state:
            self.update_game_state(self.initial_state)

        pygame.display.set_caption(f"Blackjack - VOCE E O JOGADOR {self.my_id + 1}")
        
        # Separamos a escuta da rede em uma thread paralela para não congelar a interface gráfica (que roda no loop principal).
        self.listen_thread = threading.Thread(target=self.start_listening, daemon=True)
        self.listen_thread.start()

    def start_listening(self):
        """Thread secundária que fica ouvindo o servidor"""
        self.net.receive_continuous(self.update_game_state)

    def update_game_state(self, state):
        """Callback: Chamado assincronamente quando chega dados da rede"""
        self.server_state = state
        msg_type = state.get("type")
        
        if msg_type == "WELCOME": return
        
        if msg_type == "ERROR":
            print(f"[SERVIDOR]: {state.get('msg')}")
            return

        # Sincronização de estado: atualiza modelos locais com dados do servidor
        server_hands = state.get("hands", [])
        new_hands = []
        for p_hand_data in server_hands:
            player_chances = []
            for chance_data in p_hand_data:
                cards_objs = []
                for c_data in chance_data:
                    # Recria objetos visuais 'card'
                    nova_carta = card((c_data['value'], c_data['naipe']), c_data['revealed'])
                    cards_objs.append(nova_carta)
                player_chances.append(cards_objs)
            new_hands.append(player_chances)
            
        self.hands = new_hands
        self.current_player = state.get("current_player", 0)

        # Lógica de interface: destravamento de Tela
        server_game_over = state.get("game_over")
        
        # 1. Jogo acabou: mostra tela de vitória
        if server_game_over and self.game_state != "FINISHED":
            self.game_state = "FINISHED"
            self.reveal_all_cards()
            
        # 2. Jogo reiniciou (Reset): destrava tela de vitória
        elif not server_game_over and self.game_state == "FINISHED":
            self.game_state = "PLAYING"
            self.board = [] 
            print("[CLIENTE] Sincronizacao: Jogo reiniciado.")

    def is_my_turn(self):
        """Verificação local para feedback visual (UX)"""
        return self.current_player == self.my_id and self.game_state == "PLAYING"

    # Métodos de envio (adaptação para rede)
    def deal_card(self, alternate=False):
        if self.is_my_turn():
            self.net.send({"action": "HIT"})
        else:
            print(f"[AVISO] Nao e sua vez!")

    def pass_turn(self):
        if self.is_my_turn():
            self.net.send({"action": "STAND"})

    def try_split(self):
        if self.is_my_turn():
            self.net.send({"action": "SPLIT"})

    def reset_game(self):
        # Envia solicitação de reset ao servidor
        self.net.send({"action": "RESET"})

    def draw(self):
        """Renderização com feedback de turno"""
        super().draw()
        if self.is_my_turn():
            try:
                text_surf = self.font_large.render(" SUA VEZ! ", True, (255, 255, 0))
                text_rect = text_surf.get_rect(center=(self.width // 2, self.height - 120))
                bg_rect = text_rect.inflate(20, 10)
                s = pygame.Surface((bg_rect.width, bg_rect.height))
                s.set_alpha(200)
                s.fill((0, 0, 0))
                self.screen.blit(s, bg_rect.topleft)
                self.screen.blit(text_surf, text_rect)
            except:
                pass 

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        game = NetworkGame()
        game.run()
    else:
        game = NetworkGame(sys.argv[1], sys.argv[2])
        game.run()