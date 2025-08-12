import pygame
from random import randint

pygame.init()
pygame.display.set_caption("Seis Tiros no Oeste")
largura, altura = 800, 600


#Velocidades
velocidade = 15
velocidade_tiro = 30 #coloquei o dobro da velocidade do personagem
velocidade_tiro_inimigo = 10



#tempos de intervalos dos tiros

#tempo entre tiros em ms
intervalo_tiro_inimigo = 200  
intervalo_tiro = 300 


# cores

cor_cowboy = (255, 0, 0)  # Vermelho
cor_inimigo = (0, 0, 255) # Azul
cor_tiro = (0, 0, 0) # Preto (tiro do jogador)
cor_tiro_inimigo = (255, 0, 0) # Vermelho (tiro do inimigo)


# Intervalo de respawn do inimigo e para ser usado no main
respawn_intervalo = (3000, 7000)



