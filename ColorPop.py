
from math import cos, sin, pi
from random import choice, randint
from sys import exit
import pygame
pygame.init()


WIN_SIZE = (800, 600)

win = pygame.display.set_mode(WIN_SIZE)
clock = pygame.time.Clock()

class Shape():
    def __init__(self):
        self.y = -20
        self.x = randint(30, WIN_SIZE[0] - 30)
        self.size = 20
        self.color = choice(['red', 'yellow', 'blue'])
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.point_nb = randint(3, 8)
        self.angle = (180 * (self.point_nb-2)) / self.point_nb
    
    def update(self):
        self.y += speed * dt / 100
    
    def render(self, surf):
        self.points = []
        for i in range(self.point_nb):
            x = self.x + self.size * cos(self.angle + pi * 2 * i / self.point_nb)
            y = self.y + self.size * sin(self.angle + pi * 2 * i / self.point_nb)
            self.points.append([int(x), int(y)])
        pygame.draw.polygon(surf, self.color, self.points)

shapes = []
speed = 15
spawn_rate = 2000
max_spawn_rate = 600
timer = 0
color = 'red'
lifes = 3
game_over = False
score = 0
font = pygame.font.SysFont('cooperblack', 52)
font2 = pygame.font.SysFont('cooperblack', 100)

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
        if keys[pygame.K_LEFT]:
            color = 'red'
        elif keys[pygame.K_UP]:
            color = 'yellow'
        elif keys[pygame.K_RIGHT]:
            color = 'blue'
        
        speed += 0.06 * dt/100
        if speed > 30:
            max_spawn_rate = 500
        if speed > 50:
            max_spawn_rate = 350
        if spawn_rate > max_spawn_rate:
            spawn_rate -= 6 * dt/100
        
        timer -= dt
        if timer <= 0:
            shapes.append(Shape())
            timer = spawn_rate
        
        for s in shapes:
            s.update()
            if s.y >= WIN_SIZE[1] - 20:
                shapes.remove(s)
                if s.color != color:
                    lifes -= 1
                else:
                    score += 100
        
        if lifes <= 0:
            game_over = True
        
        text = font.render(str(score), True, color)
        win.blit(text, (WIN_SIZE[0] - 50 - text.get_width(), 15))
    
    else:
        text = font2.render(str(score), True, color)
        win.blit(text, (WIN_SIZE[0]/2 - text.get_width()/2, 100))
        
        if keys[pygame.K_SPACE]:
            shapes = []
            speed = 15
            spawn_rate = 2000
            max_spawn_rate = 600
            timer = 0
            color = 'red'
            lifes = 3
            game_over = False
            score = 0
            continue
    
    for s in shapes:
        s.render(win)
    
    pygame.draw.rect(win, color, (0, WIN_SIZE[1] - 20, WIN_SIZE[0], 20))
    
    for i in range(lifes):
        pygame.draw.circle(win, color, (50 + 35 * i, 50), 15)
    
    pygame.display.flip()
