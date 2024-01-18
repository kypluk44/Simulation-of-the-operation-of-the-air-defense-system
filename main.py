import random
import pygame
from math import sqrt, atan, cos, sin, pi
import os


max_distance = 1000
dulo = 80
cold = 10
S_R = 0.01
R_R = 0.01
running = True
lr, rr = False, False
bullet_speed = 100
Pi = 3.14
spawn = 0
id = 0
radar_cd = 0
WIDTH = 1200
HEIGHT = 800
FPS = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class MovingObject(pygame.sprite.Sprite):
    rotate = False
    a0 = 0
    ang = 0
    g = -10
    d = 1
    image = pygame.Surface((50, 50))
    orig_img = image
    color = (0, 0, 0)

    def __init__(self, vx, vy, x0, y0, S, R, id, air_resistance):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.vx = vx
        self.vy = vy
        self.x = x0
        self.y = y0
        self.S = S
        self.R = R
        self.air_resistance = air_resistance

        self.rect = self.image.get_rect()
        self.image.set_colorkey(self.color)
        self.rect.center = (self.x, self.y)

    def update(self):
        dt = 0.1
        vx, vy = self.vx, self.vy
        self.angle_for_bullet = atan(self.vy / self.vx) if self.vx != 0 else 0
        asoprx = - 1.23 * vx * abs(vx) / 2 * 0.4 * pi * self.R * self.R * int(not self.air_resistance)
        asopry = - 1.23 * vy * abs(vy) / 2 * 0.4 * pi * self.R * self.R * int(not self.air_resistance)
        g = self.g
        ax = asoprx + self.a0 * sin(self.ang)
        ay = asopry + self.a0 * cos(self.ang) + g
        self.y += self.d * (self.vy * dt + ay * dt ** 2 / 2)
        self.x += self.vx * dt + ax * dt ** 2 / 2
        self.vx += ax * dt
        self.vy += ay * dt
        self.rect.center = (self.x, self.y)
        if self.rotate:
            rot = self.angle_for_bullet * 180 / pi
            self.image = pygame.transform.rotate(self.orig_img, rot - 90)
            self.rect = self.image.get_rect(center=self.rect.center)


class Rocket(MovingObject):
    color = (255, 255, 255)
    type = "enemy"
    x1, y1 = 800, 700
    v = 30 * 30 / FPS
    g = 0
    a0 = 10 * 30 / FPS
    image = pygame.Surface((70, 35))

    def __init__(self, vx, vy, x0, y0, S, R, id, air_resistance):
        super().__init__(vx, vy, x0, y0, S, R, id, air_resistance)
        pygame.sprite.Sprite.__init__(self)
        self.ang = atan((self.x1 - x0) / (self.y1 - y0))
        self.image = pygame.transform.rotate(self.image, self.ang * 180 / pi - 90)
        self.vx = self.v * sin(self.ang)
        self.vy = self.v * cos(self.ang)


class Bullet(MovingObject):
    type = "bullet"
    g = -10
    a0 = 0
    d = -1
    rotate = True
    image = pygame.image.load(os.path.join('Bullet.png')).convert()
    orig_img = image
    color = (0, 0, 0)

    def __init__(self, vx, vy, x0, y0, S, R, id, air_resistance):
        super().__init__(vx, vy, x0, y0, S, R, id, air_resistance)


class Wall(pygame.sprite.Sprite):
    image = pygame.image.load(os.path.join('wall.png')).convert()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()


class Base(pygame.sprite.Sprite):
    image = pygame.image.load(os.path.join('PVO.png')).convert()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.center = (390, 700)
        self.image.set_colorkey(BLACK)


class Target(pygame.sprite.Sprite):
    image = pygame.image.load(os.path.join('bunker.png')).convert()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.radius = 10
        self.rect.center = (800, 700)
        self.image.set_colorkey(BLACK)


class PVO(pygame.sprite.Sprite):
    image = pygame.image.load(os.path.join('PVO2.png')).convert()
    x, y = WIDTH // 3, HEIGHT - 100

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rot = 0
        self.rot_speed = 30 / FPS
        self.orig_img = self.image
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.center = (self.x, self.y)

    def rotate(self, d):
        self.rot = (self.rot + self.rot_speed * d) % 360
        self.image = pygame.transform.rotate(self.orig_img, self.rot)
        self.rect = self.image.get_rect(center=self.rect.center)


class Radar():
    x0, y0 = WIDTH // 3, HEIGHT - 100

    def __init__(self, md):
        self.md = md

    def scan(self, rockets):
        ans = []
        for elem in pygame.sprite.Group.sprites(rockets):

            x1, y1 = elem.x, elem.y
            x0, y0 = self.x0, self.y0
            ang = atan((x1 - x0) / (y1 - y0))
            distance = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            if distance < self.md:
                ans.append((elem.id, int(ang * 180 / pi), int(distance)))
        print("SCANING: ", end="")
        print(*ans)

    def machine_scan(self, rockets):
        ans = []
        for elem in pygame.sprite.Group.sprites(rockets):
            x1, y1 = elem.x, elem.y
            x0, y0 = self.x0, self.y0
            ang = atan((x1 - x0) / (y1 - y0))
            distance = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            if distance < self.md:
                ans.append(elem)
        return ans


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airdefence")

clock = pygame.time.Clock()

bullets = pygame.sprite.Group()
rockets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

target = Target()
player = PVO()
wall = Wall()
base = Base()

radar = Radar(max_distance)

all_sprites.add(wall, base, player, target)

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and cold >= 10 / 30 * FPS:
        cold = 0
        b = Bullet(bullet_speed * cos(player.rot * Pi / 180), bullet_speed * sin(player.rot * Pi / 180),
                   player.rect.center[0] + cos(player.rot * Pi / 180) * dulo,
                   player.rect.center[1] - sin(player.rot * Pi / 180) * dulo - 60, 0.01, 0.01, id, False)
        bullets.add(b)
        all_sprites.add(b)
    cold += 1

    if keys[pygame.K_a]:
        lr = True
    else:
        lr = False

    if keys[pygame.K_d]:
        rr = True
    else:
        rr = False

    if rr:
        player.rotate(-1)
    elif lr:
        player.rotate(1)

    if radar_cd > 40 / 30 * FPS:
        radar_cd = 0
        radar.scan(rockets)
    radar_cd += 1

    if spawn > 60 / 30 * FPS:
        rocket = Rocket(0, 0, random.randint(1, WIDTH), 0, S_R, R_R, id, True)
        id += 1
        all_sprites.add(rocket)
        rockets.add(rocket)

        spawn = 0
    spawn += 1
    hits = pygame.sprite.spritecollide(target, rockets, False, pygame.sprite.collide_rect_ratio(0.7))

    for bul in bullets:
        if pygame.sprite.spritecollide(bul, rockets, True):
            bul.kill()

    if hits:
        for i in hits:
            i.kill()
        if hits[0].type == "enemy":
            f1 = pygame.font.Font(None, 70)
            text1 = f1.render('АААААААААААА, КРОКОДИЛ В ВАННОЙ!!!!', True, (180, 0, 0))
            screen.blit(text1, (70, HEIGHT/2-70))
            pygame.display.update()
            f = True
            while f:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        f = False
                        break
            running = False

    all_sprites.update()
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()

