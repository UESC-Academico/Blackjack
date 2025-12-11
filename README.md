# Blackjack (21) em Python: Implementação Cliente-Servidor

[](https://www.python.org/)
[](https://www.pygame.org/)
[](https://www.google.com/search?q=https://github.com/seu-usuario/seu-repositorio)
[](https://www.google.com/search?q=LICENCA)

## Sobre o Projeto: Redes de Computadores I

Este projeto é uma implementação do clássico jogo Blackjack (21), desenvolvido em Python, utilizando a biblioteca Pygame para a interface gráfica.

O foco central é a implementação da comunicação via Sockets na arquitetura Cliente-Servidor. Ele foi desenvolvido para a disciplina de Redes de Computadores I, com o objetivo de demonstrar o uso de Sockets TCP/IP para permitir que dois jogadores (um agindo como cliente e outro como servidor) executem a aplicação em máquinas diferentes e interajam em tempo real.

O projeto permite a execução de partidas de dois jogadores com as seguintes funcionalidades:

  * Comunicação Cliente-Servidor para troca de ações de jogo e estados.

  * Uso de cartas gráficas (PNG) e redimensionamento de janela.

  * Ações básicas do Blackjack: Hit (pedir carta), Stand (passar a vez) e Split (divisão).

## Sobre o Jogo: Entendendo as regras
  * O jogo possui apenas 2 participantes.

  * Cada jogador possui turno único, não intercalado.

  * Cada jogador recebe 2 cartas, uma virada para cima e outra para baixo.

  * No seu turno, cada jogador pode pedir cartas (Hit), a fim de aumentar a sua pontuação atual.

  * O Split (divisão de mão) é permitido somente após a primeira jogada do turno, se o jogador tiver exatamente duas cartas de mesmo valor viradas para cima, dividindo a mão em dois jogos.

  * Se um jogador estourar sua mão (>21) sem revelar a carta escondida, ele automaticamente perde a vez.

  * O Jogador 1 pode passar seu turno a qualquer momento, não podendo mais realizar ações no jogo.

  * Quando o Jogador 2 encerra seu turno, o jogo é finalizado e os pontos são contabilizados.

  * Ao final, ganha o participante que chegou mais próximo de 21 pontos sem estourar.

  * Caso ambos tenham estourado, ganha aquele que estiver com uma mão mais próxima de 21 pontos

## Arquitetura e Protocolo de Rede 
A aplicação utiliza a biblioteca socket do Python para estabelecer a comunicação em rede, priorizando a confiabilidade de transmissão do estado do jogo.

1. Modelo de Comunicação (TCP/IP)
  * O projeto utiliza Sockets TCP/IP para a comunicação, seguindo um modelo de requisição-resposta.


  * Servidor: Ouve em uma porta específica, aceita a conexão do cliente e gerencia o estado principal do jogo (baralho, regras), enviando atualizações para o cliente.

  * Cliente: Conecta-se ao servidor e envia as ações do jogador (ex: pedir carta, passar a vez), recebendo em troca as atualizações do estado do jogo.

  * Motivação para TCP: O TCP garante a entrega ordenada e sem perdas, essencial para a correta sincronização das ações e do estado do tabuleiro entre os dois jogadores, prevenindo a perda de informações críticas como cartas ou pontuações.

2. Protocolo de Camada de Aplicação (Aberto)

  * Embora não detalhado em JSON, o fluxo de comunicação segue o padrão:

    * Conexão Estabelecida: Cliente conecta-se ao Servidor.

    * Troca de Estado Inicial: Servidor envia o estado inicial do jogo (ex: cartas iniciais).

    * Ciclo de Ações (Turno):

    * Cliente envia a ação do jogador (ex: HIT, STAND, SPLIT).

    * Servidor processa a ação, valida as regras e atualiza o estado do jogo.

    * Servidor envia o estado atualizado de volta ao Cliente (e ao outro jogador, caso esteja conectado).

## Sobre a conexão: Entendendo o codigo do network.py

  1. No arquivo network.py temos a classe network, ela é a responsável por definir a conexão e como será feita a troca de dados.
  Determinamos a criação de um socket e definimos a conexão como TCP em ```self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)```, alem disso também é criado um buffer para resolver o problema de fragmentação do TCP na qual a mensagem pode ser enviada em pedaços dividos em pacotes diferentes, portanto é necessário armazenar os dados em um buffer ate que a mensagem completa seja recebida.

  2. O método send é responsável por serializar os objetos python para uma string JSON e depois converter para bytes que serão enviados pela rede, é nessa função que também adicionamos o delimitador "\n" para delimitar o fim de um bloco de informações para resolver o problema da fragmentação mencionado acima.

  3. Então o método ```receive_continuous``` que fica rodando em um loop infinito, fica ouvindo todas as mensagens enviadas pela rede e decodifica os bytes para JSON. Esse metodo também salva os pacotes de chegam utilizando o buffer que foi criado anteriormente, a mensagem é guardada e quando o delimitador "\n" é encontrado, quando isso ocorre os dados em string JSON são reconvertidos para objetos python e uma função de callback é chamada para atualizar o jogo.

## Sobre o servidor: Entendendo o codigo do blackjack_server.py

É no servidor que todos os dados referentes ao estado do jogo, regras e atualização do estado são feitos, todos os calculos são feitos dentro do servidor de maneira que ele atualiza o jogo e envia um broadcast para fazer com que o client atualize a interface grafica

  O servidor funciona utilizando 3 threads, essas serão resposáveis por:

  1. Uma thread especifica é responsável por estabelecer as conexões com novos clients(handshake) criar novas threads especificas para cuidar dos dados de cada cliente

  2. Depois de feito o handshake threads especificas para cada cliente serão criadas no método "handle_client" responsáveis por: Receber comandos enviados pelo jogador atraves do client, atualizar o estado do jogo de acordo com a jogada feita e retransmitir o novo estado no método ```broadcast_state```.

  Para evitar erros de race conditions entre as threads é feito ```game_lock = threading.Lock()``` dessa forma caso ambos os jogadores apertem teclas no mesmo exato momento não ocorram bugs como dois jogadores recebendo exatamente a mesma carta

## Sobre o cliente: Entendendo o codigo do blackjack_client.py

# Requisitos:
O cliente necessita de um IP e uma Porta para iniciar, só podendo se conectar ao servidor se as duas informações forem providas, por terminal, ou através do hostlocator.txt se a máquina também estiver atuando como servidor. O cliente possui também a possibilidade de receber um nome, que será aplicado ao jogador ao se conectar com o servidor do jogo.

# Funcionalidade:
O cliente recebe os estados do jogo no servidor e é responsável por chamar as funções da interface gráfica. O cliente possui duas threads, onde:

  1. Uma thread específica é responsável pela comunicação com o servidor, recebendo as informações.

  2. A outra thread é responsavél por identificar os comandos do jogador e enviar para o servidor do jogo atualizar a interface do jogo conforme o que for solicitado.

## Requisitos

  * **Python 3.9+**
  * **Pygame 2.x**

### Instalação

```bash
pip install pygame
```

## Como Executar

Para que o jogo funcione em rede, você precisa iniciar o **Servidor** primeiro e, em seguida, o **Cliente**. Certifique-se de que as duas máquinas (ou terminais) estejam na mesma rede.

### 1\. Iniciar o Servidor

Na máquina que atuará como Servidor:

```bash
python3 blackjack_server.py
```
O servidor criará um arquivo de texto ```hostlocator.txt``` que possui o endereço de IP e a porta, podendo ser utilizado pelo Cliente na máquina que atuará como Servidor.

### 2\. Iniciar o Cliente

Na máquina que atuará como Cliente (após o servidor estar ativo):

o Cliente possui 4 possibilidades de execução. 
### 1\. (Executável apenas na máquina que está atuando como Servidor):
```bash
python3 blackjack_client.py
```
### 2\. (Executável apenas na máquina que está atuando como Servidor):
```bash
python3 blackjack_client.py <NOME>
#Exemplo: python3 blackjack_client.py Seu_Nome
```
### 3\. (Executável em qualquer máquina):
```bash
python3 blackjack_client.py <IP_DO_SERVIDOR> <PORTA>
# Exemplo: python3 blackjack_client.py 192.168.1.10 5000
```
### 4\. (Executável em qualquer máquina):
```bash
python3 blackjack_client.py <IP_DO_SERVIDOR> <PORTA> <NOME>
# Exemplo: python3 blackjack_client.py 192.168.1.10 5000 Seu_Nome
```

> **Nota:** Se você for testar na mesma máquina, use `127.0.0.1` (localhost) como IP.

## Controles

Os controles são usados pelo jogador que está interagindo com a interface gráfica (no cliente ou no servidor, dependendo da sua implementação da UI):

  * **ESPAÇO:** Pedir carta (Hit)
  * **ENTER:** Passar a vez (Stand)
  * **S:** Split (se as 2 cartas iniciais tiverem mesmo valor; J/Q/K contam como 10)
  * **ESC:** Sair
  * **R:** Reiniciar (após o término da partida)

## Estrutura do Projeto

  * `blackjack_server.py` – **Módulo Servidor:** Responsável por ouvir conexões, gerenciar o estado da partida (regras, baralho) e coordenar a comunicação.
  * `blackjack_client.py` – **Módulo Cliente:** Responsável por conectar-se, enviar ações do jogador e renderizar a interface gráfica (Pygame) com o estado recebido.
  * `regras.py` – Lógica central do jogo (baralho, avaliação de pontuação e operações como `deal`/`split`).
  * `hostlocator.txt`– Localiza o IP e a PORTA para a máquina atuando como servidor para facilitar o acesso pelo Cliente.
  * `Cartas/` – Imagens gráficas das cartas por naipe e verso (`fundo.png`).
  * `Icones/` – Assets utulizados nos jogos (`trophy.png`).
    > Mantenha a estrutura de pastas para que as imagens sejam localizadas corretamente.

## Observações

  * **Estouro (\>21):** O estouro termina a mão do jogador.
  * **Empates (Push):** São possíveis quando as pontuações máximas visíveis dos jogadores coincidem.

## Dicas de Solução de Problemas

  * **Erro de Conexão:** Verifique se o IP e a Porta estão corretos no cliente e se o servidor está rodando. O firewall da máquina do servidor pode estar bloqueando a porta.
  * **Pygame não instala no Linux:** Instale dependências SDL da sua distro (ex: `sudo apt-get install python3-dev libsdl-image-dev libsdl-mixer-dev libsdl-ttf-dev`) e tente novamente.
  * **Cartas não aparecem:** Confirme nomes e acentos das pastas e arquivos em `Cartas/`.

## Licença

Este projeto é de **uso educacional/didático** para fins de estudo de Redes de Computadores.