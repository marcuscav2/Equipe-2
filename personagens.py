import pygame

class Projetil:
    def __init__(self, x, y, largura=10, altura=5, velocidade_x=10):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.velocidade_x = velocidade_x

    def mover(self):
        self.rect.x += self.velocidade_x

class Personagem:
    def __init__(self, x, y, velocidade=5, vida=3):
        # Posição
        self.x = x
        self.y = y

        # Velocidade de movimento
        self.velocidade = velocidade

        # Vida do personagem
        self.vida = vida

        # Tamanho do personagem para desenhar ou colisões
        self.largura = 40
        self.altura = 60

        # Retângulo para colisão e desenho
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        # Atualiza a posição do retângulo para ficar sincronizado com x e y
        self.rect.topleft = (self.x, self.y)


    def mover(self, dx, dy):
        #Move o personagem somando o deslocamento dx e dy
        self.x += dx * self.velocidade
        self.y += dy * self.velocidade
        self.rect.topleft = (self.x, self.y)

    def atirar(self):
        # Cria um retângulo que representa o projétil começando na frente do personagem
        proj_pos_x = self.x + self.largura
        proj_pos_y = self.y + self.altura // 2  # Meio vertical do personagem

        # Cria o projétil como um objeto Projetil
        return Projetil(proj_pos_x, proj_pos_y)

    def desenhar(self, tela):
        #Desenha o personagem na tela
        pygame.draw.rect(tela, (0, 0, 255), self.rect)  # Retângulo azul como personagem

    def perder_vida(self, dano=1):
        self.vida -= dano
        if self.vida <= 0:
            self.morrer()

    def morrer(self):
        print("Personagem morreu")
