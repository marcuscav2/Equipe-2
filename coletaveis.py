import pygame
from config import TELA

class Drop:
    def __init__(self, cor, posicao):
        self.cor = cor
        self.posicao = posicao
        self.raio = 8

    def desenhar(self):
        pygame.draw.circle(TELA, self.cor, (self.posicao[0], self.posicao[1]), self.raio)

    def get_rect(self):
        return pygame.Rect(self.posicao[0] - self.raio, self.posicao[1] - self.raio, self.raio*2, self.raio*2)