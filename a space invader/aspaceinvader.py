#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 09:39:29 2020

@author: ta0a2000t
"""

#a space invader by ta0a2000t

import random
import pygame
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (255, 100, 203)
purple = (230,230,250)
yellow = (255, 255, 0)
screen_width = 550
screen_height = 800
size = [screen_width, screen_height]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('A Space Invader')
clock = pygame.time.Clock()
FPS = 40

pygame.mouse.set_visible(0)
heart_image = pygame.image.load('heart_image.png').convert()
heart_image.set_colorkey(black)
lobby_image = pygame.image.load('lobby_image.png').convert()
gameover_sound = pygame.mixer.Sound('gameover_sound.ogg')
player_weapon_sound = pygame.mixer.Sound('player_weapon_sound.ogg')
alien_hit_sound = pygame.mixer.Sound('alien_hit_sound.ogg')
alien_distroyed_sound = pygame.mixer.Sound('alien_distroyed_sound.ogg')
alien_move_down_sound = pygame.mixer.Sound('alien_move_down_sound.ogg')
player_hit_sound = pygame.mixer.Sound('player_hit_sound.ogg')
new_wave_sound = pygame.mixer.Sound('new_wave_sound.ogg')
iamanalligator_sound = pygame.mixer.Sound('iamanalligator.ogg')

background1 = pygame.image.load('Space-Background-1.jpg')
background2 = pygame.image.load('Space-Background-2.jpg')
background3 = pygame.image.load('Space-Background-3.jpg')
background4 = pygame.image.load('Space-Background-4.jpg')
background5 = pygame.image.load('Space-Background-5.jpg')

backgrounds_list = [background1, background2, background3, background4,\
                    background5]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        
        self.speed_x1 = 0
        self.speed_x2 = 0
        self.speed_y1 = 0
        self.speed_y2 = 0
        self.damage = 10

        self.health = 30
        self.lives = 3
        self.width = 40
        self.height = 20
        self.color = blue     
        self.fire_rate = 1 #per second
        self.reloading = False
        self.weapon_reload = 0
        self.score = 0
        self.bar_red_length = 0
        
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        
        self.rect.x = screen_width / 2
        self.rect.y = screen_height - 50

        
    def update(self): #use this if want mouse control
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = mouse_pos[0]
        if mouse_pos[1] <= screen_height - 150:
            self.rect.y = screen_height - 150
        elif mouse_pos[1] > screen_height - 150:
            self.rect.y = mouse_pos[1]
    def draw_health_bar(self):
        self.bar_green_length = self.width
        self.bar_location_y = self.rect.y + self.height + 5
        self.bar_location_x = self.rect.x
        pygame.draw.rect(screen, green, [self.bar_location_x, self.bar_location_y, self.bar_green_length, 5])
        pygame.draw.rect(screen, red, [self.bar_location_x, self.bar_location_y, self.bar_red_length, 5])
        
    def reset(self):
     
        self.speed_x1 = 0
        self.speed_x2 = 0
        self.speed_y1 = 0
        self.speed_y2 = 0
        
        self.health = 30
        self.lives = 3
        self.width = 40
        self.height = 20
        self.color = blue     
        self.fire_rate = 1 #per second
        self.reloading = False
        self.weapon_reload = 0
        self.score = 0
        self.bar_red_length = 0
        
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        
        self.rect.x = screen_width / 2
        self.rect.y = screen_height - 50

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.speed = 3
        self.width = 3
        self.height = 8
        self.color = red
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        
        
  
    def update(self):
        self.rect.y -= self.speed


class Alien(pygame.sprite.Sprite):
    width = 30
    height = 15
    
    step = width // 4
    loop = 0
    spacing = width//2
    move_down = False
        
    def __init__(self):
        super().__init__()
        self.health = 10
        self.bar_red_length = 0
        self.bar_green_length = 30
        self.bar_location_y = 0
        
        
        self.fire_rate = 15 #the less the faster
        self.reloading = True
        self.weapon_reload = 0
        
    def draw_health_bar(self):
        self.bar_location_y = self.rect.y + self.height + 5
        self.bar_location_x = self.rect.x
        pygame.draw.rect(screen, green, [self.bar_location_x, self.bar_location_y, self.bar_green_length, 5])
        pygame.draw.rect(screen, red, [self.bar_location_x, self.bar_location_y, self.bar_red_length, 5])
        
    
    def update(self):
        if Alien.loop > FPS * len(aliens_list) * 0.5:
            Alien.loop = 0
            for alien in aliens_list: #check if near boundry
                alien.weapon_reload += 1
                if abs(alien.rect.x - player.rect.x) < 50 and alien.weapon_reload > alien.fire_rate:
                   alien.weapon_reload = 0
                   alien.reloading = False
                   
                   
                if alien.rect.x + 2 * Alien.step + alien.width > screen_width\
                or alien.rect.x  +  2 * Alien.step < 0:
                    Alien.move_down = True
                    
            if Alien.move_down == False:
                for alien in aliens_list:
                    alien.rect.x += Alien.step
            else: #movedown == true
                Alien.move_down = False
                alien_move_down_sound.play()
                for alien in aliens_list:
                    alien.rect.y += 35
                
                Alien.step *= -1                
        Alien.loop += 1
        if len(aliens_list) < 10:
            Alien.loop += 4
            if len(aliens_list) < 4:
                Alien.loop += 4
          
    def alien_shoot(self):
        if self.reloading == False:
            self.reloading = True
            shoot = Shoot()
            shoot.rect.x = self.rect.x + self.width/2
            shoot.rect.y = self.rect.y + self.height
            shoot_list.add(shoot)
            all_sprites_list.add(shoot)
class Alien1(Alien):  #the alien classes would help if further \
                            #details were added into the game
                            #but now they can be combined into one
    def __init__(self):
        super().__init__()

        self.health = self.health
        self.color = white
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)


        self.rect = self.image.get_rect() 
        self.rect.x = (self.spacing + self.width) * 3
        self.rect.y = self.spacing
        


class Alien2(Alien):
    def __init__(self):
        super().__init__()
        
        self.health = self.health * 2
        self.color = pink
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)


        self.rect = self.image.get_rect() 
        self.rect.x = (self.spacing + self.width) * 3
        self.rect.y = self.spacing
        
        
class Alien3(Alien):
    def __init__(self):
        super().__init__()
        
        self.health = self.health * 3
        self.color = yellow
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)


        self.rect = self.image.get_rect() 
        self.rect.x = (self.spacing + self.width) * 3
        self.rect.y = self.spacing
        
class Shoot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.speed = 3
        self.width = 4
        self.height = 8
        self.color = random.choice([yellow, blue, pink, green])
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.y += self.speed




all_sprites_list = pygame.sprite.Group()
laser_list = pygame.sprite.Group() #player laser
aliens_list = pygame.sprite.Group()
alien1_list = pygame.sprite.Group()
alien2_list = pygame.sprite.Group()
alien3_list = pygame.sprite.Group()
shoot_list = pygame.sprite.Group() #alien laser
player = Player()
all_sprites_list.add(player)

alien1_0 = Alien1()


#spawn_alien1(10)
        
def spawn_aliens(rows):
    grid = []
    columns = screen_width // (alien1_0.width + alien1_0.spacing) - 4
    if columns <= 0:
        columns = 1
    
    for r in range(rows):
        rr = []
        for c in range(columns):
            rr += [random.choice([1, 2, 3])]
        
        grid += [rr]
            
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 1:
                alien1 = Alien1()
    
                alien1.rect.y = 35 * (1 + y)
                alien1.rect.x = alien1_0.rect.x + alien1_0.spacing + (alien1_0.width + alien1_0.spacing) * x
                
                alien1_list.add(alien1)
                aliens_list.add(alien1)
                all_sprites_list.add(alien1)
            elif grid[y][x] == 2:
                alien2 = Alien2()
                alien2.rect.y = 35 * (1 + y)
                alien2.rect.x = alien1_0.rect.x + alien1_0.spacing + (alien1_0.width + alien1_0.spacing) * x

                alien2_list.add(alien2)
                aliens_list.add(alien2)
                all_sprites_list.add(alien2)
                
            elif grid[y][x] == 3:
                alien3 = Alien3()
                alien3.rect.y = 35 * (1 + y)
                alien3.rect.x = alien1_0.rect.x + alien1_0.spacing + (alien1_0.width + alien1_0.spacing) * x

                alien3_list.add(alien3)
                aliens_list.add(alien3)
                all_sprites_list.add(alien3)

def draw_hearts():
    for i in range(player.lives):
        screen.blit(heart_image, (10 + 42 * i, screen_height - 55))
        
def draw_message(text, x, y, color, font_size = 40):
    font_style = pygame.font.SysFont('FUTURAM.ttf', font_size)
    b = font_style.render(text, True, color)
    screen.blit(b, [x, y])

def reset_aliens():
    for alien in aliens_list:
        aliens_list.remove(alien)
        alien1_list.remove(alien)
        alien2_list.remove(alien)
        alien3_list.remove(alien)
        all_sprites_list.remove(alien)
    for shoot in shoot_list:
        shoot_list.remove(shoot)
        all_sprites_list.remove(alien)
        

done = False
gameover = False
play_again = False
wave = 1
remove_alien = False
waiting_to_talk = 4000
lobby = True
lobby_game_out = False
while not done:
        
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    play_again = True
                    lobby = True
                if event.key == pygame.K_s:
                    waiting_to_talk = 2000
    if play_again:
        play_again = False
        gameover = False
        wave = 1
        remove_alien = False
        waiting_to_talk = 4000
        player.reset()
        reset_aliens()
    if lobby:
        iamanalligator_sound.play()
    while lobby:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                iamanalligator_sound.stop()
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    iamanalligator_sound.stop()
                    lobby = False
        screen.blit(lobby_image, (0, 0))
        draw_message('Press "p" to start!', screen_width/4 + 10, 3 * screen_height/4 + 80, yellow, 40)
        pygame.display.flip()
    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_t):
                if player.reloading == False:
                    player_weapon_sound.play()
                    player.reloading = True
                    laser = Laser()
                    laser.rect.x = player.rect.x + player.width/2
                    laser.rect.y = player.rect.y
                    laser_list.add(laser)
                    all_sprites_list.add(laser)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speed_x1 = -5
                if event.key == pygame.K_RIGHT:
                    player.speed_x2 = 5
                if event.key == pygame.K_UP:
                    player.speed_y1 = -5
                if event.key == pygame.K_DOWN:
                    player.speed_y2 = 5
                
            if event.type == pygame.KEYUP: #speeds = 0
                if event.key == pygame.K_LEFT:
                    player.speed_x1 = 0
                if event.key == pygame.K_RIGHT:
                    player.speed_x2 = 0
                if event.key == pygame.K_UP:
                    player.speed_y1 = 0
                if event.key == pygame.K_DOWN:
                    player.speed_y2 = 0
            
        if player.rect.x + player.speed_x1 + player.speed_x2 < screen_width - player.width\
        and player.rect.x + player.speed_x1 + player.speed_x2 > 0 :
            player.rect.x += player.speed_x1 + player.speed_x2 
        
        if player.rect.y + player.speed_y1 + player.speed_y2 >  screen_height - 150\
        and player.rect.y + player.speed_y1 + player.speed_y2 < screen_height - player.height:
            
            player.rect.y += player.speed_y1 + player.speed_y2
        
        player.weapon_reload += 1
        if player.weapon_reload > player.fire_rate * FPS:
            player.weapon_reload = 0
            player.reloading = False
            
        
        all_sprites_list.update()
            
        for laser in laser_list:
            aliens_hit_list = pygame.sprite.spritecollide(laser, aliens_list, False)
            
            
            for alien in aliens_hit_list:
                aliens_hit_list.remove(alien)
                laser_list.remove(laser)
                all_sprites_list.remove(laser)
                if alien.rect.y < 0:
                    aliens_hit_list.remove(alien)
                elif alien in alien1_list:
                    player.score += 10
                    alien1_list.remove(alien)
                    remove_alien = True
                elif alien in alien2_list:
                    if alien.health > 0:   
                        alien.health -= player.damage
                        alien.bar_red_length += 15
                    if alien.health <= 0:
                        player.score += 20
                        alien2_list.remove(alien)
                        remove_alien = True
                elif alien in alien3_list:
                    if alien.health > 0:
                        alien.health -= player.damage
                        alien.bar_red_length += 10
                    if alien.health <= 0:
                        player.score += 30
                        alien3_list.remove(alien)
                        remove_alien = True
                if remove_alien == True:
                    remove_alien = False
                    aliens_list.remove(alien)
                    all_sprites_list.remove(alien)
                    alien_distroyed_sound.play()
                else:
                    alien_hit_sound.play()

            if laser.rect.y < -10:
                laser_list.remove(laser)
                all_sprites_list.remove(laser)
                
                
        player_hit_list = pygame.sprite.spritecollide(player, shoot_list, False)
        for shoot in player_hit_list:
            player_hit_sound.play()
            player_hit_list.remove(shoot)
            shoot_list.remove(shoot)
            all_sprites_list.remove(shoot)
            if player.health >= 10:
                player.health -= 10
                player.bar_red_length += player.bar_green_length/3
            if player.health <= 0:
                player.lives -= 1
                player.bar_red_length = 0
                player.health = 30
            if player.lives <= 0:
                gameover = True
        
        player_alien_hit_list = pygame.sprite.spritecollide(player, aliens_list, False)
        for alien in player_alien_hit_list:
            player_hit_sound.play()
            player_alien_hit_list.remove(alien)
            aliens_list.remove(alien)
            all_sprites_list.remove(alien)
            player.health -= 10
        for shoot in shoot_list:
            if shoot.rect.y > screen_height + 15:
                shoot_list.remove(shoot)
                all_sprites_list.remove(shoot)
            
        if len(aliens_list) == 0:
            background = random.choice(backgrounds_list)
            new_wave_sound.play()
            if wave < 10:
                spawn_aliens(wave + 1)
            else:
                spawn_aliens(10)
            wave += 1
        
        #screen.fill(black) #all drawings below this
        screen.blit(background, (0, 0))
    
        draw_hearts()
        all_sprites_list.draw(screen)
        player.draw_health_bar()
        for alien in aliens_list:
            alien.draw_health_bar()
            alien.alien_shoot()

        draw_message('Score: ' + str(player.score), 30, 30, white, 35)
        draw_message('wave: ' + str(wave - 1), 30, 60, white, 35)
            
        pygame.display.flip()
        clock.tick(FPS)
        
    
    screen.fill(black)
    gameover_sound.play()
    draw_message('GAME OVER!', screen_width/4 - 10, screen_height/3, red, 70)
    pygame.time.wait(waiting_to_talk)
    draw_message('Press "s" to hear more noise :)', screen_width/6, screen_height - 150, pink, 30)

    draw_message('Score: ' + str(player.score), screen_width/6, 100, yellow, 50)
    draw_message('wave: ' + str(wave - 1), screen_width/6, 150, yellow, 50)
    draw_message('Press "l"(not i) for lobby...', screen_width/6 - 10, screen_height/2 + 100, green, 50)
    pygame.display.flip()
