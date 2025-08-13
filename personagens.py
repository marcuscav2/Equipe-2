import pygame
from random import randint
from config import LARGURA, ALTURA, TELA, FONTE

class Cowboy:
    def __init__(self, x, y, cor=(255, 0, 0)):
        self.x = x
        self.y = y
        self.velocidade = 15
        self.cor = cor
        self.largura = 50
        self.altura = 50
        self.projeteis = []
        self.velocidade_tiro = 30
        self.intervalo_tiro = 300
        self.ultimo_tiro = 0
        self.vidas = 3
        self.abates = 0
        self.invulneravel_ate = 0  # Adicionado para controlar invulnerabilidade após levar dano



    def mover(self, teclas):
        if teclas[pygame.K_UP] and self.y > 0:
            self.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.y < ALTURA - self.altura:
            self.y += self.velocidade
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.x < LARGURA - self.largura:
            self.x += self.velocidade

        #WASD
        if teclas[pygame.K_w] and self.y > 0:
            self.y -= self.velocidade
        if teclas[pygame.K_s] and self.y < ALTURA - self.altura:
            self.y += self.velocidade
        if teclas[pygame.K_a] and self.x > 0:
            self.x -= self.velocidade
        if teclas[pygame.K_d] and self.x < LARGURA - self.largura:
            self.x += self.velocidade

    def atirar(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_tiro >= self.intervalo_tiro:
            self.projeteis.append([self.x + self.largura, self.y + self.altura // 2])
            self.ultimo_tiro = tempo_atual

    def atualizar_projeteis(self):
        nova_lista = []
        for tiro in self.projeteis:
            tiro[0] += self.velocidade_tiro
            if tiro[0] < LARGURA:
                nova_lista.append(tiro)
        self.projeteis = nova_lista

    def desenhar(self):
    # Verifica se o cowboy está invulnerável
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual < self.invulneravel_ate:
        # Alterna entre branco e vermelho para efeito de "piscar"
            if tempo_atual // 100 % 2 == 0:
                cor_atual = (255, 255, 255)  # Cor branca para invulnerabilidade
            else:
                cor_atual = (255, 0, 0)  # Cor normal (vermelho()
        else:
            cor_atual = (255, 0, 0)  # Cor normal

        # Desenha o cowboy usando a cor definida acima
        pygame.draw.rect(TELA, cor_atual, (self.x, self.y, self.largura, self.altura))

        # Desenha os tiros
        for tiro in self.projeteis:
            pygame.draw.rect(TELA, (0, 0, 0), (tiro[0], tiro[1], 10, 5))

        # Desenha as vidas
        for v in range(self.vidas):
            TELA.blit(coracao_img, (10 + v * 35, 10))

        # Desenha a contagem de abates
        texto = FONTE.render(f"Abates: {self.abates}", True, (0, 0, 0))
        TELA.blit(texto, (600, 0))
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)
    
class Inimigo:
    def __init__(self, cor, velocidade_x, intervalo_respawn):
        self.cor = cor
        self.posicao = None
        self.ativo = False
        self.respawn = pygame.time.get_ticks() + intervalo_respawn[0]
        self.intervalo = intervalo_respawn
        self.velocidade_x = velocidade_x
        self.velocidade_y = randint(-2, 2) or 1
        self.projeteis = []
        self.velocidade_tiro = 10
        self.intervalo_tiro = 200
        self.ultimo_tiro = 0
        self.largura = 40
        self.altura = 40

    def reaparecer(self):
        tempo_atual = pygame.time.get_ticks()
        if not self.ativo and tempo_atual >= self.respawn:
            self.posicao = [randint(800, 900), randint(50, 550)]
            self.velocidade_y = randint(-2, 2) or 1
            self.ativo = True

    def mover(self, cowboy):
        if self.ativo:
            # Movimento X
            self.posicao[0] -= self.velocidade_x
            # Movimento Y com ricochete
            self.posicao[1] += self.velocidade_y
            if self.posicao[1] <= 0 or self.posicao[1] >= ALTURA - self.altura:
                self.velocidade_y *= -1

            # Se encostar na borda esquerda
            tempo_atual = pygame.time.get_ticks()
            if self.posicao[0] <= 0 and tempo_atual > cowboy.invulneravel_ate:
                cowboy.vidas = max(cowboy.vidas - 1, 0)
                cowboy.invulneravel_ate = tempo_atual + 1000  # 1 segundo invulnerabilidade
                self.ativo = False
                self.projeteis.clear()
                min_t, max_t = self.intervalo
                self.respawn = pygame.time.get_ticks() + randint(min_t, max_t)


    def atirar(self):
        tempo_atual = pygame.time.get_ticks()
        if self.posicao and self.posicao[0] < LARGURA - 40:
            if tempo_atual - self.ultimo_tiro >= self.intervalo_tiro:
                self.projeteis.append([self.posicao[0], self.posicao[1] + self.altura // 2])
                self.ultimo_tiro = tempo_atual

    def atualizar_projeteis(self, cowboy):
        nova_lista = []
        for tiro in self.projeteis:
            tiro[0] -= self.velocidade_tiro
            # Verifica colisão com o cowboy e se ele está vulnerável
            if pygame.Rect(tiro[0], tiro[1], 10, 5).colliderect(cowboy.get_rect()):
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual > cowboy.invulneravel_ate:
                    cowboy.vidas -= 1
                    cowboy.invulneravel_ate = tempo_atual + 1000  # Fica invulnerável por 1 segundo
                # Não adiciona o tiro à nova lista para removê-lo
            elif tiro[0] > 0:
                nova_lista.append(tiro)
        self.projeteis = nova_lista


    def desenhar(self):
        if self.ativo:
            pygame.draw.rect(TELA, self.cor, (self.posicao[0], self.posicao[1], self.largura, self.altura))
            for tiro in self.projeteis:
                pygame.draw.rect(TELA, (255, 0, 0), (tiro[0], tiro[1], 10, 5))

    def get_rect(self):

        return pygame.Rect(self.posicao[0], self.posicao[1], self.largura, self.altura)
