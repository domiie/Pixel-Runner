# ---------------------------------------------------------------------------
# Created By: Dominika Kamenská
# Created   : 12/12/2022
# Subject   : Game creation and user experience
# ---------------------------------------------------------------------------
""" A simple pixel runner game made with Pygame """  #
# ---------------------------------------------------------------------------
# Credits:
# Sprites By: Kenney         (https://www.kenney.nl)
# Music By  : Juhani Junkala (https://juhanijunkala.com)
# FX By     : HappyOarakeet  (https://pixabay.com/sound-effects/pixel-death-66829/)
# ---------------------------------------------------------------------------
# Colours:
# Dark Blue #4f719d, Blue #9cc2f3, Dark Grey #585858
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import pygame
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # initialize the sprite class
        self.player_walk = [pygame.image.load('mat/chars/player_walk_01.png').convert_alpha(),
                            pygame.image.load('mat/chars/player_walk_02.png').convert_alpha()]
        self.player_index = 0
        self.player_jump = pygame.image.load('mat/chars/player_jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(100, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('mat/sound/jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def player_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:  # jump "animation"
            self.image = self.player_jump
        else:  # walk "animation"
            self.player_index += 0.08  # makes the transition between the two sprites smoother
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.player_gravity()
        self.player_animation()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()

        if name == 'wasp':
            self.enemy_move = [pygame.image.load('mat/chars/wasp_01.png').convert_alpha(),
                               pygame.image.load('mat/chars/wasp_02.png').convert_alpha()]
            y_pos = 210
        else:
            self.enemy_move = [pygame.image.load('mat/chars/pinkblop_01.png').convert_alpha(),
                               pygame.image.load('mat/chars/pinkblop_02.png').convert_alpha()]
            y_pos = 300

        self.enemy_index = 0
        self.image = self.enemy_move[self.enemy_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def enemy_animation(self):
        self.enemy_index += 0.07
        if self.enemy_index >= len(self.enemy_move):
            self.enemy_index = 0
        self.image = self.enemy_move[int(self.enemy_index)]

    def update(self):
        self.enemy_animation()
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def displayIntroScreen():
    screen.fill('#9cc2f3')

    welcome_text = header_font.render('Welcome!', False, '#4f719d')
    info_text_instr = normal_font.render('Use SPACE to jump and avoid incoming enemies.', False, '#585858')
    info_text_instr_2 = normal_font.render('Try to stay alive for as long as possible!', False, '#585858')
    info_text_start = halfbold_font.render('Press SPACE to start..', False, '#4f719d')
    info_text_exit = halfbold_font.render('Press ESC to exit..', False, '#4f719d')

    screen.blits([(welcome_text, welcome_text.get_rect(center=(400, 40))),
                  (head, head.get_rect(center=(400, 160))),
                  (info_text_instr, info_text_instr.get_rect(center=(400, 260))),
                  (info_text_instr_2, info_text_instr_2.get_rect(center=(400, 280))),
                  (info_text_start, info_text_start.get_rect(center=(400, 320))),
                  (info_text_exit, info_text_exit.get_rect(center=(400, 350)))])


def displayGameOverScreen():
    screen.fill('#9cc2f3')
    gameover_text = header_font.render('Game Over!', False, '#4f719d')
    info_text_start = halfbold_font.render('Press SPACE to play again', False, '#4f719d')
    score_text = halfbold_font.render(f'Your score was: {score}', False, '#4f719d')

    screen.blits([(gameover_text, gameover_text.get_rect(center=(400, 50))),
                  (dead_head, dead_head.get_rect(center=(400, 180))),
                  (info_text_start, info_text_start.get_rect(center=(400, 300)))])
    if score > 0:
        screen.blit(score_text, score_text.get_rect(center=(400, 340)))


def displayGame():
    # display background
    screen.blit(skyBG, (0, 0))
    screen.blit(groundBG, (0, 300))

    # get score
    global score
    score = displayScore()


def displayScore():
    current_time = (pygame.time.get_ticks() - start_time) // 1000  # time in seconds
    score_text = halfbold_font.render(f'Score: {current_time}', False, '#585858')
    score_rect = score_text.get_rect(center=(400, 20))
    screen.blit(score_text, score_rect)
    return current_time


def collision():
    if pygame.sprite.spritecollide(player.sprite, enemy_group, False):
        enemy_group.empty()
        hit_sound.play()
        return False
    else:
        return True


pygame.init()   # initialize pygame

# scale of the screen
screenWidth = 800
screenHeight = 400

# load and set all the important stuff
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pixel Runner © Kamenská Dominika 3nAIVS')

clock = pygame.time.Clock()     # clock object for frame rate
start_time = 0
score = 0                       # global variable to store score

background_music = pygame.mixer.Sound('mat/sound/music_background.wav')
background_music.play(loops=-1).set_volume(0.35)

hit_sound = pygame.mixer.Sound('mat/sound/death.mp3')
hit_sound.set_volume(1)

# fonts
header_font = pygame.font.Font('mat/fonts/Symtext.ttf', 60)             # load font for headers
halfbold_font = pygame.font.Font('mat/fonts/DePixelHalbfett.ttf', 20)   # load half-bold font
normal_font = pygame.font.Font('mat/fonts/DePixelSchmal.ttf', 18)       # load font for info texts
pygame.font.Font.set_underline(normal_font, True)                       # underlines the chosen font

# load background images
skyBG = pygame.image.load('mat/backgrounds/background_01.png').convert()
groundBG = pygame.image.load('mat/backgrounds/background_02.png').convert()

# load decorative images
head = pygame.transform.scale(pygame.image.load('mat/head.png').convert_alpha(), (200, 175))
dead_head = pygame.transform.scale(pygame.image.load('mat/head_dead.png').convert_alpha(), (200, 175))
empty_heart = pygame.image.load('mat/empty_heart.png').convert_alpha()

# create player group & player
player = pygame.sprite.GroupSingle()
player.add(Player())

# create enemy group
enemy_group = pygame.sprite.Group()

# timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1200)     # triggers enemy_timer every 1200 ms

# boolean variables
intro_screen = True
game_active = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            running = False
            pygame.quit()
            exit()

        if game_active:
            # enemy mechanics
            if event.type == enemy_timer:
                enemy_group.add(Enemy(choice(['wasp', 'blop', 'blop', 'blop'])))
        # game start from game over screen
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()    # help variable to get the proper score
        # game start from intro screen
        if intro_screen:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                intro_screen = False
                game_active = True

    if intro_screen:
        # display intro screen
        displayIntroScreen()
    else:
        if game_active:
            # display game
            displayGame()

            # drawing & animating player
            player.draw(screen)
            player.update()

            # drawing & animating enemies
            enemy_group.draw(screen)
            enemy_group.update()

            # collision
            game_active = collision()
        else:
            displayGameOverScreen()

    pygame.display.update()
    clock.tick(60)  # 60fps (frame rate)
