# Gamerbot #01: Telegram LumberJack

## RESUMO

Eu fiquei irritado por não bater o record de um amigo num jogo para crianças e escrevi um bot que fez todo o trabalho sujo por mim.

## INTRODUÇÃO

Um dos motivos para o Telegram ser meu mensageiro favorito é a quantidade de opções ricas de iteração que ele oferece, como bots e super-grupos. Entretanto, uma *feature* subutilizada desse aplicativo é a interface de jogos. O Telegram oferece um *framework* de criação de jogos em HTML5 e um sistema de persistência de pontuação. A iteração com o usuário deve ser feita mediante a API de bots; opções como criar nova partida, desafiar um amigo e ver a pontuação salva estão entre as opções mais comuns.

Para ilustrar o *framework* de jogos, o Telegram criou um bot de demonstração chamado [GameBot ](https://t.me/gamebot); com três joguinhos simples, esse bot promove um pouco do que a plataforma de jogos do Telegram é capaz de fazer. Um desses jogos, o LumberJack, me deixou bastante irritado nesse final de semana.

## O JOGO

LumberJack é um jogo onde você controla um lenhador que corta uma árvore de tamanho infinito. À medida que a árvore vai sendo cortada, seus galhos vão ficando mais próximo do chão e, consequentemente, do lenhador. O jogador deve alternar a posição do lenhador entre esquerda e direita, evitando ser atingido pelos galhos cadentes, e num ritmo o mais rápido o possível: uma barra de tempo diminui se o lenhador ficar parado, e se enche um pouco a cada batida do machado; ficar parado por muito tempo é fim de jogo.

![Componentes do jogo LumberJack](https://i.imgur.com/iWq3ZSK.png)
![Gameplay do LumberJack](https://i.imgur.com/NdtmpyW.gif)

## O PROBLEMA

Depois de descobrir o jogo e compartilhar com um grupo de amigos próximos, começou a corrida por quem fazia mais pontos. Um amigo próximo com [problemas de vício em jogos](https://www.urbandictionary.com/define.php?term=Gamers) logo partiu na frente, primeiro abrindo 112 pontos, depois 176, depois 201 e por fim fechando o máximo de 248. Atrás, com 245, um outro amigo pareceu arriscar o lugar mais alto do podium, mas depois desistiu afirmando ter chegado ao limite. Já eu, [bastante focado em dar o meu melhor](https://www.urbandictionary.com/define.php?term=competitious), estava em terceiro, com 244; 1 ponto atrás do segundo e apenas 4 para o primeiro.

Ao perceber que eu tinha gastado quase 1 hora do meu dia em um jogo onde eu fico empurrando de lá pra cá um boneco vestido de dono de barbearia que vende cerveja e tem um videogame na sala de espera, me restaram apenas duas opções: a) aceitar que eu tinha alcançado os limites da minha capacidade motora ou b) culpar o jogo/celular/internet por eu não estar no lugar aonde eu merecia estar como o *super gamer* que eu sou.

No final eu acabei tomando uma [terceira via](https://pcb.org.br/portal2/25449/o-centrao-o-centroavante-e-o-cartao-amarelo/).

## A SOLUÇÃO

Aproveitando a minhas habilidades em programação cultivadas pelos últimos 10 anos, eu concebi um bot que joga LumberJack a partir de análise de imagens e automação de cliques do mouse. As regras do algoritmo do bot são tão simples quanto o próprio jogo:

 - Continuar clickando no mesmo lado enquanto não houver um galho logo acima do lenhador;
 - Se houver um galho na região logo acima do lenhador, mudar de lado.
 - Repetir até o inifito ou até que algo aconteça (mais detalhes a seguir...)

A Figura abaixo mostra todas as regiões de interesse do bot: as que ele vê e as que ele controla. Eu executei o jogo e o bot no meu computador, logo as coordenadas definidas abaixo são relativas às dimensões da minha tela e às bordas do meu navegador.

![Artefatos na imagem vistos/controlados pelo bot](https://i.imgur.com/9Np1hGH.png)

Só precisamos nos preocupar com a região logo acima do lenhador, portanto nos preocuparesmo apenas com os retângulos em vermelho com os símbolos de robozinho e olho; em azul temos as coordendas do canto superior esquerdo e nas linhas ao longo do retângulo esquerdo, as dimensões da região de interesse. O controle se dá com cliques nos dois botões abaixo da tela principal do jogo. As coordenadas do centro dos botões estão escritas próximo dos símbolos de robozinho e mouse. Todas essas regiões foram encontradas a partir de uma *screenshot* tirada do jogo e analisada num editor de imagens e anotadas a parte. Também com a ajuda do editor de imagens eu recortei apenas as imagens de um galho da esquerda (`left_branch.png`) e outro da direita (`right_branch.png`), como na Figura a seguir.

![Recorte do galhos para reconhecimento do padrão na imagem](https://i.imgur.com/t4wYxeJ.png)

Pronto, agora é implementar o bot. Essa parte foi a mais tranquila, visto que o trabalho pesado foi encontrar as regiões de interesse. Escolhi Python por ser a linguagem mais legal para esse tipo de projetinho: simples e prática, com praticamente tudo pronto para usar. O algoritmo a ser escrito é: a) tirar uma *screenshot* apenas da região logo acima do lenhador; b) verificar se existe um galho ali; c) se tiver, troca de posição; d) senão, continua no mesmo lugar; e) faz um clique; f) repete.

Para automatizar o processo de intereção com a tela, tanto de visão quanto de controle, eu escolhi usar a biblioteca [PyAutoGUI](https://github.com/asweigart/pyautogui). Para ter um melhor resultado do método que análise a imagem e procura pelo padrão do galho, é necessário também instalar a versão Python da [OpenCV](https://pypi.org/project/opencv-python/). Você consegue instalar ambas usando `pip`:

```python
pip3 install --user pyautogui opencv-python
```

## A IMPLEMENTAÇÃO

As informações das regiões de interesse foram guardadas num dicionário com os seguintes campos:

```python
config = {
    "left" : {
        "click_x" : 876,
        "click_y" : 924,
        "branch" : "left_branch.png",
        "region" : (824, 575, 111, 69),
    },
    "right" : {
        "click_x" : 1044,
        "click_y" : 924,
        "branch" : "right_branch.png",
        "region" : (985, 575, 111, 69),
    },
}

c = config["right"]
```

A variável `c` guarda as configurações atuais. Agora é só uma questão de encontrar ou não o galho acima do lenhador e trocar `c` para o lado destino, `left` ou `right`. Todas as informações que precisamos (aonde clicar, qual imagem usar para reconhecimento e a região de interesse atual) estarão à mão. Agora é só uma questão de encontrar ou não um galho (`.locateOnScreen()`), mudar ou não o lado do lenhador e sair clicando (`.click()`).

```python
for i in range(400): # por que não infinitamente???
    if pag.locateOnScreen(c["branch"], grayscale=True, region=c["region"], confidence=0.9):
        c = config["right"] if c == config["left"] else config["left"]
    
    pag.click(c["click_x"], c["click_y"])
```

Você deve ter notado que o laço não roda para sempre. Dois motivos para isso. Primeiro, se o algoritmo rodasse para sempre, eu nunca mais teria controle do meu mouse real e não poderia abortar a execução. Segundo, eu só queria ultrapassar a pontuação do meu bróder. Entretanto, enquanto testava o bot, eu descobri um terceiro motivo mais interessante: é impossível passar de uma certa pontuação.

## OS RESULTADOS

O vídeo abaixo mostra o gamerbot em ação:

[![O bot!!!](http://img.youtube.com/vi/9ZJq9pZGWrE/0.jpg)](http://www.youtube.com/watch?v=9ZJq9pZGWrE "Gamerbot Telegram LumberJack")

Lindo, nê?

Agora a pergunta que fica: por que ele morreu com 351 pontos se o laço principal deveria rodar pelo menos 1000 vezes? A resposta está nas velocidades da animação de corte e da barra de tempo: próximo aos 340 pontos, a velocidade que a barra de tempo descresce é mais rápida que a velocidade necessária para superar a animação de corte. Muito provavelmente os desenvolvedores do Telegram não esperavam que alguém chegasse tão longe, até porque esse joguinho tem o único objetivo de ser uma demonstração da plataforma de jogos. Se por um acaso você descobrir que eu estou errado, eu ficaria muito contente em ver esse bot turbinado! Use os *issues* deste repositório para mandar sua sugestão.

Aqui vai o código completo com comentários. A versão do repositório (`gamerbot-telegram-lumberjack.py`) contém apenas linhas de código válidas.

```python
# A única biblioteca necessária
# Instalação: pip3 install pyautogui opencv-python
import pyautogui as pag

# Um dicionário que guarda as configurações necessárias do jogo
#   - click_x: coordenada x do botão
#   - click_y: coordenada y do botão
#   - branch: caminho para a imagem usada para reconhecimento de padrão
#   - region: o retângulo que representa a região da tela que o bot enxerga
config = {
    "left" : {
        "click_x" : 876,
        "click_y" : 924,
        "branch" : "left_branch.png",
        "region" : (824, 575, 111, 69),
    },
    "right" : {
        "click_x" : 1044,
        "click_y" : 924,
        "branch" : "right_branch.png",
        "region" : (985, 575, 111, 69),
    },
}

# Essa variável fica alternando o lado que o lenhador está
c = config["right"]

# Esse laço roda uma quantidade de vezes igual a quantos pontos você quer fazer
# Entretanto, só é possível no máximo 351 pontos
# Aos 340 pontos, a barra de tempo descresce mais rapidamente que o corte do lenhador
for i in range(400):
    if pag.locateOnScreen(c["branch"], grayscale=True, region=c["region"], confidence=0.9):
        c = config["right"] if c == config["left"] else config["left"]
    
    pag.click(c["click_x"], c["click_y"])

# Fim do jogo!
print("Game Over")
```

## CONCLUSÃO

Espero que esse projetinho te ajude a pensar um pouco sobre como alguns bots funcionam! Essa brincadeira acabou sendo mais divertida do que eu imaginava. Fique à vontade para mandar sua dúvida, crítica e sugestão usando o sistema de *issues* do GitHub.
