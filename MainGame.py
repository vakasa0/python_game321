import random
import sys
import pygame


class Plat:
    def __init__(self, x, y):
        self.x = x
        self.y = y


pygame.init()
# Tanımlar
Rmavi = (119, 224, 255)
Rsiyah = (0, 0, 0)
GENISLIK = 500
YUKSEKLIK = 700
arkaplanRengi = Rmavi
oyuncuResmi = pygame.transform.scale(pygame.image.load('karakter.png'), (80, 80))
platformResmi = pygame.transform.scale(pygame.image.load('platform.png'), (80, 10))
genel_font = pygame.font.Font('futurab.ttf', 16)
fps = 60
# EKRAN
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption('Among Platforms')
# Platformlar
platformlar = [Plat(random.randrange(0, GENISLIK - 80), random.randrange(0, YUKSEKLIK)) for i in range(10)]
# Baslangıç Değerleri
x = 200
y = 100
dy = 0.0
h = 200
ziplama = -20
puan = 0
ziplamaPuan = 0
renkPuan = 0
superZiplamaHakki = 0
superZiplamaUseTime = 0
gameOver = False

while True:
    pygame.time.Clock().tick(fps)
    olaylar = pygame.event.get()
    for olay in olaylar:
        if olay.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    ekran.fill(arkaplanRengi)

    if not gameOver:
        for platform in platformlar:
            ekran.blit(platformResmi, (platform.x, platform.y))

        # karakter zeminin en altına indiğinde game over
        if y > YUKSEKLIK:
            gameOver = True

        # oyuncunun sağa sola hareketi #
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT]:
            x -= 10
            oyuncuResmi = pygame.transform.flip(pygame.transform.scale(pygame.image.load('karakter.png'), (80, 80)),
                                                True,
                                                False)
        if tuslar[pygame.K_RIGHT]:
            x += 10
            oyuncuResmi = pygame.transform.scale(pygame.image.load('karakter.png'), (80, 80))
        if x < -40:
            x = -40
        if x > GENISLIK - 40:
            x = GENISLIK - 40

        # platformların aşağı yönde hareketi #
        if y < h:
            y = h
            for platform in platformlar:
                platform.y = platform.y - dy
                if platform.y > YUKSEKLIK:
                    platform.y = 0
                    platform.x = random.randrange(0, GENISLIK - 80)
                    puan += 1
                    ziplamaPuan += 1
                    renkPuan += 1

        # ekran reniginin her 30 puanda değişmesi
        if renkPuan == 30:
            arkaplanRengi = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
            renkPuan = 0

        # Süper Zıplama #
        if ziplamaPuan == 30:
            superZiplamaHakki += 1
            ziplamaPuan = 0

        if tuslar[pygame.K_SPACE] and superZiplamaHakki > 0:
            ziplama = -30
            superZiplamaHakki -= 1
            superZiplamaUseTime = 180

        if ziplama < -20 and superZiplamaUseTime > 0:
            superZiplamaUseTime -= 1

        if ziplama < -20 and superZiplamaUseTime == 0:
            ziplama = -20

        dy += .7
        y += dy

        # karakterin platformlar ile teması #
        for platform in platformlar:
            if (x + 60 > platform.x) and (x + 20 < platform.x + 72) and (y + 74 > platform.y) and (
                    y + 74 < platform.y + 20) and dy > 0:
                dy = ziplama

        # EKRANDA YAZACAK YAZILAR #
        yaziSkor = genel_font.render("Puan " + str(puan), 1, (0, 0, 0))
        yaziSuperZiplama = genel_font.render("Süper Zıplama Hakkı " + str(superZiplamaHakki), 1, (0, 0, 0))
        yaziSuperZiplamaTime = genel_font.render("Süper Zıplama Süresi " + str(superZiplamaUseTime), 1, (0, 0, 0))

        # YAZILARIN EKRANA YAZDIRILMASI #
        ekran.blit(yaziSkor, (GENISLIK - 10 - yaziSkor.get_width(), 10))
        ekran.blit(yaziSuperZiplama, (10, 10))
        if superZiplamaUseTime > 0:
            ekran.blit(yaziSuperZiplamaTime, (10, 30))
        ekran.blit(oyuncuResmi, (x, y))
    else:
        yaziGameOver = genel_font.render("GAME OVER", 1, (0, 0, 0))
        yaziReset = genel_font.render("yeniden oynamak için 'Boşluk' tuşuna basınız", 1, (0, 0, 0))
        yaziGameOverPuan = genel_font.render("Puanınız " + str(puan), 1, (0, 0, 0))
        ekran.blit(yaziGameOver, (170, 300))
        ekran.blit(yaziGameOverPuan, (160, 330))
        ekran.blit(yaziReset, (50, 550))
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_SPACE]:
            x = 200
            y = 100
            dy = 0.0
            h = 200
            ziplama = -20
            puan = 0
            ziplamaPuan = 0
            superZiplamaHakki = 0
            superZiplamaUseTime = 0
            gameOver = False
            platformlar = [Plat(random.randrange(0, GENISLIK - 80), random.randrange(0, YUKSEKLIK)) for i in range(10)]

    pygame.display.update()
