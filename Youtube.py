import pygame

pygame.init()

win = pygame.display.set_mode((852, 480))
pygame.display.set_caption("First Game!")

walkRight = [pygame.image.load('Images/R1.png'), pygame.image.load('Images/R2.png'), pygame.image.load('Images/R3.png'),
             pygame.image.load('Images/R4.png'), pygame.image.load('Images/R5.png'), pygame.image.load('Images/R6.png'),
             pygame.image.load('Images/R7.png'), pygame.image.load('Images/R8.png'), pygame.image.load('Images/R9.png')]
walkLeft = [pygame.image.load('Images/L1.png'), pygame.image.load('Images/L2.png'), pygame.image.load('Images/L3.png'),
            pygame.image.load('Images/L4.png'), pygame.image.load('Images/L5.png'), pygame.image.load('Images/L6.png'),
            pygame.image.load('Images/L7.png'), pygame.image.load('Images/L8.png'), pygame.image.load('Images/L9.png')]
bg = pygame.image.load('Images/bg.jpg')
char = pygame.image.load('Images/standing.png')

bulletSound = pygame.mixer.Sound('Sounds/bullet.wav')
goblin_hitSound = pygame.mixer.Sound('Sounds/goblin_hit.wav')
man_hitSound = pygame.mixer.Sound('Sounds/man_hit.wav')
win_sound = pygame.mixer.Sound('Sounds/win.wav')
lose_sound = pygame.mixer.Sound('Sounds/lose.wav')
jump_sound = pygame.mixer.Sound('Sounds/jump.wav')
music = pygame.mixer.music.load('Sounds/music.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

score = 0


class player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 10
        self.standing = True
        self.hitBox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 50
        self.visible = True
        self.life = 1

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        pygame.draw.rect(win, (255, 0, 0), (self.hitBox[0], self.hitBox[1] - 20, 50, 5))
        pygame.draw.rect(win, (0, 128, 0), (self.hitBox[0], self.hitBox[1] - 20, 50 - (1 * (50 - self.health)), 5))
        self.hitBox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitBox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 405
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (852/2 - text.get_width()/2, 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy:
    walkRight = [pygame.image.load('Images/R1E.png'), pygame.image.load('Images/R2E.png'), pygame.image.load('Images/R3E.png'),
                 pygame.image.load('Images/R4E.png'), pygame.image.load('Images/R5E.png'), pygame.image.load('Images/R6E.png'),
                 pygame.image.load('Images/R7E.png'), pygame.image.load('Images/R8E.png'), pygame.image.load('Images/R9E.png'),
                 pygame.image.load('Images/R10E.png'), pygame.image.load('Images/R11E.png')]
    walkLeft = [pygame.image.load('Images/L1E.png'), pygame.image.load('Images/L2E.png'), pygame.image.load('Images/L3E.png'),
                pygame.image.load('Images/L4E.png'), pygame.image.load('Images/L5E.png'), pygame.image.load('Images/L6E.png'),
                pygame.image.load('Images/L7E.png'), pygame.image.load('Images/L8E.png'), pygame.image.load('Images/L9E.png'),
                pygame.image.load('Images/L10E.png'), pygame.image.load('Images/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [10, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitBox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 100
        self.visible = True
        self.life = 1

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitBox[0], self.hitBox[1] - 20, 50, 5))
            pygame.draw.rect(win, (0, 128, 0), (self.hitBox[0], self.hitBox[1] - 20, 50 - (0.5 * (100 - self.health)), 5))
            self.hitBox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255, 0, 0), self.hitBox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            win_sound.play()
            self.visible = False


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text_score = font_for_score.render('Score : ' + str(score), 1, (0, 0, 0))
    text_end = font_for_end.render('Game Over !', 1, (0, 0, 0))
    text_result1 = font_for_result.render('You WIN !', 1, (0, 0, 0))
    text_result2 = font_for_result.render('You LOSE !', 1, (0, 0, 0))
    text_exit = font_for_message.render('Press ESC to close the game.', 1, (0, 0, 0))
    text_info = font_for_message.render('How to play :', 1, (0, 0, 0))
    text_insts = font_for_message.render(' < = left   > = right   ^ = jump   space = shoot ', 1, (0, 0, 0))
    win.blit(text_score, (700, 10))
    win.blit(text_info, (10, 10))
    win.blit(text_insts, (10, 30))
    if goblin.visible and man.visible:
        man.draw(win)
        goblin.draw(win)
        for bullet in bullets:
            bullet.draw(win)
    elif (not goblin.visible and goblin.life == 1) or (not man.visible and man.life == 1):
        pygame.mixer.music.stop()
        pygame.time.delay(300)
        for i in range(-text_end.get_height(), 200):
            pygame.time.delay(5)
            win.blit(bg, (0, 0))
            win.blit(text_score, (700, 10))
            win.blit(text_end, (180, i))
            pygame.display.update()

        if not goblin.visible:
            pygame.time.delay(500)
            win.blit(text_result1, (330, 270))
        if not man.visible:
            pygame.time.delay(500)
            win.blit(text_result2, (320, 270))
        pygame.time.delay(500)
        win.blit(text_exit, (280, 450))
        goblin.life = 0
        man.life = 0

    pygame.display.update()


font_for_score = pygame.font.SysFont('comicsans', 30, True)
font_for_end = pygame.font.SysFont('comicsans', 100, True)
font_for_result = pygame.font.SysFont('comicsans', 50, True)
font_for_message = pygame.font.SysFont('comicsans', 30)
man = player(300, 405, 64, 64)
goblin = enemy(100, 410, 64, 64, 788)
shootLoops = 0
bullets = []
run = True
while run:
    clock.tick(27)

    if man.hitBox[1] < goblin.hitBox[1] + goblin.hitBox[3] and man.hitBox[1] + man.hitBox[3] > goblin.hitBox[1]:
        if man.hitBox[0] + man.hitBox[2] > goblin.hitBox[0] and man.hitBox[0] < goblin.hitBox[0] + goblin.hitBox[2]:
            if goblin.visible and man.visible:
                man_hitSound.play()
                man.hit()
                score -= 5
                man.health -= 5

    if man.health <= 0 and man.life != 0:
        lose_sound.play()
        man.visible = False

    if shootLoops > 0:
        shootLoops += 1
    if shootLoops > 3:
        shootLoops = 0

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitBox[1] + goblin.hitBox[3] and bullet.y + bullet.radius > goblin.hitBox[1]:
            if bullet.x + bullet.radius > goblin.hitBox[0] and bullet.x - bullet.radius < goblin.hitBox[0] + goblin.hitBox[2]:
                if goblin.visible:
                    goblin_hitSound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))

        if 0 < bullet.x < 852:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoops == 0:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 10:
            bulletSound.play()
            bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 3, (0, 0, 0), facing))
        shootLoops = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x + man.width < 852 - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not man.isJump:
        if keys[pygame.K_UP]:
            jump_sound.play()
            man.isJump = True
            walkCount = 0
    else:
        if man.jumpCount >= -10:
            mul = 1
            if man.jumpCount < 0:
                mul = -1
            man.y -= mul * (man.jumpCount ** 2)/2
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    if goblin.life != 0 and man.life != 0:
        redrawGameWindow()
    else:
        if keys[pygame.K_ESCAPE]:
            run = False

pygame.quit()
