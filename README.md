# ♠️ Blackjack (21) em Python: Implementação Cliente-Servidor

[](https://www.python.org/)
[](https://www.pygame.org/)
[](https://www.google.com/search?q=https://github.com/seu-usuario/seu-repositorio)
[](https://www.google.com/search?q=LICENCA)

## 🎯 Sobre o Projeto: Redes de Computadores I

Este projeto é uma implementação do clássico jogo **Blackjack (21)**, desenvolvido em Python, utilizando a biblioteca **Pygame** para a interface gráfica.

O foco central é a implementação da comunicação via **Sockets** na arquitetura **Cliente-Servidor**. Ele foi desenvolvido para a disciplina de **Redes de Computadores I**, com o objetivo de demonstrar o uso de Sockets TCP/IP para permitir que dois jogadores (um agindo como cliente e outro como servidor) executem a aplicação em máquinas diferentes e interajam em tempo real.

O projeto permite a execução de partidas de dois jogadores com as seguintes funcionalidades:

  * Comunicação **Cliente-Servidor** para troca de ações de jogo e estados.
  * Uso de cartas gráficas (PNG) e redimensionamento de janela.
  * Ações básicas do Blackjack: `Hit` (pedir carta), `Stand` (passar a vez) e `Split` (divisão).

## 🚀 Arquitetura de Rede

A aplicação utiliza a biblioteca `socket` do Python para estabelecer a comunicação.

  * **Servidor:** Ouve em uma porta específica, aceita a conexão do cliente e gerencia o estado principal do jogo, enviando atualizações para o cliente.
  * **Cliente:** Conecta-se ao servidor e envia as ações do jogador (ex: pedir carta, passar a vez), recebendo em troca as atualizações do estado do jogo.

[Image of a client-server socket communication diagram]

## 🛠️ Requisitos

  * **Python 3.9+**
  * **Pygame 2.x**

### Instalação

```bash
pip install pygame
```

## 🔌 Como Executar

Para que o jogo funcione em rede, você precisa iniciar o **Servidor** primeiro e, em seguida, o **Cliente**. Certifique-se de que as duas máquinas (ou terminais) estejam na mesma rede.

### 1\. Iniciar o Servidor

Na máquina que atuará como Servidor:

```bash
python3 blackjack_server.py
```

### 2\. Iniciar o Cliente

Na máquina que atuará como Cliente (após o servidor estar ativo):

```bash
python3 blackjack_client.py <IP_DO_SERVIDOR> <PORTA>
# Exemplo: python3 blackjack_client.py 192.168.1.10 5000
```

> **Nota:** Se você for testar na mesma máquina, use `127.0.0.1` (localhost) como IP.

## 🕹️ Controles

Os controles são usados pelo jogador que está interagindo com a interface gráfica (no cliente ou no servidor, dependendo da sua implementação da UI):

  * **ESPAÇO:** Pedir carta (Hit)
  * **ENTER:** Passar a vez (Stand)
  * **S:** Split (se as 2 cartas iniciais tiverem mesmo valor; J/Q/K contam como 10)
  * **ESC:** Sair
  * **R:** Reiniciar (após o término da partida)

## 📂 Estrutura do Projeto

  * `blackjack_server.py` – **Módulo Servidor:** Responsável por ouvir conexões, gerenciar o estado da partida (regras, baralho) e coordenar a comunicação.
  * `blackjack_client.py` – **Módulo Cliente:** Responsável por conectar-se, enviar ações do jogador e renderizar a interface gráfica (Pygame) com o estado recebido.
  * `regras.py` – Lógica central do jogo (baralho, avaliação de pontuação e operações como `deal`/`split`).
  * `Cartas/` – Imagens gráficas das cartas por naipe e verso (`fundo.png`).
    > Mantenha a estrutura de pastas para que as imagens sejam localizadas corretamente.

## 📝 Observações

  * **Blackjack Inicial:** Apenas considerado se as duas primeiras cartas estiverem reveladas.
  * **Estouro (\>21):** O estouro termina a mão do jogador.
  * **Empates (Push):** São possíveis quando as pontuações máximas visíveis dos jogadores coincidem.

## ⚠️ Dicas de Solução de Problemas

  * **Erro de Conexão:** Verifique se o IP e a Porta estão corretos no cliente e se o servidor está rodando. O firewall da máquina do servidor pode estar bloqueando a porta.
  * **Pygame não instala no Linux:** Instale dependências SDL da sua distro (ex: `sudo apt-get install python3-dev libsdl-image-dev libsdl-mixer-dev libsdl-ttf-dev`) e tente novamente.
  * **Cartas não aparecem:** Confirme nomes e acentos das pastas e arquivos em `Cartas/`.

## 📜 Licença

Este projeto é de **uso educacional/didático** para fins de estudo de Redes de Computadores.