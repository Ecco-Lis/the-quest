import pygame
import time

# Inicializar Pygame
pygame.init()

# Definir los colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Definir las dimensiones de la ventana
ANCHO = 800
ALTO = 600

# Crear la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))

# Definir la fuente de texto
fuente = pygame.font.Font(None, 24)

# Definir la historia del juego
historia_juego = [
    "En un futuro distante, la humanidad se enfrentaba a una crisis sin precedentes en la Tierra.",
    "La contaminación había alcanzado niveles críticos.",
    "los recursos naturales se agotaban rápidamente y el clima era cada vez más hostil.",
    "La esperanza parecía desvanecerse, pero los científicos descubrieron un antiguo.",
    "pergamino que hablaba de un planeta misterioso y próspero llamado 'Gaia'.",
    "Según las leyendas, Gaia era un paraíso oculto en las profundidades del universo,",
    "con una naturaleza exuberante y una fuente infinita de energía.",
    "Inspirados por esta esperanza, la humanidad decidió embarcarse en una misión audaz",
    " y desesperada: abandonar la Tierra y buscar un nuevo hogar en Gaia.",
    "La nave espacial 'Aurora' fue construida con tecnología de vanguardia y tripulada",
    "por los mejores científicos, ingenieros y exploradores.",
    "Bajo el liderazgo del intrépido Capitán XX, la tripulación se embarcó en un viaje.",
    " épico a través del vasto cosmos en busca de Gaia.",
    "A medida que la nave se adentraba en el espacio desconocido, se encontraron con ",
    "peligros inimaginables: tormentas de asteroides, nebulosas traicioneras .",
    "La historia de la humanidad había dado un giro inesperado. A través de su valentía",
    "y determinación, habían encontrado un nuevo comienzo en Gaia, un planeta",
    "que les ofrecía una segunda oportunidad para preservar su legado y construir.",
    "un futuro próspero.......",
    "¡Así comienza tu aventura en la búsqueda de otro planeta.",
    "¡Buena suerte, Capitán xx!.",
]

# Definir la posición inicial de la historia
pos_y = -len(historia_juego) * 30

# Definir la posición de la nave
nave_x = ANCHO / 2
nave_y = ALTO - 100

# Crear una lista para almacenar la animación de la historia
animacion_historia = []

# Bucle principal del juego
jugando = True
mostrando_instrucciones = False

for i, linea in enumerate(historia_juego):
    # Esperar un momento antes de mostrar cada línea de la historia
    time.sleep(1)

    # Mostrar la historia desplazante letra por letra
    for j in range(len(linea) + 1):
        # Manejar eventos de Pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        # Mostrar la historia desplazante
        pantalla.fill(NEGRO)

        for k in range(i + 1):
            if k < i:
                texto = fuente.render(historia_juego[k], True, BLANCO)
            else:
                texto = fuente.render(historia_juego[k][:j], True, BLANCO)

            texto_pos = texto.get_rect(
                centerx=ANCHO / 2, centery=ALTO / 2 - len(historia_juego) / 2 * 30 + k * 30)
            pantalla.blit(texto, texto_pos)

        pygame.display.flip()

        # Controlar la velocidad de escritura
        time.sleep(0.05)

        # Almacenar cada fotograma de la animación en la lista
        animacion_historia.append(pygame.surfarray.array3d(pantalla))

        # Salir del bucle si se cierra la ventana
        if not jugando:
            break

    # Mostrar la línea parpadeante de instrucciones al final de la historia
    if i == len(historia_juego) - 1:
        while jugando:
            # Manejar eventos de Pygame
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jugando = False

            # Mostrar las instrucciones de control de la nave
            if pos_y % 40 < 20:
                instrucciones_texto = fuente.render(
                    "Con la tecla dirección arriba y abajo controlas la nave", True, BLANCO)
                instrucciones_pos = instrucciones_texto.get_rect(
                    centerx=ANCHO / 2, centery=ALTO - 50)
                pantalla.blit(instrucciones_texto, instrucciones_pos)

            pygame.display.flip()

            # Salir del bucle si se cierra la ventana
            if not jugando:
                break

# Exportar la animación de la historia a un archivo
pygame.surfarray.save_animation(
    "animacion_historia.gif", animacion_historia, 10)

# Salir de Pygame
pygame.quit()
