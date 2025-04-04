import pygame

from game import Game

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    #Game
    game = Game()
    game.start()

    pygame.quit()
if __name__ == "__main__":
    main()