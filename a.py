import pygame
import os
import sys
import textwrap

# Файл с игровыми уровнями
GAME_LEVELS_FILE = os.path.join("data", "game_levels.txt")

def load_levels_from_file(filename):
    levels = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            level_lines = []
            for line in f:
                line = line.strip()
                if not line:
                    if level_lines:
                        level = [list(map(int, row.split())) for row in level_lines]
                        levels.append(level)
                        level_lines = []
                else:
                    level_lines.append(line)
            if level_lines:
                level = [list(map(int, row.split())) for row in level_lines]
                levels.append(level)
    except FileNotFoundError:
        print("Levels file not found; a new one will be created.")
    return levels

def append_level_to_file(level, filename):
    with open(filename, "a", encoding="utf-8") as f:
        for row in level:
            f.write(" ".join(map(str, row)) + "\n")
        f.write("\n")
    print("New level saved to", filename)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Image '{fullname}' not found")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

def load_music():
    try:
        music_path = os.path.join('data', 'game_music.mp3')
        print("Music path:", music_path)
        if not os.path.isfile(music_path):
            print("Music file not found!")
            return
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        print("Music loaded and playing")
    except Exception as e:
        print("Error loading music:", e)

# Инициализация Pygame и микшера
pygame.init()
try:
    pygame.mixer.init()
    print("Mixer initialized")
except Exception as e:
    print("Mixer init error:", e)
load_music()

# Глобальные параметры экрана
TILE_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 8
GAME_SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
GAME_SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE + 50
FPS = 60

# Параметры для редактора уровней (увеличенная ширина для палитры)
EDITOR_PALETTE_WIDTH = 150
EDITOR_SCREEN_WIDTH = GAME_SCREEN_WIDTH + EDITOR_PALETTE_WIDTH
EDITOR_SCREEN_HEIGHT = GAME_SCREEN_HEIGHT

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Загрузка изображений
player_img = load_image("player.png")
box_img = load_image("box.png")
wall_img = load_image("brick.png")
goal_img = load_image("platform.png")
floor_img = pygame.Surface((TILE_SIZE, TILE_SIZE)); floor_img.fill(WHITE)
button_img = load_image("button.png")
door_img = load_image("door.png")
teleport_img = load_image("teleport.png")
left_arrow_img = load_image("left_arrow.png", colorkey=(255,255,255))
down_arrow_img = load_image("down_arrow.jpg", colorkey=(255,255,255))
up_arrow_img = load_image("up_arrow.png", colorkey=(255,255,255))
left_arrow_img = pygame.transform.scale(left_arrow_img, (30,30))
down_arrow_img = pygame.transform.scale(down_arrow_img, (30,30))
up_arrow_img = pygame.transform.scale(up_arrow_img, (30,30))

# Словарь изображений для тайлов
tile_images = {
    0: floor_img, 1: wall_img, 2: box_img, 3: goal_img,
    4: player_img, 5: button_img, 6: door_img, 7: teleport_img
}

# Уровни обучения (заданы в коде)
tutorial_levels = [
    [[1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,0,0,0,0,0,0,0,1],
     [1,1,4,0,2,0,0,0,3,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1],
     [1,0,0,0,1,1,0,0,0,1],
     [1,0,3,0,1,1,0,0,0,1],
     [1,7,0,0,1,1,7,0,0,1],
     [1,0,2,0,1,1,0,0,0,1],
     [1,0,0,0,1,1,2,0,0,1],
     [1,0,4,0,1,1,3,0,0,1],
     [1,1,1,1,1,1,1,1,1,1]],
    [[1,1,1,1,1,1,1,1,1,1],
     [1,0,0,0,0,0,0,0,3,1],
     [1,0,0,0,1,0,0,0,0,1],
     [1,0,2,0,1,0,0,0,3,1],
     [1,0,0,0,0,0,0,0,0,1],
     [1,0,4,0,1,0,0,2,0,1],
     [1,0,0,0,0,0,0,0,0,1],
     [1,1,1,1,1,1,1,1,1,1]]
]

# Функция валидации уровня (проверка основных условий)
def validate_level(level_data):
    count_player = sum(row.count(4) for row in level_data)
    count_box = sum(row.count(2) for row in level_data)
    count_goal = sum(row.count(3) for row in level_data)
    count_teleport = sum(row.count(7) for row in level_data)
    errors = []
    if count_player != 1:
        errors.append(f"Игровой персонаж должен быть ровно один (найдено {count_player})")
    if count_box < 1:
        errors.append("Должна быть хотя бы одна коробка (найдена 0)")
    if count_goal < 1:
        errors.append("Должна быть хотя бы одна конечная цель (найдена 0)")
    if count_goal > count_box:
        errors.append(f"Конечных целей не должно быть больше, чем коробок (коробок: {count_box}, целей: {count_goal})")
    if count_teleport not in (0, 2):
        errors.append(f"Телепортов должно быть либо 0, либо ровно 2 (найдено {count_teleport})")
    return "\n".join(errors) if errors else None

# Функция для показа окна ошибки с кнопкой OK
def show_error_message(screen, message):
    overlay = pygame.Surface((EDITOR_SCREEN_WIDTH, EDITOR_SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0,0,0))
    screen.blit(overlay, (0,0))
    max_line_length = 40
    wrapped_lines = []
    for line in message.split("\n"):
        wrapped_lines.extend(textwrap.wrap(line, width=max_line_length))
    line_height = 30
    padding = 20
    box_width = 450
    box_height = max(padding*2 + line_height*len(wrapped_lines), 250)
    box_rect = pygame.Rect((EDITOR_SCREEN_WIDTH - box_width)//2,
                           (EDITOR_SCREEN_HEIGHT - box_height)//2,
                           box_width, box_height)
    pygame.draw.rect(screen, WHITE, box_rect)
    pygame.draw.rect(screen, (255,0,0), box_rect, 3)
    font = pygame.font.Font(None, 20)
    y_offset = box_rect.top + padding
    for line in wrapped_lines:
        text_surf = font.render(line, True, BLACK)
        text_rect = text_surf.get_rect(centerx=box_rect.centerx, top=y_offset)
        screen.blit(text_surf, text_rect)
        y_offset += line_height
    # Кнопка OK смещена ещё ниже (верхняя граница кнопки на 30 пикселей от нижней границы окна)
    ok_button_rect = pygame.Rect(box_rect.centerx - 40, box_rect.bottom - 30, 80, 30)
    pygame.draw.rect(screen, (180,180,180), ok_button_rect)
    ok_text = font.render("OK", True, BLACK)
    ok_text_rect = ok_text.get_rect(center=ok_button_rect.center)
    screen.blit(ok_text, ok_text_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and ok_button_rect.collidepoint(event.pos):
                waiting = False
            elif event.type == pygame.KEYDOWN:
                waiting = False

# Функция загрузки уровня из двумерного списка
def load_level(level):
    player_pos = None
    boxes = []
    goals = []
    teleport_pairs = {}
    tp_positions = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            val = level[y][x]
            if val == 4:
                player_pos = [x, y]
            elif val == 2:
                boxes.append([x, y])
            elif val == 3:
                goals.append([x, y])
            elif val == 7:
                tp_positions.append((x, y))
    if len(tp_positions) >= 2:
        teleport_pairs[tp_positions[0]] = tp_positions[1]
        teleport_pairs[tp_positions[1]] = tp_positions[0]
    if player_pos is None:
        print("Error: no player position")
        sys.exit()
    return player_pos, boxes, goals, teleport_pairs

def get_restart_button_rect():
    if current_mode == "tutorial":
        return pygame.Rect(10, 10, 100, 30)
    else:
        return pygame.Rect(GAME_SCREEN_WIDTH - 110, GAME_SCREEN_HEIGHT - 40, 100, 30)

def draw_level(screen, current_level_data, player_pos, boxes, goals, teleport_pairs):
    screen.fill(WHITE)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if current_level_data[y][x] == 1:
                screen.blit(wall_img, rect)
            else:
                screen.blit(floor_img, rect)
                if current_level_data[y][x] == 3:
                    screen.blit(goal_img, rect)
                elif current_level_data[y][x] == 5:
                    screen.blit(button_img, rect)
                elif current_level_data[y][x] == 6:
                    if not is_door_open(boxes):
                        screen.blit(door_img, rect)
                elif current_level_data[y][x] == 7:
                    screen.blit(teleport_img, rect)
    for box in boxes:
        rect = pygame.Rect(box[0] * TILE_SIZE, box[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(box_img, rect)
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(player_img, player_rect)
    if current_mode == "tutorial":
        hint_text = ""
        if current_tutorial_index == 0:
            hint_text = "Двигайте ящики на знаки, используя стрелки."
        elif current_tutorial_index == 1:
            hint_text = "Используйте стрелки для перемещения."
        elif current_tutorial_index == 2:
            hint_text = "Перемещайте ящики на цели."
        if hint_text:
            font = pygame.font.Font(None, 28)
            screen.blit(font.render(hint_text, True, BLACK), (10, GAME_SCREEN_HEIGHT - 40))
    restart_rect = get_restart_button_rect()
    pygame.draw.rect(screen, (200,200,200), restart_rect)
    font = pygame.font.Font(None, 24)
    screen.blit(font.render("Restart", True, BLACK), font.render("Restart", True, BLACK).get_rect(center=restart_rect.center))

def is_door_open(boxes):
    return any(box == [3,3] for box in boxes)

def show_loading_screen(screen, width, height):
    loading_path = os.path.join("data", "loading.jpg")
    if os.path.isfile(loading_path):
        loading_image = pygame.image.load(loading_path)
        loading_image = pygame.transform.scale(loading_image, (width, height))
        screen.blit(loading_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)
    else:
        screen.fill(BLACK)
        pygame.display.flip()
        pygame.time.wait(1000)

# Режим редактора уровней
def level_editor_screen():
    editor_screen = pygame.display.set_mode((EDITOR_SCREEN_WIDTH, EDITOR_SCREEN_HEIGHT))
    pygame.display.set_caption("Level Creator")
    level_data = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    selected_tile = 1
    # Изменили palette_start_y на 40, чтобы картинки располагались ниже надписи "Палитра:"
    palette_start_x = GAME_SCREEN_WIDTH + 10
    palette_start_y = 40
    palette_tile_size = 50
    tile_types = [0, 1, 2, 3, 4, 5, 6, 7]
    save_button_rect = pygame.Rect(GAME_SCREEN_WIDTH + 10, EDITOR_SCREEN_HEIGHT - 80, 120, 30)
    cancel_button_rect = pygame.Rect(GAME_SCREEN_WIDTH + 10, EDITOR_SCREEN_HEIGHT - 40, 120, 30)
    clock = pygame.time.Clock()
    running_editor = True
    while running_editor:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_editor = False; return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if mx < GAME_SCREEN_WIDTH and my < GAME_SCREEN_HEIGHT - 50:
                    grid_x = mx // TILE_SIZE
                    grid_y = my // TILE_SIZE
                    level_data[grid_y][grid_x] = selected_tile
                elif mx >= GAME_SCREEN_WIDTH:
                    if save_button_rect.collidepoint(event.pos):
                        error_message = validate_level(level_data)
                        if error_message:
                            show_error_message(editor_screen, error_message)
                        else:
                            append_level_to_file(level_data, GAME_LEVELS_FILE)
                            running_editor = False; return
                    elif cancel_button_rect.collidepoint(event.pos):
                        running_editor = False; return
                    else:
                        for idx, t in enumerate(tile_types):
                            col = idx % 2; row = idx // 2
                            tile_rect = pygame.Rect(palette_start_x + col*(palette_tile_size+10),
                                                      palette_start_y + row*(palette_tile_size+10),
                                                      palette_tile_size, palette_tile_size)
                            if tile_rect.collidepoint(event.pos):
                                selected_tile = t; break
        editor_screen.fill((220,220,220))
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                tile_value = level_data[y][x]
                image = tile_images.get(tile_value, floor_img)
                editor_screen.blit(image, rect)
                pygame.draw.rect(editor_screen, BLACK, rect, 1)
        font = pygame.font.Font(None, 24)
        editor_screen.blit(font.render("Палитра:", True, BLACK), (GAME_SCREEN_WIDTH+10, 0))
        for idx, t in enumerate(tile_types):
            col = idx % 2; row = idx // 2
            tile_rect = pygame.Rect(palette_start_x + col*(palette_tile_size+10),
                                     palette_start_y + row*(palette_tile_size+10),
                                     palette_tile_size, palette_tile_size)
            image = tile_images.get(t, floor_img)
            small_image = pygame.transform.scale(image, (palette_tile_size, palette_tile_size))
            editor_screen.blit(small_image, tile_rect)
            if t == selected_tile:
                pygame.draw.rect(editor_screen, (255,0,0), tile_rect, 3)
            else:
                pygame.draw.rect(editor_screen, BLACK, tile_rect, 1)
        pygame.draw.rect(editor_screen, (180,180,180), save_button_rect)
        editor_screen.blit(font.render("Сохранить", True, BLACK), font.render("Сохранить", True, BLACK).get_rect(center=save_button_rect.center))
        pygame.draw.rect(editor_screen, (180,180,180), cancel_button_rect)
        editor_screen.blit(font.render("Отмена", True, BLACK), font.render("Отмена", True, BLACK).get_rect(center=cancel_button_rect.center))
        pygame.display.flip()
        clock.tick(FPS)

# Главное меню
def show_start_screen():
    screen = pygame.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
    pygame.display.set_caption("Sokoban - Main Menu")
    font = pygame.font.Font(None, 50)
    play_button = font.render("Играть", True, WHITE)
    tutorial_button = font.render("Обучение", True, WHITE)
    creator_button = font.render("Креатор уровней", True, WHITE)
    play_rect = play_button.get_rect(center=(GAME_SCREEN_WIDTH//2, GAME_SCREEN_HEIGHT//2 - 60))
    tutorial_rect = tutorial_button.get_rect(center=(GAME_SCREEN_WIDTH//2, GAME_SCREEN_HEIGHT//2))
    creator_rect = creator_button.get_rect(center=(GAME_SCREEN_WIDTH//2, GAME_SCREEN_HEIGHT//2 + 60))
    while True:
        screen.fill(BLACK)
        screen.blit(play_button, play_rect)
        screen.blit(tutorial_button, tutorial_rect)
        screen.blit(creator_button, creator_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if play_rect.collidepoint(pos):
                    return "play"
                elif tutorial_rect.collidepoint(pos):
                    return "tutorial"
                elif creator_rect.collidepoint(pos):
                    return "creator"

# Меню выбора уровня
def show_level_menu():
    levels_from_file = load_levels_from_file(GAME_LEVELS_FILE)
    if not levels_from_file:
        print("Нет игровых уровней. Добавьте уровни через креатор.")
        return "back"
    screen = pygame.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
    pygame.display.set_caption("Выбор уровня")
    font = pygame.font.Font(None, 40)
    title_font = pygame.font.Font(None, 50)
    title_text = title_font.render("Выберите уровень:", True, WHITE)
    visible_levels = 5
    start_index = 0
    while True:
        screen.fill(BLACK)
        screen.blit(title_text, (GAME_SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        left_arrow_rect = left_arrow_img.get_rect(topleft=(10,10))
        screen.blit(left_arrow_img, left_arrow_rect)
        if start_index > 0:
            up_arrow_rect = up_arrow_img.get_rect(center=(GAME_SCREEN_WIDTH//2, 100))
            screen.blit(up_arrow_img, up_arrow_rect)
        else:
            up_arrow_rect = None
        level_buttons = []
        for i in range(start_index, min(start_index+visible_levels, len(levels_from_file))):
            level_text = font.render(f"Уровень {i+1}", True, WHITE)
            text_rect = level_text.get_rect(center=(GAME_SCREEN_WIDTH//2, 140 + (i - start_index)*50))
            screen.blit(level_text, text_rect)
            level_buttons.append((text_rect, i))
        if start_index+visible_levels < len(levels_from_file):
            down_arrow_rect = down_arrow_img.get_rect(center=(GAME_SCREEN_WIDTH//2, 380))
            screen.blit(down_arrow_img, down_arrow_rect)
        else:
            down_arrow_rect = None
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0 and start_index > 0:
                    start_index -= 1
                elif event.y < 0 and start_index+visible_levels < len(levels_from_file):
                    start_index += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if left_arrow_rect.collidepoint(pos):
                    return "back"
                if up_arrow_rect and up_arrow_rect.collidepoint(pos):
                    start_index -= 1
                elif down_arrow_rect and down_arrow_rect.collidepoint(pos):
                    start_index += 1
                for button, index in level_buttons:
                    if button.collidepoint(pos):
                        return index

# Режим обучения
def show_tutorial_screen():
    global current_tutorial_index, current_level, player_pos, boxes, goals, teleport_pairs, current_mode
    current_mode = "tutorial"
    current_tutorial_index = 0
    current_level = tutorial_levels[current_tutorial_index]
    player_pos, boxes, goals, teleport_pairs = load_level(current_level)
    screen = pygame.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
    pygame.display.set_caption("Обучение")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "back"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                if event.key == pygame.K_r:
                    player_pos, boxes, goals, teleport_pairs = load_level(current_level)
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    new_player_pos = list(player_pos)
                    move_x = 0; move_y = 0
                    if event.key == pygame.K_LEFT: move_x = -1
                    elif event.key == pygame.K_RIGHT: move_x = 1
                    elif event.key == pygame.K_UP: move_y = -1
                    elif event.key == pygame.K_DOWN: move_y = 1
                    new_player_pos[0] += move_x; new_player_pos[1] += move_y
                    if 0 <= new_player_pos[0] < GRID_WIDTH and 0 <= new_player_pos[1] < GRID_HEIGHT and current_level[new_player_pos[1]][new_player_pos[0]] != 1:
                        for i, box in enumerate(boxes):
                            if new_player_pos == box:
                                new_box_pos = [box[0] + move_x, box[1] + move_y]
                                if 0 <= new_box_pos[0] < GRID_WIDTH and 0 <= new_box_pos[1] < GRID_HEIGHT and current_level[new_box_pos[1]][new_box_pos[0]] != 1 and new_box_pos not in boxes:
                                    boxes[i] = new_box_pos
                                    player_pos = new_player_pos
                                    if (player_pos[0], player_pos[1]) in teleport_pairs:
                                        player_pos = list(teleport_pairs[(player_pos[0], player_pos[1])])
                                break
                        else:
                            if current_level[new_player_pos[1]][new_player_pos[0]] != 6 or is_door_open(boxes):
                                if (new_player_pos[0], new_player_pos[1]) in teleport_pairs:
                                    player_pos = list(teleport_pairs[(new_player_pos[0], new_player_pos[1])])
                                else:
                                    player_pos = new_player_pos
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                restart_rect = get_restart_button_rect()
                if restart_rect.collidepoint(event.pos):
                    player_pos, boxes, goals, teleport_pairs = load_level(current_level)
        draw_level(screen, current_level, player_pos, boxes, goals, teleport_pairs)
        pygame.display.flip()
        if check_level_complete(boxes, goals):
            current_tutorial_index += 1
            if current_tutorial_index < len(tutorial_levels):
                current_level = tutorial_levels[current_tutorial_index]
                player_pos, boxes, goals, teleport_pairs = load_level(current_level)
            else:
                return "back"
        clock.tick(FPS)

def check_level_complete(boxes, goals):
    return all(goal in boxes for goal in goals)

# Режим игры
def game_mode():
    global current_mode, current_level, player_pos, boxes, goals, teleport_pairs
    current_mode = "play"
    game_levels = load_levels_from_file(GAME_LEVELS_FILE)
    if not game_levels:
        print("No game levels. Add levels using the creator.")
        return
    choice = show_level_menu()
    if choice == "back":
        return
    current_level = game_levels[choice]
    player_pos, boxes, goals, teleport_pairs = load_level(current_level)
    screen = pygame.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
    pygame.display.set_caption("Sokoban")
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_pos, boxes, goals, teleport_pairs = load_level(current_level)
                new_player_pos = list(player_pos)
                move_x = 0; move_y = 0
                if event.key == pygame.K_LEFT: move_x = -1
                elif event.key == pygame.K_RIGHT: move_x = 1
                elif event.key == pygame.K_UP: move_y = -1
                elif event.key == pygame.K_DOWN: move_y = 1
                new_player_pos[0] += move_x; new_player_pos[1] += move_y
                if 0 <= new_player_pos[0] < GRID_WIDTH and 0 <= new_player_pos[1] < GRID_HEIGHT and current_level[new_player_pos[1]][new_player_pos[0]] != 1:
                    for i, box in enumerate(boxes):
                        if new_player_pos == box:
                            new_box_pos = [box[0] + move_x, box[1] + move_y]
                            if 0 <= new_box_pos[0] < GRID_WIDTH and 0 <= new_box_pos[1] < GRID_HEIGHT and current_level[new_box_pos[1]][new_box_pos[0]] != 1 and new_box_pos not in boxes:
                                boxes[i] = new_box_pos
                                player_pos = new_player_pos
                                if (player_pos[0], player_pos[1]) in teleport_pairs:
                                    player_pos = list(teleport_pairs[(player_pos[0], player_pos[1])])
                            break
                    else:
                        if current_level[new_player_pos[1]][new_player_pos[0]] != 6 or is_door_open(boxes):
                            if (new_player_pos[0], new_player_pos[1]) in teleport_pairs:
                                player_pos = list(teleport_pairs[(new_player_pos[0], new_player_pos[1])])
                            else:
                                player_pos = new_player_pos
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                restart_rect = get_restart_button_rect()
                if restart_rect.collidepoint(event.pos):
                    player_pos, boxes, goals, teleport_pairs = load_level(current_level)
        draw_level(screen, current_level, player_pos, boxes, goals, teleport_pairs)
        pygame.display.flip()
        if check_level_complete(boxes, goals):
            choice += 1
            if choice < len(game_levels):
                current_level = game_levels[choice]
                player_pos, boxes, goals, teleport_pairs = load_level(current_level)
            else:
                print("All levels completed!")
                running = False
        clock.tick(FPS)

# Основной цикл приложения
current_mode = "play"
current_tutorial_index = 0

screen = pygame.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
show_loading_screen(screen, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT)

while True:
    choice = show_start_screen()
    if choice == "play":
        game_mode()
    elif choice == "tutorial":
        result = show_tutorial_screen()
        if result == "back":
            continue
    elif choice == "creator":
        level_editor_screen()

pygame.quit()
