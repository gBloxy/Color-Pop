
from math import cos, sin, pi
from random import choice, randint
from sys import exit
from os.path import join
import pygame
import pygame.freetype
pygame.init()

from client import Client


WIN_SIZE = (800, 600)
SCREENSHOT = False

win = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption('Color Pop')
clock = pygame.time.Clock()


colors = ['red', 'yellow', 'blue'] # 'lime'
controls = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT]
color = colors[0]


logo_original = pygame.image.load(join('asset', 'logo.png'))
logos = []
for c in colors:
    logo = logo_original.copy()
    pixels = pygame.surfarray.pixels3d(logo)
    mask = (pixels == [0, 0, 0]).all(axis=-1)
    col = pygame.Color(c)
    pixels[mask] = (col.r, col.g, col.b)
    del pixels
    logos.append(logo)
del logo_original, logo


font4 = pygame.font.SysFont('cooperblack', 52)
font2 = pygame.font.SysFont('cooperblack', 100)
font3 = pygame.font.SysFont('cooperblack', 40)

font = pygame.freetype.SysFont('cooperblack', size=0)


client = Client('color_pop')


def blit_center(surface, source, center):
    surface.blit(source, (center[0] - source.get_width() / 2, center[1] - source.get_height() / 2))


class TextInput():
    def __init__(self, pos, callback, placeholder):
        self.font = pygame.freetype.SysFont('cooperblack', size=32)
        self.center = pos
        self.callback = callback
        self.placeholder = placeholder
        self.text = ''
        self.focus = False
        self.hovered = False
        self.resize()
    
    def exit(self):
        self.focus = False
        self.callback(self.text)
    
    def resize(self):
        if self.text:
            surf, text_rect = self.font.render(self.text, 'black' if self.focus else color)
        else:
            text, text_rect = self.font.render(self.placeholder, 'lightgray')
        width = max(text_rect.width + 30, 220)
        height = max(text_rect.height + 20, 60)
        x = self.center[0] - width / 2
        y = self.center[1] - height / 2
        self.rect = pygame.Rect(x, y, width, height)
    
    def update(self, events):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False
        if self.focus:
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        if self.text:
                            self.text = self.text[:-1]
                            self.resize()
                    elif e.key == pygame.K_RETURN:
                        self.exit()
                    else:
                        self.text += e.unicode
                        self.resize()
    
    def render(self, surf):
        if self.text:
            text, trect = self.font.render(self.text, 'black' if self.focus else color)
        else:
            text, trect = self.font.render(self.placeholder, 'lightgray')
        pygame.draw.rect(surf, 'lightgray' if self.focus else ('darkgray' if not self.hovered else 'gray'), self.rect, border_radius=25)
        blit_center(surf, text, self.center)


class Shape():
    def __init__(self):
        self.y = -40
        self.x = randint(30, WIN_SIZE[0] - 30)
        self.size = 40
        self.radius = self.size / 2
        self.color = choice(colors)
        self.point_nb = randint(3, 8)
        self.angle = 0
        self.angle_rot = 0.008 * choice([-1, 1])
    
    def update(self):
        self.y += speed * dt / 100
        self.angle += self.angle_rot
    
    def render(self, surf):
        pygame.draw.polygon(surf, self.color,
            [
                (
                    int(self.x + self.radius * cos(self.angle + pi * 2 * i / self.point_nb)),
                    int(self.y + self.radius * sin(self.angle + pi * 2 * i / self.point_nb))
                )
                for i in range(self.point_nb)
            ]
        )


def set_username(username):
    global message, message_timer
    if client.registred:
        res = client.setUsername(username)
    else:
        res = client.register(username)
    if 'error' in res:
        message = res['error']
        message_timer = 10000


def score_thread(score):
    high_score = client.getMinScore()
    if score > high_score:
        response = client.sendScore(score)
        if response:
            print(response)


def end_game():
    global game_over, go_surf, score_surf, restart_surf
    game_over = True
    go_surf = font2.render('Game Over !', True, color)
    score_surf = font2.render(str(score), True, color)
    restart_surf = font3.render('Press SPACE to retry', True, color)
    if client.connected and client.registred:
        client.thread(score_thread, args=(score,))


message = ''
message_timer = 0

if not client.connected:
    message = 'Connection to server failed'
    message_timer = 10000


text_input = TextInput((WIN_SIZE[0] / 2, 220), set_username, 'name')

if client.registred:
    text_input.text = client.username
    text_input.resize()


speed = 15
spawn_rate = 2000
max_spawn_rate = 600
timer = 0
lifes = 3
score = 0
game_over = False
shapes = []


while True:
    dt = clock.tick(60)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if text_input.hovered:
                    if not text_input.focus:
                        text_input.focus = True
                elif text_input.focus:
                    text_input.exit()
    
    if keys[pygame.K_SPACE] and not text_input.focus:
        break
    
    for i, c in enumerate(controls):
        if keys[c]:
            color = colors[i]
            break
    
    win.fill('black')
    
    center = WIN_SIZE[0] / 2
    size = 30
    
    blit_center(win, font.render('Color Pop',            color, size=100 )[0], (center,  80))
    blit_center(win, font.render('Press SPACE to start', color, size=35  )[0], (center, 355))
    blit_center(win, font.render('Controls :',           color, size=size)[0], (center, 415))
    blit_center(win, font.render('Red : LEFT',           color, size=size)[0], (center, 460))
    blit_center(win, font.render('Yellow : UP',          color, size=size)[0], (center, 490))
    blit_center(win, font.render('Blue : RIGHT',         color, size=size)[0], (center, 520))
    
    win.blit(logos[colors.index(color)], (25, 510))
    win.blit(font.render('Press ESCAPE to quit', color, size=20)[0], (550, 530))
    
    if message_timer > 0:
        message_timer -= dt
        if message_timer <= 0:
            message = ''
        else:
            blit_center(win, font.render(message, 'white', size=20)[0], (center, 285))
    
    text_input.update(events)
    text_input.render(win)
    
    if keys[pygame.K_s] and SCREENSHOT:
        pygame.image.save(win, 'image'+str(clock.get_time())+'.png')
        pygame.time.wait(300)
    
    pygame.display.flip()


pygame.mouse.set_visible(False)


while True:
    dt = clock.tick(60)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    win.fill('black')
    
    if not game_over:
        for i, c in enumerate(controls):
            if keys[c]:
                color = colors[i]
                break
        
        speed += 0.06 * dt/100
        if speed > 30:
            max_spawn_rate = 500
        elif speed > 50:
            max_spawn_rate = 350
        if spawn_rate > max_spawn_rate:
            spawn_rate -= 5 * dt/100
        
        timer -= dt
        if timer <= 0:
            shapes.append(Shape())
            timer = spawn_rate
        
        for s in shapes:
            s.update()
            if s.y >= WIN_SIZE[1] - s.radius:
                shapes.remove(s)
                if s.color != color:
                    lifes -= 1
                    if lifes <= 0:
                        end_game()
                else:
                    score += 100
        
        text = font4.render(str(score), True, color)
        win.blit(text, (WIN_SIZE[0] - 50 - text.get_width(), 15))
    
    for s in shapes:
        s.render(win)
    
    if game_over:
        win.blit(go_surf, (95, 100))
        win.blit(score_surf, (WIN_SIZE[0]/2 - score_surf.get_width()/2, 225))
        win.blit(restart_surf, (WIN_SIZE[0]/2 - restart_surf.get_width()/2, 400))
        
        if keys[pygame.K_SPACE]:
            speed = 15
            spawn_rate = 2000
            max_spawn_rate = 600
            timer = 0
            lifes = 3
            score = 0
            game_over = False
            shapes = []
            color = colors[0]
            continue
    
    pygame.draw.rect(win, color, (0, WIN_SIZE[1] - 20, WIN_SIZE[0], 20))
    
    for i in range(lifes):
        pygame.draw.circle(win, color, (50 + 35 * i, 50), 15)
    
    if keys[pygame.K_s] and SCREENSHOT:
        pygame.image.save(win, 'image'+str(clock.get_time())+'.png')
        pygame.time.wait(300)
    
    pygame.display.flip()
