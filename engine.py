import sys
import pygame
import pathlib
from pygame.locals import *
from classes import *

background = Sprite("images/backgrounds/bridge.jpg", 0, 0, width=1)
background.centerX()

textbox = TextBox("images/UI/textbox.svg", 0, 0.75, width=0.75)
textbox.centerX()

character = Sprite("images/characters/Low/happy/happy1.png", 0.3, 0.15, height=1.5)
# HWSURFACE | DOUBLEBUF
character.loadAnimation("images/characters/Low/happy")

textbox.text = 'Hello my name is sam low. I love going to school and learning things. My favourite subject at school is math. I love to math!'

clock = pygame.time.Clock()

def dialogue(text="...", characterName=None, animation=None):
    finished = False

    if animation != None:
        character.loadAnimation("images/characters/"+characterName + "/" + animation)
    textbox.text = text

    sprites = [background]
    if characterName != None:
        sprites.append(character)
    sprites.append(textbox)

    while not finished:
        clock.tick(settings.framerate)
        for event in pygame.event.get():
            windowCheck(event)

        updateScreen(sprites)
        if True in pygame.key.get_pressed():
            finished = True

        pygame.display.flip()

if __name__ == "__main__":

    while True:
        dialogue(text="I love doing it", characterName="Low", animation="happy")
        dialogue(text="By it I mean sex", characterName="Low", animation="happy")
        dialogue(text="I love sex", characterName="Low", animation="happy")

