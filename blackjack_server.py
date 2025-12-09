import socket
import threading
import json
from regras import *

HOST = '0.0.0.0' # escutar em todas as placas de rede disponíveis
PORT = 5000


# o lock garante que apenas um altere o baralho por vez.
game_lock = threading.Lock()

# Gerenciamento de sessão: slots fixos para 2 clientes
player_sockets = [None, None] 

# O servidor mantém o estado real do jogo. Os clientes são apenas visualizadores.
game_data = {
    "deck": [],
    "hands": [], 
    "current_player": 0,
    "game_over": False,
    "msg": "Aguardando...",
    "players_done": [False, False] # Rastreia quem já parou ou estourou
}

def broadcast_state():
    """
    Envia o estado atualizado para todos os clientes, garantindo que
    ambos vejam a mesma mesa.
    """
    state = get_game_state_json()
    msg = json.dumps(state) + "\n"
    encoded_msg = msg.encode('utf-8')
    
    for i in range(2):
        sock = player_sockets[i]
        if sock is not None:
            try:
                sock.sendall(encoded_msg)
            except Exception:
                # Se falhar o envio, assume desconexão e limpa o slot
                try: sock.close()
                except: pass
                player_sockets[i] = None

def serialize_hand(hand_list):
    """Converte objetos card para dicionários (para JSON)"""
    serialized = []
    for mao in hand_list:
        cards_data = []
        for carta in mao:
            cards_data.append({
                "value": carta.getValue(),
                "naipe": carta.getNaipe(),
                "revealed": carta.isRevealed()
            })
        serialized.append(cards_data)
    return serialized

def get_game_state_json():
    """Empacota todo o estado do jogo para envio"""
    hands_json = []
    for p_hand in game_data["hands"]:
        hands_json.append(serialize_hand(p_hand))
    
    return {
        "hands": hands_json,
        "current_player": game_data["current_player"],
        "game_over": game_data["game_over"],
        "msg": game_data["msg"],
        "connected_players": sum(1 for s in player_sockets if s is not None)
    }

def handle_client(conn, player_id):
    """
    Cada cliente é atendido por uma thread independente.
    """
    # 1. Handshake (Protocolo de Entrada)
    welcome_msg = {
        "type": "WELCOME",
        "my_id": player_id,
        "msg": f"Bem-vindo Jogador {player_id + 1}"
    }
    
    try:
        conn.sendall((json.dumps(welcome_msg) + "\n").encode('utf-8'))
        with game_lock:
            state_msg = get_game_state_json()
            state_msg["type"] = "UPDATE" 
            conn.sendall((json.dumps(state_msg) + "\n").encode('utf-8'))
    except Exception as e:
        print(f"[ERRO] Handshake falhou para Player {player_id}: {e}")
        return 

    buffer = "" 

    # 2. Loop de eventos
    while True:
        try:
            chunk = conn.recv(4096).decode('utf-8')
            if not chunk: break
            
            buffer += chunk
            
            while "\n" in buffer:
                msg_str, buffer = buffer.split("\n", 1)
                if not msg_str.strip(): continue
                
                try:
                    data = json.loads(msg_str)
                except json.JSONDecodeError:
                    continue 

                action = data.get("action")
                
                # 3. Seção crítica (Acesso protegido ao estado global)
                with game_lock:
                    # Validação: É reset permitido?
                    is_reset = (action == "RESET" and game_data["game_over"])
                    # Validação: É turno válido?
                    is_valid_turn = (game_data["current_player"] == player_id and not game_data["game_over"])

                    if is_valid_turn or is_reset:
                        player_hand = game_data["hands"][player_id]
                        
                        # Processamento da lógica do jogo
                        if action == "HIT":
                            dealCards(player_hand, game_data["deck"])
                            if max(calculateFaceUp(player_hand)) > 21:
                                game_data["players_done"][player_id] = True
                                if not all(game_data["players_done"]):
                                    game_data["current_player"] = (game_data["current_player"] + 1) % 2
                        elif action == "STAND":
                            game_data["players_done"][player_id] = True
                            if not all(game_data["players_done"]):
                                game_data["current_player"] = (game_data["current_player"] + 1) % 2
                        elif action == "SPLIT":
                            splitCards(player_hand, game_data["deck"])
                        elif action == "RESET":
                            # Lógica de reinício do jogo
                            print(f"[JOGO] Reset solicitado pelo Jogador {player_id + 1}")
                            game_data["deck"] = createShuffledDeck(False)
                            game_data["hands"] = createHands(game_data["deck"], 2)
                            game_data["current_player"] = 0
                            game_data["game_over"] = False
                            game_data["players_done"] = [False, False]
                            game_data["msg"] = "Novo jogo iniciado!"
                        
                        # Verifica condição de fim de jogo
                        if all(game_data["players_done"]):
                            game_data["game_over"] = True

                        broadcast_state()
                    else:
                        # Feedback de erro
                        error_msg = {"type": "ERROR", "msg": "Nao e sua vez ou o jogo acabou!"}
                        try:
                            conn.sendall((json.dumps(error_msg) + "\n").encode('utf-8'))
                        except: pass

        except Exception as e:
            print(f"[ERRO] Excecao no Player {player_id}: {e}")
            break

    # Cleanup na desconexão
    with game_lock:
        if player_sockets[player_id] == conn:
            player_sockets[player_id] = None
            # Evita deadlock se um jogador sair no meio
            game_data["players_done"][player_id] = True
            if all(game_data["players_done"]): game_data["game_over"] = True
            broadcast_state()

    try: conn.close()
    except: pass

def start_server():
    game_data["deck"] = createShuffledDeck(False)
    game_data["hands"] = createHands(game_data["deck"], 2)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR: permite reiniciar o servidor sem erro de porta travada
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
    except Exception as e:
        print(f"[ERRO CRITICO] Porta {PORT} em uso ou bloqueada: {e}")
        return

    server.listen()
    print(f"--- SERVIDOR ONLINE ---")
    print(f"IP: {socket.gethostbyname(socket.gethostname())}")
    print(f"PORTA: {PORT}")
    with open("hostlocator.txt", "w") as hostlocator:
        hostlocator.write(f"{socket.gethostbyname(socket.gethostname())}\n{PORT}")

    while True:
        conn, addr = server.accept()
        slot_found = -1
        
        with game_lock:
            if player_sockets[0] is None: slot_found = 0
            elif player_sockets[1] is None: slot_found = 1
            
            if slot_found != -1:
                player_sockets[slot_found] = conn
                # Daemon=True: thread morre se o programa principal fechar
                t = threading.Thread(target=handle_client, args=(conn, slot_found), daemon=True)
                t.start()
            else:
                print(f"[AVISO] Sala cheia. Rejeitando {addr}")
                conn.close()

if __name__ == "__main__":
    start_server()