#importa a biblioteca pygame
import pygame
from fighter import fighter
from musica import init_and_play_music, stop_music # Importa as funções do novo módulo


# Inicializa o Pygame e o módulo de fontes
pygame.init()
pygame.font.init()



MUSIC_FILE_PATH = 'music/Guile\'s Theme 8 Bit Remix - Street Fighter 2.mp3'
init_and_play_music(MUSIC_FILE_PATH) # Chama a função para iniciar a música
# --- Fim da Configuração de Áudio ---


#define o tamanho da janela
janela_altura= 600
janela_largura= 800
janela= pygame.display.set_mode((janela_largura , janela_altura))

font = pygame.font.Font(None, 80)

#define o nome do jogo
pygame.display.set_caption('stick fighther')

#define o fps do jogo
clock = pygame.time.Clock()
fps = 60


#define cor das barras de vida
YELLOW = (255, 255 ,0)
RED =(255,0,0)
WHITE =(255,255,255)


#define cenario
cenario = pygame.image.load("images\cenario luta.jpg").convert_alpha()


#define funçao desenhar cenario
def drawn_cenario():
    scaled_cenario= pygame.transform.scale(cenario,(janela_largura ,janela_altura))
    janela.blit(scaled_cenario,(0,0))


#desenha barras de vida
def drawn_health_bar(health,x,y):
    ratio = health /100
    pygame.draw.rect(janela,WHITE,(x-5,y-5,310,40))#desenha a borda da barra de vida
    pygame.draw.rect(janela,RED,(x,y,300,30))#desenha a barra de vida perdida
    pygame.draw.rect(janela,YELLOW,(x,y,300 * ratio,30)) #desenha a barra de vida que altera o tamanho 


#define posição dos personagens
fighter_1 = fighter(200, 410)
fighter_2 = fighter(500, 410)


game_over = False
winner_text = ""

# Define a variável rum para iniciar o loop do jogo
rum = True

#mantem a janela aberta
while rum:

    clock.tick(fps)

    drawn_cenario()

    drawn_health_bar(fighter_1.helth, 10, 20)
    drawn_health_bar(fighter_2.helth, 490, 20)

    if not game_over:
        # mover fighters
        fighter_1.move(janela_largura, janela_altura, janela, fighter_2)
        fighter_2.move1(janela_largura, janela_altura, janela, fighter_1)

        # Verifica a condição de vitória
        if fighter_1.helth <= 0:
            winner_text = "Player 2 venceu!"
            game_over = True
            stop_music() # Para a música ao final do jogo
        elif fighter_2.helth <= 0:
            winner_text = "Player 1 venceu!"
            game_over = True
            stop_music() # Para a música ao final do jogo

    for Events in pygame.event.get():
        # fecha a janela se clicar no X
        if Events.type == pygame.QUIT:
            rum = False

    # desenha os personagens
    fighter_1.draw(janela)
    fighter_2.draw(janela)

    # Exibe o texto de vitória se o jogo acabou
    if game_over:
        text_surface = font.render(winner_text, True, RED)
        text_rect = text_surface.get_rect(center=(janela_largura // 2, janela_altura // 2))
        janela.blit(text_surface, text_rect)

    # atualiza a exibição na tela
    pygame.display.update()

pygame.quit()