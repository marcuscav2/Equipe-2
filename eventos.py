import pygame
from config import intervalo_tiro

# Verifica se o usuário fechou a janela
def verificar_saida():
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            return True
    return False
    

# Controla o movimento do cowboy com base nas teclas
def mover_cowboy(teclas,cowboy):
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        cowboy.y -= cowboy.velocidade
    
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        cowboy.y += cowboy.velocidade

    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        cowboy.x -= cowboy.velocidade
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        cowboy.x += cowboy.velocidade

# Controla a lógica de tiro do cowboy (tempo e criação)
def controlar_tiro (cowboy, projeteis, ultimo_tiro):
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultimo_tiro >= intervalo_tiro:
        projeteis.append(cowboy.atirar())
        ultimo_tiro = tempo_atual
    return ultimo_tiro
