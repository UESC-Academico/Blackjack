import socket
import json
# py -3.12 blackjack_server.py
# py -3.12 blackjack_client.py 127.0.0.1 5000

class Network:
    def __init__(self, ip, port):
        # Configura o socket para IPv4 (AF_INET) e TCP (SOCK_STREAM)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, int(port))
        self.connected = False
        # Buffer para remontar pacotes quebrados
        self.buffer = "" 
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            self.connected = True
            return True
        except:
            return False

    def send(self, data):
        """
        Serializa o dicionário (Python) para JSON (Texto) e envia.
        Adiciona \n como delimitador para indicar fim da mensagem.
        """
        try:
            msg = json.dumps(data) + "\n"
            # sendall: para garantir que a mensagem inteira seja enviada, mesmo que a rede precise quebrar em pacotes menores.
            self.client.sendall(msg.encode('utf-8'))
        except socket.error as e:
            print(f"[ERRO DE REDE] Falha no envio: {e}")

    def receive_continuous(self, callback_function):
        """
        Loop infinito que fica escutando a rede.
        Resolve o problema de fragmentação do TCP usando um buffer.
        """
        while self.connected:
            try:
                # Tenta receber até 4096 bytes do socket
                chunk = self.client.recv(4096).decode('utf-8')
                if not chunk: 
                    # Se receber vazio, o servidor fecha a conexão
                    self.connected = False
                    break
                
                # Adiciona o pedaço recebido ao buffer
                self.buffer += chunk
                
                # Processa mensagens completas (que terminam em \n)
                while "\n" in self.buffer:
                    msg, self.buffer = self.buffer.split("\n", 1)
                    if msg.strip():
                        try:
                            # Deserializa (JSON -> Objeto Python)
                            data = json.loads(msg)
                            # Chama a função do jogo para atualizar a tela
                            callback_function(data)
                        except json.JSONDecodeError:
                            pass # Ignora pacotes corrompidos
            except:
                self.connected = False
                break