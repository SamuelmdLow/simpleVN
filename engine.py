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

stage = "None"

clock = pygame.time.Clock()

def fadeAll(sprites, fadingSprites, amountOfFrames=3, fadeDir=1):

    if fadeDir == 1:
        for sprite in fadingSprites:
            sprite.alpha = 0
    else:
        for sprite in fadingSprites:
            sprite.alpha = 255

    updateScreen(sprites)
    pygame.display.flip()

    for i in range(amountOfFrames):
        clock.tick(settings.framerate)
        for event in pygame.event.get():
            windowCheck(event)

        if pygame.key.get_pressed()[K_SPACE]:
            if fadeDir == 1:
                for sprite in fadingSprites:
                    sprite.alpha = 255
            else:
                for sprite in fadingSprites:
                    sprite.alpha = 0
            break

        #print(i)
        for sprite in fadingSprites:
            sprite.fade(255/amountOfFrames*fadeDir)
            #print(sprite.alpha)

        updateScreen(sprites)
        pygame.display.flip()

    if fadeDir == 1:
        for sprite in fadingSprites:
            sprite.alpha = 255
    else:
        for sprite in fadingSprites:
            sprite.alpha = 0

def dialogue(text="...", characterName=None, animation=None):
    global stage, character, textbox, background

    finished = False

    fadingSprites = []
    if stage != "dialouge":
        fadingSprites.append(textbox)
        fadingSprites.append(textbox.textbox)
        fadingSprites.append(character)

        if characterName != None:
            character.name = characterName
        stage = "dialouge"
    else:
        if characterName != character.name and characterName != None:
            fadingSprites.append(character)

            character.name = characterName

    fadingSprites.append(textbox.textbox)

    if animation != None:
        character.loadAnimation("images/characters/"+characterName + "/" + animation)
    textbox.text = text

    sprites = [background]
    if characterName != None:
        sprites.append(character)
    sprites.append(textbox)

    fadeAll(sprites, fadingSprites)

    while not finished:
        clock.tick(settings.framerate)
        for event in pygame.event.get():
            windowCheck(event)

        if pygame.key.get_pressed()[K_SPACE]:

            #fadingSprites = [textbox.textbox]
            #fadeAll(sprites, fadingSprites, fadeDir=-1)

            finished = True

        updateScreen(sprites)

        pygame.display.flip()


if __name__ == "__main__":

    while True:
        dialogue(text="I love doing it", characterName="Low", animation="happy")
        dialogue(text="By it I mean dancing", characterName="Low", animation="happy")
        dialogue(text="I love dancing", characterName="Low", animation="happy")
        dialogue(text="Yeah me too!", characterName="Naruto", animation="happy")
