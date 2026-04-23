import pygame
from pygame.locals import *
import random
import sys

pygame.init()

#create the window
game_width = 500
game_height = 500
game_window = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Space Shooter")

#colours
white = (255, 255, 255)
red = (255, 0, 0)

#game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

#high score
high_score = 0

#buttons
start_btn = None
exit_btn = None
restart_btn = None
menu_btn = None

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.lives = 3
        self.score = 0
        
        self.invincibility_frames = 0

        image = pygame.image.load('Assets/PNG/playerShip1_blue.png')
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()

        damage_image = pygame.image.load('Assets/PNG/Damage/playerShip1_damage1.png')
        self.damage_image = pygame.transform.scale(damage_image, (80, 80))

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        if self.invincibility_frames > 0:
            self.invincibility_frames -= 1

    def draw_image(self):
        if self.invincibility_frames > 0:
            damage_x = self.x - self.damage_image.get_width() / 3
            damage_y = self.y - self.damage_image.get_height() / 3
            game_window.blit(self.damage_image, (damage_x, damage_y))

class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        color = random.choice(['Brown', 'Grey'])
        size = random.choice(['big', 'med', 'small', 'tiny'])
        num = 1
        self.image = pygame.image.load(f'Assets/PNG/Meteors/meteor{color}_{size}{num}.png')

        if size == 'big':
            self.hits = 4
            self.points = 4
        elif size == 'med':
            self.hits = 3
            self.points = 3
        elif size == 'small':
            self.hits = 2
            self.points = 2
        else:
            self.hits = 1
            self.points = 1

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.base_speed = 2
        self.speed_multiplier = random.uniform(0.75, 1.5)

    def update(self):
        speed_increase = player.score // 20
        self.speed = (self.base_speed + speed_increase) * self.speed_multiplier
        self.rect.y += self.speed

        if pygame.sprite.collide_rect(self, player):
            if player.invincibility_frames == 0:
                player.lives -= 1
                player.invincibility_frames = 50

        if pygame.sprite.spritecollide(self, missile_group, True):
            self.hits -= 1
            if self.hits == 0:
                player.score += self.points

        if self.rect.top > game_height or self.hits == 0:
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        image = pygame.image.load('Assets/PNG/Lasers/laserBlue01.png')
        self.image = pygame.transform.scale(image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 6
        if self.rect.bottom < 0:
            self.kill()

#groups
player_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()

#backgrounds
bg = pygame.image.load('Assets/Bonus/Backggournd.png')
bg = pygame.transform.scale(bg, (game_width, game_height))

black_bg = pygame.image.load('Assets/Backgrounds/black.png')
black_bg = pygame.transform.scale(black_bg, (game_width, game_height))

#player
player = Player(250, 450)
player_group.add(player)

#missile cooldown
missile_cooldown = 200
last_missile = pygame.time.get_ticks()

def write_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x, y))

    for ox, oy in [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,2),(-2,2),(2,-2)]:
        outline = font.render(text, True, (0, 0, 0))
        game_window.blit(outline, (text_rect.x + ox, text_rect.y + oy))

    game_window.blit(text_surface, text_rect)
    return text_rect

def create_meteor():
    meteor_x = random.randint(0, game_width)
    meteor_group.add(Meteor(meteor_x, 0))

clock = pygame.time.Clock()
loop_ctr = 0
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if game_state == MENU:
                if start_btn and start_btn.collidepoint((mx, my)):
                    player_group.empty()
                    meteor_group.empty()
                    missile_group.empty()
                    player = Player(250, 450)
                    player_group.add(player)
                    loop_ctr = 0
                    game_state = PLAYING

                if exit_btn and exit_btn.collidepoint((mx, my)):
                    running = False

            if game_state == GAME_OVER:
                if restart_btn and restart_btn.collidepoint((mx, my)):
                    player_group.empty()
                    meteor_group.empty()
                    missile_group.empty()
                    player = Player(250, 450)
                    player_group.add(player)
                    loop_ctr = 0
                    game_state = PLAYING

                if menu_btn and menu_btn.collidepoint((mx, my)):
                    game_state = MENU

    if game_state == MENU:
        game_window.blit(bg, (0, 0))
        write_text("SPACE SHOOTER", 80, 250, 150)
        start_btn = write_text("START", 50, 250, 250)
        exit_btn = write_text("EXIT", 50, 250, 320)

    elif game_state == PLAYING:
        game_window.blit(black_bg, (0, 0))
        loop_ctr += 1

        keys = pygame.key.get_pressed()

        if keys[K_LEFT] and player.rect.left > 0:
            player.x -= 7
        if keys[K_RIGHT] and player.rect.right < game_width:
            player.x += 7

        if keys[K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_missile > missile_cooldown:
                missile = Missile(player.rect.centerx, player.rect.top)
                missile_group.add(missile)
                last_missile = current_time

        player.update()
        player_group.draw(game_window)
        player.draw_image()

        missile_group.update()
        missile_group.draw(game_window)

        if loop_ctr == 100:
            create_meteor()
            loop_ctr = 0

        meteor_group.update()
        meteor_group.draw(game_window)

        write_text(f'Score: {player.score}', 30, game_width / 8, 20)
        write_text(f'Lives: {player.lives}', 30, game_width * 7 / 8, 20)

        if player.lives <= 0:
            meteor_group.empty()
            missile_group.empty()
            if player.score > high_score:
                high_score = player.score
            game_state = GAME_OVER

    elif game_state == GAME_OVER:
        game_window.fill((0, 0, 0))
        write_text("GAME OVER", 70, 250, 140)
        write_text(f"Score: {player.score}", 40, 250, 210)
        write_text(f"High Score: {high_score}", 40, 250, 250)

        restart_btn = write_text("PLAY AGAIN", 50, 250, 320)
        menu_btn = write_text("MAIN MENU", 50, 250, 380)

    pygame.display.update()

pygame.quit()
sys.exit()