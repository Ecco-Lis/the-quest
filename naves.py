import pygame

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
VERDE = (0, 255, 0)


class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((int(50 * 0.75), int(50 * 0.75)))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (45, ALTO_PANTALLA // 2)
        self.velocidad = 5
        self.vidas = 3
        self.invulnerable = False

    def update(self):
        teclas_pulsadas = pygame.key.get_pressed()
        if teclas_pulsadas[pygame.K_UP]:
            self.rect.y -= self.velocidad
        elif teclas_pulsadas[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= ALTO_PANTALLA - self.rect.height:
            self.rect.y = ALTO_PANTALLA - self.rect.height

        if self.invulnerable:
            if pygame.time.get_ticks() % 500 < 250:
                self.image.set_alpha(0)
            else:
                self.image.set_alpha(255)

            if pygame.time.get_ticks() - self.inicio_invulnerable >= 2000:
                self.invulnerable = False
                self.image.set_alpha(255)

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
