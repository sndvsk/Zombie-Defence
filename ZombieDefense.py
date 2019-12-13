import pygame, random, threading, time
pygame.init()
width = 1024    #1024
height = 768    #768 or 900

screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)

gray_background = pygame.image.load("img/other/gray_background.png")

gunSound = pygame.mixer.Sound('sounds/gunSound.wav')
musicBG = pygame.mixer.music.load("sounds/musicBG.mp3")

font = pygame.font.SysFont("monospace", 24, bold=True, italic=False)
scoreFont = pygame.font.SysFont("monospace", 48, bold=True, italic=False)
GAMEOVERfont = pygame.font.SysFont("monospace", 72, bold=True, italic=False)

GAMEOVERImg = GAMEOVERfont.render("GAME OVER", 1, (255,0,0))
GAMEOVERX = screen.get_width() / 2 - GAMEOVERImg.get_width() / 2
GAMEOVERY = screen.get_height() / 2 - GAMEOVERImg.get_height() / 2 - 80

turret = pygame.image.load("img/weapons/Desert.png")
turretHeight = turret.get_height()
turretX = width / 2 - turret.get_width() / 2

wallX = 0
wallY = height - turret.get_height()

bullet = pygame.image.load("img/other/bullet.png")
bulletX = turretX + turret.get_width() / 2 - bullet.get_width() / 2
bulletY = height - turret.get_height()
bulletState = "waiting"

fire = pygame.image.load("img/other/fire.png")

zombies = []
spawnSpeed = 1
zombieSpeed = 1


class Zombie:
    def __init__(self, zombieX, zombieY, zombieImg):
        self.zombieX = zombieX
        self.zombieY = zombieY
        self.image = zombieImg
        self.hp3Image = pygame.image.load("img/hp/3hp.png")
        self.hp2Image = pygame.image.load("img/hp/2hp.png")
        self.hp1Image = pygame.image.load("img/hp/1hp.png")
        self.hp = 150

    def attack(self):
        self.zombieY += zombieSpeed
        screen.blit(self.image, [self.zombieX, self.zombieY])
        if self.hp == 150:
            screen.blit(self.hp3Image, [self.zombieX, self.zombieY - 10])
        elif self.hp == 100:
            screen.blit(self.hp2Image, [self.zombieX, self.zombieY - 10])
        elif self.hp == 50:
            screen.blit(self.hp1Image, [self.zombieX, self.zombieY - 10])


class Level:

    def __init__(self, location):
        self.location = location
        self.bg = pygame.image.load("img/bg/"+location+".png")
        self.icon = pygame.image.load("img/icons/"+location+".png")

        self.zombie = pygame.image.load("img/zombies/"+location+".png")
        self.weapon = pygame.image.load("img/weapons/"+location+".png")
        self.bullet = pygame.image.load("img/bullets/"+location+".png")
        self.wall = pygame.image.load("img/walls/"+location+".png")

        self.HP = 100
        self.record = 0
        self.KILLED_ZOMBIES = 0
        self.enabled = False


class GameController:

    levels = {"Desert": Level("Desert"), "Football": Level("Football"), "Neon": Level("Neon"), "Tartu": Level("Tartu")}
    backgrounds = {"START": pygame.image.load("img/bg/start.jpg"), "SELECT": pygame.image.load("img/bg/level_select.png")}

    play_button = pygame.image.load("img/buttons/playButtonRed.png")
    play_x = screen.get_width() / 2 - play_button.get_width() / 2
    play_y = screen.get_height() / 2 + 50

    def __init__(self):
        self.level = None
        self.bg = self.backgrounds["START"]
        self.is_started = False
        self.state = "START"
        self.zombies = []

        self.levels["Desert"].enabled = True

    def start_menu(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        if ((mouse_x >= self.play_x) and (mouse_x <= (self.play_x + self.play_button.get_width()))) and (
                (mouse_y >= self.play_y) and (mouse_y <= (self.play_y + self.play_button.get_height()))):
            self.play_button = pygame.image.load("img/buttons/playButtonBlue.png")
        else:
            self.play_button = pygame.image.load("img/buttons/playButtonRed.png")

        screen.blit(self.bg, [0, 0])
        screen.blit(self.play_button, [self.play_x, self.play_y])

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if ((mouse_x >= self.play_x) and (mouse_x <= (self.play_x + self.play_button.get_width()))) and (
                        (mouse_y >= self.play_y) and (mouse_y <= (self.play_y + self.play_button.get_height()))):
                    gunSound.play()
                    self.state = "SELECT LEVEL"
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    pygame.quit()

    def select_level(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        desert_pos = [screen.get_width() / 2 - 70 - self.levels["Desert"].icon.get_width(), 330]
        football_pos = [screen.get_width() / 2 + 280 - self.levels["Football"].icon.get_width(), 330]
        neon_pos = [screen.get_width() / 2 - 70 - self.levels["Neon"].icon.get_width(), 545]
        tartu_pos = [screen.get_width() / 2 + 280 - self.levels["Tartu"].icon.get_width(), 545]

        overlay = pygame.image.load("img/icons/overlay.png")

        self.bg = self.backgrounds["SELECT"]
        screen.blit(self.bg, [0, 0])

        screen.blit(self.levels["Desert"].icon, desert_pos)
        screen.blit(self.levels["Football"].icon, football_pos)
        screen.blit(self.levels["Neon"].icon, neon_pos)
        screen.blit(self.levels["Tartu"].icon, tartu_pos)

        if ((mouse_x >= desert_pos[0]) and (mouse_x <= (desert_pos[0] + self.levels["Desert"].icon.get_width()))) and (
                (mouse_y >= desert_pos[1]) and (mouse_y <= (desert_pos[1] + self.levels["Desert"].icon.get_height()))):
            screen.blit(overlay, desert_pos)
        if ((mouse_x >= football_pos[0]) and (mouse_x <= (football_pos[0] + self.levels["Football"].icon.get_width()))) and (
                (mouse_y >= football_pos[1]) and (mouse_y <= (football_pos[1] + self.levels["Football"].icon.get_height()))):
            screen.blit(overlay, football_pos)
        if ((mouse_x >= neon_pos[0]) and (mouse_x <= (neon_pos[0] + self.levels["Neon"].icon.get_width()))) and (
                (mouse_y >= neon_pos[1]) and (mouse_y <= (neon_pos[1] + self.levels["Neon"].icon.get_height()))):
            screen.blit(overlay, neon_pos)
        if ((mouse_x >= tartu_pos[0]) and (mouse_x <= (tartu_pos[0] + self.levels["Tartu"].icon.get_width()))) and (
                (mouse_y >= tartu_pos[1]) and (mouse_y <= (tartu_pos[1] + self.levels["Tartu"].icon.get_height()))):
            screen.blit(overlay, tartu_pos)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if ((mouse_x >= desert_pos[0]) and (
                        mouse_x <= (desert_pos[0] + self.levels["Desert"].icon.get_width()))) and (
                        (mouse_y >= desert_pos[1]) and (
                        mouse_y <= (desert_pos[1] + self.levels["Desert"].icon.get_height()))):
                    gunSound.play()
                    self.level = self.levels["Desert"]
                    self.is_started = True
                    threading.Thread(target=self.spawn_zombies).start()
                if ((mouse_x >= football_pos[0]) and (
                        mouse_x <= (football_pos[0] + self.levels["Football"].icon.get_width()))) and (
                        (mouse_y >= football_pos[1]) and (
                        mouse_y <= (football_pos[1] + self.levels["Football"].icon.get_height()))):
                    gunSound.play()
                    self.level = self.levels["Football"]
                    self.is_started = True
                    threading.Thread(target=self.spawn_zombies).start()
                if ((mouse_x >= neon_pos[0]) and (
                        mouse_x <= (neon_pos[0] + self.levels["Neon"].icon.get_width()))) and (
                        (mouse_y >= neon_pos[1]) and (
                        mouse_y <= (neon_pos[1] + self.levels["Neon"].icon.get_height()))):
                    screen.blit(overlay, neon_pos)
                    gunSound.play()
                    self.level = self.levels["Neon"]
                    self.is_started = True
                    threading.Thread(target=self.spawn_zombies).start()
                if ((mouse_x >= tartu_pos[0]) and (
                        mouse_x <= (tartu_pos[0] + self.levels["Tartu"].icon.get_width()))) and (
                        (mouse_y >= tartu_pos[1]) and (
                        mouse_y <= (tartu_pos[1] + self.levels["Tartu"].icon.get_height()))):
                    screen.blit(overlay, tartu_pos)
                    gunSound.play()
                    self.level = self.levels["Tartu"]
                    self.is_started = True
                    threading.Thread(target=self.spawn_zombies).start()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    pygame.quit()

        pygame.display.flip()

    def pause(self):
        screen.blit(gray_background, [0, 0])

        hp_label = font.render(str(self.level.HP) + "HP", 1, (255, 0, 0))

        killed_zombies_label = font.render("Killed Zombies: " + str(self.level.KILLED_ZOMBIES), 1, (255, 0, 0))

        score_label = scoreFont.render("Your score: " + str(self.level.KILLED_ZOMBIES), 1, (255, 0, 0))
        scoreX = screen.get_width() / 2 - score_label.get_width() / 2
        scoreY = GAMEOVERY + GAMEOVERImg.get_height()

        resume_button = scoreFont.render("RESUME", 1, (255, 0, 0))
        resumeX = screen.get_width() / 2 - resume_button.get_width() / 2
        resumeY = scoreY + score_label.get_height() + 10

        quit_button = scoreFont.render("QUIT", 1, (255, 0, 0))
        quitX = screen.get_width() / 2 - quit_button.get_width() / 2
        quitY = resumeY + resume_button.get_height() + 10

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        if ((mouseX >= resumeX) and (mouseX <= (resumeX + resume_button.get_width()))) and (
                (mouseY >= resumeY) and (mouseY <= (resumeY + resume_button.get_height()))):
            resume_button = scoreFont.render("RESUME", 1, (0, 0, 255))
        else:
            resume_button = scoreFont.render("RESUME", 1, (255, 0, 0))
        if ((mouseX >= quitX) and (mouseX <= (quitX + quit_button.get_width()))) and (
                (mouseY >= quitY) and (mouseY <= (quitY + quit_button.get_height()))):
            quit_button = scoreFont.render("QUIT", 1, (0, 0, 255))
        else:
            quit_button = scoreFont.render("QUIT", 1, (255, 0, 0))

        screen.blit(hp_label, [0, 0])
        screen.blit(killed_zombies_label, [width - killed_zombies_label.get_width(), 0])
        screen.blit(score_label, [scoreX, scoreY])
        screen.blit(resume_button, [resumeX, resumeY])
        screen.blit(quit_button, [quitX, quitY])

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.is_started = True
                    self.state = "play"
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if ((mouseX >= resumeX) and (mouseX <= (resumeX + resume_button.get_width()))) and (
                        (mouseY >= resumeY) and (mouseY <= (resumeY + resume_button.get_height()))):
                    self.is_started = True
                    self.state = "play"
                if ((mouseX >= quitX) and (mouseX <= (quitX + quit_button.get_width()))) and (
                        (mouseY >= quitY) and (mouseY <= (quitY + quit_button.get_height()))):
                    pygame.quit()

        pygame.display.flip()

    def end_round(self):
        self.zombies = []

        scoreImg = scoreFont.render("Your score: " + str(self.level.KILLED_ZOMBIES), 1, (255, 0, 0))
        scoreX = screen.get_width() / 2 - scoreImg.get_width() / 2
        scoreY = GAMEOVERY + GAMEOVERImg.get_height()

        tryAgainImg = scoreFont.render("TRY AGAIN", 1, (255, 0, 0))
        tryAgainX = screen.get_width() / 2 - tryAgainImg.get_width() / 2
        tryAgainY = scoreY + scoreImg.get_height() + 10

        quitImg = scoreFont.render("QUIT", 1, (255, 0, 0))
        quitX = screen.get_width() / 2 - quitImg.get_width() / 2
        quitY = tryAgainY + tryAgainImg.get_height() / 2 + 30

        screen.fill([0, 0, 0])
        screen.blit(GAMEOVERImg, [GAMEOVERX, GAMEOVERY])
        screen.blit(scoreImg, [scoreX, scoreY])

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        if ((mouseX >= tryAgainX) and (mouseX <= (tryAgainX + tryAgainImg.get_width()))) and (
                (mouseY >= tryAgainY) and (mouseY <= (tryAgainY + tryAgainImg.get_height()))):
            tryAgainImg = scoreFont.render("TRY AGAIN", 1, (0, 0, 255))
        else:
            tryAgainImg = scoreFont.render("TRY AGAIN", 1, (255, 0, 0))

        if ((mouseX >= quitX) and (mouseX <= (quitX + quitImg.get_width()))) and (
                (mouseY >= quitY) and (mouseY <= (quitY + quitImg.get_height()))):
            quitImg = scoreFont.render("QUIT", 1, (0, 0, 255))
        else:
            quitImg = scoreFont.render("QUIT", 1, (255, 0, 0))

        screen.blit(quitImg, [quitX, quitY])
        screen.blit(tryAgainImg, [tryAgainX, tryAgainY])

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if ((mouseX >= tryAgainX) and (mouseX <= (tryAgainX + tryAgainImg.get_width()))) and (
                        (mouseY >= tryAgainY) and (mouseY <= (tryAgainY + tryAgainImg.get_height()))):
                    gunSound.play()
                    self.is_started = True
                    self.HP = 100
                    self.level.KILLED_ZOMBIES = 0
                    threading.Thread(target=self.spawn_zombies).start()
                if ((mouseX >= quitX) and (mouseX <= (quitX + quitImg.get_width()))) and (
                        (mouseY >= quitY) and (mouseY <= (quitY + quitImg.get_height()))):
                    gunSound.play()
                    pygame.quit()

    def move_zombies(self):
        for zombie in self.zombies:
            zombie.attack()
            if ((bulletY <= (zombie.zombieY + zombie.image.get_height())) and bulletY >= zombie.zombieY + zombie.image.get_height() - 50) and (bulletX >= zombie.zombieX and (bulletX <= zombie.zombieX + zombie.image.get_width())):
                zombie.hp -= 50
                if zombie.hp == 0:
                    del self.zombies[self.zombies.index(zombie)]
                    self.level.KILLED_ZOMBIES += 1
            if zombie.zombieY > height:
                del self.zombies[self.zombies.index(zombie)]
                self.level.HP -= 10

    def spawn_zombies(self):
        while self.is_started:
            if len(self.zombies) < 7:
                temp_zombie_x = random.randint(0, width - ZF.level.zombie.get_width())
                temp_zombie_y = 210
                self.zombies.append(Zombie(temp_zombie_x, temp_zombie_y, ZF.level.zombie))
            time.sleep(spawnSpeed)


pygame.mixer.music.play()
ZF = GameController()

while True:

    if ZF.is_started:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    gunSound.play()
                    bulletState = "shooting"
                    bulletY = height - turret.get_height()
                if e.key == pygame.K_ESCAPE:
                    ZF.is_started = False
                    ZF.state = "PAUSE"

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            turretX += 7
        if key[pygame.K_LEFT]:
            turretX -= 7

        if bulletState == "shooting" and bulletY > 250:
            shootSpeed = 50

            bulletX = turretX + ZF.level.weapon.get_width() / 2 - ZF.level.bullet.get_width() / 2
            bulletY -= shootSpeed

        elif bulletState == "shooting" and bulletY <= 250:
            bulletState = "waiting"

        screen.blit(ZF.level.bg, [0, 0])

        """ SHOOTING ACTION """
        if bulletState == "shooting":
            screen.blit(ZF.level.bullet, [bulletX, bulletY])

            fireX = turretX + turret.get_width() / 2 - fire.get_width() / 2
            fireY = height - turret.get_height() - fire.get_height()
            screen.blit(fire, [fireX, fireY])

        ZF.move_zombies()

        HPImg = font.render(str(ZF.level.HP) + "HP", 1, (255,0,0))
        screen.blit(HPImg, [0, 0])

        KILLED_ZOMBIESImg = font.render("Killed Zombies: " + str(ZF.level.KILLED_ZOMBIES), 1, (255, 0, 0))
        screen.blit(KILLED_ZOMBIESImg, [width - KILLED_ZOMBIESImg.get_width(), 0])

        screen.blit(ZF.level.wall, [wallX, wallY])
        screen.blit(ZF.level.weapon, [turretX, height-turretHeight])

        pygame.display.flip()

        if ZF.level.HP <= 0:
            ZF.is_started = False
            ZF.state = "END"

    else:

        if ZF.state == "START":
            ZF.start_menu()

        elif ZF.state == "SELECT LEVEL":
            ZF.select_level()

        elif ZF.state == "PAUSE":
            ZF.pause()

        elif ZF.state == "END":
            ZF.end_round()
