import pygame
from random import randint
#from sys import exit

pygame.init()
pygame.display.set_caption("Seis Tiros no Oeste")
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()
fonte = pygame.font.Font("Bleeding_Cowboys.ttf", 40)
abates = 0

# Posição do cowboy
x, y = 100, 100
velocidade = 15
# Posição do inimigo
w, z = 760, 550

# Configuração dos coletáveis
coletaveis = [
    {"cor": (255, 0, 0), "posicao": None, "vel": [0, 0],
     "ativo": False, "respawn": pygame.time.get_ticks() + 2000, "intervalo": (1000, 3000)},
    
    {"cor": (0, 255, 0), "posicao": None, "vel": [0, 0],
     "ativo": False, "respawn": pygame.time.get_ticks() + 5000, "intervalo": (2000, 5000)},
    
    {"cor": (0, 0, 255), "posicao": None, "vel": [0, 0],
     "ativo": False, "respawn": pygame.time.get_ticks() + 8000, "intervalo": (3000, 7000)}
]

# Lista de projéteis
projeteis = []
velocidade_tiro = 30  # Coloquei o dobro da velocidade do personagem

# Timer para controlar a frequência dos tiros
intervalo_tiro = 300  # 300ms = 0.3 segundos
ultimo_tiro = 0

#Lista de drops
drops = []
tipos_de_drops = [(255,0,0),(0,0,255)]#Ex de cores para os drops
# Loop principal
fim_de_jogo = False
while not fim_de_jogo:
    # Mensagem de abates na tela
    msg = f'Abates: {abates}'
    txt_formatado = fonte.render(msg, True, (0, 0, 0))  # Cor preta para o texto

    # Encerra o jogo se o jogador apertar em sair
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fim_de_jogo = True

    # Verifica teclas pressionadas
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_UP]:
        y -= velocidade
    if teclas[pygame.K_DOWN]:
        y += velocidade
    if teclas[pygame.K_LEFT]:
        x -= velocidade
    if teclas[pygame.K_RIGHT]:
        x += velocidade
    
    if teclas[pygame.K_w]:
        y -= velocidade
    if teclas[pygame.K_s]:
        y += velocidade
    if teclas[pygame.K_a]:
        x -= velocidade
    if teclas[pygame.K_d]:
        x += velocidade

    # Verifica tempo desde o último tiro
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultimo_tiro >= intervalo_tiro:
        projeteis.append([x + 50, y + 20])
        ultimo_tiro = tempo_atual  # Registra o momento do tiro

    for tiro in projeteis:
        tiro[0] += velocidade_tiro

    nova_lista = []
    for t in projeteis:
        if t[0] < largura:  # Bala ainda não passou do lado direito da tela
            nova_lista.append(t)
    projeteis = nova_lista

    # Desenha fundo, cowboy, coletáveis e projéteis
    tela.fill((255, 255, 255))  # Fundo branco
    cowboy = pygame.draw.rect(tela, (255, 0, 0), (x, y, 50, 50))  # Quadrado vermelho como cowboy provisório
    for tiro in projeteis:
        pygame.draw.rect(tela, (0, 0, 0), (tiro[0], tiro[1], 10, 5))  # Projeteis na cor preta

    # Atualiza coletáveis
    for c in coletaveis:
        if c["ativo"]:
            # Atualiza a posição somando a velocidade
            pos_x, pos_y = c["posicao"]
            vel_x, vel_y = c["vel"]

            pos_x += vel_x
            pos_y += vel_y

            # Rebater nas bordas (inverte a direção se bater)
            if pos_x <= 0 or pos_x >= largura - 40:
                vel_x *= -1
            if pos_y <= 0 or pos_y >= altura - 40:
                vel_y *= -1
            
            # Atualizar posição
            c['posicao'] = [pos_x, pos_y]
            c['vel'] = [vel_x, vel_y]
            # Desenha coletável
            coletavel = pygame.draw.rect(tela, c["cor"], (c["posicao"][0], c["posicao"][1], 40, 40))
            # Colisão
            for tiro in projeteis:
                if pygame.Rect(tiro[0], tiro[1], 10, 5).colliderect(coletavel):
                    c["ativo"] = False
                    min_tempo, max_tempo = c["intervalo"]
                    c["respawn"] = tempo_atual + randint(min_tempo, max_tempo)
                    abates += 1
                    if randint(1,100) < 10:
                        cor_drop = tipos_de_drops[randint(0,len(tipos_de_drops) - 1)]
                        pos_drop = [randint(100,700 ), randint(100,500)]
                        drops.append({'cor': cor_drop, 'posicao': pos_drop})
                            
        else:
            # Verifica se é hora de reaparecer
            if tempo_atual >= c["respawn"]:
                c["posicao"] = [randint(400, w), randint(400, z)]
                c["vel"] = [randint(-4, 4), randint(-4, 4)]
                while c["vel"] == [0, 0]:
                    c["vel"] = [randint(-4, 4), randint(-4, 4)]
                c["ativo"] = True

    for drop in drops[:]:  # Iterando sobre uma cópia da lista de drops
        pygame.draw.circle(tela, drop["cor"], (drop["posicao"][0], drop["posicao"][1]), 8)
        
        # Colisão entre o jogador e o drop
        drop_rect = pygame.Rect(drop["posicao"][0] - 8, drop["posicao"][1] - 8, 16, 16)  # Ajuste para o tamanho do círculo
        if pygame.Rect(x, y, 50, 50).colliderect(drop_rect):  # Colisão do cowboy com o drop
            drops.remove(drop)
            intervalo_tiro -= 150

    # Desenha o texto formatado
    tela.blit(txt_formatado, (600, 0))  # Posição do texto de abates

    # Atualiza a tela
    pygame.display.flip()
    relogio.tick(60)  # FPS

pygame.quit()
