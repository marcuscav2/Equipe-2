import pygame
from random import randint
from config import TELA, RELOGIO
from personagens import Cowboy, Inimigo
from coletaveis import Drop

pygame.init()

# ----------------- FUNÇÃO PRINCIPAL -----------------
def main():
    cowboy = Cowboy(100, 100)
    inimigos = [
        Inimigo((255, 0, 0), 2, (1000, 3000)),
        Inimigo((0, 255, 0), 3, (2000, 5000)),
        Inimigo((0, 0, 255), 4, (4000, 8000))
    ]
    drops = []
    tipos_drops = [(255, 0, 0), (0, 0, 255)]
    fim_de_jogo = False

    while not fim_de_jogo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fim_de_jogo = True

        teclas = pygame.key.get_pressed()
        cowboy.mover(teclas)
        cowboy.atirar()
        cowboy.atualizar_projeteis()

        for inimigo in inimigos:
            inimigo.reaparecer()
            if inimigo.ativo:
                inimigo.mover(cowboy)
                inimigo.atirar()
                inimigo.atualizar_projeteis(cowboy)

                # colisão tiro do cowboy com inimigo
                for tiro in cowboy.projeteis[:]:
                    if pygame.Rect(tiro[0], tiro[1], 10, 5).colliderect(inimigo.get_rect()):
                        inimigo.ativo = False
                        inimigo.projeteis.clear()
                        min_t, max_t = inimigo.intervalo
                        inimigo.respawn = pygame.time.get_ticks() + randint(min_t, max_t)
                        cowboy.abates += 1
                        cowboy.projeteis.remove(tiro)
                        if randint(1, 100) <= 10:  # 10% de chance
                            cor = tipos_drops[randint(0, len(tipos_drops) - 1)]
                            drops.append(Drop(cor, inimigo.posicao[:]))


        # Drops
        for drop in drops[:]:
            drop.desenhar()
            if cowboy.get_rect().colliderect(drop.get_rect()):
                drops.remove(drop)
                cowboy.intervalo_tiro = max(100, cowboy.intervalo_tiro - 150)

                

        # Desenho
        TELA.fill((255, 255, 255))
        cowboy.desenhar()
        for inimigo in inimigos:
            inimigo.desenhar()

        pygame.display.flip()
        RELOGIO.tick(60)

        if cowboy.vidas <= 0:
            fim_de_jogo = True

    pygame.quit()

if __name__ == "__main__":
    main()