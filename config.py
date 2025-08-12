import pygame
from random import randint

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Seis Tiros no Oeste")
RELOGIO = pygame.time.Clock()
FONTE = pygame.font.SysFont("arial", 40)
ABATES = 0
VIDAS = 3