import pygame
from pygame.locals import *
import random
import sys

pygame.init()

#STEP 2: OBJECTS - Over the whole game

#STEP 4: GAME SETUP - Over the whole game

#STEP 6: ADDITIONS - Over the whole game

#STEP 1: SETUP
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
LEADERBOARD = 3
game_state = PLAYING  # start directly in game

#added leaderboard + name system
player_name = ""
entering_name = False
high_score = 0
leaderboard = []

#added button safety
start_btn = None
exit_btn = None
leaderboard_btn = None
restart_btn = None
back_btn = None

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.lives = 3
        self.score = 0
        
        #for displaying damage
        self.invincibility_frames = 0

        #space ship image
        image = pygame.image.load('Assets/PNG/playerShip1_blue.png')
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()

        #damage image
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

        #select a random color, size, and number for the image
        color = random.choice(['Brown', 'Grey'])
        size = random.choice(['big', 'med', 'small', 'tiny'])
        num = 1
        self.image = pygame.image.load(f'Assets/PNG/Meteors/meteor{color}_{size}{num}.png')
        #set number of hits required to destroy the meteor
        if size == 'big':
            self.hits = 4
            self.points = 4
        elif size == 'med':
            self.hits = 3
            self.points = 3
        elif size == 'small':
            self.hits = 2
            self.points = 2
        elif size == 'tiny':
            self.hits = 1
            self.points = 1
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # base speed (before multiplier)
        self.base_speed = 2
        # random speed multiplier between 0.75 and 1.5 (some slower, some faster)
        self.speed_multiplier = random.uniform(0.75, 1.5)

    def update(self):
        # base speed increases every 20 points
        speed_increase = player.score // 20
        # final speed is base speed plus increase times multiplier
        self.speed = (self.base_speed + speed_increase) * self.speed_multiplier
        self.rect.y += self.speed

        #check for collision with player
        if pygame.sprite.collide_rect(self, player):
            if player.invincibility_frames == 0:
                player.lives -= 1
                player.invincibility_frames = 50

        #check for collision with missiles
        if pygame.sprite.spritecollide(self, missile_group, True):
            self.hits -= 1
            if self.hits == 0:
                player.score += self.points

        #remove meteor if it goes off the screen or it's been destroyed
        if self.rect.top > game_height or self.hits == 0:
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        #missile image
        image = pygame.image.load('Assets/PNG/Lasers/laserBlue01.png')
        self.image = pygame.transform.scale(image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):

        #missile shoots up the screen
        self.rect.y -= 6
        if self.rect.bottom < 0:
            self.kill()

#STEP 3: GROUPS
#create the sprite groups
player_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()

#load background image
bg = pygame.image.load('Assets/Bonus/Backggournd.png')
bg = pygame.transform.scale(bg, (game_width, game_height))

#load gameplay background image
black_bg = pygame.image.load('Assets/Backgrounds/black.png')
black_bg = pygame.transform.scale(black_bg, (game_width, game_height))

#create the player
player = Player(250, 450)
player_group.add(player)

#STEP 5: INPUT - missiles & left/right movement
#missile cooldown
missile_cooldown = 200
last_missile = pygame.time.get_ticks()

#helper function to display text on the screen (white with black outline)
def write_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x, y))
    #draw outline
    for ox, oy in [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,2),(-2,2),(2,-2)]:
        outline = font.render(text, True, (0, 0, 0))
        game_window.blit(outline, (text_rect.x + ox, text_rect.y + oy))
    #draw main text
    game_window.blit(text_surface, text_rect)
    return text_rect

#create a new meteor
def create_meteor():
    meteor_x = random.randint(0, game_width)
    meteor_group.add(Meteor(meteor_x, 0))

#game loop setup
clock = pygame.time.Clock()
loop_ctr = 0
running = True

#game loop
while running:
    clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if game_state == GAME_OVER:
                if restart_btn and restart_btn.collidepoint((mx, my)):
                    # FULL RESET
                    player_group.empty()
                    meteor_group.empty()
                    missile_group.empty()
                    player = Player(250, 450)
                    player_group.add(player)
                    loop_ctr = 0
                    game_state = PLAYING

    #playing screen
    if game_state == PLAYING:
        game_window.blit(black_bg, (0, 0))
        loop_ctr += 1
        keys = pygame.key.get_pressed()

        #move the spaceship using the left/right arrow keys
        if keys[K_LEFT] and player.rect.left > 0:
            player.x -= 7
        if keys[K_RIGHT] and player.rect.right < game_width:
            player.x += 7

        #shoot missile with spacebar
        if keys[K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_missile > missile_cooldown:
                missile = Missile(player.rect.centerx, player.rect.top)
                missile_group.add(missile)
                last_missile = current_time

        #move and draw the player's spaceship
        player.update()
        player_group.draw(game_window)

        #draw damage if player is hit
        player.draw_image()

        #move and draw the missiles
        missile_group.update()
        missile_group.draw(game_window)

        #create meteors
        if loop_ctr == 100:
            create_meteor()
            loop_ctr = 0

        #move and draw meteors
        meteor_group.update()
        meteor_group.draw(game_window)

        #display score and lives
        write_text(f'Score: {player.score}', 30, game_width / 8, 20)
        write_text(f'Lives: {player.lives}', 30, game_width * 7 / 8, 20)

        #check game over
        if player.lives <= 0:
            meteor_group.empty()
            missile_group.empty()
            game_state = GAME_OVER

    #game over screen
    elif game_state == GAME_OVER:
        game_window.fill((0, 0, 0))
        write_text("GAME OVER", 70, 250, 150)
        write_text(f"Score: {player.score}", 40, 250, 220)
        restart_btn = write_text("RESTART", 50, 250, 320)

    pygame.display.update()

pygame.quit()
sys.exit()