import pygame
from naves import Nave
from obstaculos import Obstaculo
from explosiones import Explosion
pygame.init()
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
NEGRO = (0, 0, 0)

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pantalla.fill(NEGRO)
pygame.display.set_caption("Colonización Espacial")

nave = Nave()
obstaculos = pygame.sprite.Group()
explosiones = pygame.sprite.Group()

reloj = pygame.time.Clock()
jugando = True
esquivados = 0
nivel = 1

while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    pantalla.fill(NEGRO)
    nave.update()
    nave.draw(pantalla)

    if len(obstaculos) < nivel:
        obstaculo = Obstaculo()
        obstaculos.add(obstaculo)

    obstaculos.update()
    obstaculos.draw(pantalla)

    colisiones = pygame.sprite.spritecollide(nave, obstaculos, True)
    for colision in colisiones:
        explosion = Explosion(colision.rect.center)
        explosiones.add(explosion)
        nave.vidas -= 1

    explosiones.update()
    explosiones.draw(pantalla)

    if nave.vidas <= 0:
        jugando = False

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
