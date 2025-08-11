import pygame
from random import randint
#from sys import exit

pygame.init()
pygame.display.set_caption("Seis Tiros no Oeste")
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

#Posição do cowboy
x, y = 100, 100
velocidade = 15

#Lista de projéteis do cowboy
projeteis = []
velocidade_tiro = 30 #coloquei o dobro da velocidade do personagem
# Timer para controlar a frequência dos tiros 
intervalo_tiro = 300 #300ms = 0.3 segundos
ultimo_tiro = 0

#configuração dos inimigos
inimigos = {"cor": (0, 0, 255), "posicao": None, "ativo": False, 
"respawn": pygame.time.get_ticks() + 8000, "intervalo": (3000, 7000), "velocidade": randint(1, 2)}

projeteis_inimigo = []
intervalo_tiro_inimigo = 200  #tempo entre tiros em ms
ultimo_tiro_inimigo = 0
velocidade_tiro_inimigo = 10

#Loop principal
fim_de_jogo = False
while not fim_de_jogo:

    #encerra o jogo se o jogador apertar em sair
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fim_de_jogo = True


    #Verifica teclas pressionadas
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_UP]:
        y -= velocidade
    if teclas[pygame.K_DOWN]:
        y += velocidade
    if teclas[pygame.K_LEFT]:
        x -= velocidade
    if teclas[pygame.K_RIGHT]:
        x += velocidade

    
    # Verifica tempo desde o último tiro
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultimo_tiro >= intervalo_tiro:
        projeteis.append([x + 50, y + 20])
        ultimo_tiro = tempo_atual  # registra o momento do tiro

    for tiro in projeteis:
        tiro[0] += velocidade_tiro

    nova_lista = []
    for t in projeteis:
        if t[0] < largura: #bala ainda não passou do lado direito da tela
            nova_lista.append(t)
    projeteis = nova_lista


    #Desenha fundo, cowboy, inimigos e projeteis
    tela.fill((255, 255, 255)) #Fundo branco
    cowboy = pygame.draw.rect(tela, (255, 0, 0), (x, y, 50, 50))  #Quadrado vermelho como cowboy provisório
    for tiro in projeteis:
        pygame.draw.rect(tela, (0, 0, 0), (tiro[0], tiro[1], 10, 5)) #projeteis na cor preta
    for tiro in projeteis_inimigo:
        pygame.draw.rect(tela, (255, 0, 0), (tiro[0], tiro[1], 10, 5))  # vermelho


    #Atualiza coletáveis
    if inimigos["ativo"]:

        #tiros do inimigo
        if inimigos["posicao"][0] < largura - 40: #so atira quando tiver dentro da tela 
            if tempo_atual - ultimo_tiro_inimigo >= intervalo_tiro_inimigo:
                projeteis_inimigo.append([inimigos["posicao"][0], inimigos["posicao"][1] + 20])
                ultimo_tiro_inimigo = tempo_atual

        for tiro in projeteis_inimigo:
            tiro[0] -= velocidade_tiro_inimigo

        cowboy_rect = pygame.Rect(x, y, 50, 50)
        for tiro in projeteis_inimigo:
            if cowboy_rect.colliderect(pygame.Rect(tiro[0], tiro[1], 10, 5)):
                fim_de_jogo = True


        # Remover tiros que saíram da tela
        projeteis_inimigo = [t for t in projeteis_inimigo if t[0] > 0]

        #mover no eixo x
        inimigos["posicao"][0] -= inimigos["velocidade"]

        #Se o inimigo encostar na borda, fim de jogo
        if inimigos["posicao"][0] <= 0:
            fim_de_jogo = True

        #Desenha o inimigo
        coletavel = pygame.draw.rect(tela, inimigos["cor"], (inimigos["posicao"][0], inimigos["posicao"][1], 40, 40))

        #Colisão do tiro do jogador com o inimigo
        for tiro in projeteis:
            tiro = pygame.Rect(tiro[0], tiro[1], 10, 5)
            if tiro.colliderect(coletavel):
                inimigos["ativo"] = False
                min_tempo, max_tempo = inimigos["intervalo"]
                inimigos["respawn"] = tempo_atual + randint(min_tempo, max_tempo)

    else:
        # Verifica se é hora de reaparecer
        if tempo_atual >= inimigos["respawn"]:
                inimigos["posicao"] = [randint(800, 900), randint(50, 550)]
                inimigos["ativo"] = True

    #atualiza a tela
    pygame.display.flip()
    relogio.tick(60)  # FPS


pygame.quit()