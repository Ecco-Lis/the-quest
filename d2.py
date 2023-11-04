import pygame

# Definir los atributos de d1.py que serán utilizados en d2.py


def configurar_ventana(ancho, alto, color_fondo):
    pygame.init()
    ventana = pygame.display.set_mode((ancho, alto))
    ventana.fill(color_fondo)
    return ventana


def dibujar_elementos(ventana, texto_nombre, texto_instruccion, fuente_titulo, fuente_normal, fuente_pequena, color_letra):
    ventana.fill(color_fondo)
    ventana.blit(texto_nombre, rect_texto_nombre)
    ventana.blit(texto_instruccion, rect_texto_instruccion)
    # Aquí puedes agregar el código para dibujar los demás elementos de la ventana

# Resto del código de d2.py
