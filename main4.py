import pygame
import random
import time

pygame.init()
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pantalla.fill(NEGRO)
pygame.display.set_caption("Colonización Espacial")

# Definir clase Nave


# Definir clase Nave
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("nave.png"), (int(82 * 0.5), int(55 * 0.5)))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
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
# Resto del código sin cambios
# Definir clase Obstaculo


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if random.random() < 0.5:  # 50% de probabilidad de ser meteorito rápido
            self.image = pygame.transform.scale(pygame.image.load(
                "meteor0.png"), (int(50 * 0.5), int(50 * 0.5)))
            self.velocidad = random.randint(5, 10)  # Velocidad rápida
        else:
            self.image = pygame.transform.scale(pygame.image.load(
                "meteor2.png"), (int(50 * 0.5), int(50 * 0.5)))
            self.velocidad = random.randint(1, 3)  # Velocidad normal
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_PANTALLA
        self.rect.y = random.randint(0, ALTO_PANTALLA - self.rect.height)
        self.esquivado = False

    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.left < 0 and not self.esquivado:
            self.esquivado = True
            obstaculos_esquivados[0] += 1 if self.rect.left < nave.rect.left else 0
# Definir clase Explosión


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("explosion.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.animation_time = pygame.time.get_ticks()
        # Carga el archivo de sonido de explosión
        self.sound = pygame.mixer.Sound("low-impactwav-14905.mp3")

    def update(self):
        # Animar la explosión
        current_time = pygame.time.get_ticks()
        # Duración de medio segundo (500 milisegundos)
        if current_time - self.animation_time > 500:
            self.kill()  # Elimina la explosión actual
        else:
            self.animation_time = current_time
            if not self.sound.get_busy():  # Reproduce el sonido solo si no está en reproducción
                self.sound.play()


def generar_explosion(center):
    explosion = Explosion(center)
    todos_los_sprites.add(explosion)
    explosiones.add(explosion)


# Inicializar variables y objetos
todos_los_sprites = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
explosiones = pygame.sprite.Group()
nave = Nave()
todos_los_sprites.add(nave)
for _ in range(10):
    obstaculo = Obstaculo()
    todos_los_sprites.add(obstaculo)
    obstaculos.add(obstaculo)
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 50)
game_over = False
nivel = 1
obstaculos_esquivados = [0]
mensaje_nivel = False
mensaje_tiempo = 0
velocidad_aumentada = False
contador_fuente = pygame.font.Font(None, 30)
contador_texto = contador_fuente.render("Esquivados: 0", True, BLANCO)
contador_rect = contador_texto.get_rect()
contador_rect.topleft = (10, 10)
jugando = True

# Bucle principal del juego
while jugando:
    todos_los_sprites.update()
    if len(obstaculos) < 10:
        obstaculo = Obstaculo()
        todos_los_sprites.add(obstaculo)
        obstaculos.add(obstaculo)
    for obstaculo in obstaculos:
        if obstaculo.rect.right < 0:
            obstaculos.remove(obstaculo)
            todos_los_sprites.remove(obstaculo)
    if pygame.sprite.spritecollide(nave, obstaculos, False) and not nave.invulnerable:
        nave.image.set_alpha(0)
        nave.invulnerable = True
        nave.inicio_invulnerable = pygame.time.get_ticks()
        nave.rect.topleft = (45, nave.rect.y)
        nave.vidas -= 1
        if nave.vidas <= 0:
            game_over = True
        for obstaculo in pygame.sprite.spritecollide(nave, obstaculos, True):
            # Generar explosión cuando la nave colisione con un obstáculo
            generar_explosion(obstaculo.rect.center)
            nave.rect.topleft = (45, nave.rect.y)  # Mover la línea aquí
    # Requiere 50 obstáculos esquivados para superar el primer nivel, luego el doble de obstáculos para cada nivel siguiente
    if obstaculos_esquivados[0] >= nivel * 50:
        mensaje_nivel = True
        mensaje_tiempo = pygame.time.get_ticks()
        nivel += 1
        for obstaculo in obstaculos:
            obstaculo.velocidad *= 1.05  # Aumenta la velocidad en un 5% cada vez
        reloj.tick(10)  # Juego en cámara lenta durante el mensaje de nivel
    if mensaje_nivel and pygame.time.get_ticks() - mensaje_tiempo >= 3000 and not velocidad_aumentada:
        velocidad_aumentada = True
        for obstaculo in obstaculos:
            obstaculo.velocidad *= 1.1
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
    pantalla.fill(NEGRO)  # Cambiar el color de fondo a negro
    todos_los_sprites.draw(pantalla)
    if game_over:
        texto = fuente.render("Game Over", True, NEGRO)
        pantalla.blit(texto, (ANCHO_PANTALLA // 2 - texto.get_width() //
                              2, ALTO_PANTALLA // 2 - texto.get_height() // 2))
        jugando = False
    if mensaje_nivel:
        texto = fuente.render("Has superado el nivel " +
                              str(nivel), True, BLANCO)
        texto_rect = texto.get_rect(
            center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
        tiempo_transcurrido = pygame.time.get_ticks() - mensaje_tiempo
        if tiempo_transcurrido < 1500:
            pantalla.blit(texto, texto_rect)
        elif tiempo_transcurrido >= 3000:
            mensaje_nivel = False
            velocidad_aumentada = False
    contador_texto = contador_fuente.render(
        "Esquivados: " + str(obstaculos_esquivados[0]), True, BLANCO)
    pantalla.blit(contador_texto, contador_rect)
    pygame.display.flip()
    if mensaje_nivel:
        reloj.tick(10)  # Ralentizar el juego durante el mensaje de nivel
    else:
        reloj.tick(60)
pygame.quit()
