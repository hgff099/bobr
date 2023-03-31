import pygame
import random

pygame.init()

"""общие параметры"""
FPS = 80
WIDTH = 800
HEIGHT = 450
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

"""изоброжения"""
ferrari = pygame.image.load("pngegg.png")
ferrari_white = pygame.image.load("hatchback-car-top-view-silhouette-420913.png")
ferrari_green = pygame.image.load("car-top-view-210079.png")
block = pygame.image.load("block.png")
fon_game_over = pygame.image.load("maxresdefault.jpg")
fon_road = pygame.image.load("1644914480_23-fikiwiki-com-p-kartinki-asfalta-25.jpg")
fon = pygame.image.load("background.png")
fon_score = pygame.image.load("score_fon.jpg")

"""получение прямоугольников и зображение"""
# ferrari_rect = ferrari.get_rect()
block_rect = block.get_rect(top=random.choice([20, 120]))

"""кнопки меню"""
rect_start = pygame.Rect(280, 120, 250, 80)
rect_exit = pygame.Rect(280, 240, 250, 80)

"""переменные для подсчёта очков"""
damage = 0
distance = 0
frame_count = 0

"""шрифты"""
font_menu = pygame.font.SysFont("arial", 60, bold=True)
font_style = pygame.font.SysFont("arial", 20)
font_button = pygame.font.SysFont("arial", 40, bold=True)
font_status = pygame.font.SysFont("arial", 20, bold=True)

"""натписи"""
new_game_txt = font_button.render("нажмите пробел чтобы продолжить", True, WHITE)
menu_title = font_menu.render("ROCKET RACE!", True, WHITE)
start_btn = font_menu.render("START", True, BLACK)
exit_btn = font_menu.render("EXIT", True, BLACK)

"""пораметры окна и часы"""
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
run = True

"""музыка"""
pygame.mixer.music.load("audio55544.mp3")
crash_sound = pygame.mixer.Sound("car_horn.wav")
end_crash_sound = pygame.mixer.Sound("93ef12aac58d82a.mp3")

"""упровление машины"""
direction = "stop"

"""игровой режими"""
game_mode = "menu"

"""разметка"""
road = []
for i in range(10, WIDTH, 100):
    road.append([i, 112, 50, 10])

"""обект экрана"""
screen = window.get_rect()

while run:
    if game_mode == "menu":
        """режим: меню"""
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1 and rect_start.collidepoint(i.pos):
                    game_mode = "select"
                elif i.button == 1 and rect_exit.collidepoint(i.pos):
                    run = False
        window.blit(fon, (0,0))
        window.blit(menu_title, (230, 20))
        """отрисовка кнопок"""
        pygame.draw.rect(window, YELLOW, rect_start)
        window.blit(start_btn, rect_start)

        pygame.draw.rect(window, YELLOW, rect_exit)
        window.blit(exit_btn, rect_exit)

    elif game_mode == 'select':
        """Блок выбора скина машинки"""
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1 and ferrari_rect.collidepoint(i.pos):
                    game_mode = 'game'
                    skin_car = ferrari
                    skin_rect = ferrari.get_rect(left=0, top=0)
                    car_name = "Белая"
                elif i.button == 1 and ferrari_white_rect.collidepoint(i.pos):
                    game_mode = 'game'
                    skin_car = ferrari_white
                    skin_rect = ferrari_white.get_rect(left=0, top=0)
                    car_name = "сераяя"
                elif i.button == 1 and ferrari_green_rect.collidepoint(i.pos):
                    game_mode = 'game'
                    skin_car = ferrari_green
                    skin_rect = ferrari_green.get_rect(left=0, top=0)
                    car_name = "зелённая"

        window.blit(fon_score, (0, 0))
        ferrari_rect = ferrari.get_rect(left=305, top=100)
        ferrari_white_rect = ferrari_white.get_rect(left=305, top=180)
        ferrari_green_rect = ferrari_green.get_rect(left=150, top=360 )

        window.blit(ferrari, ferrari_rect)
        window.blit(ferrari_white, ferrari_white_rect)
        window.blit(ferrari_green, ferrari_green_rect)

    elif game_mode == "game":
        """режим: игра"""
        window.blit(fon_road, (0, 0))

        for i in pygame.event.get():
            """отслеживание игровых событий"""
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_UP:
                    direction = "up"
                elif i.key == pygame.K_DOWN:
                    direction = "down"
            elif i.type == pygame.KEYUP:
                direction = "stop"

        """перемещение машины"""
        if direction == "up" and skin_rect.top > screen.top:
            skin_rect.top -= 3
        elif direction == "down" and skin_rect.bottom < screen.bottom // 2:
            skin_rect.bottom += 3

        """столкновение с блоком"""
        if skin_rect.colliderect(block_rect):
            damage += 1
            block_rect.left = WIDTH
            block_rect.top = random.choice([20, 120])
            crash_sound.play()


        """отрисовка разметки"""
        for i in road:
            if i[0] < 0:
                i[0] = WIDTH
            else:
                i[0] -= 2
            pygame.draw.rect(window, WHITE, i)

        frame_count += 1
        speed = frame_count // FPS

        """статус-бар"""
        pygame.draw.rect(window, WHITE, (0, 225, WIDTH, 225))
        label = font_status.render(f'пройденное расстояние: {speed}', True, BLACK)
        damage_text = font_status.render(f'повреждения: {damage}', True, BLACK)
        window.blit(label, (10, 300))
        window.blit(damage_text, (250, 300))

        """отрисовка блоков"""
        if block_rect.right > screen.left:
            block_rect.right -= 5
        else:
            block_rect.left = screen.right
            block_rect.top = random.choice([20, 120])

        """проверка столкновений"""
        if damage >= 3:
            """запись в файл"""
            with open('files/test.txt', 'a', encoding='utf-8') as file:
                file.write(f'{car_name} машинка набирает {speed} очков\n')
            """экран конца"""
            game_mode = 'game_over'
        else:
            window.blit(block, block_rect)
            window.blit(skin_car, skin_rect)

    elif game_mode == 'game_over':
        """конец игры"""
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE:
                frame_count = 0
                game_mode = 'score'
        window.blit(fon_game_over, (0, 0))
        window.blit(new_game_txt, (100, 300))


    elif game_mode == 'score':
        """блок выведения результатов"""
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE:
                frame_count = 0
                game_mode = 'menu'
        window.fill(WHITE)

        """чтение результатов из файла"""
        with open('files/test.txt.','r', encoding='utf-8') as file:
            top_score = file.readlines()

        """вывидение на экран"""
        window.blit(fon_score, (0,0))
        y_pose = 50
        for line in top_score[-5:]:
            score_surf = font_style.render(line, True, WHITE)
            window.blit(score_surf, (20, y_pose))
            y_pose += 30


        window.blit(new_game_txt, (100,350))




    pygame.display.update()
    clock.tick(FPS)
