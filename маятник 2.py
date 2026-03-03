from random import randrange as rnd, choice
import math
import pygame
from pygame.draw import *

pygame.init()
WIDTH = 800
HEIGHT = 600
sc = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

finished = False
pygame.display.update()
clock = pygame.time.Clock()
FPS = 200
g = 9.8 * 1000
dt = 1 / FPS


def Moment_effect(m, g, l, phi, A, omega, t):
    return m * g * l * math.sin(phi) - 0.25 * m * A * A * omega * omega * math.sin(
        2 * phi
    )


def Moment(m, g, l, phi, A, omega, t):
    return m * g * l * math.sin(phi) - m * l * A * omega * omega * math.sin(
        phi
    ) * math.sin(omega * t)


class Kapiza:
    def __init__(self, phi, omega, length, amplitude):
        self.phi = phi
        self.dphidt = 0
        self.omega = omega
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.r = 20
        self.m = 1
        self.length = length
        self.screen = sc
        self.ampltude = amplitude
        self.time = 0

    def draw(self):
        X = self.x + self.length * math.sin(self.phi)
        Y = self.y - self.length * math.cos(self.phi)
        pygame.draw.line(self.screen, BLACK, [self.x, self.y], [X, Y], 5)
        pygame.draw.circle(self.screen, BLACK, (int(X), int(Y)), int(self.r))

    def move(self):
        self.phi += self.dphidt * dt
        self.dphidt += (
            Moment(
                self.m, g, self.length, self.phi, self.ampltude, self.omega, self.time
            )
            / self.m
            / self.length
            / self.length
            * dt
        )

    def update(self, x, y):
        L = ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5
        angle = math.acos((y - self.y) / L)
        if x < self.x:
            angle *= -1
        self.phi = math.pi - angle


def draw_parameters(mayatnick):
    font = pygame.font.Font(None, 40)
    text = font.render(
        "A="
        + str(round(mayatnick.ampltude, 3))
        + " omega="
        + str(round(mayatnick.omega, 3))
        + " phi="
        + str(mayatnick.phi),
        True,
        BLACK,
    )
    textpos = (50, 40)
    sc.blit(text, textpos)


mayatnick = Kapiza(math.pi, 0, 150, 0)
pause = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pause = True
            mayatnick.dphidt = 0
        if event.type == pygame.MOUSEBUTTONUP:
            pause = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                mayatnick.ampltude += 0.01
            if event.key == pygame.K_DOWN:
                mayatnick.ampltude -= 0.01
            if event.key == pygame.K_LEFT:
                mayatnick.omega -= 100
            if event.key == pygame.K_RIGHT:
                mayatnick.omega += 100
        if pause:
            mayatnick.update(event.pos[0], event.pos[1])

    sc.fill(WHITE)
    if not pause:
        mayatnick.move()
    mayatnick.draw()
    mayatnick.time += dt
    draw_parameters(mayatnick)
    pygame.display.update()
