import pygame


class fighter():
    def __init__(self, x, y):
        self.flip =False
        self.rect = pygame.Rect(x, y, 80, 180) # x, y, largura, altura
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.helth = 100
        self.image_sprite = [pygame.image.load("images/stop ryu 2.png"),#ryu stop (0)
                             pygame.image.load("images/stop ryu 2.png"),#ryu passo1 (1)
                             pygame.image.load("images/stop ryu 2.png"),#ryu passo2 (2)

                             pygame.image.load("images/ken01png.png"),#ken stop (3)
                             pygame.image.load("images/ken01_walk_1.png"),#ken passo1 (4)
                             pygame.image.load("images/ken01_walk_2.png"),#ken passo2 (5)
                             pygame.image.load("images/ken01_jump_up_01.png"),#ken pulo1 (6)
                             pygame.image.load("images/ken01_stand_punsh_far_01.png"),#ken soco 1 (7) - prepara
                             pygame.image.load("images/ken01_stand_punch_far_02.png"),#ken soco 2 (8) - da o soco
                             pygame.image.load("images/fighters_1.png"),#ryu passo 1 (9)
                             pygame.image.load("images/ryu02_walk_02.png"),#ryu passo 2 (10) 
                             pygame.image.load("images/ryu02_jump_up_01.png"),#ryu jump (11)
                             # NOVOS SPRITES PARA O SOCO DO RYU
                             pygame.image.load("images/fighters_2_stand_punsh_far_01.png"), 
                             pygame.image.load("images/fighters_2_stand_punch_far_02.png")]
        
        self.next_image_idx = 0
        self.n_falses = 0 
        self.count =0
        self.cont1 =0
        self.cont2 =0
        self.cont3 =0
        self.cont4 =0

        self.flag = False # Para controle de pulo do Ken
        self.flag1 = False # Para controle de pulo do Ryu

        # Variáveis para a animação do soco (compartilhadas para Ken e Ryu)
        self.punch_animation_total_frames = 15 # Duração total para a animação de soco (0.25 segundos * 60 FPS)
        self.punch_frame_1_duration = self.punch_animation_total_frames // 2 # ~7 ou 8 frames para o primeiro sprite
        self.punch_frame_2_duration = self.punch_animation_total_frames # 15 frames para o segundo sprite


    def move1(self, janela_largura, janela_altura, surface, target):
        SPEED = 5
        grvidade = 2
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        
        # Resetar para o sprite de parado se não houver movimento E não estiver atacando E não estiver pulando.
        self.n_falses += 1
        if self.n_falses >= 15 and not self.jump and not self.attacking:
            self.next_image_idx = 3 # Ken parado (padrão)

        # Pulo
        # Só permite pular se não estiver pulando E não estiver atacando
        if key[pygame.K_UP] and self.jump == False and not self.attacking:
            self.vel_y = -30
            self.jump = True
            self.flag = True # Sinaliza que o pulo começou
            self.next_image_idx = 6 # Ken pulando (definido aqui, pode ser sobrescrito pelo soco se ele cair e atacar)
                        
        if self.attacking == False: # Só permite movimento se não estiver atacando
            # Movimento
            if key[pygame.K_LEFT]:  # Seta para ESQUERDA
                dx = -SPEED # Move para a esquerda
                self.n_falses = 0
                if self.next_image_idx == 3 or self.next_image_idx == 5:
                    self.cont1 += 1
                    if self.cont1 > 15:
                        self.cont2 = 3
                        self.next_image_idx = 4 # Ken andando 1
                elif self.next_image_idx == 4:
                    self.cont2 += 1
                    if self.cont2 > 15:
                        self.cont1 = 3
                        self.next_image_idx = 5 # Ken andando 2
                        
            if key[pygame.K_RIGHT]: # Seta para DIREITA
                dx = SPEED # Move para a direita
                self.n_falses = 0
                if self.next_image_idx == 3 or self.next_image_idx == 5:
                    self.cont1 += 1
                    if self.cont1 > 15:
                        self.cont2 = 3
                        self.next_image_idx = 4 # Ken andando 1
                elif self.next_image_idx == 4:
                    self.cont2 += 1
                    if self.cont2 > 15:
                        self.cont1 = 3
                        self.next_image_idx = 5 # Ken andando 2

            # Ataque (Ken - Player 2)
            if key[pygame.K_i]: 
                self.attack_p2(surface, target) # Chama o método de ataque
                self.count = 0 # Reinicia o contador para a duração da animação de soco
                self.attacking = True # Ativa o estado de ataque
                self.attack_type = 1 # Define o tipo de ataque como 1 (soco padrão)
                self.next_image_idx = 7 # COMEÇA A ANIMAÇÃO DO KEN AQUI (sprite 7)
                    
        # Aplica gravidade
        self.vel_y += grvidade
        dy += self.vel_y

        # Limite do cenário
        if self.rect.bottom + dy > janela_altura - 110:
            dy = janela_altura - 110 - self.rect.bottom
            self.vel_y = 0
            self.jump = False 

            if self.flag == True:
                # Volta para Ken parado apenas se não estiver atacando
                if not self.attacking: 
                    self.next_image_idx = 3 
                self.flag = False

        # Deixa os players um de frente para o outro (Lógica de flip para o Player 2 - Ken)
        if target.rect.centerx > self.rect.centerx: 
            self.flip = True 
        else: 
            self.flip = False 

        # Limite do cenário (laterais)
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > janela_largura:
            dx = janela_largura - self.rect.right

        # Atualiza player position
        self.rect.x += dx
        self.rect.y += dy
        
    # move para o Player 1 (Ryu)
    def move(self, janela_largura, janela_altura, surface, target):
        SPEED = 5
        grvidade = 2
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        
        # Resetar para o sprite de parado se não houver movimento E não estiver atacando E não estiver pulando.
        self.n_falses += 1
        if self.n_falses >= 10 and not self.jump and not self.attacking:
            self.next_image_idx = 0 # Ryu parado

        # Pulo
        if key[pygame.K_w] and self.jump == False and not self.attacking: # Não pode pular enquanto ataca
            self.vel_y = -30
            self.jump = True
            self.flag1 = True # Sinaliza que o pulo começou
            self.next_image_idx = 11 # Ryu pulando

        if self.attacking == False: # Só permite movimento se não estiver atacando
            # Movimento
            if key[pygame.K_a]: # Tecla 'A'
                dx = -SPEED # Move para a esquerda
                self.n_falses = 0
                if self.next_image_idx == 0 or self.next_image_idx == 10:
                    self.cont1 += 1
                    if self.cont1 > 15:
                        self.cont2 = 0
                        self.next_image_idx = 9 # Ryu andando 1
                elif self.next_image_idx == 9:
                    self.cont2 += 1
                    if self.cont2 > 15:
                        self.cont1 = 3
                        self.next_image_idx = 10 # Ryu andando 2
                        
            if key[pygame.K_d]: # Tecla 'D'
                dx = SPEED # Move para a direita
                self.n_falses = 0
                if self.next_image_idx == 0 or self.next_image_idx == 10:
                    self.cont1 += 1
                    if self.cont1 > 15:
                        self.cont2 = 0
                        self.next_image_idx = 9 # Ryu andando 1
                elif self.next_image_idx == 9:
                    self.cont2 += 1
                    if self.cont2 > 15:
                        self.cont1 = 3
                        self.next_image_idx = 10 # Ryu andando 2

            # Ataque (Ryu - Player 1)
            if key[pygame.K_r]: # Tecla para o primeiro tipo de ataque do Ryu
                self.attack(surface, target)
                self.count = 0 # Reinicia o contador para animação de ataque
                self.attacking = True # Garante que o estado de ataque seja True
                self.attack_type = 2 # Define o tipo de ataque como 2 (soco do Ryu)
                self.next_image_idx = 12 # COMEÇA A ANIMAÇÃO DO RYU AQUI (sprite 12)
                
        # Aplica gravidade
        self.vel_y += grvidade
        dy += self.vel_y

        # Limite do cenário
        if self.rect.bottom + dy > janela_altura - 110:
            dy = janela_altura - 110 - self.rect.bottom
            self.vel_y = 0
            self.jump = False 
            if self.flag1 == True:
                # Volta para Ryu parado apenas se não estiver atacando
                if not self.attacking:
                    self.next_image_idx = 0 
                self.flag1 = False

        # Deixa os players um de frente para o outro (Lógica de flip para o Player 1 - Ryu)
        if target.rect.centerx > self.rect.centerx:
            self.flip = False # Ryu olhando para a direita (imagem original)
        else:
            self.flip = True # Ryu olhando para a esquerda (imagem original é virada)

        # Limite do cenário (laterais)
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > janela_largura:
            dx = janela_largura - self.rect.right

        # Atualiza player position
        self.rect.x += dx
        self.rect.y += dy

    # Função de ataque para o Player 1 (Ryu)
    def attack(self, surface, target):
        attacking_rect = pygame.Rect(self.rect.right if not self.flip else self.rect.x - self.rect.width, 
                                     self.rect.y, self.rect.width, self.rect.height)
        # pygame.draw.rect(surface, (0, 255, 0), attacking_rect) # REMOVIDO: Debug hitbox do Ryu
        if attacking_rect.colliderect(target.rect):
            target.helth -= 10
            
    # FUNÇÃO DE ATAQUE PARA O PLAYER 2 (Ken)
    def attack_p2(self, surface, target): 
        attacking_rect = pygame.Rect(self.rect.right if self.flip else self.rect.x - self.rect.width, 
                                     self.rect.y, self.rect.width, self.rect.height)
        # pygame.draw.rect(surface, (255, 0, 255), attacking_rect) # REMOVIDO: Debug hitbox do Ken
        if attacking_rect.colliderect(target.rect):
            target.helth -= 10
            
    def draw(self, surface):
        # Lógica da ANIMAÇÃO DE SOCO para Ken (Player 2, type 1)
        if self.attacking and self.attack_type == 1: # Se for o soco do Ken (type 1)
            if self.count < self.punch_frame_1_duration: 
                self.next_image_idx = 7 # Sprite "prepara o soco" do Ken
            elif self.count < self.punch_frame_2_duration:
                self.next_image_idx = 8 # Sprite "dá o soco" do Ken
            else: # Animação concluída
                self.attacking = False
                self.count = 0 # Reseta o contador para o próximo ataque
                
                # Após o ataque, retorna ao sprite parado (3 para Ken)
                # OU ao sprite de pulo se ainda estiver no ar
                if not self.jump: # Se não estiver pulando, volta para parado
                    self.next_image_idx = 3 
                else: # Se estiver pulando, volta para o sprite de pulo
                    self.next_image_idx = 6 
        
        # Lógica da ANIMAÇÃO DE SOCO para Ryu (Player 1, type 2)
        elif self.attacking and self.attack_type == 2: # Se for o soco do Ryu (type 2)
            if self.count < self.punch_frame_1_duration: 
                self.next_image_idx = 12 # Sprite "prepara o soco" do Ryu
            elif self.count < self.punch_frame_2_duration:
                self.next_image_idx = 13 # Sprite "dá o soco" do Ryu
            else: # Animação concluída
                self.attacking = False
                self.count = 0 # Reseta o contador para o próximo ataque
                
                # Após o ataque, retorna ao sprite parado (0 para Ryu)
                # OU ao sprite de pulo se ainda estiver no ar
                if not self.jump: # Se não estiver pulando, volta para parado
                    self.next_image_idx = 0 
                else: # Se estiver pulando, volta para o sprite de pulo
                    self.next_image_idx = 11

        # Obtém a imagem do sprite atual
        image = self.image_sprite[self.next_image_idx]
        
        # Aplica o flip horizontal se necessário
        if self.flip:
            image = pygame.transform.flip(image, True, False) 
        surface.blit(image,  (self.rect.x,self.rect.y))

        # Incrementa o contador de ataque SOMENTE se estiver atacando
        if self.attacking:
            self.count += 1