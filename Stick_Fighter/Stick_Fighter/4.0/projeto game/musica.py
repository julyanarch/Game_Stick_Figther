import pygame

def init_and_play_music(file_path, volume=0.5, loops=-1):
    
    pygame.mixer.init() # Inicializa o mixer

    pygame.mixer.music.load("music/Guile's Theme 8 Bit Remix - Street Fighter 2.mp3") # Carrega a música
    pygame.mixer.music.set_volume(volume) # Define o volume
    pygame.mixer.music.play(loops) # Reproduz em loop
   

def stop_music():
    #Para a reprodução da música de fundo.
    pygame.mixer.music.stop()
    print("Música parada.")