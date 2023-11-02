import pygame
import random

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
NEGRO = (0, 0, 0)


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, int(random.randint(15, 50) * 0.75)))
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_PANTALLA
        self.rect.y = random.randint(0, ALTO_PANTALLA - self.rect.height)
        self.velocidad = random.randint(1, 3)
        self.esquivado = False

    def update(self):
        self.rect.x -= self.velocidad

        if self.rect.left < 0 and not self.esquivado:
            self.esquivado = True

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
