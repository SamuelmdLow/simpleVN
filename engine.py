import sys
import pygame
import pathlib
from pygame.locals import *
pygame.init()

colour = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 156, 160),
    "blue": (152, 233, 235),
    "green": (203, 251, 164),
    "orange": (245, 215, 157),
    "purple": (190, 162, 250)
}

monitor_ratio = pygame.display.get_desktop_sizes()[0][0]/pygame.display.get_desktop_sizes()[0][1]

size = [450 * monitor_ratio, 450]
screen = pygame.display.set_mode(size, RESIZABLE)
pygame.display.set_caption('Game')

def textSize():
    return int(0.025*screen.get_height())

def center(item, domain):
    return (domain - item)/2

def calcHeight(fraction):
    global screen
    return screen.get_height() * fraction

def calcWidth(fraction):
    global screen
    return screen.get_width() * fraction

font = pygame.font.Font('freesansbold.ttf', textSize())
text = font.render('GeeksForGeeks', True, colour["black"])
textRect = text.get_rect()

background = pygame.image.load("images/backgrounds/bridge.jpg")
textbox = pygame.image.load("images/UI/textbox.png")
character = pygame.image.load("images/characters/Low/Low_neutral.png")
character_ratio = character.get_width()/character.get_height()
# HWSURFACE | DOUBLEBUF

textString = 'Hello my name is sam low. I love going to school and learning things. My favourite subject at school is math. I love to math!'

lines = []
index = 0
lastSpace = 0
while index < len(textString):
    if textString[index] == " ":
        text = font.render(textString[0:index], True, colour["black"])
        if text.get_width() > screen.get_width() * 0.9:
            lines.append(textString[0:lastSpace])
            textString = textString[lastSpace+1:]
            index = 0
            lastSpace = 0

        elif text.get_width() < screen.get_width() * 0.9:
            lastSpace = index

    index += 1
lines.append(textString[0:])

if __name__ == "__main__":

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == VIDEORESIZE:
                width, height = event.size
                if width < size[0]:
                    width = size[0]
                if height < size[1]:
                    height = size[1]

                if width/height != monitor_ratio:
                    height = width * (1/monitor_ratio)

                screen = pygame.display.set_mode((width, height), RESIZABLE)
                #pygame.display.flip()

        screen.fill(colour["black"])
        background = pygame.transform.smoothscale(background, screen.get_size())
        textbox = pygame.transform.smoothscale(textbox, (calcWidth(0.9), calcHeight(0.2)))
        character = pygame.transform.smoothscale(character, (calcHeight(1.5)*character_ratio, calcHeight(1.5)))
        font = pygame.font.Font('freesansbold.ttf', textSize())

        screen.blit(background, (0, 0))
        screen.blit(character, (calcWidth(0.3), calcHeight(0.15)))
        screen.blit(textbox, (center(textbox.get_width(), screen.get_width()), calcHeight(0.75)))

        multi = 0
        for line in lines:
            text = font.render(line, True, colour["black"])
            screen.blit(text, (center(textbox.get_width(), screen.get_width()) + calcWidth(0.02), (calcHeight(0.79) + (multi * textSize() * 1.01))))
            multi += 1

        pygame.display.flip()