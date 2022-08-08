import sys
import pygame
import pathlib
from pygame.locals import *
from classes import *

class Engine():
    def __init__(self):
        self.background = Sprite("images/backgrounds/bridge.jpg", 0, 0, width=1)
        self.background.centerX()

        self.textbox = TextBox("images/UI/textbox.svg", 0, 0.75, width=0.75)
        self.textbox.centerX()

        self.character = Sprite("images/characters/Naruto/happy/Naruto.png", 0.3, 0.15, height=1.5)

        self.stage = "None"
        self.clock = pygame.time.Clock()

    def fadeAll(self, sprites, fadingSprites, amountOfFrames=3, fadeDir=1):

        if fadeDir == 1:
            for sprite in fadingSprites:
                sprite.alpha = 0
        else:
            for sprite in fadingSprites:
                sprite.alpha = 255

        updateScreen(sprites)
        pygame.display.flip()

        for i in range(amountOfFrames):
            self.clock.tick(settings.framerate)
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

    def dialogue(self, text="...", characterName=None, animation=None):
        # stage, character, textbox, background

        finished = False

        fadingSprites = []
        if self.stage != "dialouge":
            fadingSprites.append(self.textbox)
            fadingSprites.append(self.textbox.textbox)
            fadingSprites.append(self.character)

            if characterName != None:
                self.character.name = characterName
            self.stage = "dialouge"
        else:
            if characterName != self.character.name and characterName != None:
                fadingSprites.append(self.character)

                self.character.name = characterName

        fadingSprites.append(self.textbox.textbox)

        if animation != None:
            self.character.loadAnimation("images/characters/"+characterName + "/" + animation)
        self.textbox.text = text

        sprites = [self.background]
        if characterName != None:
            sprites.append(self.character)
        sprites.append(self.textbox)

        self.fadeAll(sprites, fadingSprites)

        while not finished:
            self.clock.tick(settings.framerate)
            for event in pygame.event.get():
                windowCheck(event)

            if pygame.key.get_pressed()[K_SPACE]:

                #fadingSprites = [textbox.textbox]
                #fadeAll(sprites, fadingSprites, fadeDir=-1)

                finished = True

            updateScreen(sprites)

            pygame.display.flip()

    def playScript(self, file):
        content = open("scripts/"+file).read()
        while "\n\n" in content:
            content = content.replace("\n\n", "\n")

        while "\n " in content:
            content = content.replace("\n ", "\n")

        while " \n" in content:
            content = content.replace(" \n", "\n")

        content = content.split("\n")

        for line in content:
            if line[0] == "[":
                self.background.image = "images/backgrounds/"+line[1:-1]
                self.fadeAll([], [self.background])

            else:
                if "|" in line:
                    if line.index("|") < line.index(":"):
                        end = line.index("|")-1
                    else:
                        end = line.index("(") - 1
                else:
                    end = line.index("(") - 1

                character = line[0: end]
                animation = line[line.index("(")+1:line.index(")")]
                text = line[line.index(":")+2:]

                self.dialogue(text, characterName=character, animation=animation)

if __name__ == "__main__":
    game = Engine()
    while True:
        game.playScript("0.txt")