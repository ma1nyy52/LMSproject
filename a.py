import pygame
import os
import sys

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

pygame.init()

def load_music():
    pygame.mixer.music.load(os.path.join('data', 'game_music.mp3'))
    pygame.mixer.music.play(-1)

TILE_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 8
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

player_img = load_image("player.png")
box_img = load_image("box.png")
wall_img = load_image("brick.png")
goal_img = load_image("platform.png")
floor_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
floor_img.fill(WHITE)
button_img = load_image("button.png")
door_img = load_image("door.png")
teleport_img = load_image("teleport.png")
left_arrow_img = load_image("left_arrow.png", colorkey=(255, 255, 255))
left_arrow_img = pygame.transform.scale(left_arrow_img, (30, 30))

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
        [1, 0, 0, 0, 0, 7, 0, 0, 0, 1],
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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Сокобан")
clock = pygame.time.Clock()

def draw_level():
    screen.fill(WHITE)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if current_level[y][x] == 1:
                screen.blit(wall_img, rect)
            else:
                screen.blit(floor_img, rect)
                if current_level[y][x] == 3:
                    screen.blit(goal_img, rect)
                elif current_level[y][x] == 5:
                    screen.blit(button_img, rect)
                elif current_level[y][x] == 6:
                    if not is_door_open():
                        screen.blit(door_img, rect)
                elif current_level[y][x] == 7:
                    screen.blit(teleport_img, rect)

    for box in boxes:
        rect = pygame.Rect(box[0] * TILE_SIZE, box[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(box_img, rect)

    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(player_img, player_rect)

def check_level_complete():
    for goal in goals:
        if goal not in boxes:
            return False
    return True

def is_door_open():
    for box in boxes:
        if box == [3, 3]:
            return True
    return False

def show_loading_screen():
    loading_image = pygame.image.load("data/loading.jpg")
    loading_image = pygame.transform.scale(loading_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(loading_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)

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

        left_arrow_rect = left_arrow_img.get_rect(topleft=(10, 10))
        screen.blit(left_arrow_img, left_arrow_rect)

        if start_index > 0:
            up_arrow_rect = up_arrow_img.get_rect(center=(SCREEN_WIDTH // 2, 120))
            screen.blit(up_arrow_img, up_arrow_rect)
        else:
            up_arrow_rect = None

        level_buttons = []
        for i in range(start_index, min(start_index + visible_levels, len(levels))):
            level_text = font.render(f"Уровень {i + 1}", True, WHITE)
            text_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 140 + (i - start_index) * 50))
            screen.blit(level_text, text_rect)
            level_buttons.append((text_rect, i))

        if start_index + visible_levels < len(levels):
            down_arrow_rect = down_arrow_img.get_rect(center=(SCREEN_WIDTH // 2, 360))
            screen.blit(down_arrow_img, down_arrow_rect)
        else:
            down_arrow_rect = None

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0 and start_index > 0:
                    start_index -= 1
                elif event.y < 0 and start_index + visible_levels < len(levels):
                    start_index += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if left_arrow_rect.collidepoint(event.pos):
                        return "back"
                    if up_arrow_rect and up_arrow_rect.collidepoint(event.pos):
                        start_index -= 1
                    elif down_arrow_rect and down_arrow_rect.collidepoint(event.pos):
                        start_index += 1
                    for button, index in level_buttons:
                        if button.collidepoint(event.pos):
                            return index

def show_start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)

    play_button = font.render("Играть", True, WHITE)
    play_rect = play_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    tutorial_button = font.render("Обучение", True, WHITE)
    tutorial_rect = tutorial_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    while True:
        screen.fill(BLACK)
        screen.blit(play_button, play_rect)
        screen.blit(tutorial_button, tutorial_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_rect.collidepoint(event.pos):
                        return "play"
                    elif tutorial_rect.collidepoint(event.pos):
                        return "tutorial"

def show_tutorial_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    text = font.render("Обучение (в разработке)", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    while True:
        screen.fill(BLACK)
        screen.blit(text, text_rect)

        left_arrow_rect = left_arrow_img.get_rect(topleft=(10, 10))
        screen.blit(left_arrow_img, left_arrow_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if left_arrow_rect.collidepoint(event.pos):
                        return "back"

running = True
load_music()
show_loading_screen()

while True:
    start_screen_choice = show_start_screen()

    if start_screen_choice == "play":
        while True:
            level_choice = show_level_menu()
            if level_choice == "back":
                break  # Возврат на стартовый экран
            else:
                current_level_index = level_choice
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

                            if 0 <= new_player_pos[0] < GRID_WIDTH and 0 <= new_player_pos[1] < GRID_HEIGHT and \
                                    current_level[new_player_pos[1]][new_player_pos[0]] != 1:
                                for i, box in enumerate(boxes):
                                    if new_player_pos == box:
                                        new_box_pos = [box[0] + move_x, box[1] + move_y]
                                        if 0 <= new_box_pos[0] < GRID_WIDTH and 0 <= new_box_pos[1] < GRID_HEIGHT and \
                                                current_level[new_box_pos[1]][new_box_pos[0]] != 1 and new_box_pos not in boxes:
                                            boxes[i] = new_box_pos
                                            player_pos = new_player_pos
                                        break
                                else:
                                    if current_level[new_player_pos[1]][new_player_pos[0]] != 6 or is_door_open():
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
    elif start_screen_choice == "tutorial":
        tutorial_result = show_tutorial_screen()
        if tutorial_result == "back":
            continue

pygame.quit()
