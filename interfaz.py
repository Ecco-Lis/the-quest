import pygame
import random

# Function to load sounds


def cargar_sonidos():
    pygame.init()
    sonido_tecla_salir = pygame.mixer.Sound(
        "sounds/mech-keyboard-02-102918.wav")
    sonido_tecla_aceptar = pygame.mixer.Sound(
        "sounds/mech-keyboard-02-102918.wav")
    pygame.mixer.music.load("sounds/Scavengers Reign Main Title Theme.mp3")
    pygame.mixer.music.play(-1)  # Play in a loop
    return sonido_tecla_salir, sonido_tecla_aceptar

# Function to initialize the screen


def inicializar_pantalla():
    tamaño_pantalla = (800, 600)
    pantalla = pygame.display.set_mode(tamaño_pantalla)
    return pantalla, tamaño_pantalla

# Function to load the logo


def cargar_logo(tamaño_pantalla):
    logo = pygame.image.load("logo.png")
    logo_rect = logo.get_rect()
    logo_rect.center = (tamaño_pantalla[0] // 2, tamaño_pantalla[1] // 2)
    return logo, logo_rect

# Function to generate stars


def generar_estrellas(tamaño_pantalla):
    estrellas = []
    for _ in range(100):
        x = random.randint(0, tamaño_pantalla[0])
        y = random.randint(0, tamaño_pantalla[1] // 2)
        tamaño = random.randint(1, 3)
        color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        estrellas.append([x, y, tamaño, color])
    return estrellas

# Function to generate meteorites


def generar_meteoritos(tamaño_pantalla):
    meteoritos = []
    for _ in range(20):
        x = random.randint(0, tamaño_pantalla[0])
        y = random.randint(tamaño_pantalla[1] // 2, tamaño_pantalla[1])
        velocidad = random.uniform(0.2, 0.5)
        tamaño = random.randint(5, 10)
        color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        meteoritos.append([x, y, velocidad, tamaño, color])
    return meteoritos

# Function to draw buttons


def dibujar_botones(fuente_texto, pantalla, tamaño_pantalla):
    boton_salir = pygame.Rect(
        tamaño_pantalla[0] // 2 - 200, tamaño_pantalla[1] // 2 + 200, 200, 50)
    boton_aceptar = pygame.Rect(
        tamaño_pantalla[0] // 2 + 50, tamaño_pantalla[1] // 2 + 200, 200, 50)
    casilla_texto = pygame.Rect(
        tamaño_pantalla[0] // 2 - 150, tamaño_pantalla[1] // 2 + 100, 300, 40)
    texto_ingrese_nombre = fuente_texto.render(
        "Ingrese el nombre", True, (255, 255, 255))
    texto_salir = fuente_texto.render("Salir", True, (0, 0, 0))
    texto_aceptar = fuente_texto.render("Aceptar", True, (0, 0, 0))
    return boton_salir, boton_aceptar, casilla_texto, texto_ingrese_nombre, texto_salir, texto_aceptar

# Function to display a falling message


def mostrar_mensaje(pantalla, fuente_texto, mensaje, y_position, tamaño_pantalla):
    fuente_texto_pequeña = pygame.font.Font(None, 24)
    texto_mensaje = fuente_texto_pequeña.render(mensaje, True, (255, 255, 255))
    pantalla.blit(texto_mensaje, (tamaño_pantalla[0] // 2 - texto_mensaje.get_width() // 2, y_position))

# Function to animate a falling message


def animar_mensaje(pantalla, fuente_texto, mensaje, tamaño_pantalla, sonido_tecla_salir, sonido_tecla_aceptar):
    mensaje_y = -fuente_texto.get_height()  # Start off-screen
    velocidad_mensaje = 0.5  # Adjust the speed as needed
    while mensaje_y < tamaño_pantalla[1] // 2:
        # Resto del código...
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
        pantalla.fill((0, 0, 0))  # Clear the screen
        mostrar_mensaje(pantalla, fuente_texto, mensaje,
                        mensaje_y, tamaño_pantalla)
        pygame.display.flip()
        mensaje_y += velocidad_mensaje

        if mensaje_y >= tamaño_pantalla[1] // 2:
            # Esperar 1 segundo antes de mostrar los botones
            pygame.time.wait(1000)

            boton_continuar = pygame.Rect(
                tamaño_pantalla[0] // 2 - 100, tamaño_pantalla[1] // 2 + 200, 200, 50)
            boton_salir = pygame.Rect(
                tamaño_pantalla[0] // 2 - 100, tamaño_pantalla[1] // 2 + 300, 200, 50)

            texto_continuar = fuente_texto.render("Continuar", True, (0, 0, 0))
            texto_salir = fuente_texto.render("Salir", True, (0, 0, 0))

            while True:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        if evento.button == 1:
                            if boton_continuar.collidepoint(evento.pos):
                                pygame.mixer.Sound.play(sonido_tecla_aceptar)
                                return  # Salir de la función y continuar con el programa
                            elif boton_salir.collidepoint(evento.pos):
                                pygame.mixer.Sound.play(sonido_tecla_salir)
                                pygame.quit()
                                quit()

                pantalla.fill((0, 0, 0))  # Clear the screen
                mostrar_mensaje(pantalla, fuente_texto, mensaje,
                                tamaño_pantalla[1] // 2, tamaño_pantalla)
                pygame.draw.rect(pantalla, (255, 255, 255), boton_continuar)
                pygame.draw.rect(pantalla, (255, 255, 255), boton_salir)
                pantalla.blit(texto_continuar,
                              (boton_continuar.x + 50, boton_continuar.y + 15))
                pantalla.blit(
                    texto_salir, (boton_salir.x + 75, boton_salir.y + 15))
                pygame.display.flip()
# Main function


def main():
    # Initialize pygame
    pygame.init()

    # Initialize the screen and sounds
    pantalla, tamaño_pantalla = inicializar_pantalla()
    sonido_tecla_salir, sonido_tecla_aceptar = cargar_sonidos()

    # Load logo and generate stars and meteorites
    logo, logo_rect = cargar_logo(tamaño_pantalla)
    estrellas = generar_estrellas(tamaño_pantalla)
    meteoritos = generar_meteoritos(tamaño_pantalla)

    # Set up the font
    fuente_texto = pygame.font.Font(None, 32)

    # Draw buttons and text input field
    boton_salir, boton_aceptar, casilla_texto, texto_ingrese_nombre, texto_salir, texto_aceptar = dibujar_botones(
        fuente_texto, pantalla, tamaño_pantalla)

    # Initialize the text input variable
    texto_ingresado = ""
    nombre_ingresado = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if boton_salir.collidepoint(evento.pos):
                        pygame.mixer.Sound.play(sonido_tecla_salir)
                        pygame.quit()
                        quit()
                    elif boton_aceptar.collidepoint(evento.pos):
                        pygame.mixer.Sound.play(sonido_tecla_aceptar)
                        nombre = texto_ingresado.strip()
                        print("Nombre ingresado:", nombre)
                        nombre_ingresado = True
                        pantalla.fill((0, 0, 0))
                        animar_mensaje(pantalla, fuente_texto,
                                       "En un futuro distante, la humanidad se enfrentaba a una crisis sin precedentes en la Tierra.\nLa contaminación había alcanzado niveles críticos.\nLos recursos naturales se agotaban rápidamente y el clima era cada vez más hostil.\nLa esperanza parecía desvanecerse, pero los científicos descubrieron un antiguo pergamino que hablaba de un planeta misterioso y próspero llamado 'Gaia'.\nSegún las leyendas, Gaia era un paraíso oculto en las profundidades del universo, con una naturaleza exuberante y una fuente infinita de energía.\nInspirados por esta esperanza, la humanidad decidió embarcarse en una misión audaz y desesperada: abandonar la Tierra y buscar un nuevo hogar en Gaia.\nLa nave espacial 'Aurora' fue construida con tecnología de vanguardia y tripulada por los mejores científicos, ingenieros y exploradores.\nBajo el liderazgo del intrépido Capitán XX, la tripulación se embarcó en un viaje épico a través del vasto cosmos en busca de Gaia.\nA medida que la nave se adentraba en el espacio desconocido, se encontraron con peligros inimaginables: tormentas de asteroides, nebulosas traicioneras, etc.\nLa historia de la humanidad había dado un giro inesperado. A través de su valentía y determinación, habían encontrado un nuevo comienzo en Gaia, un planeta que les ofrecía una segunda oportunidad para preservar su legado y construir un futuro próspero...\n¡Así comienza tu aventura en la búsqueda de otro planeta!\n¡Buena suerte, Capitán Valerian!",
                                       tamaño_pantalla, sonido_tecla_salir, sonido_tecla_aceptar)
                        pygame.quit()
                        quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    texto_ingresado = texto_ingresado[:-1]
                else:
                    texto_ingresado += evento.unicode

        pantalla.fill((0, 0, 0))

        for meteorito in meteoritos:
            pygame.draw.circle(pantalla, (200, 200, 200),
                               (meteorito[0], meteorito[1]), meteorito[3])
            meteorito[0] -= meteorito[2] * 0.5
            if meteorito[0] < 0:
                meteorito[0] = tamaño_pantalla[0]
                meteorito[1] = random.randint(
                    tamaño_pantalla[1] // 2, tamaño_pantalla[1])

        for estrella in estrellas:
            pygame.draw.circle(
                pantalla, estrella[3], (estrella[0], estrella[1]), estrella[2])
            estrella[0] -= 0.1
            if estrella[0] < 0:
                estrella[0] = tamaño_pantalla[0]
                estrella[1] = random.randint(0, tamaño_pantalla[1] // 2)

        pantalla.blit(logo, logo_rect)
        pygame.draw.rect(pantalla, (255, 255, 255), casilla_texto, 2)
        pantalla.blit(texto_ingrese_nombre,
                      (tamaño_pantalla[0] // 2 - 140, tamaño_pantalla[1] // 2 + 80))
        texto_ingresado_render = fuente_texto.render(
            texto_ingresado, True, (255, 255, 255))
        pantalla.blit(texto_ingresado_render,
                      (casilla_texto.x + 10, casilla_texto.y + 10))
        pygame.draw.rect(pantalla, (255, 255, 255), boton_aceptar)
        texto_aceptar_rect = texto_aceptar.get_rect()
        texto_aceptar_rect.center = boton_aceptar.center
        pantalla.blit(texto_aceptar, texto_aceptar_rect)
        pygame.draw.rect(pantalla, (255, 255, 255), boton_salir)
        texto_salir_rect = texto_salir.get_rect()
        texto_salir_rect.center = boton_salir.center
        pantalla.blit(texto_salir, texto_salir_rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()
