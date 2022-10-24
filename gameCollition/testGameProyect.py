""" 
Adigma team
Brianna Ayelen Balam Velasco
Jesús Javier Can Noh
Damaris Yuselin Dzul Uc
Fátima Miranda Pestaña
""" 

import random 
from pygame.locals import *
import pygame 
from block import *  
from bullet import *
from global_constants import *

pygame.init()
# Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fullscreen = False
# Window titlebar
pygame.display.set_caption('Collition Bros')    
#reducir tamaño de la imagen 
pygame.display.set_icon(pygame.image.load('bullet.png'))  
# Timing
fps_clock = pygame.time.Clock()
FPS = 60   

default_font = pygame.font.Font("SuperMario256.ttf", 30)   

def draw_text(text, font, surface, x, y, main_color, background_color=None):
    textobj = font.render(text, True, main_color, background_color)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.centery = y
    surface.blit(textobj, textrect)

def toggle_fullscreen():
    if pygame.display.get_driver() == 'x11':
        pygame.display.toggle_fullscreen()
    else: 
        global screen, fullscreen 
        screen_copy = screen.copy()
        if fullscreen:
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
        else:
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        fullscreen = not fullscreen
        screen.blit(screen_copy, (0, 0)) 

 
def start_screen():
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    while True:
        title_font = pygame.font.Font('SuperMario256.ttf', 90)  
        big_font = pygame.font.Font("SuperMario256.ttf", 36) 
        small_font = pygame.font.Font("smw.ttf", 300)    
        draw_text('COLLITION BROS', title_font, screen,
                  WIDTH / 2, HEIGHT / 3, RED, WHITE)             
        draw_text('Use the mouse to dodge the bullets', big_font, screen,
                  WIDTH / 2 , HEIGHT / 2, WHITE, BLACK) 
        draw_text('Press any mouse button\n', 
                  default_font, screen, WIDTH / 2, HEIGHT / 1.7, BLUE, BLACK) 
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_loop()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    main_loop()
                    return
            if event.type == QUIT:
                pygame.quit()
                return 

def main_loop():
    pygame.mouse.set_visible(False)

    square = Block()
    square.set_pos(*pygame.mouse.get_pos())
    bullets = pygame.sprite.Group()
    running = True
    game_over = False
    points = 0
    min_bullet_speed = 1
    max_bullet_speed = 1
    bullets_per_gust = 1 
    sound = pygame.mixer.Sound("marioSong.wav")  
    
    

    
      
    while running:
        sound.play(-1)  
        

        pygame.display.update() 
        fps_clock.tick(FPS)
        screen.fill(BLACK) 

        if points >= 2000:
            bullets_per_gust = 3000
            max_bullet_speed = 80
        elif points >= 1000:
            bullets_per_gust = 3
            min_bullet_speed = 3
            max_bullet_speed = 15
        elif points >= 800:
            max_bullet_speed = 20
        elif points >= 600:
            bullets_per_gust = 2
            max_bullet_speed = 10
        elif points >= 500:
            min_bullet_speed = 2
        elif points >= 400:
            max_bullet_speed = 8
        elif points >= 200:
            # The smaller this number is, the probability for a bullet
            # to be shot is higher
            odds = 4
            max_bullet_speed = 7
        elif points >= 100:
            odds = 5
            max_bullet_speed = 6
        elif points >= 60:
            odds = 6
            max_bullet_speed = 5
        elif points >= 30:
            odds = 7
            max_bullet_speed = 4
        elif points < 30:
            odds = 8

        if random.randint(1, odds) == 1:
            for _ in range(0, bullets_per_gust):
                bullets.add(random_bullet(random.randint(min_bullet_speed,
                                                         max_bullet_speed)))
                points += 1
        draw_text('{}  points'.format(points), default_font, screen,
                  WIDTH / 2, 20, BLUE) 
        bullets.update()
        bullets.draw(screen)

        if square.collide(bullets):
            game_over = True


        screen.blit(square.img, square.rect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                square.set_pos(*mouse_pos)
            if event.type == QUIT:
                running = False

        while game_over:
             
            pygame.mouse.set_visible(True)
            # Text
            draw_text('{}  points'.format(points), default_font, screen,
                      WIDTH / 2, 20, GREEN)
            # Transparent surface
            transp_surf = pygame.Surface((WIDTH, HEIGHT))
            transp_surf.set_alpha(200)
            screen.blit(transp_surf, transp_surf.get_rect())

            draw_text('You lose', pygame.font.Font(None, 40), screen,
                      WIDTH / 2, HEIGHT / 3, RED)
            draw_text('To quit the game press Q', default_font, screen,
                      WIDTH / 2, HEIGHT / 1.9, GREEN)
            draw_text('double click to restart', default_font, screen,
                      WIDTH / 2, HEIGHT / 1.1, GREEN, BLACK)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_F11:
                        toggle_fullscreen()
                    if event.key == pygame.K_q:
                        game_over = False
                        running = False
                        #main_loop()  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_over = False 
  
                    main_loop() 
                    return 
                if event.type == QUIT:
                    game_over = False 
                    running = False   
                    main_loop()
                    return
    pygame.quit() 
    quit()

             
start_screen()

