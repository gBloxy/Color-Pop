
from math import cos, sin, pi
from random import choice, randint
from sys import exit
from os.path import join
import pygame
pygame.init()


WIN_SIZE = (800, 600)

win = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption('Color Pop')
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


colors = ['red', 'yellow', 'blue'] # 'lime'
controls = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT]


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


font = pygame.font.SysFont('cooperblack', 52)
font2 = pygame.font.SysFont('cooperblack', 100)
font3 = pygame.font.SysFont('cooperblack', 40)

speed = 15
spawn_rate = 2000
max_spawn_rate = 600
timer = 0
lifes = 3
score = 0
game_over = False
shapes = []
color = colors[0]


while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    if keys[pygame.K_SPACE]:
        break
    
    for i, c in enumerate(controls):
        if keys[c]:
            color = colors[i]
            break
    
    win.fill('black')
    
    win.blit(font2.render('Color Pop', True, color), (150, 40))
    win.blit(font3.render('Press SPACE to start', True, color), (190, 205))
    win.blit(font3.render('Controls :', True, color), (300, 290))
    win.blit(font3.render('Red : LEFT', True, color), (295, 350))
    win.blit(font3.render('Yellow : UP', True, color), (286, 395))
    win.blit(font3.render('Blue : RIGHT', True, color), (274, 440))
    
    win.blit(logos[colors.index(color)], (25, 510))
    
    clock.tick(60)
    pygame.display.flip()


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
                        game_over = True
                        go_surf = font2.render('Game Over !', True, color)
                        score_surf = font2.render(str(score), True, color)
                else:
                    score += 100
        
        text = font.render(str(score), True, color)
        win.blit(text, (WIN_SIZE[0] - 50 - text.get_width(), 15))
    
    for s in shapes:
        s.render(win)
    
    if game_over:
        win.blit(go_surf, (95, 100))
        win.blit(score_surf, (WIN_SIZE[0]/2 - score_surf.get_width()/2, 225))
        
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
    
    pygame.display.flip()
