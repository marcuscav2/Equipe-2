import pygame
from config import TELA, LARGURA, ALTURA, RELOGIO

def tela_game_over():
    fonte_titulo = pygame.font.Font(None, 80)
    fonte_botao = pygame.font.Font(None, 50)
    jogando = True
    while jogando:
        TELA.fill((0, 0, 0))  # fundo preto

        # Texto "GAME OVER"
        texto = fonte_titulo.render("GAME OVER", True, (255, 0, 0))
        rect_texto = texto.get_rect(center=(LARGURA // 2, ALTURA // 3))
        TELA.blit(texto, rect_texto)

        # Botão "Jogar Novamente"
        texto_botao = fonte_botao.render("Jogar Novamente", True, (255, 255, 255))
        rect_botao = texto_botao.get_rect(center=(LARGURA // 2, ALTURA // 2))
        pygame.draw.rect(TELA, (0, 128, 0), rect_botao.inflate(20, 10))  # fundo do botão
        TELA.blit(texto_botao, rect_botao)

        # Captura eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_botao.collidepoint(event.pos):
                    return  # Sai do menu e volta pro jogo

        pygame.display.flip()
        RELOGIO.tick(60)
