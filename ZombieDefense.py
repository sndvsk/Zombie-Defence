import pygame, random, threading, time
pygame.init()
width = 1024    #1024
height = 768    #768 or 900

screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)

background = pygame.image.load("backgroundZD.jpg")
backgroundStart = pygame.image.load("backgroundStart.jpg")

gray_background = pygame.image.load("img/gray_background.png")

gunSound = pygame.mixer.Sound('gunSound.wav')
musicBG = pygame.mixer.music.load("musicBG.mp3")

playImg = pygame.image.load("playButtonRed.png")
playX = screen.get_width() / 2 - playImg.get_width() / 2
playY = screen.get_height() / 2 + 50

font = pygame.font.SysFont("monospace", 24, bold=True, italic=False)
scoreFont = pygame.font.SysFont("monospace", 48, bold=True, italic=False)
GAMEOVERfont = pygame.font.SysFont("monospace", 72, bold=True, italic=False)

HP = 100
KILLED_ZOMBIES = 0

GAMEOVERImg = GAMEOVERfont.render("GAME OVER", 1, (255,0,0))
GAMEOVERX = screen.get_width() / 2 - GAMEOVERImg.get_width() / 2
GAMEOVERY = screen.get_height() / 2 - GAMEOVERImg.get_height() / 2 - 80

turret = pygame.image.load("turret.png")
turretHeight = turret.get_height()
turretX = background.get_width() / 2 - turret.get_width() / 2

wall = pygame.image.load("zombieWall.png")
wallX = 0
wallY = height - turret.get_height()

bullet = pygame.image.load("bullet.png")
bulletX = turretX + turret.get_width() / 2 - bullet.get_width() / 2
bulletY = height - turret.get_height()
bulletState = "waiting"

fire = pygame.image.load("fire.png")

zombieList = []
spawnSpeed = 1
zombieSpeed = 1
zombieImg = pygame.image.load("zombie.png")


class Zombie:
    def __init__(self, zombieX, zombieY, zombieImg):
        self.zombieX = zombieX
        self.zombieY = zombieY
        self.image = zombieImg
        self.hp3Image = pygame.image.load("3hp.png")
        self.hp2Image = pygame.image.load("2hp.png")
        self.hp1Image = pygame.image.load("1hp.png")
        self.hp = 150

    def attack(self):
        self.zombieY = self.zombieY + zombieSpeed
        screen.blit(self.image, [self.zombieX, self.zombieY])
        if self.hp == 150:
            screen.blit(self.hp3Image, [self.zombieX, self.zombieY - 10])
        elif self.hp == 100:
            screen.blit(self.hp2Image, [self.zombieX, self.zombieY - 10])
        elif self.hp == 50:
            screen.blit(self.hp1Image, [self.zombieX, self.zombieY - 10])


def zombieMove():
    for zombie in zombieList:
        zombie.attack()
        if ((bulletY <= (zombie.zombieY + zombieImg.get_height())) and bulletY >= zombie.zombieY + zombieImg.get_height() - 50) and (bulletX >= zombie.zombieX and (bulletX <= zombie.zombieX + zombieImg.get_width())):
            zombie.hp -= 50
            if zombie.hp == 0:
                del zombieList[zombieList.index(zombie)]
                global KILLED_ZOMBIES
                KILLED_ZOMBIES += 1
        if zombie.zombieY > height:
            del zombieList[zombieList.index(zombie)]
            global HP
            HP -= 10


def spawnZombies():
    while gameOn == True:
        if len(zombieList) < 7:
            tempZombieX = random.randint(0, width - zombieImg.get_width())
            tempZombieY = 210
            zombieList.append(Zombie(tempZombieX, tempZombieY, zombieImg))
        time.sleep(spawnSpeed)

gameOn = False

gameState = "start"

pygame.mixer.music.play()

while True:

    if gameOn:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    gunSound.play()
                    bulletState = "shooting"
                    bulletY = height - turret.get_height()
                if e.key == pygame.K_ESCAPE:
                    gameOn = False
                    gameState = "pause"
        
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            turretX += 7
            
        if key[pygame.K_LEFT]:
            turretX -= 7

        if bulletState == "shooting" and bulletY > 250:
            shootSpeed = 50

            bulletX = turretX + turret.get_width() / 2 - bullet.get_width() / 2
            bulletY -= shootSpeed

        elif bulletState == "shooting" and bulletY <= 250:
            bulletState = "waiting"

        screen.blit(background, [0, 0])
        
        """ SHOOTING ACTION """
        if bulletState == "shooting":
            screen.blit(bullet, [bulletX, bulletY])
            
            fireX = turretX + turret.get_width() / 2 - fire.get_width() / 2
            fireY = height - turret.get_height() - fire.get_height()
            screen.blit(fire, [fireX, fireY])
        
        zombieMove()

        HPImg = font.render(str(HP) + "HP", 1, (255,0,0))
        screen.blit(HPImg, [0, 0])
        
        KILLED_ZOMBIESImg = font.render("Killed Zombies: " + str(KILLED_ZOMBIES), 1, (255, 0, 0))
        screen.blit(KILLED_ZOMBIESImg, [width - KILLED_ZOMBIESImg.get_width(), 0])

        screen.blit(wall, [wallX, wallY])        
        screen.blit(turret, [turretX, height-turretHeight])

        pygame.display.flip()

    else:

        if gameState == "start":

            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]

            if ((mouseX >= playX) and (mouseX <= (playX + playImg.get_width()))) and ((mouseY >= playY) and (mouseY <= (playY + playImg.get_height()))):
                playImg = pygame.image.load("playButtonBlue.png")
            else:
                playImg = pygame.image.load("playButtonRed.png")

            screen.blit(backgroundStart, [0, 0])
            screen.blit(playImg, [playX, playY])

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if ((mouseX >= playX) and (mouseX <= (playX + playImg.get_width()))) and ((mouseY >= playY) and (mouseY <= (playY + playImg.get_height()))):
                        gunSound.play()
                        gameOn = True
                        threading.Thread(target=spawnZombies).start()

        #elif gameState == "CHOOSE LEVEL":


        elif gameState == "pause":
            screen.blit(gray_background, [0, 0])

            HPImg = font.render(str(HP) + "HP", 1, (255, 0, 0))

            KILLED_ZOMBIESImg = font.render("Killed Zombies: " + str(KILLED_ZOMBIES), 1, (255, 0, 0))

            scoreImg = scoreFont.render("Your score: " + str(KILLED_ZOMBIES), 1, (255, 0, 0))
            scoreX = screen.get_width() / 2 - scoreImg.get_width() / 2
            scoreY = GAMEOVERY + GAMEOVERImg.get_height()

            resume_img = scoreFont.render("RESUME", 1, (255, 0, 0))
            resumeX = screen.get_width() / 2 - resume_img.get_width() / 2
            resumeY = scoreY + scoreImg.get_height() + 10

            quitImg = scoreFont.render("QUIT", 1, (255, 0, 0))
            quitX = screen.get_width() / 2 - quitImg.get_width() / 2
            quitY = resumeY + resume_img.get_height() + 10

            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]

            if ((mouseX >= resumeX) and (mouseX <= (resumeX + resume_img.get_width()))) and ((mouseY >= resumeY) and (mouseY <= (resumeY + resume_img.get_height()))):
                resume_img = scoreFont.render("RESUME", 1, (0, 0, 255))
            else:
                tryAgainImg = scoreFont.render("RESUME", 1, (255, 0, 0))
            if ((mouseX >= quitX) and (mouseX <= (quitX + quitImg.get_width()))) and ((mouseY >= quitY) and (mouseY <= (quitY + quitImg.get_height()))):
                quitImg = scoreFont.render("QUIT", 1, (0, 0, 255))
            else:
                quitImg = scoreFont.render("QUIT", 1, (255, 0, 0))

            screen.blit(HPImg, [0, 0])
            screen.blit(KILLED_ZOMBIESImg, [width - KILLED_ZOMBIESImg.get_width(), 0])
            screen.blit(scoreImg, [scoreX, scoreY])
            screen.blit(resume_img, [resumeX, resumeY])
            screen.blit(quitImg, [quitX, quitY])

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        gameOn = True
                        gameState = "play"
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if ((mouseX >= resumeX) and (mouseX <= (resumeX + resume_img.get_width()))) and ((mouseY >= resumeY) and (mouseY <= (resumeY + resume_img.get_height()))):
                        gameOn = True
                        gameState = "play"
                    if ((mouseX >= quitX) and (mouseX <= (quitX + quitImg.get_width()))) and ((mouseY >= quitY) and (mouseY <= (quitY + quitImg.get_height()))):
                        pygame.quit()

            pygame.display.flip()

        elif gameState == "end":
        
            zombieList = []
            
            scoreImg = scoreFont.render("Your score: " + str(KILLED_ZOMBIES), 1, (255, 0, 0))
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

            if ((mouseX >= tryAgainX) and (mouseX <= (tryAgainX + tryAgainImg.get_width()))) and ((mouseY >= tryAgainY) and (mouseY <= (tryAgainY + tryAgainImg.get_height()))):
                tryAgainImg = scoreFont.render("TRY AGAIN", 1, (0, 0, 255))
            else:
                tryAgainImg = scoreFont.render("TRY AGAIN", 1, (255, 0, 0))

            if ((mouseX >= quitX) and (mouseX <= (quitX + quitImg.get_width()))) and ((mouseY >= quitY) and (mouseY <= (quitY + quitImg.get_height()))):
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
                    if ((mouseX >= tryAgainX) and (mouseX <= (tryAgainX + tryAgainImg.get_width()))) and ((mouseY >= tryAgainY) and (mouseY <= (tryAgainY + tryAgainImg.get_height()))):
                        gunSound.play()
                        gameOn = True
                        HP = 100
                        KILLED_ZOMBIES = 0
                        threading.Thread(target=spawnZombies).start()
                    if ((mouseX >= quitX) and (mouseX <= (quitX + quitImg.get_width()))) and ((mouseY >= quitY) and (mouseY <= (quitY + quitImg.get_height()))):
                        gunSound.play()
                        pygame.quit()

    if HP <= 0:
        gameOn = False
        gameState = "end"

pygame.quit()