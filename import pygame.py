import pygame
import sys
import random
import sqlite3

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mi Juego Pygame")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

# Fuentes
font = pygame.font.Font(None, 36)

# Variables del juego
player_x = 100
player_y = 300
player_speed = 5
player_lives = 3
score = 0
level = 1
obstacles = []

# Base de datos SQLite para récords
conn = sqlite3.connect("records.db")
cursor = conn.cursor()

# Función para generar obstáculos


def generate_obstacle():
    obstacle = pygame.Rect(screen_width, random.randint(
        50, screen_height - 50), 30, 30)
    obstacles.append(obstacle)

# Función para mostrar puntuación


def show_score():
    score_text = font.render("Puntuación: " + str(score), True, white)
    screen.blit(score_text, (10, 10))

# Función para mostrar vidas


def show_lives():
    lives_text = font.render("Vidas: " + str(player_lives), True, white)
    screen.blit(lives_text, (10, 50))

# Pantalla Inicial


def show_start_screen():
    screen.fill(black)
    start_text = font.render(
        "¡Bienvenido a la búsqueda de otro planeta!", True, white)
    instructions_text = font.render(
        "Presiona cualquier tecla para comenzar", True, white)
    screen.blit(start_text, (screen_width // 2 - 250, 200))
    screen.blit(instructions_text, (screen_width // 2 - 200, 300))
    pygame.display.flip()
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_start = False

# Mostrar pantalla de fin de nivel


def show_level_end_screen():
    screen.fill(black)
    level_end_text = font.render(
        "¡Nivel " + str(level) + " completado!", True, white)
    continue_text = font.render(
        "Presiona cualquier tecla para continuar", True, white)
    screen.blit(level_end_text, (screen_width // 2 - 200, 200))
    screen.blit(continue_text, (screen_width // 2 - 200, 300))
    pygame.display.flip()
    waiting_for_continue = True
    while waiting_for_continue:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_continue = False

# Mostrar pantalla de fin del juego


def show_game_over_screen():
    screen.fill(black)
    game_over_text = font.render("¡Juego terminado!", True, white)
    if is_high_score(score):
        new_record_text = font.render("¡Nuevo récord!", True, white)
        screen.blit(new_record_text, (screen_width // 2 - 120, 260))
    screen.blit(game_over_text, (screen_width // 2 - 100, 200))
    pygame.display.flip()
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_restart = False

# Función para verificar si es un nuevo récord


def is_high_score(current_score):
    cursor.execute("SELECT MAX(score) FROM records")
    high_score = cursor.fetchone()[0]
    if high_score is None:
        return True
    return current_score > high_score


# Bucle principal del juego
show_start_screen()
while level <= 2:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Generar obstáculos
    if random.randint(0, 100) < 5:
        generate_obstacle()

    # Mover y dibujar obstáculos
    for obstacle in obstacles:
        obstacle.x -= level * 2
        pygame.draw.rect(screen, blue, pygame.Rect(player_x, player_y, 30, 30))
        pygame.draw.rect(screen, red, obstacle)

        if obstacle.colliderect(player_x, player_y, 30, 30):
            obstacles.remove(obstacle)
            explosion_sound.play()
            player_lives -= 1

    # Limpiar pantalla
    screen.fill(black)

    # Mostrar puntuación y vidas
    show_score()
    show_lives()

    # Actualizar pantalla
    pygame.display.flip()

    # Lógica de fin de nivel
    if not obstacles:
        show_level_end_screen()
        level += 1
        obstacles = []
        player_lives = 3
        landing_sound.play()

# Lógica de fin del juego
show_game_over_screen()
if is_high_score(score):
    name = input("¡Nuevo récord! Ingresa tus iniciales: ")
    cursor.execute(
        "INSERT INTO records (name, score) VALUES (?, ?)", (name, score))
    conn.commit()

# Cierre de la base de datos SQLite
conn.close()

pygame.quit()
sys.exit()
