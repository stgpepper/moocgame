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

    def __init__(self, peli_kaynnissa = True):
        pygame.init()

        self.peli_kaynnissa = peli_kaynnissa
        self.kello = pygame.time.Clock()
        self.aloitus_aika = pygame.time.get_ticks()
        self.trigger_aika = pygame.time.get_ticks()
        self.este_objektit = 1
        self.este_objektit_nopeus = 1
        self.raha_objektit = 5

        self.lopetus_syy = None
        self.lopetus_aika = None

        self.moron_nopeus = 0
        self.lopetus_moron_maximi = 0

        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus))
        self.fontti = pygame.font.SysFont("Arial", 26)
        pygame.display.set_caption("Pakoon")

        #Pelin ja näpäinten tilan atribuutit
        self.vasemmalle = False
        self.ylos = False
        self.oikealle = False
        self.alas = False
        self.nuolinappaimet = (self.vasemmalle, self.ylos, self.oikealle, self.alas)
        self.tausta_suunta = random.randint(1, 8) #1-8 vasemmalta alkaen jokainen väliilmansuunta

        #Alustetaan kaikki ruudulla liikkuvat hahmot
        self.objektit = []
        self.objektit.append(Robotti())
        self.robotin_sijainti = self.objektit[0].hae_sijainti()
        self.objektit.append((Morko()))

        #Pääsilmukka
        self.silmukka()

    def silmukka(self):
        while self.peli_kaynnissa:
            self.tutki_tapahtumat()
            self.kasittele_tapahtumat()
            self.piirra_naytto()
            self.poista_kaukaiset()

            #Generoidaan Esteet
            if sum(isinstance(objekti, Este) for objekti in self.objektit) < self.este_objektit:
                uusi_este = Este()
                uusi_este.nopeus = self.este_objektit_nopeus
                if self.onko_liike_alueella(uusi_este) == False:
                    self.objektit.append(uusi_este)

            #Generoidaan rahat
            if sum(isinstance(objekti, Raha) for objekti in self.objektit) < self.raha_objektit:
                uusi_raha = Raha()
                if self.onko_liike_alueella(uusi_raha) == False:
                    self.objektit.append(uusi_raha)
            self.trigger()
            self.kello.tick(60)
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
            self.kello.tick(10)

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():

            # Painetaan painikkeet alas
            if tapahtuma.type == pygame.KEYDOWN:

                if tapahtuma.key == pygame.K_RETURN:
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
        if self.peli_kaynnissa:
            self.onko_tormays()

    #Määrittelee objektien muuttuneet arvot ja ajaa kunkin objektin oman loopin
    def kasittele_tapahtumat(self):
        for objekti in self.objektit:
            if type(objekti) == type(Robotti()):
                self.robotin_sijainti = objekti.hae_sijainti()
            if type(objekti) == type(Morko()):
                self.moron_nopeus = max(abs(objekti.nopeus_x), abs(objekti.nopeus_y))
                if self.moron_nopeus > self.lopetus_moron_maximi:
                    self.lopetus_moron_maximi = self.moron_nopeus
            objekti.looppi(self.nuolinappaimet, self.robotin_sijainti, self.tausta_suunta)

    #Vaihtaa taustan suuntaa ja esteiden määrää, sekä nopeutta 10 sekuntin välein
    def trigger(self):
        if pygame.time.get_ticks() >= self.trigger_aika + 10000:
            self.tausta_suunta += 1
            if self.tausta_suunta > 8:
                self.tausta_suunta = 1
            self.trigger_aika = pygame.time.get_ticks()
            self.este_objektit += 2
            self.este_objektit_nopeus += 0.1

    def onko_liike_alueella(self, objekti):
        return objekti.hitbox.colliderect(pygame.Rect(rajaus_alue_leveys, rajaus_alue_korkeus, nayton_leveys - rajaus_alue_leveys * 2, nayton_korkeus - rajaus_alue_korkeus * 2))

    #poistaa Rahat ja esteet, jotka ovat liian kaukana ruudusta
    def poista_kaukaiset(self):
            for objekti in self.objektit:
                if type(objekti) == Este or type(objekti) == Raha:
                    if math.sqrt((objekti.x - nayton_leveys / 2)**2 + (objekti.y - nayton_korkeus / 2)**2) > nayton_leveys:
                        self.objektit.remove(objekti)

    #Tarkistaa onko törmäys ja suorittaa asianmukaisen toimenpiteen
    def onko_tormays(self):
        for objekti_a in self.objektit:
            for objekti_b in self.objektit:
                if objekti_a == objekti_b:
                    continue
                else:
                    #Robotin ja Mörön törmäys
                    if type(objekti_a) == Robotti and type(objekti_b) == Morko and objekti_a.hitbox.colliderect(objekti_b.hitbox):
                        self.peli_kaynnissa = False
                        self.lopetus_syy = "Mörköön"
                        self.lopetus_aika = pygame.time.get_ticks()
                    #Robotin ja rahan törmäys
                    if type(objekti_a) == Robotti and type(objekti_b) == Raha and objekti_a.hitbox.colliderect(objekti_b.hitbox):
                        self.objektit.remove(objekti_b)
                        for i in self.objektit:
                            if type(i) == Morko:
                                if i.max_vauhti > 0:
                                    i.max_vauhti -= 0.5
                                    i.hidastuu += 10
                    #Robotin ja Esteen törmäys
                    if type(objekti_a) == Robotti and type(objekti_b) == Este and objekti_a.hitbox.colliderect(objekti_b.hitbox):
                        self.peli_kaynnissa = False
                        self.lopetus_syy = "esteeseen"
                        self.lopetus_aika = pygame.time.get_ticks()

    def piirra_naytto(self):
        #Piirretään tausta
        self.naytto.fill((0, 0, 0))

        #Ilmoitetaan suunnanvaihdosta
        if pygame.time.get_ticks() >= self.trigger_aika + 9000 and self.peli_kaynnissa == True:
            textsurface = self.fontti.render(f"SUUNNAN VAIHTO", False, (255, 0, 0))
            self.naytto.blit(textsurface, (nayton_leveys / 2 - textsurface.get_width()/2, 20))

        #Piirtää vaalean suorakulmion ruudulle
        pygame.draw.rect(self.naytto, (255, 255, 255), pygame.Rect(rajaus_alue_leveys, rajaus_alue_korkeus, nayton_leveys - rajaus_alue_leveys*2, nayton_korkeus - rajaus_alue_korkeus*2))
        pygame.draw.rect(self.naytto, (20, 20, 20), pygame.Rect(rajaus_alue_leveys + 1, rajaus_alue_korkeus + 1, (nayton_leveys - rajaus_alue_leveys * 2)-2, (nayton_korkeus - rajaus_alue_korkeus * 2)-2))

        #Objektien piirto
        for objekti in self.objektit:
            # Piirretään mikä tahansa muu kuin este
            if type(objekti) != Este:
                #pygame.draw.rect(self.naytto, (255, 0, 0), pygame.Rect(objekti.hitbox)) #piirtää tarvittaessa hitboxin ohjelmoijaa varten
                self.naytto.blit(objekti.kuva, (objekti.x, objekti.y))
            #Piirretään este
            else:
                pygame.draw.rect(self.naytto, (0, 0, 255), pygame.Rect(objekti.x, objekti.y, objekti.leveys, objekti.korkeus))
            #Piirretään mörölle punainen merkki jos raha on otettu
            if type(objekti) == Morko and objekti.hidastuu > 0:
                pygame.draw.rect(self.naytto, (255, 0, 0), pygame.Rect(objekti.x, objekti.y, objekti.kuva.get_width(), objekti.kuva.get_height()))

        #Ajan näyttö (in game)
        textsurface = self.fontti.render(f"Aika: {(pygame.time.get_ticks() - self.aloitus_aika)/1000:.1f}", False, (255,0,0))
        self.naytto.blit(textsurface, (0,nayton_korkeus-30))

        #Mörön nopeuden näyttö (in game)
        textsurface = self.fontti.render(f"Mörön nopeus: {self.moron_nopeus:.1f} m/s", False, (255, 0, 0))
        self.naytto.blit(textsurface, (200, nayton_korkeus - 30))

        #Ohjenäkymä (still kuva)
        if not self.peli_kaynnissa:
            try:
                if self.lopetus_syy == None:
                    raise ValueError("Ei lopetussyytä. Peli on todennäköisesti juuri aloitettu")
                # Tilastot
                ruudun_koko = (600, 300)
                pygame.draw.rect(self.naytto, (20, 20, 20), pygame.Rect(rajaus_alue_leveys + 1, rajaus_alue_korkeus + 1,(nayton_leveys - rajaus_alue_leveys * 2) - 2, (nayton_korkeus - rajaus_alue_korkeus * 2) - 2))

                if self.lopetus_syy == "Mörköön":
                    self.naytto.blit(Morko().kuva, (800, 130))
                elif self.lopetus_syy == "esteeseen":
                    pygame.draw.rect(self.naytto, (0, 0, 255), pygame.Rect(800, 130, 100, 100))

                textsurface = self.fontti.render(f"Törmäsit  {self.lopetus_syy}!", False, (255, 0, 0))
                self.naytto.blit(textsurface, (nayton_leveys/2 - ruudun_koko[0]/2 + 10, rajaus_alue_korkeus + 10))

                textsurface = self.fontti.render(f"Selviydyit yhteensä {(self.aloitus_aika/1000 - self.lopetus_aika/1000) *-1 :.1f} sekuntia!", False, (255, 0, 0))
                self.naytto.blit(textsurface, (nayton_leveys / 2 - ruudun_koko[0] / 2 + 10, rajaus_alue_korkeus + 40))

                textsurface = self.fontti.render(f"Mörön maksiminopeus oli {self.lopetus_moron_maximi:.1f}", False, (255, 0, 0))
                self.naytto.blit(textsurface, (nayton_leveys / 2 - ruudun_koko[0] / 2 + 10, rajaus_alue_korkeus + 70))

            except:
                pass

            #Otsikko
            self.otsikko_fontti = pygame.font.SysFont("Arial", 100)
            textsurface = self.otsikko_fontti.render(f"PAKOON!", False, (255, 255, 0))
            self.naytto.blit(textsurface, (nayton_leveys /2 - 216, nayton_korkeus / 2-120))

            #Ohjeet
            textsurface = self.fontti.render(f"OHJEET",False, (0, 255, 0))
            self.naytto.blit(textsurface, (rajaus_alue_leveys + 10, nayton_korkeus / 2))

            textsurface = self.fontti.render(f"Tavoitteenasi on selvitä mahdollisimman kauan", False, (0, 255, 0))
            self.naytto.blit(textsurface, (rajaus_alue_leveys + 10, nayton_korkeus / 2 + 25))

            textsurface = self.fontti.render(f"Liiku nuolinäppäimillä Mörköä pakoon, mutta varo Mörkö nopeutuu jatkuvasti", False, (0, 255, 0))
            self.naytto.blit(textsurface, (rajaus_alue_leveys + 10, nayton_korkeus / 2 + 50))

            textsurface = self.fontti.render(f"Rahat hidastavat Mörköä väliaikaisesti", False, (0, 255, 0))
            self.naytto.blit(textsurface, (rajaus_alue_leveys + 10, nayton_korkeus / 2 + 75))

            textsurface = self.fontti.render(f"Varo koskemasta sinisiä esteitä", False, (0, 255, 0))
            self.naytto.blit(textsurface, (rajaus_alue_leveys + 10, nayton_korkeus / 2 + 100))

            textsurface = self.fontti.render(f"Paina Enteriä aloittaaksesi peli", False, (0, 255, 0))
            self.naytto.blit(textsurface, (rajaus_alue_leveys + 10, nayton_korkeus / 2 + 125))

            pygame.draw.rect(self.naytto, (0, 0, 0), pygame.Rect(0, nayton_korkeus - rajaus_alue_korkeus, nayton_leveys, rajaus_alue_korkeus))

        pygame.display.flip()

    def uusi_peli(self):
        Peli()

class Robotti:

    def __init__(self):
        self.kuva = pygame.image.load("robo.png")
        self.x = nayton_leveys / 2 - self.kuva.get_width()
        self.y = nayton_korkeus / 2 - self.kuva.get_height()
        self.hitbox = pygame.Rect(self.x + 6, self.y+1, self.kuva.get_width()-13, self.kuva.get_height()-2)
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
        self.hitbox = pygame.Rect(self.x + 6, self.y+1, self.kuva.get_width()-13, self.kuva.get_height()-2)

class Morko:

    def __init__(self):
        self.kuva = pygame.image.load("hirvio.png")
        self.x = 0
        self.y = 0
        self.nopeus_x = 0.0
        self.nopeus_y = 0.0
        self.kiihtyvyys = 0
        self.max_vauhti = 3 # 3
        self.hitbox = pygame.Rect(self.x+7, self.y+4, self.kuva.get_width()-10, self.kuva.get_height()-7)
        self.hidastuu = 0 #Mittaa kauanko rahan oton jälkeen näytetään punaista merkkiä

    def looppi(self, nuolinappaimet, robotin_sijainti, taustan_suunta):
        self.hidastuu -= 1
        if self.hidastuu > 10:
            self.hidastuu = 10
        if self.hidastuu < 0:
            self.hidastuu = 0

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

        #Tarkistetaan onko nopeus liian korkea
        if self.nopeus_x > self.max_vauhti:
            self.nopeus_x = self.max_vauhti
        if self.nopeus_y > self.max_vauhti:
            self.nopeus_y = self.max_vauhti

        #Tarkistetaan onko nopeus liian pieni
        if self.nopeus_x < self.max_vauhti *-1:
            self.nopeus_x = self.max_vauhti *-1
        if self.nopeus_y < self.max_vauhti *-1:
            self.nopeus_y = self.max_vauhti *-1

        #Määritetään mörön sijainti
        self.x += self.nopeus_x
        self.y += self.nopeus_y

        self.hitbox = pygame.Rect(self.x+7, self.y+4, self.kuva.get_width()-10, self.kuva.get_height()-7)

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

        self.hae_hitbox()

class Raha(TaustaObjekti):
    def __init__(self):
        self.kuva = pygame.image.load("kolikko.png")
        self.x = random.randint(0, nayton_leveys)
        self.y = random.randint(0, nayton_korkeus)
        self.hitbox = pygame.Rect(self.x+2, self.y+2, self.kuva.get_width()-4, self.kuva.get_height()-4)
        self.nopeus = 1

    def hae_hitbox(self):
        self.hitbox = pygame.Rect(self.x+2, self.y+2, self.kuva.get_width()-4, self.kuva.get_height()-4)

class Este(TaustaObjekti):  # Esteet scrollaa (liikkuu) aina samaan suuntaan.
    def __init__(self):
        self.x = random.randint(-rajaus_alue_leveys, nayton_leveys + rajaus_alue_leveys)
        self.y = random.randint(-rajaus_alue_korkeus, nayton_korkeus + rajaus_alue_korkeus)
        self.leveys = random.randint(5, nayton_leveys / 10)
        self.korkeus = random.randint(5, nayton_korkeus / 10)
        self.hitbox = pygame.Rect(self.x, self.y, self.leveys, self.korkeus)
        self.nopeus = 1

    def hae_hitbox(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.leveys, self.korkeus)

if __name__ == "__main__":
    Peli(False)
