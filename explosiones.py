import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        self.sprites = []
        for i in range(9):
            sprite = pygame.image.load(f"explosion{i}.png")
            self.sprites.append(sprite)
        self.indice_sprite = 0
        self.image = self.sprites[self.indice_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = posicion
        self.tiempo_animacion = 100
        self.ultimo_cambio = pygame.time.get_ticks()

    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_cambio > self.tiempo_animacion:
            self.indice_sprite += 1
            if self.indice_sprite >= len(self.sprites):
                self.kill()
            else:
                self.image = self.sprites[self.indice_sprite]
                self.ultimo_cambio = tiempo_actual

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
