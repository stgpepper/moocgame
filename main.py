import pygame

# Määritellään muutamia koko ohjelman kannalta olennaisia muuttujia,
# jotka eivät muutu pelin aikana.
nayton_leveys = 1300
nayton_korkeus = 800

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

        self.silmukka()

    def kasittele_tapahtumat(self):
        for objekti in self.objektit:
            objekti.looppi(self.nuolinappaimet)

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.kasittele_tapahtumat()
            self.piirra_naytto()

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():

            #Painetaan painikkeet alas
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

            #painikkeiden vapautus
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False

            #Päivitetään Peliin tieto painetuista nuolinäppäimistä
            self.nuolinappaimet = (self.vasemmalle, self.ylos, self.oikealle, self.alas)

            if tapahtuma.type == pygame.QUIT:
                exit()


    def liiku(self, liike_y, liike_x):
        if self.peli_ohi():
            return




    def piirra_naytto(self):
        self.naytto.fill((0, 0, 0))

        for objekti in self.objektit:
            self.naytto.blit(objekti.kuva, (objekti.x, objekti.y))
        

        pygame.display.flip()

    def peli_ohi(self):
        pass



class Robotti:

    def __init__(self):
        self.kuva = pygame.image.load("robo.png")
        self.x = nayton_leveys / 2 - self.kuva.get_width()
        self.y = nayton_korkeus / 2 - self.kuva.get_height()
        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())
    
    def looppi(self, nuolinappaimet):
        if nuolinappaimet[0]:
            self.x -= 1
        if nuolinappaimet[1]:
            self.y -= 1
        if nuolinappaimet[2]:
            self.x += 1
        if nuolinappaimet[3]:
            self.y += 1
        self.hitbox = pygame.Rect(self.x, self.y, self.kuva.get_width(), self.kuva.get_height())



class Morko:
    pass

class Raha:
    pass

class Este: #Esteet scrollaa (liikkuu) aina samaan suuntaan. 
    pass


if __name__ == "__main__":
    Peli()
    
