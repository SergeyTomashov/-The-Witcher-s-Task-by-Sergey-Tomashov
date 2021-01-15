import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 720
WINDOWHEIGHT = 720
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 30
BADDIEMAXSIZE = 80
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5


# Задается функция terminate() для выхода из игры
def terminate():
    pygame.quit()
    sys.exit()


# Функция, которая проверяет нажатие клавиши на клавиатуре от игрока
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


# Функция для проверки соприкосновения главного героя и противника
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False


# Определение функции для рисоания текста
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# настройки дисплея видеоигры и курсора
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("The Witcher's Task")
pygame.mouse.set_visible(False)

# Настройки системных шрифтов в pygame
font = pygame.font.SysFont(None, 40)

# Настройки изображения главного героя и противника
playerImage = pygame.image.load('Novigrad.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')

# Отображение начального или стартового экрана для игрока в pygame
# Заливка цветом дисплея в pygame
windowSurface.fill(BACKGROUNDCOLOR)
# Определение заголока, его шрифта и начального меню в pygame
drawText("The Witcher's Task", font, windowSurface,
         (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText("Sergey Tomashov's Game", font, windowSurface,
         (WINDOWWIDTH / 4), (WINDOWHEIGHT / 4))
drawText('Press any key button to start the game', font, windowSurface,
         (WINDOWWIDTH / 5) - 30, (WINDOWHEIGHT / 3) + 50)
# Отображение всего текста и шрифтов на дисплее
pygame.display.update()
# Запуск игры после нажатия пользователя на любую клавишу клавиатуры в pygame
waitForPlayerToPressKey()

# Начальное значение лучшего рекорда в pygame
topScore = 0
while True:
    # Настройки для начала игры с игровым циклом
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0

    while True:  # Игровой цикл работает во время запуска игры
        score += 1

        for event in pygame.event.get():  # Обработка события выхода из игры
            if event.type == QUIT:
                terminate()

            # Обработка нажатой пользователем клавиши на клавиатуре
            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            # Обработка отпускаемой пользователем клавиши на клавиатуре
            if event.type == KEYUP:
                # Обработка чит-кодов
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # Обработка движений курсора мыши для перемещения главного героя
                # Проверка направления у персонажа
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
            # Если это требуется для игры, то добавляются новые противники
            if not reverseCheat and not slowCheat:
                baddieAddCounter += 1
            if baddieAddCounter == ADDNEWBADDIERATE:
                baddieAddCounter = 0
                baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
                newBaddie = {
                    'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize),
                                        0 - baddieSize, baddieSize,
                                        baddieSize),
                    'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                    'surface': pygame.transform.scale(baddieImage,
                                                      (baddieSize, baddieSize)), }
                baddies.append(newBaddie)

            # Главный герой перемещается на поверхности дисплея
            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            if moveRight and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(PLAYERMOVERATE, 0)
            if moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -1 * PLAYERMOVERATE)
            if moveDown and playerRect.bottom < WINDOWHEIGHT:
                playerRect.move_ip(0, PLAYERMOVERATE)

            # Передвижение противников
            for b in baddies:
                if not reverseCheat and not slowCheat:
                    b['rect'].move_ip(0, b['speed'])
                elif reverseCheat:
                    b['rect'].move_ip(0, -5)
                elif slowCheat:
                    b['rect'].move_ip(0, 1)

            # Удаление противников, кто спаунится за пределами дисплея
            for b in baddies[:]:
                if b['rect'].top > WINDOWHEIGHT:
                    baddies.remove(b)

            # Отображение игрового мира на дисплее игрока
            windowSurface.fill(BACKGROUNDCOLOR)

            # Отображение подсчета игровых очков и лучшего рекорда игрока
            drawText('Score: %s' % (score), font, windowSurface, 10, 0)
            drawText('Top score: %s' % (topScore), font, windowSurface, 10, 40)

            # Отображение прямоугольника игрока
            windowSurface.blit(playerImage, playerRect)

            # Отображение всех противников
            for b in baddies:
                windowSurface.blit(b['surface'], b['rect'])
            pygame.display.update()

        # Проверка на соприкосновение противников и главного героя
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score  # Отображение нового лучшего рекорда игрока
            break

        mainClock.tick(FPS)
    # Отображение игры и текста 'game over'
    drawText('GAME IS OVER!', font, windowSurface,
             (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press the key to start the new game', font,
             windowSurface, (WINDOWWIDTH / 3) - 120,
             (WINDOWHEIGHT / 3) + 50)
    # Отображения всех изображений на дисплее игрока
    pygame.display.update()
    # Действие обработки нажития клавиши клавиатуры игроком
    waitForPlayerToPressKey()
