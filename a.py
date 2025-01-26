import pygame
import os
import sys

# Функция для загрузки изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

pygame.init()

# Загрузка музыки
def load_music():
    pygame.mixer.music.load(os.path.join('data', 'game_music.mp3'))  # Замените на имя вашего файла
    pygame.mixer.music.play(-1)  # Воспроизводить в бесконечном цикле

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

player_img = load_image("player.png")
box_img = load_image("box.png")
wall_img = load_image("brick.png")
goal_img = load_image("platform.png")
floor_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
floor_img.fill(WHITE)
button_img = load_image("button.png")
door_img = load_image("door.png")
teleport_img = load_image("teleport.png")

# Уровни (0 - пол, 1 - стена, 2 - ящик, 3 - цель, 4 - игрок, 5 - кнопка, 6 - дверь, 7 - телепорт)
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
        [1, 0, 0, 0, 0, 7, 0, 0, 0, 1],  # Телепорт
        [1, 0, 2, 0, 1, 0, 2, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 3, 1],
        [1, 0, 2, 0, 0, 4, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 7, 2, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 2, 5, 1, 0, 2, 0, 3, 1],
        [1, 0, 0, 0, 0, 4, 0, 2, 0, 1],
        [1, 0, 6, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 3, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
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
        [1, 0, 0, 0, 0, 7, 0, 0, 0, 1],  # Телепорт
        [1, 0, 2, 0, 1, 0, 2, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 3, 1],
        [1, 0, 2, 0, 0, 4, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 7, 2, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 2, 5, 1, 0, 2, 0, 3, 1],
        [1, 0, 0, 0, 0, 4, 0, 2, 0, 1],
        [1, 0, 6, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 3, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
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
        [1, 0, 0, 0, 0, 7, 0, 0, 0, 1],  # Телепорт
        [1, 0, 2, 0, 1, 0, 2, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 3, 1],
        [1, 0, 2, 0, 0, 4, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 7, 2, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 2, 5, 1, 0, 2, 0, 3, 1],
        [1, 0, 0, 0, 0, 4, 0, 2, 0, 1],
        [1, 0, 6, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 3, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
]

current_level_index = 0
current_level = levels[current_level_index]

# Поиск начальной позиции игрока и ящиков
def load_level():
    player_pos = None
    boxes = []
    goals = []
    teleport_pairs = {}
    lst = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if current_level[y][x] == 4:
                player_pos = [x, y]
            elif current_level[y][x] == 2:
                boxes.append([x, y])
            elif current_level[y][x] == 3:
                goals.append([x, y])
            elif current_level[y][x] == 7:
                lst.append((x, y))
    if lst:
        teleport_pairs[lst[0]] = lst[1]
        teleport_pairs[lst[1]] = lst[0]

    if player_pos is None:
        print("Ошибка: На уровне отсутствует начальная позиция игрока")
        print("Уровень:")
        for row in current_level:
            print(row)
        sys.exit()

    return player_pos, boxes, goals, teleport_pairs

player_pos, boxes, goals, teleport_pairs = load_level()

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
                elif current_level[y][x] == 7:  # Телепорт
                    screen.blit(teleport_img, rect)

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

# Функция для отображения загрузочного экрана
def show_loading_screen():
    loading_image = pygame.image.load("data/loading.jpg")
    loading_image = pygame.transform.scale(loading_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.blit(loading_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)

up_arrow_img = load_image("up_arrow.png")
down_arrow_img = load_image("down_arrow.jpg")
arrow_size = (30, 30)
up_arrow_img = pygame.transform.scale(up_arrow_img, arrow_size)
down_arrow_img = pygame.transform.scale(down_arrow_img, arrow_size)

def show_level_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 40)
    title_font = pygame.font.Font(None, 50)
    title_text = title_font.render("Выберите уровень:", True, WHITE)

    visible_levels = 5
    start_index = 0

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Отрисовка стрелки вверх, если есть уровни выше
        if start_index > 0:
            up_arrow_rect = up_arrow_img.get_rect(center=(SCREEN_WIDTH // 2, 110))
            screen.blit(up_arrow_img, up_arrow_rect)
        else:
            up_arrow_rect = None

        level_buttons = []
        for i in range(start_index, min(start_index + visible_levels, len(levels))):
            level_text = font.render(f"Уровень {i + 1}", True, WHITE)
            text_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 140 + (i - start_index) * 50))
            screen.blit(level_text, text_rect)
            level_buttons.append((text_rect, i))

        # Отрисовка стрелки вниз, если есть уровни ниже
        if start_index + visible_levels < len(levels):
            down_arrow_rect = down_arrow_img.get_rect(center=(SCREEN_WIDTH // 2, 370))
            screen.blit(down_arrow_img, down_arrow_rect)
        else:
            down_arrow_rect = None

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                # Прокрутка колесиком мыши
                if event.y > 0 and start_index > 0:
                    start_index -= 1
                elif event.y < 0 and start_index + visible_levels < len(levels):
                    start_index += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Проверка, нажата ли стрелка вверх
                    if up_arrow_rect and up_arrow_rect.collidepoint(event.pos):
                        start_index -= 1
                    elif down_arrow_rect and down_arrow_rect.collidepoint(event.pos):
                        start_index += 1
                    for button, index in level_buttons:
                        if button.collidepoint(event.pos):
                            return index

running = True
load_music()
show_loading_screen()
current_level_index = show_level_menu()
current_level = levels[current_level_index]
player_pos, boxes, goals, teleport_pairs = load_level()

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
            # Проверка перемещения игрока
            if 0 <= new_player_pos[0] < GRID_WIDTH and 0 <= new_player_pos[1] < GRID_HEIGHT and \
                    current_level[new_player_pos[1]][new_player_pos[0]] != 1:
                # Проверка на столкновение с ящиком
                for i, box in enumerate(boxes):
                    if new_player_pos == box:
                        new_box_pos = [box[0] + move_x, box[1] + move_y]
                        # Проверка, можно ли сдвинуть ящик
                        if 0 <= new_box_pos[0] < GRID_WIDTH and 0 <= new_box_pos[1] < GRID_HEIGHT and \
                                current_level[new_box_pos[1]][new_box_pos[0]] != 1 and new_box_pos not in boxes:
                            boxes[i] = new_box_pos
                            player_pos = new_player_pos
                        break
                else:
                    # Проверка на возможность прохода через дверь
                    if current_level[new_player_pos[1]][new_player_pos[0]] != 6 or is_door_open():
                        # Проверка на телепорт
                        if (new_player_pos[0], new_player_pos[1]) in teleport_pairs:
                            player_pos = list(teleport_pairs[(new_player_pos[0], new_player_pos[1])])
                        else:
                            player_pos = new_player_pos

    draw_level()
    pygame.display.flip()

    if check_level_complete():
        current_level_index += 1
        if current_level_index < len(levels):
            current_level = levels[current_level_index]
            player_pos, boxes, goals, teleport_pairs = load_level()
        else:
            print("Вы прошли все уровни!")
            running = False

    clock.tick(FPS)

pygame.quit()
