import pygame
import os
import sys

# Функция для загрузки изображений
def load_image(name, colorkey=None):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image

pygame.init()

# Константы
TILE_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 8
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)  # Цвет для кнопки
PURPLE = (128, 0, 128)  # Цвет для двери

# Загрузка изображений (можно заменить простыми цветами)
player_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
player_img.fill(YELLOW)
box_img = load_image("box.png")
wall_img = load_image("brick.png")
goal_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
goal_img.fill(GREEN)
floor_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
floor_img.fill(WHITE)
button_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
button_img.fill(BLUE)
door_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
door_img.fill(PURPLE)

# Уровни (0 - пол, 1 - стена, 2 - ящик, 3 - цель, 4 - игрок, 5 - кнопка, 6 - дверь)
levels = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 2, 0, 1, 0, 2, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 3, 1],
        [1, 0, 2, 0, 0, 4, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 2, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 2, 0, 1, 0, 2, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 3, 1],
        [1, 0, 2, 2, 0, 4, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 2, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 2, 5, 1, 0, 2, 0, 3, 1, 0],
        [1, 0, 0, 0, 0, 4, 0, 2, 0, 1, 0],  # Дверь на этом уровне
        [1, 0, 6, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    ]
]

current_level_index = 0
current_level = levels[current_level_index]

# Поиск начальной позиции игрока и ящиков
def load_level():
    player_pos = None
    boxes = []
    goals = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if current_level[y][x] == 4:
                player_pos = [x, y]
                current_level[y][x] = 0
            elif current_level[y][x] == 2:
                boxes.append([x, y])
            elif current_level[y][x] == 3:
                goals.append([x, y])
    return player_pos, boxes, goals

player_pos, boxes, goals = load_level()

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Сокобан")
clock = pygame.time.Clock()

# Функция отрисовки уровня
def draw_level():
    screen.fill(WHITE)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if current_level[y][x] == 1:
                screen.blit(wall_img, rect)
            else:
                screen.blit(floor_img, rect)
                if current_level[y][x] == 3:  # Цель
                    screen.blit(goal_img, rect)
                elif current_level[y][x] == 5:  # Кнопка
                    screen.blit(button_img, rect)
                elif current_level[y][x] == 6:  # Дверь
                    if not is_door_open():
                        screen.blit(door_img, rect)

    # Отрисовка ящиков
    for box in boxes:
        rect = pygame.Rect(box[0] * TILE_SIZE, box[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(box_img, rect)


    # Отрисовка игрока
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(player_img, player_rect)

# Проверка завершения уровня
def check_level_complete():
    for goal in goals:
        if goal not in boxes:
            return False
    return True

# Проверка, открыта ли дверь
def is_door_open():
    for box in boxes:
        if box == [3, 3]:  # Позиция кнопки
            return True
    return False

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            new_player_pos = list(player_pos)
            move_x = 0
            move_y = 0
            if event.key == pygame.K_LEFT:
                move_x = -1
            elif event.key == pygame.K_RIGHT:
                move_x = 1
            elif event.key == pygame.K_UP:
                move_y = -1
            elif event.key == pygame.K_DOWN:
                move_y = 1

            new_player_pos[0] += move_x
            new_player_pos[1] += move_y

            # Проверка на столкновение со стеной
            if 0 <= new_player_pos[0] < GRID_WIDTH and 0 <= new_player_pos[1] < GRID_HEIGHT and current_level[new_player_pos[1]][new_player_pos[0]] != 1:
                # Проверка на столкновение с ящиком
                for i, box in enumerate(boxes):
                    if new_player_pos == box:
                        new_box_pos = [box[0] + move_x, box[1] + move_y]
                        # Проверка, можно ли сдвинуть ящик
                        if 0 <= new_box_pos[0] < GRID_WIDTH and 0 <= new_box_pos[1] < GRID_HEIGHT and current_level[new_box_pos[1]][new_box_pos[0]] != 1 and new_box_pos not in boxes:
                            boxes[i] = new_box_pos
                            player_pos = new_player_pos
                        break  # Прекратить проверку ящиков, если один был сдвинут
                else:
                    # Проверка на возможность прохода через дверь
                    if current_level[new_player_pos[1]][new_player_pos[0]] != 6 or is_door_open():
                        player_pos = new_player_pos

    draw_level()
    pygame.display.flip()

    if check_level_complete():
        current_level_index += 1
        if current_level_index < len(levels):
            current_level = levels[current_level_index]
            player_pos, boxes, goals = load_level()
        else:
            print("Вы прошли все уровни!")
            running = False

    clock.tick(FPS)

pygame.quit()
