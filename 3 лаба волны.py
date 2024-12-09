import pygame
import math
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH = 1600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция волн и поплавков")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Параметры волн и поплавков
waves = [
    {"amplitude": 1, "period": 2, "speed": 1},
    {"amplitude": 0.5, "period": 3, "speed": 0.8},
]

buoys = [
    {"mass": 1, "volume": 1, "position": 2},
    {"mass": 1.5, "volume": 1.2, "position": 5},
    {"mass": 0.8, "volume": 0.9, "position": 8},
]


# Функция для рисования волн
def draw_wave(wave, frame):
    for x in range(0, WIDTH):
        y = wave["amplitude"] * math.sin(2 * math.pi * (x / (WIDTH / wave["period"]) - frame * wave["speed"] / 100))
        pygame.draw.line(screen, BLUE, (x, HEIGHT // 2 - y * 50), (x + 1, HEIGHT // 2 - y * 50))


# Функция для рисования поплавков с учетом силы Архимеда
def draw_buoy(buoy, frame):
    wave_height = sum(
        wave["amplitude"] * math.sin(
            2 * math.pi * (buoy["position"] * WIDTH / len(waves) / wave["period"] - frame * wave["speed"] / 100))
        for wave in waves
    )
    buoy_y = HEIGHT // 2 - wave_height * 50 - (buoy["mass"] - buoy["volume"]) * 10
    x_pos = int(buoy["position"] * WIDTH / len(waves))
    pygame.draw.circle(screen, RED, (x_pos, int(buoy_y)), 10)


# Функция для отображения окна ввода параметров
def get_input(prompt):
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 50)
    input_text = ""
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen.fill(WHITE)
        prompt_surface = font.render(prompt, True, BLACK)
        input_surface = font.render(input_text, True, BLACK)
        pygame.draw.rect(screen, GRAY, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        screen.blit(prompt_surface, (WIDTH // 4, HEIGHT // 3 - 50))
        screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))
        pygame.display.flip()

    return input_text


# Основной цикл программы
def main():
    running = True
    clock = pygame.time.Clock()
    frame = 0

    while running:
        screen.fill(WHITE)  # Очистка экрана

        # Обработка событий
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Левый клик мыши
                    mouse_pos = event.pos
                    if 10 <= mouse_pos[0] <= 210 and HEIGHT - 50 <= mouse_pos[1] <= HEIGHT - 20:
                        amplitude = float(get_input("Введите амплитуду волны:"))
                        period = float(get_input("Введите период волны:"))
                        speed = float(get_input("Введите скорость волны:"))
                        waves.append({"amplitude": amplitude, "period": period, "speed": speed})
                    elif 220 <= mouse_pos[0] <= 420 and HEIGHT - 50 <= mouse_pos[1] <= HEIGHT - 20:
                        mass = float(get_input("Введите массу поплавка:"))
                        volume = float(get_input("Введите объем поплавка:"))
                        position = float(get_input("Введите позицию поплавка:"))
                        buoys.append({"mass": mass, "volume": volume, "position": position})
                    elif 430 <= mouse_pos[0] <= 630 and HEIGHT - 50 <= mouse_pos[1] <= HEIGHT - 20:
                        if waves:
                            waves.pop()
                    elif 640 <= mouse_pos[0] <= 840 and HEIGHT - 50 <= mouse_pos[1] <= HEIGHT - 20:
                        if buoys:
                            buoys.pop()

        # Рисуем волны
        for wave in waves:
            draw_wave(wave, frame)

        # Рисуем поплавки
        for buoy in buoys:
            draw_buoy(buoy, frame)

        # Кнопки управления
        font = pygame.font.Font(None, 36)

        pygame.draw.rect(screen, BLACK, (10, HEIGHT - 50, 200, 30))
        add_wave_button = font.render('Добавить волну', True, WHITE)
        screen.blit(add_wave_button, (15, HEIGHT - 45))

        pygame.draw.rect(screen, BLACK, (220, HEIGHT - 50, 200, 30))
        add_buoy_button = font.render('Добавить поплавок', True, WHITE)
        screen.blit(add_buoy_button, (225, HEIGHT - 45))

        pygame.draw.rect(screen, BLACK, (430, HEIGHT - 50, 200, 30))
        delete_wave_button = font.render('Удалить волну', True, WHITE)
        screen.blit(delete_wave_button, (435, HEIGHT - 45))

        pygame.draw.rect(screen, BLACK, (640, HEIGHT - 50, 200, 30))
        delete_buoy_button = font.render('Удалить поплавок', True, WHITE)
        screen.blit(delete_buoy_button, (645, HEIGHT - 45))

        # Обновление экрана
        pygame.display.flip()
        frame += 1
        clock.tick(50)  # Ограничение FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
