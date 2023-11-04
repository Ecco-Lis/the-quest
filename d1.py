import pygame
import sys
import sqlite3
# Definir el tamaño de la ventana
ancho_ventana = 800
alto_ventana = 600
# Definir colores
color_fondo = (218, 212, 187)
color_letra = (205, 102, 77)
# Inicializar Pygame
pygame.init()
# Crear la ventana
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
ventana.fill(color_fondo)
# Cargar las fuentes de texto
fuente_titulo = pygame.font.Font("Call of Ops Duty II.otf", 80)
fuente_normal = pygame.font.Font("peg-holes.ttf", 40)
fuente_pequena = pygame.font.Font("peg-holes.ttf", 20)
# Crear los textos
texto_nombre = fuente_titulo.render("The Quest", True, color_letra)
texto_instruccion = fuente_normal.render(
    "Ingrese su nombre:", True, color_letra)
texto_boton_aceptar = fuente_pequena.render("Aceptar", True, color_letra)
texto_boton_salir = fuente_pequena.render("Salir", True, color_letra)
# Crear los rectángulos
rect_texto_nombre = texto_nombre.get_rect(
    center=(ancho_ventana // 2, alto_ventana // 2 - 50))
rect_texto_instruccion = texto_instruccion.get_rect(
    center=(ancho_ventana // 2, alto_ventana // 2 + 50))
rect_nombre = pygame.Rect(ancho_ventana // 2 - 150,
                          alto_ventana // 2 + 100, 300, 50)
rect_boton_aceptar = pygame.Rect(
    ancho_ventana // 2 - 100, alto_ventana // 2 + 200, 100, 50)
rect_boton_salir = pygame.Rect(
    ancho_ventana // 2, alto_ventana // 2 + 200, 100, 50)
# Variables para guardar el nombre y puntuación
nombre_jugador = ""
puntuacion_jugador = 0
# Conexión a la base de datos SQLite
conexion = sqlite3.connect("basededatos.db")
cursor = conexion.cursor()
# Crear tabla si no existe
cursor.execute("CREATE TABLE IF NOT EXISTS jugadores (nombre TEXT)")
# Bucle principal del juego
while True:
    # Comprobar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                nombre_jugador = nombre_jugador[:-1]
            else:
                nombre_jugador += evento.unicode
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_boton_aceptar.collidepoint(evento.pos):
                # Guardar nombre en la tabla
                cursor.execute(
                    "INSERT INTO jugadores VALUES (?)", (nombre_jugador,))
                conexion.commit()
                # Cambiar a otra página o mostrar otra historia
                # Aquí puedes agregar la lógica para cambiar la página o mostrar la historia deseada
                # Por ahora, simplemente imprimimos el nombre guardado
                print("Nombre guardado:", nombre_jugador)
            elif rect_boton_salir.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()
    # Dibujar los elementos en la ventana
    ventana.fill(color_fondo)
    ventana.blit(texto_nombre, rect_texto_nombre)
    ventana.blit(texto_instruccion, rect_texto_instruccion)
    pygame.draw.rect(ventana, color_letra, rect_nombre, 2)
    texto_nombre_jugador = fuente_pequena.render(
        nombre_jugador, True, color_letra)
    rect_nombre_jugador = texto_nombre_jugador.get_rect(
        center=(ancho_ventana // 2, alto_ventana // 2 + 120))
    rect_nombre_jugador.left = rect_nombre.left + 10
    ventana.blit(texto_nombre_jugador, rect_nombre_jugador)
    ventana.blit(texto_boton_aceptar, rect_boton_aceptar)
    ventana.blit(texto_boton_salir, rect_boton_salir)
    # Actualizar la pantalla
    pygame.display.update()
# Cerrar la conexión a la base de datos
cursor.close()
conexion.close()
