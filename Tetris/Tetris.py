import pygame as pg
import random
boje = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]
class figura:
  x=0
  y=0
  figure = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 5, 6]],
        [[3,6,7,10],[1,2,6,7]],
        [[2,6,7,11],[2,3,5,6]]
    ]
  def __init__(self, x, y):
        self.x = x
        self.y = y
        self.oblik = random.randint(0, len(self.figure) - 1)
        self.boja = random.randint(1, len(boje) - 1)
        self.orjentacija = 0
  def slika(self):
        return self.figure[self.oblik][self.orjentacija]

  def okreni(self):
        self.orjentacija = (self.orjentacija + 1) % len(self.figure[self.oblik])

class Tetris:
    nivo = 2
    poeni = 0
    stanje = "start"
    pozadina = []
    visina = 0
    sirina = 0
    x = 100
    y = 60
    zoom = 20
    figura = None
    def __init__(self, visina, sirina):
        self.visina = visina
        self.sirina = sirina
        for i in range(visina):
            novi_red = []
            for j in range(sirina):
                novi_red.append(0)
            self.pozadina.append(novi_red)
    def nova_figura(self):
        self.figura = figura(3, 0)
    def sudar(self):
        sudar = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figura.slika():
                    if i + self.figura.y > self.visina - 1 or \
                            j + self.figura.x > self.sirina - 1 or \
                            j + self.figura.x < 0 or \
                            self.pozadina[i + self.figura.y][j + self.figura.x] > 0:
                        sudar = True
        return sudar
    def skloni_red(self):
        redovi = 0
        for i in range(1, self.visina):
            prazno = 0
            for j in range(self.sirina):
                if self.pozadina[i][j] == 0:
                    prazno += 1
            if prazno == 0:
                redovi += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.sirina):
                        self.pozadina[i1][j] = self.pozadina[i1 - 1][j]
        self.poeni += redovi ** 2
    def zaustavi(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figura.slika():
                    self.pozadina[i + self.figura.y][j + self.figura.x] = self.figura.boja
        self.skloni_red()
        self.nova_figura()
        if self.sudar():
            self.stanje = "kraj"


    def dole(self):
        self.figura.y += 1
        if self.sudar():
            self.figura.y -= 1
            self.zaustavi()
    def strana(self, dx):
        staro_x = self.figura.x
        self.figura.x += dx
        if self.sudar():
            self.figura.x = staro_x
    def okreni(self):
        stara_orjentacija = self.figura.orjentacija
        self.figura.okreni()
        if self.sudar():
            self.figura.orjentacija = stara_orjentacija
    def teleport(self):
        while not self.sudar():
            self.figura.y += 1
        self.figura.y -= 1
        self.zaustavi()
pg.init()


crno = (0, 0, 0)
belo = (255, 255, 255)
sivo = (127, 127, 127)

velicina = (400, 500)
ekran = pg.display.set_mode(velicina)

pg.display.set_caption("Tetris")


kraj = False
sat = pg.time.Clock()
fps = 25
igra = Tetris(20, 10)
brojac = 0

pritisnuto = False

while not kraj:
    if igra.figura is None:
        igra.nova_figura()
    brojac += 1
    if brojac > 100000:
        brojac = 0

    if brojac % (fps // igra.nivo // 2) == 0 or pritisnuto:
        if igra.stanje == "start":
            igra.dole()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                igra.okreni()
            if event.key == pg.K_DOWN:
                pritisnuto = True
            if event.key ==pg.K_LEFT:
                igra.strana(-1)
            if event.key == pg.K_RIGHT:
                igra.strana(1)
            if event.key == pg.K_SPACE:
                igra.teleport()
            if event.key == pg.K_ESCAPE:
                igra.__init__(20, 10)

    if event.type == pg.KEYUP:
            if event.key == pg.K_DOWN:
                pritisnuto = False

    ekran.fill(belo)

    for i in range(igra.visina):
        for j in range(igra.sirina):
            pg.draw.rect(ekran, sivo, [igra.x + igra.zoom * j, igra.y + igra.zoom * i, igra.zoom, igra.zoom], 1)
            if igra.pozadina[i][j] > 0:
                pg.draw.rect(ekran, boje[igra.pozadina[i][j]],
                                 [igra.x + igra.zoom * j + 1, igra.y + igra.zoom * i + 1, igra.zoom - 2, igra.zoom - 1])

    if igra.figura is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in igra.figura.slika():
                    pg.draw.rect(ekran, boje[igra.figura.boja],
                                     [igra.x + igra.zoom * (j + igra.figura.x) + 1,
                                      igra.y + igra.zoom * (i + igra.figura.y) + 1,
                                      igra.zoom - 2, igra.zoom - 2])

    font = pg.font.SysFont('Calibri', 30, True, False)
    font1 = pg.font.SysFont('Calibri', 30, True, False)
    text = font.render("Poeni: " + str(igra.poeni), True, crno)
    kraj_igre = font1.render("kraj", True, (255, 125, 125))
    kraj_igre1 = font1.render("Pritisni ESC", True, (255, 215, 0))

    ekran.blit(text, [0, 0])
    if igra.stanje == "kraj":
        ekran.blit(kraj_igre, [20, 200])
        ekran.blit(kraj_igre1, [25, 265])

    pg.display.flip()
    sat.tick(fps)
print("zavrsio")
pg.quit()