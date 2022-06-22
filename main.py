import pygame as game
from cvfpygame import *
from time import sleep as s
from random import randint as ran
game.init()
clock = game.time.Clock()
font = game.font.SysFont("calibri", 75)
screen = game.display.set_mode((1920, 1080))


# Used to map a number key pressed to its digit
digitpressdict = {
    game.K_1: 1,
    game.K_2: 2,
    game.K_3: 3,
    game.K_4: 4,
    game.K_5: 5,
    game.K_6: 6,
    game.K_7: 7,
    game.K_8: 8,
    game.K_9: 9
}


# Each tile on the board
class Tile(game.sprite.Sprite):
    def __init__(self):
        super(Tile, self).__init__()
        self.surf = game.image.load("tile.jpg")
        self.rect = self.surf.get_rect()
        self.number = 0
        self.selected = False

    def update(self, selected):
        self.selected = selected
        if selected:
            self.surf = game.image.load("selectedtile.jpg")
        else:
            self.surf = game.image.load("tile.jpg")

# Tracking where the cursor is clicking
class CursorClick(game.sprite.Sprite):
    def __init__(self):
        super(CursorClick, self).__init__()
        self.surf = game.image.load("whitepixel.jpg")
        self.rect = self.surf.get_rect()
        self.surf.set_colorkey(white)

# Draws the sudoku board
def DrawBoard():
    for i in range(1,10):
        for j in range(1,10):
            newtile = Tile()
            alltiles.add(newtile)
            newtile.rect.topleft = (450 + i * 85,100 + j * 85)
            screen.blit(newtile.surf,newtile.rect)
            game.display.flip()

# Takes a digit and coordinates of top left and prints it
def PrintDigit(number, coords):
    coords = (list(coords)[0] + 25, coords[1])
    printvalue = font.render(str(number),True,black)
    screen.blit(printvalue,coords)


thicksep = game.image.load("ThickSeperator.jpg")
cursor = CursorClick()


alltiles = game.sprite.Group()
seltilegroup = game.sprite.Group()

screen.fill(grey)
DrawBoard()

tileselect = False
tileselecttemp = False
run = True
while run:
    cursor.rect.center = game.mouse.get_pos()
    for event in game.event.get():
        if event.type == game.QUIT:
            run = False
        elif event.type == game.KEYDOWN:
            if event.key == game.K_ESCAPE:
                run = False
            else:
                try:
                    if tileselecttemp:
                        for selectedtile in seltilegroup:
                            if selectedtile.number != 0:
                                screen.blit(selectedtile.surf, selectedtile.rect)
                            selectedtile.number = digitpressdict[event.key]
                            digcoords = selectedtile.rect.topleft
                            PrintDigit(selectedtile.number, digcoords)
                            game.display.flip()
                except KeyError:
                    if event.key == game.K_BACKSPACE:
                        for selectedtile in seltilegroup:
                            screen.blit(selectedtile.surf, selectedtile.rect)
        elif event.type == game.MOUSEBUTTONDOWN and event.button == 1:
            if game.sprite.spritecollideany(cursor,alltiles):
                tileselecttemp = False
                for tile in alltiles:
                    if game.sprite.collide_rect(cursor,tile):
                        tileselect = True
                        seltilegroup.empty()
                        tile.update(tileselect)
                        seltilegroup.add(tile)
                        tileselecttemp = True
                    else:
                        tileselect = False
                        tile.update(tileselect)
                    screen.blit(tile.surf, tile.rect)
                for tile in alltiles:
                    if tile.number != 0:
                        PrintDigit(tile.number, tile.rect.topleft)

                game.display.flip()

