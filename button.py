import pygame.font

class Button:
    """Define a button"""

    def __init__(self, ai_game, msg, posx, posy, width, height, text_color, button_color,*font_size):
        """Initialize the button attributes"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        """Set the dimension and proprieties of the button"""
        self.width, self.height = width, height
        self.button_color = button_color
        self.text_color = text_color
        self.msg = msg

        """Check the size of the font and create it"""
        size = 48
        if font_size:
            size = font_size[0]

        self.font = pygame.font.SysFont(None, size)

        """Create the buttons rect and center it"""
        self.rect = pygame.rect.Rect(0, 0, self.width, self.height)
        self.rect.centerx = int(posx)
        self.rect.centery = int(posy)

        """The button message needs to be prepped once"""
        self._prep_msg()

    def _prep_msg(self):
        """Make the msg into an image and center it"""
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        """Draw black button and then draw msg"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)