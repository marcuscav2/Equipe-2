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

#configuração dos coletaveis
coletaveis = [
    {"cor": (255, 0, 0), "posicao": None,
     "ativo": False, "respawn": pygame.time.get_ticks() + 2000, "intervalo": (1000, 3000)},  # 1 a 3s

    {"cor": (0, 255, 0), "posicao": None,
     "ativo": False, "respawn": pygame.time.get_ticks() + 5000, "intervalo": (2000, 5000)},  # 2 a 5s

    {"cor": (0, 0, 255), "posicao": None,
     "ativo": False, "respawn": pygame.time.get_ticks() + 8000, "intervalo": (3000, 7000)}   # 4 a 8s
]

#Lista de projéteis
projeteis = []
velocidade_tiro = 30 #coloquei o dobro da velocidade do personagem

# Timer para controlar a frequência dos tiros
intervalo_tiro = 300 #300ms = 0.3 segundos
ultimo_tiro = 0

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


    #Desenha fundo, cowboy, coletaveis e projeteis
    tela.fill((255, 255, 255)) #Fundo branco
    cowboy = pygame.draw.rect(tela, (255, 0, 0), (x, y, 50, 50))  #Quadrado vermelho como cowboy provisório
    for tiro in projeteis:
        pygame.draw.rect(tela, (0, 0, 0), (tiro[0], tiro[1], 10, 5)) #projeteis na cor preta

    #Atualiza coletáveis
    for c in coletaveis:
        if c["ativo"]:
            #Desenha coletável
            coletavel = pygame.draw.rect(tela, c["cor"], (c["posicao"][0], c["posicao"][1], 40, 40))
            #Colisão
            for tiro in projeteis:
                if tiro.colliderect(coletavel):
                    c["ativo"] = False
                    min_tempo, max_tempo = c["intervalo"]
                    c["respawn"] = tempo_atual + randint(min_tempo, max_tempo)

        else:
            # Verifica se é hora de reaparecer
            if tempo_atual >= c["respawn"]:
                c["posicao"] = [randint(40, 760), randint(50, 550)]
                c["ativo"] = True

    #atualiza a tela
    pygame.display.flip()
    relogio.tick(60)  # FPS


pygame.quit()