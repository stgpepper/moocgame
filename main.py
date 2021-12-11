import random

import pygame
import math

# Määritellään muutamia koko ohjelman kannalta olennaisia muuttujia,
# jotka eivät muutu pelin aikana.
nayton_leveys = 1300
nayton_korkeus = 800

rajaus_alue_leveys = 100
rajaus_alue_korkeus = 100


class Peli:

    def __init__(self):
        pygame.init()

        self.peli_kaynnissa = True
        self.kello = pygame.time.Clock()
        self.aloitus_aika = pygame.time.get_ticks()

        self.pelin_leveys = 1640
        self.pelin_korkeus = 950

        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus))


        self.fontti = pygame.font.SysFont("Arial", 24)

        pygame.display.set_caption("Pakoon")

        self.vasemmalle = False
        self.ylos = False
        self.oikealle = False
        self.alas = False
        self.nuolinappaimet = (self.vasemmalle, self.ylos, self.oikealle, self.alas)
        self.tausta_suunta = random.randint(1, 8) #1-8 vasemmalta alkaen jokainen väliilmansuunta

        self.objektit = []
        self.objektit.append(Robotti())
        self.robotin_sijainti = self.objektit[0].hae_sijainti()
        self.objektit.append((Morko()))
        for i in range(10):
            self.objektit.append(Raha())
        self.objektit.append(Este())

        self.silmukka()

    def kasittele_tapahtumat(self):
        for objekti in self.objektit:
            if type(objekti) == type(Robotti()):
                self.robotin_sijainti = objekti.hae_sijainti()
            objekti.looppi(self.nuolinappaimet, self.robotin_sijainti, self.tausta_suunta)

    def silmukka(self):
        while self.peli_kaynnissa:
            self.tutki_tapahtumat()
            self.kasittele_tapahtumat()
            self.piirra_naytto()
            self.kello.tick(60)
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
            self.kello.tick(1)

    def onko_tormays(self):
        for objekti_a in self.objektit:
            for objekti_b in self.objektit:
                if objekti_a == objekti_b:
                    continue
                else:
                    #Robotin ja Mörön törmäys
                    if type(objekti_a) == Robotti and type(objekti_b) == Morko and objekti_a.hitbox.colliderect(objekti_b.hitbox):
                        self.peli_kaynnissa = False
                    #Robotin ja rahan törmäys
                    if type(objekti_a) == Robotti and type(objekti_b) == Raha and objekti_a.hitbox.colliderect(objekti_b.hitbox):
                        self.objektit.remove(objekti_b)
                        for i in self.objektit:
                            if type(i) == Morko:
                                if i.max_vauhti > 0:
                                    i.max_vauhti -= 0.5


    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():

            # Painetaan painikkeet alas
            if tapahtuma.type == pygame.KEYDOWN:

                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = True

            # painikkeiden vapautus
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False

            # Päivitetään Peliin tieto painetuista nuolinäppäimistä
            self.nuolinappaimet = (self.vasemmalle, self.ylos, self.oikealle, self.alas)



            if tapahtuma.type == pygame.QUIT:
                exit()

        self.onko_tormays()


    def liiku(self, liike_y, liike_x):
        if self.peli_ohi():
            return

    def piirra_naytto(self):
        self.naytto.fill((0, 0, 0))

        #Piirtää vaalean suorakulmion ruudulle
        pygame.draw.rect(self.naytto, (255, 255, 255), pygame.Rect(rajaus_alue_leveys, rajaus_alue_korkeus, nayton_leveys - rajaus_alue_leveys*2, nayton_korkeus - rajaus_alue_korkeus*2))
        pygame.draw.rect(self.naytto, (20, 20, 20), pygame.Rect(rajaus_alue_leveys + 1, rajaus_alue_korkeus + 1, (nayton_leveys - rajaus_alue_leveys * 2)-2, (nayton_korkeus - rajaus_alue_korkeus * 2)-2))

        #Obejktien piirto
        for objekti in self.objektit:
            if type(objekti) != Este:
                self.naytto.blit(objekti.kuva, (objekti.x, objekti.y))
            else:
                pygame.draw.rect(self.naytto, (255, 255, 255), pygame.Rect(objekti.x, objekti.y, objekti.leveys, objekti.korkeus))

        #Ajan näyttö
        textsurface = self.fontti.render("Aika: "+str((pygame.time.get_ticks() - self.aloitus_aika)/1000), False, (255,0,0))
        self.naytto.blit(textsurface, (0,nayton_korkeus-30))

        if not self.peli_kaynnissa:
            print("TRUE")
            ruudun_koko = (600, 300)
            pygame.draw.rect(self.naytto, (255, 255, 255), pygame.Rect(nayton_leveys/2 - ruudun_koko[0]/2, nayton_korkeus/2 - ruudun_koko[1]/2, ruudun_koko[0], ruudun_koko[1]))

        pygame.display.flip()

    def uusi_peli(self):
        Peli()


class Robotti:

    def __init__(self):
        self.kuva = pygame.image.load("robo.png")
        self.x = nayton_leveys / 2 - self.kuva.get_width()
        self.y = nayton_korkeus / 2 - self.kuva.get_height()
        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())
        self.nopeus = 3

    def hae_sijainti(self):
        return (self.x +self.kuva.get_width()/2, self.y +self.kuva.get_height()/2)

    def looppi(self, nuolinappaimet, robotin_sijainti, taustan_suunta):
        if self.x > rajaus_alue_leveys:
            if nuolinappaimet[0]:
                self.x -= 1 * self.nopeus
        if self.y > rajaus_alue_korkeus:
            if nuolinappaimet[1]:
                self.y -= 1 * self.nopeus
        if nayton_leveys - rajaus_alue_leveys - self.kuva.get_width() > self.x:
            if nuolinappaimet[2]:
                self.x += 1 * self.nopeus
        if nayton_korkeus - rajaus_alue_korkeus - self.kuva.get_height() > self.y:
            if nuolinappaimet[3]:
                self.y += 1 * self.nopeus
        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())


class Morko:

    def __init__(self):
        self.kuva = pygame.image.load("hirvio.png")
        self.x = 0
        self.y = 0
        self.nopeus_x = 0.0
        self.nopeus_y = 0.0
        self.kiihtyvyys = 0
        self.max_vauhti = 3 # 1.5
        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())

    def looppi(self, nuolinappaimet, robotin_sijainti, taustan_suunta):
        self.max_vauhti += 0.001
        self.kiihtyvyys = math.sqrt((self.x - robotin_sijainti[0])**2 + (self.y - robotin_sijainti[1])**2) /1500

        if robotin_sijainti[0] > self.x +20:
            self.nopeus_x += self.kiihtyvyys
        if robotin_sijainti[0] < self.x +20:
            self.nopeus_x -= self.kiihtyvyys
        if robotin_sijainti[1] > self.y +30:
            self.nopeus_y += self.kiihtyvyys
        if robotin_sijainti[1] < self.y +30:
            self.nopeus_y -= self.kiihtyvyys

        #Nopeus liian korkea
        if self.nopeus_x > self.max_vauhti:
            self.nopeus_x = self.max_vauhti
        if self.nopeus_y > self.max_vauhti:
            self.nopeus_y = self.max_vauhti

        #Nopeus liian pieni
        if self.nopeus_x < self.max_vauhti *-1:
            self.nopeus_x = self.max_vauhti *-1
        if self.nopeus_y < self.max_vauhti *-1:
            self.nopeus_y = self.max_vauhti *-1

        #Määritetään mörön sijainti
        self.x += self.nopeus_x
        self.y += self.nopeus_y

        #print(f" nopeus_x:{self.nopeus_x}     nopeus_y:{self.nopeus_y}     kiihtyvyys:{self.kiihtyvyys}")

        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())

class TaustaObjekti:

    def looppi(self, nuolinappaimet, robotin_sijainti, taustan_suunta):
        if taustan_suunta == 1:
            self.x -= self.nopeus
        if taustan_suunta == 2:
            self.x -= self.nopeus
            self.y -= self.nopeus
        if taustan_suunta == 3:
            self.y -= self.nopeus
        if taustan_suunta == 4:
            self.x += self.nopeus
            self.y -= self.nopeus
        if taustan_suunta == 5:
            self.x += self.nopeus
        if taustan_suunta == 6:
            self.x += self.nopeus
            self.y += self.nopeus
        if taustan_suunta == 7:
            self.y += self.nopeus
        if taustan_suunta == 8:
            self.y += self.nopeus
            self.x -= self.nopeus

        self.hae_hitbox


class Raha(TaustaObjekti):
    def __init__(self):
        self.kuva = pygame.image.load("kolikko.png")
        self.x = random.randint(0, nayton_leveys)
        self.y = random.randint(0, nayton_korkeus)
        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())
        self.nopeus = 1

    def hae_hitbox(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())

class Este(TaustaObjekti):  # Esteet scrollaa (liikkuu) aina samaan suuntaan.
    def __init__(self):
        self.x = random.randint(0, nayton_leveys)
        self.y = random.randint(0, nayton_korkeus)
        self.leveys = random.randint(5, nayton_leveys / 10)
        self.korkeus = random.randint(5, nayton_korkeus / 10)
        self.hitbox = pygame.Rect(self.x, self.y, self.leveys, self.korkeus)
        self.nopeus = 1

    def hae_hitbox(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.leveys, self.korkeus())

if __name__ == "__main__":
    Peli()
