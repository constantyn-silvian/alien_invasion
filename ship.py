import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class for the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and its starting position"""

        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        """Load the ship and get it s rect"""
        self.image = pygame.image.load("images/ship.bmp")
        self.image = pygame.transform.scale(self.image, (self.screen_rect.width // 15, self.screen_rect.height // 15))
        self.rect = self.image.get_rect()

        """Start each new ship at the bottom center of the screen"""
        self.rect.midbottom = self.screen_rect.midbottom

        """A decimal value for the ship's horizontal position"""
        self.x = float(self.rect.x)

        """Movement flags"""
        self.moving_left = False
        self.moving_right = False

    def update(self):
        """Update the ships decimal position"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        """Update the ship's real x position"""
        self.rect.x = self.x
        
    def center_ship(self):
        """Center the ship"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the ship to the screen"""
        self.screen.blit(self.image, self.rect)