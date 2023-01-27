import pygame, random, math
from pygame import mixer

# Initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# Add music
# mixer.music.load('') load background music audio file
# mixer.music.set_volume()  edit volume
# mixer.music.play(-1)   (This is to make it loop)

# Title & Icon

pygame.display.set_caption("Space Invasion")
icon = pygame.image.load('spaceship_Icon.png')
pygame.display.set_icon(icon)
background = pygame.image.load("space_invader_background.png")
# player
img_player = pygame.image.load('player_spaceship.png')
player_x = 368
player_y = 536
# Modify Location
player_x_change = 0

# enemy
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 8
for e in range(number_of_enemies):
    img_enemy.append(pygame.image.load('enemy_ufo.png'))
    enemy_x.append(random.randint(0, 738))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(0.5)
    enemy_y_change.append(50)

# missile
img_missile = pygame.image.load('missile.png')
missile_x = 0
missile_y = 500
missile_y_change = 10
visible_missile = False

# score
score = 0
my_font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# End of game text
end_font = pygame.font.Font('freesansbold.ttf', 40)


def final_text():
    my_final_font = end_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(my_final_font, (200, 200))


# show score function
def show_score(x, y):
    text = my_font.render(f'SCORE:{score}', True, (255, 255, 255))
    screen.blit(text, (x, y))


# Detct colision
def Detect_collision(x_1, x_2, y_1, y_2):
    distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if distance < 27:
        return True
    else:
        return False


def shoot_missle(x, y):
    global visible_missile
    visible_missile = True
    screen.blit(img_missile, (x + 16, y + 10))


# enemy function
def enemy(x, y, en):
    screen.blit(img_enemy[en], (x, y))


# player function
def player(x, y):
    screen.blit(img_player, (x, y))


# Game Loop (Backbone of the game)
is_running = True
while is_running:
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                player_x_change = 1
            if event.key == pygame.K_SPACE:
                missile_sound = mixer.Sound('mixkit-laser-weapon-shot-1681.mp3')
                missile_sound.play()
                if not visible_missile:
                    missile_x = player_x
                    shoot_missle(missile_x, missile_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # modify Player Location
    player_x += player_x_change
    # set Boundary
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # set enemy Boundary
    for enem in range(number_of_enemies):
        # end of game
        if enemy_y[enem] > 500:
            for k in range(number_of_enemies):
                enemy_y[k] = 1000
            final_text()
            break
        enemy_x[enem] += enemy_x_change[enem]
        if enemy_x[enem] <= 0:
            enemy_x_change[enem] = 1
            enemy_y[enem] += enemy_y_change[enem]
        elif enemy_x[enem] >= 736:
            enemy_x_change[enem] = -1
            enemy_y[enem] += enemy_y_change[enem]
            # Collision
        collision = Detect_collision(enemy_x[enem], missile_x, enemy_y[enem], missile_y)
        if collision:
            collision_sound = mixer.Sound('enemy_crash.mp3')
            collision_sound.play()
            missile_y = 500
            visible_missile = False
            score += 1
            enemy_x[enem] = random.randint(0, 738)
            enemy_y[enem] = random.randint(50, 200)
        enemy(enemy_x[enem], enemy_y[enem], enem)
        # bullet movement
    if missile_y <= -64:
        missile_y = 500
        visible_missile = False
    if visible_missile:
        shoot_missle(missile_x, missile_y)
        missile_y -= missile_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
