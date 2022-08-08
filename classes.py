import sys
from math import floor

import pygame
from pathlib import Path
from pygame.locals import *

colour = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 156, 160),
    "blue": (152, 233, 235),
    "green": (203, 251, 164),
    "orange": (245, 215, 157),
    "purple": (190, 162, 250)
}

class Settings():
    def __init__(self, windowName="Game", icon="images/characters/Low/happy/happy1.png", framerate=60):
        self.monitor_ratio = pygame.display.get_desktop_sizes()[0][0] / pygame.display.get_desktop_sizes()[0][1]
        pygame.display.set_caption(windowName)
        pygame.display.set_icon(pygame.image.load(icon))
        self.framerate = framerate

class Sprite():
    def __init__(self, image, x, y, width=None, height=None):
        self.image = image
        try:
            self.screen = pygame.image.load(image)
        except:
            self.screen = pygame.Surface((1,1))
        self.ratio = self.screen.get_width()/self.screen.get_height()
        self.x = x
        self.y = y

        # animation
        self.animation = []
        self.frame = 0
        self.frameGap = 3
        self.frameCount = 0
        self.looping = True

        self.alpha = 255
        self.fading = 0
        self.name = ""

        if width != None:
            self.setWidth(width)
        if height != None:
            self.setHeight(height)

    def loadAnimation(self, file, looping=True):
        # images/characters/Low/happy
        self.looping = looping
        p = Path(file).glob('**/*')
        self.animation = [x for x in p if x.is_file()]
        self.frameCount = 0
        self.frame = 0

    def setWidth(self, width):
        self.width = width
        self.height = (width/self.ratio) * settings.monitor_ratio
        self.screen = pygame.transform.smoothscale(pygame.image.load(self.image), (calcWidth(self.width), calcHeight(self.height)))

    def setHeight(self, height):
        self.width = (height*self.ratio) / settings.monitor_ratio
        self.height = height
        self.screen = pygame.transform.smoothscale(pygame.image.load(self.image), (calcWidth(self.width), calcHeight(self.height)))

    def centerX(self):
        self.x = (1 - self.width)/2

    def centerY(self):
        self.y = (1 - self.height)/2

    def setImage(self, image):
        self.image = image
        self.screen = pygame.image.load(image)
        self.ratio = self.screen.get_width()/self.screen.get_height()

    def fade(self, amount):
        newAlpha = self.alpha + amount
        if newAlpha > 255:
            self.alpha = 255
        elif newAlpha < 0:
            self.alpha = 0
        else:
            self.alpha = newAlpha

    def update(self):
        if len(self.animation) > 0:
            self.screen = pygame.transform.smoothscale(pygame.image.load(self.animation[self.frame]), (calcWidth(self.width), calcHeight(self.height)))
        else:
            self.screen = pygame.transform.smoothscale(pygame.image.load(self.image),(calcWidth(self.width), calcHeight(self.height)))

        if self.frameCount != None:
            self.frameCount += 1

            if self.frameCount >= self.frameGap:
                self.frameCount = 0
                self.frame += 1

            if self.frame == len(self.animation):
                if self.looping == True:
                    self.frame = 0
                else:
                    self.frame -= 1
                    self.frameCount = None

        self.screen.set_alpha(self.alpha)

    def stamp(self, surface):
        surface.blit(self.screen, (calcWidth(self.x), calcHeight(self.y)))

class TextBox(Sprite):
    def __init__(self, image, x, y, text="", textSize=0.025, textMargin=0.03, lineSpacing=1.5, font="freesansbold.ttf", width=None, height=None):
        super().__init__(image, x, y, width=width, height=height)
        self.textSize = textSize
        self.textMargin = textMargin
        self.lineSpacing = lineSpacing
        self.fontName = font
        self.font = pygame.font.Font(font, int(calcHeight(textSize)))
        self.text = text
        self.textbox = Sprite("", 0, 0)

    def getLines(self):
        self.font = pygame.font.Font(self.fontName, int(calcHeight(self.textSize)))
        lines = []
        index = 0
        lastSpace = 0
        textString = self.text
        while index < len(textString):
            if textString[index] == " ":
                text = self.font.render(textString[0:index], True, colour["black"])
                if text.get_width() > calcWidth(self.width - (2*self.textMargin)):
                    lines.append(textString[0:lastSpace])
                    textString = textString[lastSpace + 1:]
                    index = 0
                    lastSpace = 0

                elif text.get_width() < calcWidth(self.width - (2*self.textMargin)):
                    lastSpace = index

            index += 1
        lines.append(textString[0:])
        return lines

    def update(self):
        size = (calcWidth(self.width-(2*self.textMargin)), calcHeight(self.height-(2*self.textMargin)))
        self.textbox.screen = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.textbox.screen = self.textbox.screen.convert_alpha()

        self.font = pygame.font.Font(self.fontName, int(calcHeight(self.textSize)))
        lines = self.getLines()
        multi = 0
        topMargin = center((len(lines)*(self.textSize*self.lineSpacing)) - (self.textSize*(self.lineSpacing-1)), self.height)
        for line in lines:
            text = self.font.render(line, True, colour["black"])
            self.textbox.screen.blit(text, (0, calcHeight(self.textSize * multi * self.lineSpacing)))
            multi += 1

        self.textbox.screen.set_alpha(self.textbox.alpha)

        self.screen = pygame.transform.smoothscale(pygame.image.load(self.image), (calcWidth(self.width), calcHeight(self.height)))
        self.screen.blit(self.textbox.screen, (calcWidth(self.textMargin), calcHeight(topMargin)))

        self.screen.set_alpha(self.alpha)

def center(item, domain):
    return (domain - item)/2

def calcHeight(fraction):
    global screen
    return screen.get_height() * fraction

def calcWidth(fraction):
    global screen
    return screen.get_width() * fraction

def windowCheck(event):
    if event.type == pygame.QUIT:
        sys.exit()

    elif event.type == VIDEORESIZE:
        width, height = event.size
        if width < size[0]:
            width = size[0]
        if height < size[1]:
            height = size[1]

        if width / height != settings.monitor_ratio:
            height = width * (1 / settings.monitor_ratio)

        screen = pygame.display.set_mode((width, height), RESIZABLE)

def updateScreen(sprites):
    screen.fill(colour["black"])

    for sprite in sprites:
        sprite.update()

    for sprite in sprites:
        sprite.stamp(screen)

pygame.init()

size = [800, 450]
screen = pygame.display.set_mode(size, RESIZABLE)
settings = Settings()
