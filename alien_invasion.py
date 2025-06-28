import sys
import pygame

from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """A class which controls the game behaviors and resources"""

    def __init__(self):
        """Initialize the game, game resources"""
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        
        """Create an instance to store game statistics and a scoreboard"""
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        """Create the ship, bullets and aliens"""
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        """A shooting flag, when active the ship fires continously"""
        self.shooting = False
        self.last_shot_time = 0

        """Make the play button"""
        self.play_button = Button(self, "Play", self.screen.get_rect().centerx, self.screen.get_rect().centery, 200, 50, (255, 255, 255), (0, 255, 0))

        """Make the difficulty buttons"""
        self._create_difficulty_buttons()

    def run_game(self):
        """Main loop of game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update() # Update the ships position
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Watch for keyboard or mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats._save_highscore()
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_easy_button(mouse_pos)
                self._check_normal_button(mouse_pos)
                self._check_hard_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game if the play button is pressed"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            """Reset the game settings"""
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _check_easy_button(self, mouse_pos):
        """Check if the player presses this button"""
        if self.easy_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.settings.difficulty = 'easy'

    def _check_normal_button(self, mouse_pos):
        """Check if the player presses this button"""
        if self.normal_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.settings.difficulty = 'normal'

    def _check_hard_button(self, mouse_pos):
        """Check if the player presses this button"""
        if self.hard_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.settings.difficulty = 'hard'

    def _check_selected_difficulty(self):
        """Color the button selected button to green and the rest to red"""
        self._initialize_difficulty_buttons_color()

        if self.settings.difficulty == 'easy':
            self.easy_button.button_color = (0, 153, 0)
            self.easy_button._prep_msg()
        elif self.settings.difficulty == 'normal':
            self.normal_button.button_color = (0, 153, 0)
            self.normal_button._prep_msg()
        elif self.settings.difficulty == 'hard':
            self.hard_button.button_color = (0, 153, 0)
            self.hard_button._prep_msg()

    def _initialize_difficulty_buttons_color(self):
        """Initialize their button and text background color to red"""
        self.easy_button.button_color = (255, 0, 0)
        self.normal_button.button_color = (255, 0, 0)
        self.hard_button.button_color = (255, 0, 0)
        self.easy_button._prep_msg()
        self.normal_button._prep_msg()
        self.hard_button._prep_msg()

    def _check_keydown_events(self, event):
        """Check the keydown events"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.stats._save_highscore()
            sys.exit()
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self.shooting = True
        elif event.key == pygame.K_p:
            self._start_game()

    def _check_keyup_events(self, event):
        """Check the keyup events"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self.shooting = False

    def _create_difficulty_buttons(self):
        """Initialize the buttons proprieties"""
        button_width = 60
        button_height = 60
        button_color = (255, 0, 0)
        text_color = (255, 255, 255)
        font_size = 22

        """Create the easy, normal, hard buttons for difficulty"""
        self.easy_button = Button(self, "Easy", self.settings.screen_width - 50, self.settings.screen_height // 3 , button_width, button_height, text_color, button_color, font_size)
        self.normal_button = Button(self, "Normal", self.settings.screen_width - 50, self.settings.screen_height // 2 , button_width, button_height, text_color, button_color, font_size)
        self.hard_button = Button(self, "Hard", self.settings.screen_width - 50, self.settings.screen_height // 3 * 2 , button_width, button_height, text_color, button_color, font_size)

    def _start_game(self):
        """Reset the games statistics"""
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()

        """Get rid of any remaining bullets and aliens"""
        self.aliens.empty()
        self.bullets.empty()

        """Create new fleet and center ship"""
        self._create_fleet()
        self.ship.center_ship()

        """Hide the mouse cursor"""
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Creates a bullet instance and adds it to the fired bullets group"""
        if len(self.bullets) < self.settings.allowed_bullets:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        
    def _update_bullets(self):
        """Shoot bullets if the shooting flag is active with a cooldown"""
        if self.shooting:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.settings.shooting_cooldown:
                self._fire_bullet()
                self.last_shot_time = current_time

        """Updates the bullets positions and deletes the old ones"""
        self.bullets.update() # Update the bullets position

        for bullet in self.bullets.copy(): # Deletes the old bullets
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullets_alien_collision()

    def _check_bullets_alien_collision(self):
        """Check if any bullet hit any alien"""
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        """Add to the score new earned points"""
        for aliens in collision.values():
            self.stats.score += self.settings.alien_points * len(aliens)
        self.sb.prep_score()
        self.sb.check_high_score()

        """Start new level if fleet destroyed"""
        self._start_new_level()
    
    def _start_new_level(self):
        """If the fleet is destroyed start a new level"""
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            """Increase level"""
            self.stats.level += 1
            self.sb.prep_images()

    def _update_aliens(self):
        """Update the ship position and direction"""
        self._check_fleet_edges()
        self.aliens.update()
        
        """Check for alien ship collision"""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        """Look for any alien touching the bottom edge"""
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Check if the fleet touches the edges and change its direction if it is"""
        for alien in self.aliens:
            if alien.check_edges():
                self._check_fleet_direction()
                break

    def _check_fleet_direction(self):
        """Changes the direction of the fleet because it touched the edge"""
        for alien in self.aliens:
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""

        """Decrement ship left"""
        if self.stats.ship_left > 1:
            self.stats.ship_left -= 1
            self.sb.prep_ships()
            
            """Delete all the existing aliens and bullets"""
            self.aliens.empty()
            self.bullets.empty()

            """Create a new fleet and center the ship"""
            self._create_fleet()
            self.ship.center_ship()

            """Pause"""
            sleep(0.5)
        else:
            """Stop the game and show cursor"""
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """Check collision between alien and bottom border"""
        screen_rec = self.screen.get_rect()
        for alien in self.aliens:
            if alien.rect.bottom >= screen_rec.bottom:
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create a fleet of aliens"""
        
        """Find how many aliens can you fit in a row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Find the number of rows you can fit"""
        available_space_y = self.settings.screen_height - (4 * alien_height) - self.ship.rect.height
        number_rows = available_space_y // (2 * alien_height)

        """Create the rows of aliens"""
        for number_row in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, number_row)

    def _create_alien(self, alien_number, number_row):
        """Create an alien and add it to the group of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width) * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + (2 * alien_width) * number_row
        self.aliens.add(alien)

    def _update_screen(self):
        """Draw the frame each time through the loop"""
        self.screen.fill(self.settings.bgcolor) # Color of background
        self.ship.blitme() # Draw the ship

        for bullet in self.bullets:
            bullet.draw_bullet()
            
        self.aliens.draw(self.screen)

        """Draw the score"""
        self.sb.show_score()

        """Draw the play button and difficulty buttons if the game is inactive"""
        if not self.stats.game_active:
            self.play_button.draw_button()

            """Check witch difficulty is selected"""
            self._check_selected_difficulty()

            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()

        """Show the new frame"""
        pygame.display.flip()

if __name__ == '__main__':
    """Run the game"""
    ai = AlienInvasion()
    ai.run_game()