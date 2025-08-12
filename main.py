import pygame
from random import randint

pygame.init()
pygame.display.set_caption("Seis Tiros no Oeste")
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 40)
abates = 0

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
inimigos = [
    {"cor": (255, 0, 0), "posicao": None, "velocidade_x": 2, "velocidade_y": randint(-2, 2) or 1,
     "ativo": False,  "ultimo_tiro": 0, "respawn": pygame.time.get_ticks() + 2000, "intervalo": (1000, 3000)},
    
    {"cor": (0, 255, 0), "posicao": None, "velocidade_x": 3, "velocidade_y": randint(-2, 2) or 1,
     "ativo": False,  "ultimo_tiro": 0, "respawn": pygame.time.get_ticks() + 5000, "intervalo": (2000, 5000)},
    
    {"cor": (0, 0, 255), "posicao": None, "velocidade_x": 4, "velocidade_y": randint(-2, 2) or 1,
     "ativo": False,  "ultimo_tiro": 0, "respawn": pygame.time.get_ticks() + 8000, "intervalo": (4000, 8000)}
]

projeteis_inimigo = []
intervalo_tiro_inimigo = 200  #tempo entre tiros em ms
ultimo_tiro_inimigo = 0
velocidade_tiro_inimigo = 10

#Lista de drops
drops = []
tipos_de_drops = [(255,0,0),(0,0,255)]#Ex de cores para os drops

#Loop principal
fim_de_jogo = False
while not fim_de_jogo:

    #encerra o jogo se o jogador apertar em sair
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fim_de_jogo = True

    # Mensagem de abates na tela
    msg = f'Abates: {abates}'
    txt_formatado = fonte.render(msg, True, (0, 0, 0))  # Cor preta para o texto

    #Verifica teclas pressionadas
    teclas = pygame.key.get_pressed()

    #Movimenta com setas
    if teclas[pygame.K_LEFT] and x > 0: #O x > 0 ta limitando o personagem para ele não sair da tela 
        x -= velocidade
    if teclas[pygame.K_RIGHT] and x < largura - 50:
        x += velocidade
    if teclas[pygame.K_UP] and y > 0:
        y -= velocidade
    if teclas[pygame.K_DOWN] and y < altura - 50:
        y += velocidade

    #Movimentava WASD
    if teclas[pygame.K_w] and y > 0:
        y -= velocidade
    if teclas[pygame.K_s] and y < altura - 50:
        y += velocidade
    if teclas[pygame.K_a] and x > 0:
        x -= velocidade
    if teclas[pygame.K_d] and x < largura - 50:
        x += velocidade


    
    # Verifica tempo desde o último tiro
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultimo_tiro >= intervalo_tiro:
        projeteis.append([x + 50, y + 20])
        ultimo_tiro = tempo_atual  #registra o momento do tiro

    for tiro in projeteis:
        tiro[0] += velocidade_tiro

    nova_lista = []
    for t in projeteis:
        if t[0] < largura: #bala ainda não passou do lado direito da tela
            nova_lista.append(t)
    projeteis = nova_lista


    #Desenha fundo, cowboy, inimigos e projeteis
    tela.fill((255, 255, 255))  # Fundo branco
    cowboy = pygame.draw.rect(tela, (255, 0, 0), (x, y, 50, 50))  #Quadrado vermelho como cowboy provisório
    for tiro in projeteis:
        pygame.draw.rect(tela, (0, 0, 0), (tiro[0], tiro[1], 10, 5)) #projeteis na cor preta
    for tiro in projeteis_inimigo:
        pygame.draw.rect(tela, (255, 0, 0), (tiro[0], tiro[1], 10, 5))  # vermelho


    #Atualiza inimigos
    for i in inimigos:

        if i["ativo"]:

            #tiros do inimigo
            if i["posicao"][0] < largura - 40: #so atira quando tiver dentro da tela 
                if tempo_atual - ultimo_tiro_inimigo >= intervalo_tiro_inimigo:
                    if tempo_atual - i["ultimo_tiro"] >= intervalo_tiro_inimigo:
                        projeteis_inimigo.append([i["posicao"][0], i["posicao"][1] + 20])
                        i["ultimo_tiro"] = tempo_atual

            for tiro in projeteis_inimigo:
                tiro[0] -= velocidade_tiro_inimigo

            cowboy_rect = pygame.Rect(x, y, 50, 50)
            for tiro in projeteis_inimigo:
                if cowboy_rect.colliderect(pygame.Rect(tiro[0], tiro[1], 10, 5)):
                    fim_de_jogo = True

            #Remover tiros que saíram da tela
            projeteis_inimigo = [t for t in projeteis_inimigo if t[0] > 0]

            #Mover no eixo x
            i["posicao"][0] -= i["velocidade_x"]

            #Mover no eixo y
            i["posicao"][1] += i["velocidade_y"]

            #Ricochete nas bordas
            if i["posicao"][1] <= 0 or i["posicao"][1] >= altura - 40:
                i["velocidade_y"] *= -1


            #Se o inimigo encostar na borda, fim de jogo
            if i["posicao"][0] <= 0:
                fim_de_jogo = True

            #Desenha o inimigo
            inimigo = pygame.draw.rect(tela, i["cor"], (i["posicao"][0], i["posicao"][1], 40, 40))

            #Colisão do tiro do jogador com o inimigo
            for tiro in projeteis:
                tiro = pygame.Rect(tiro[0], tiro[1], 10, 5)
                if tiro.colliderect(inimigo):
                    i["ativo"] = False
                    min_tempo, max_tempo = i["intervalo"]
                    i["respawn"] = tempo_atual + randint(min_tempo, max_tempo)
                    abates += 1
                    # Chance de drop
                    if randint(1,100) < 10:  # 10% de chance
                        cor_drop = tipos_de_drops[randint(0, len(tipos_de_drops) - 1)]
                        pos_drop = i["posicao"][:]  # drop na posição do inimigo
                        drops.append({'cor': cor_drop, 'posicao': pos_drop})

        else:
            # Verifica se é hora de reaparecer
            if tempo_atual >= i["respawn"]:
                    i["posicao"] = [randint(800, 900), randint(50, 550)]
                    i["velocidade_y"] = randint(-2, 2) or 1
                    i["ativo"] = True

    #Logica de exibir e coletar os drops
    for drop in drops[:]:  # Iterando sobre uma cópia da lista de drops
        pygame.draw.circle(tela, drop["cor"], (drop["posicao"][0], drop["posicao"][1]), 8)
        
        # Colisão entre o jogador e o drop
        drop_rect = pygame.Rect(drop["posicao"][0] - 8, drop["posicao"][1] - 8, 16, 16)  # Ajuste para o tamanho do círculo
        if pygame.Rect(x, y, 50, 50).colliderect(drop_rect):  # Colisão do cowboy com o drop
            drops.remove(drop)
            intervalo_tiro = max(100, intervalo_tiro - 150) #limitando para o intervalo nunca ser menor que 100ms, assim não tem o risco de ficar negativo


    #Desenha o texto formatado
    tela.blit(txt_formatado, (600, 0))  # Posição do texto de abates

    #atualiza a tela
    pygame.display.flip()
    relogio.tick(60)  # FPS


pygame.quit()