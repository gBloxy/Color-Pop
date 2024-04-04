
from math import cos, sin, pi
from random import choice, randint
from sys import exit
import pygame
pygame.init()


WIN_SIZE = (800, 600)

win = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption('Color Pop')
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


class Shape():
    def __init__(self):
        self.y = -40
        self.x = randint(30, WIN_SIZE[0] - 30)
        self.size = 40
        self.radius = self.size / 2
        self.color = choice(['red', 'yellow', 'blue'])
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

speed = 15
spawn_rate = 2000
max_spawn_rate = 600
timer = 0
lifes = 3
score = 0
game_over = False
shapes = []
color = 'red'


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
            speed = 15
            spawn_rate = 2000
            max_spawn_rate = 600
            timer = 0
            lifes = 3
            score = 0
            game_over = False
            shapes = []
            color = 'red'
            continue
    
    for s in shapes:
        s.render(win)
    
    pygame.draw.rect(win, color, (0, WIN_SIZE[1] - 20, WIN_SIZE[0], 20))
    
    for i in range(lifes):
        pygame.draw.circle(win, color, (50 + 35 * i, 50), 15)
    
    pygame.display.flip()
