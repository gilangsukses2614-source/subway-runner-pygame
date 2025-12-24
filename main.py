import json, os

import pygame, random, sys

pygame.init()
pygame.mixer.init()

# Sound effect
coin_sound = pygame.mixer.Sound("sounds/coin.wav")
crash_sound = pygame.mixer.Sound("sounds/crash.wav")
click_sound = pygame.mixer.Sound("sounds/click.wav")

coin_sound.set_volume(0.5)
crash_sound.set_volume(0.7)
click_sound.set_volume(0.5)

WIDTH, HEIGHT = 500, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subway Runner Advanced")

clock = pygame.time.Clock()
font = pygame.font.SysFont("bubble", 28)


player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (50, 50))

road_img = pygame.image.load("assets/road1.jpg")
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

obs_img = pygame.image.load("assets/obstacle1.png")
obs_img = pygame.transform.scale(obs_img, (40, 40))

menu_bg = pygame.image.load("assets/menu_bg.jpg")
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))



coins = 0
selected_level = 1

skins_owned = ["default"]
current_skin = "default"

SKINS = {
    "default":  {"price": 0,   "img": "assets/skins/default.png"},
    "red":      {"price": 20,  "img": "assets/skins/red.png"},
    "blue":     {"price": 30,  "img": "assets/skins/blue.png"},
    "gold":     {"price": 50,  "img": "assets/skins/gold.png"},
    "purple":   {"price": 120, "img": "assets/skins/purple.png"},
    "diamond":  {"price": 250, "img": "assets/skins/diamond.png"},
}


skin_images = {}
for skin in SKINS:
    img = pygame.image.load(SKINS[skin]["img"]).convert_alpha()
    skin_images[skin] = pygame.transform.scale(img, (50, 50))



LEVEL_DATA = {
    1: (4, 60),
    2: (5, 55),
    3: (6, 50),
    4: (7, 45),
    5: (8, 40),
    6: (9, 35),
    7: (10, 30),
    8: (12, 25)
}
SAVE_FILE = "save.json"

def save_game():
    data = {
        "coins": coins,
        "skins_owned": skins_owned,
        "current_skin": current_skin,
        "high_score": high_score
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game():
    global coins, skins_owned, current_skin, high_score

    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            coins = data.get("coins", 0)
            skins_owned = data.get("skins_owned", ["default"])
            current_skin = data.get("current_skin", "default")
            high_score = data.get("high_score", 0)


class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.speed = 6

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 50:
            self.x += self.speed

    def draw(self):
        screen.blit(skin_images[current_skin], (self.x, self.y))



class Obstacle:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - 40)
        self.y = -40
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(obs_img, (self.x, self.y))

# =====================
# GAME LOOP
# =====================
def play_game(level):
    pygame.mixer.music.load("sounds/bgm_game.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    global coins

    player = Player()
    obstacles = []
    score = 0
    coins_run = 0

    speed, spawn_rate = LEVEL_DATA[level]
    road_y = 0

    running = True
    while running:

        # ================= EVENT =================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.move(keys)

        # ================= LOGIC =================
        if random.randint(1, spawn_rate) == 1:
            obstacles.append(Obstacle(speed))

        for obs in obstacles[:]:
            obs.move()

            if obs.y > HEIGHT:
                obstacles.remove(obs)
                score += 1
                coins += 1
                coins_run += 1
                coin_sound.play()

            if pygame.Rect(player.x, player.y, 50, 50).colliderect(
                pygame.Rect(obs.x, obs.y, 40, 40)
            ):
                crash_sound.play()
                pygame.mixer.music.stop()
                pygame.time.delay(300)
                game_over(score, coins_run)
                return

        # ================= DRAW =================
        screen.blit(road_img, (0, road_y))
        screen.blit(road_img, (0, road_y - HEIGHT))

        road_y += 5
        if road_y >= HEIGHT:
            road_y = 0

        player.draw()
        for obs in obstacles:
            obs.draw()

        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Coins: {coins}", 10, 40)

        pygame.display.update()
        clock.tick(60)




        

        


def game_over(score, coins_run):
    global high_score

    if score > high_score:
        high_score = score
        save_game()

    while True:
        screen.fill((0, 0, 0))

        draw_center("GAME OVER", 250)
        draw_center(f"Score: {score}", 290)
        draw_center(f"Coins Didapat: {coins_run}", 330)
        draw_center(f"Total Coins: {coins}", 370)
        draw_center(f"High Score: {high_score}", 410)
        draw_center("ENTER = Menu | ESC = Keluar", 460)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    save_game()
                    return   

                if event.key == pygame.K_ESCAPE:
                    save_game()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)



# =====================
# MENU
# =====================
def main_menu():
    pygame.mixer.music.load("sounds/bgm_menu.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    global selected_level

    # Tombol (Rect)
    btn_start = pygame.Rect(150, 230, 200, 40)
    btn_inv   = pygame.Rect(150, 280, 200, 40)
    btn_level = pygame.Rect(150, 330, 200, 40)
    btn_exit  = pygame.Rect(150, 380, 200, 40)

    while True:
        screen.blit(menu_bg, (0, 0))

        draw_center("SUBWAY RUNNER", 150)

        mouse_pos = pygame.mouse.get_pos()

        # Warna hover
        def draw_button(rect, text):
            color = (100, 200, 100) if rect.collidepoint(mouse_pos) else (80, 80, 80)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            txt = font.render(text, True, (255, 255, 255))
            txt_rect = txt.get_rect(center=rect.center)
            screen.blit(txt, txt_rect)

        draw_button(btn_start, "Start Game")
        draw_button(btn_inv, "Inventori")
        draw_button(btn_level, "Pilih Level")
        draw_button(btn_exit, "Exit")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    click_sound.play()
 
                    if btn_start.collidepoint(event.pos):
                        play_game(selected_level)

                    elif btn_inv.collidepoint(event.pos):
                        inventori()

                    elif btn_level.collidepoint(event.pos):
                        pilih_level()

                    elif btn_exit.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(60)

def buy_animation(rect):
    for scale in range(1, 8):
        glow = pygame.Surface((rect.width+scale*4, rect.height+scale*4))
        glow.set_alpha(80)
        glow.fill((255, 215, 0))
        screen.blit(glow, (rect.x-scale*2, rect.y-scale*2))
        pygame.display.update()
        pygame.time.delay(20)

def inventori():
    global coins, current_skin, skins_owned

    card_w, card_h = 120, 120
    gap = 20
    start_x = (WIDTH - (card_w * 2 + gap)) // 2
    start_y = 200

    skin_list = list(SKINS.keys())

    while True:
        screen.fill((25, 25, 25))
        draw_center("INVENTORI SKIN", 120)
        draw_center(f"Coins: {coins}", 160)

        mouse_pos = pygame.mouse.get_pos()

        skin_rects = []

        for i, skin in enumerate(skin_list):
            row = i // 2
            col = i % 2
            x = start_x + col * (card_w + gap)
            y = start_y + row * (card_h + gap)
            rect = pygame.Rect(x, y, card_w, card_h)
            skin_rects.append((skin, rect))

            owned = skin in skins_owned
            selected = skin == current_skin

            color = (100, 200, 120) if selected else (120, 120, 120) if rect.collidepoint(mouse_pos) else (80, 80, 80)

            rect_draw = rect.inflate(6, 6) if rect.collidepoint(mouse_pos) else rect

            pygame.draw.rect(screen, color, rect_draw, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect_draw, 2, border_radius=10)

            screen.blit(skin_images[skin], (x + 35, y + 20))

            label = "ACTIVE" if selected else "SELECT" if owned else f"{SKINS[skin]['price']} COIN"
            txt = font.render(label, True, (255, 255, 0))
            screen.blit(txt, (x + 10, y + 90))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for skin, rect in skin_rects:
                    if rect.collidepoint(event.pos):
                        if skin in skins_owned:
                            current_skin = skin
                            click_sound.play()
                        elif coins >= SKINS[skin]["price"]:
                            coins -= SKINS[skin]["price"]
                            skins_owned.append(skin)
                            current_skin = skin
                            coin_sound.play()
                            buy_animation(rect)
                            save_game()

        pygame.display.update()
        clock.tick(60)



def pilih_level():
    global selected_level

    cols = 2
    box_w, box_h = 140, 60
    gap = 20
    start_x = (WIDTH - (cols * box_w + gap)) // 2
    start_y = 200

    level_boxes = []

    for i in range(8):
        row = i // cols
        col = i % cols
        x = start_x + col * (box_w + gap)
        y = start_y + row * (box_h + gap)
        rect = pygame.Rect(x, y, box_w, box_h)
        level_boxes.append((i + 1, rect))

    while True:
        screen.fill((25, 25, 25))
        draw_center("PILIH LEVEL", 120)

        mouse_pos = pygame.mouse.get_pos()

        for lvl, rect in level_boxes:
            # warna level
            if lvl == selected_level:
                color = (80, 200, 120)      # aktif
            elif rect.collidepoint(mouse_pos):
                color = (120, 120, 120)     # hover
            else:
                color = (70, 70, 70)        # normal

            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)

            txt = font.render(f"Level {lvl}", True, (255, 255, 255))
            txt_rect = txt.get_rect(center=rect.center)
            screen.blit(txt, txt_rect)
        
        
        draw_center("Klik level • ESC untuk kembali", 600)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for lvl, rect in level_boxes:
                        if rect.collidepoint(event.pos):
                            selected_level = lvl
                            click_sound.play()
                            return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()
        clock.tick(60)


# =====================
# TEXT HELPER
# =====================
def draw_text(text, x, y):
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))

def draw_center(text, y):
    img = font.render(text, True, (255, 255, 255))
    rect = img.get_rect(center=(WIDTH // 2, y))
    screen.blit(img, rect)

# =====================
# RUN
# =====================
high_score = 0
load_game()
main_menu()

