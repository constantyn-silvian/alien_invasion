import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class that reprezents an alien of the game"""

    def __init__(self, ai_game):
        """Initialize the aliens elements"""

        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        """Load the alien image and set its rect position"""
        self.image = pygame.image.load('images/alien.bmp')
        self.image = pygame.transform.scale(self.image, (self.settings.alien_width, self.settings.alien_height))
        self.rect = self.image.get_rect()

        """Start each alien near the topleft corner"""
        self.rect.x = self.settings.alien_width
        self.rect.y = self.settings.alien_height

        """Store the aliens exact horizontal position"""
        self.x = float(self.rect.x)

    def check_edges(self):
        """Check if the alien collides with the edges"""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True   

    def update(self):
        """Update the aliens position based on its direction"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x