# Blackjack (21) em Python: Implementação Cliente-Servidor

[](https://www.python.org/)
[](https://www.pygame.org/)
[](https://www.google.com/search?q=https://github.com/seu-usuario/seu-repositorio)
[](https://www.google.com/search?q=LICENCA)

## Sobre o Projeto: Redes de Computadores I

Este projeto é uma implementação do clássico jogo **Blackjack (21)**, desenvolvido em Python, utilizando a biblioteca **Pygame** para a interface gráfica.

O foco central é a implementação da comunicação via **Sockets** na arquitetura **Cliente-Servidor**. Ele foi desenvolvido para a disciplina de **Redes de Computadores I**, com o objetivo de demonstrar o uso de Sockets TCP/IP para permitir que dois jogadores (um agindo como cliente e outro como servidor) executem a aplicação em máquinas diferentes e interajam em tempo real.

O projeto permite a execução de partidas de dois jogadores com as seguintes funcionalidades:

  * Comunicação **Cliente-Servidor** para troca de ações de jogo e estados.
  * Uso de cartas gráficas (PNG) e redimensionamento de janela.
  * Ações básicas do Blackjack: `Hit` (pedir carta), `Stand` (passar a vez) e `Split` (divisão).

## Sobre o Jogo: Entendendo as regras
* O jogo possui apenas 2 participantes.
* Cada jogador possui turno único, não intercalado.
* Cada jogador recebe 2 cartas, uma virada para cima e outra para baixo.
* No seu turno, cada jogador pode pedir cartas (Hit), a fim de aumentar a sua pontuação atual.
* Somente após a primeira jogada do turno, se o jogador tiver exatamente duas cartas de mesmo valor viradas para cima na mão, ele pode pedir um Split, dividindo sua mão em dois jogos (montantes de baralho), contabilizando os pontos separadamente.
* Se um jogador estourar sua mão sem revelar a carta escondida, ele automaticamente perde a vez.
* O jogador 1 pode pedir para passar seu turno em qualquer momento, porém não poderá realizar mais ações no jogo. Iniciando, então, o turno do próximo jogador da mesa. Caso o jogador 2 encerre seu turno, o jogo é finalizado e os pontos contabilizados.
* Ao final do jogo, ganha o participante que chegou mais próximo de 21 pontos sem estourar.
* Caso ambos tenham estourado, ganha aquele que estiver com uma mão mais próxima de 21 pontos.

## Arquitetura de Rede

A aplicação utiliza a biblioteca `socket` do Python para estabelecer a comunicação.

  * **Servidor:** Ouve em uma porta específica, aceita a conexão do cliente e gerencia o estado principal do jogo, enviando atualizações para o cliente.
  * **Cliente:** Conecta-se ao servidor e envia as ações do jogador (ex: pedir carta, passar a vez), recebendo em troca as atualizações do estado do jogo.

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