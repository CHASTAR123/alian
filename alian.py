import pygame
pygame.init()

W,H = 600,600
invasion = pygame.display.set_mode((W,H))

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('alian.png')
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
    def update(self,keypressed):
        if keypressed[pygame.K_UP]:
            self.rect.move_ip(0,-5)
        if keypressed[pygame.K_DOWN]:
            self.rect.move_ip(0,+5)
        if keypressed[pygame.K_LEFT]:
            # self.rect.move_ip(0,-5)
            self.rect.x -= 5
        if keypressed[pygame.K_RIGHT]:
            # self.rect.move_ip(0,-5)
            self.rect.x += 5
sprites = pygame.sprite.Group()
object = Alien()
sprites.add(object)
while object.rect.x > 0 and object.rect.x < W   and object.rect.y > 0 and object.rect.y < H:
    keypressed = pygame.key.get_pressed()
    object.update(keypressed)
    invasion.fill('black')
    sprites.draw(invasion)
    pygame.display.update()

