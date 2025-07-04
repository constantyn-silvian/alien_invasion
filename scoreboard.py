import pygame.font

from pygame.sprite import Group
from ship import Ship

class ScoreBoard:
    """A class to report scoring information"""

    def __init__(self, ai_game):
        """Initializing scorekeeping attributes"""
        
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        """Font settings for scoring information"""
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        """Prepare the images"""
        self.prep_images()

    def prep_images(self):
        """Prepare the initial score and others image"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_high_score(self):
        """Turn the high score into a render image"""
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        """Position the high score in the top center"""
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.top = self.score_image_rect.top
        self.high_score_image_rect.centerx = self.screen_rect.centerx

    def prep_score(self):
        """Turn the score into a render image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        """Position the score in the top right corner"""
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top += 20

    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)

        """Position the level beneath the score"""
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_image_rect.right
        self.level_image_rect.top = self.score_image_rect.bottom + 10

    def prep_ships(self):
        """Shows the number of ships left"""
        self.ships = Group()

        """Make the ships smaller and position them next to each other"""
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.image = pygame.transform.scale(ship.image, (50, 40))
            ship.rect = ship.image.get_rect()

            ship.rect.x = 10 + (ship_number * ship.rect.width)
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        """Check for a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            
    def show_score(self):
        """Draw the scores and level to the screen"""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)