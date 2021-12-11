import pygame

# Määritellään muutamia koko ohjelman kannalta olennaisia muuttujia,
# jotka eivät muutu pelin aikana.
nayton_leveys = 1300
nayton_korkeus = 800

rajaus_alue_leveys = 100
rajaus_alue_korkeus = 100


class Peli:

    def __init__(self):
        pygame.init()

        self.pelin_leveys = 1640
        self.pelin_korkeus = 950

        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus))

        self.liikkeen_leveys = 500
        self.liikkeen_korkeus = 500
        self.fontti = pygame.font.SysFont("Arial", 24)

        pygame.display.set_caption("Pakoon")

        self.vasemmalle = False
        self.ylos = False
        self.oikealle = False
        self.alas = False
        self.nuolinappaimet = (self.vasemmalle, self.ylos, self.oikealle, self.alas)

        self.objektit = []
        self.objektit.append(Robotti())
        self.robotin_sijainti = self.objektit[0].hae_sijainti()
        self.objektit.append((Morko()))

        self.silmukka()

    def kasittele_tapahtumat(self):
        for objekti in self.objektit:
            if type(objekti) == type(Robotti()):
                self.robotin_sijainti = objekti.hae_sijainti()
            objekti.looppi(self.nuolinappaimet, self.robotin_sijainti)

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.kasittele_tapahtumat()
            self.piirra_naytto()

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

    def liiku(self, liike_y, liike_x):
        if self.peli_ohi():
            return

    def piirra_naytto(self):
        self.naytto.fill((0, 0, 0))

        #Piirtää vaalean suorakulmion ruudulle
        pygame.draw.rect(self.naytto, (255, 255, 255), pygame.Rect(rajaus_alue_leveys, rajaus_alue_korkeus, nayton_leveys - rajaus_alue_leveys*2, nayton_korkeus - rajaus_alue_korkeus*2))
        pygame.draw.rect(self.naytto, (20, 20, 20), pygame.Rect(rajaus_alue_leveys + 1, rajaus_alue_korkeus + 1, (nayton_leveys - rajaus_alue_leveys * 2)-2, (nayton_korkeus - rajaus_alue_korkeus * 2)-2))

        for objekti in self.objektit:
            self.naytto.blit(objekti.kuva, (objekti.x, objekti.y))

        #pygame.draw.rect(self.naytto, (255, 0, 0), pygame.Rect(self.robotin_sijainti[0], self.robotin_sijainti[1], 10, 10))
        pygame.display.flip()

    def peli_ohi(self):
        pass


class Robotti:

    def __init__(self):
        self.kuva = pygame.image.load("robo.png")
        self.x = nayton_leveys / 2 - self.kuva.get_width()
        self.y = nayton_korkeus / 2 - self.kuva.get_height()
        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())

    def hae_sijainti(self):
        return (self.x +self.kuva.get_width()/2, self.y +self.kuva.get_height()/2)

    def looppi(self, nuolinappaimet, robotin_sijainti):
        if self.x > rajaus_alue_leveys:
            if nuolinappaimet[0]:
                self.x -= 1
        if self.y > rajaus_alue_korkeus:
            if nuolinappaimet[1]:
                self.y -= 1
        if nayton_leveys - rajaus_alue_leveys - self.kuva.get_width() > self.x:
            if nuolinappaimet[2]:
                self.x += 1
        if nayton_korkeus - rajaus_alue_korkeus - self.kuva.get_height() > self.y:
            if nuolinappaimet[3]:
                self.y += 1
        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())


class Morko:

    def __init__(self):
        self.kuva = pygame.image.load("hirvio.png")
        self.x = 0
        self.y = 0
        self.nopeus_x = 0
        self.nopeus_y = 0
        self.kiihtyvyys = 0.01
        self.max_vauhti = 1.5
        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())

    def looppi(self, nuolinappaimet, robotin_sijainti):
        #määritetään mörön vauhti tiettyyn suuntaan jarrutus *4 tehokkaampi kiihdytystä
        if robotin_sijainti[0] > self.x - self.kuva.get_width():
            self.nopeus_x += self.kiihtyvyys
        if robotin_sijainti[0] < self.x - self.kuva.get_width():
            self.nopeus_x -= self.kiihtyvyys*4
        if robotin_sijainti[1] > self.y + self.kuva.get_height():
            self.nopeus_y += self.kiihtyvyys
        if robotin_sijainti[1] < self.y + self.kuva.get_height():
            self.nopeus_y -= self.kiihtyvyys*4

        if self.nopeus_x > self.max_vauhti:
            self.nopeus_x = self.max_vauhti
        if self.nopeus_y > self.max_vauhti:
            self.nopeus_y = self.max_vauhti


        #Määritetään mörön sijainti
        self.x += self.nopeus_x
        self.y += self.nopeus_y

        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())

class Raha:
    pass


class Este:  # Esteet scrollaa (liikkuu) aina samaan suuntaan.
    pass


if __name__ == "__main__":
    Peli()
