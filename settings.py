class Settings:
    """The settings of the game"""
    def __init__(self):
        """Initialize the games static settings"""
        self.screen_width = 1100
        self.screen_height = 700
        self.bgcolor = (230, 230, 230)
        
        """Ship settings"""
        self.ship_limit = 3
        self.ship_max_speed = 5

        """Bullet settings"""
        self.bullet_width = 4 # 4
        self.bullet_height = 20 
        self.bullet_color = (255, 0, 0)
        self.allowed_bullets = 4
        self.bullet_max_speed = 30
        self.shooting_min_cooldown = 10

        """Alien settings"""
        self.alien_width = 50
        self.alien_height = 50
        self.fleet_drop_speed = 10
        self.alien_max_speed = 10
        
        """Where the data will be stored"""
        self.filepath = 'data/highscore.json'

        """The difficulty"""
        self.difficulty = 'easy'

        """How quick the games speeds up"""
        self.speedup_scale = 1.1 # 1.1

        """How quick the score goes up"""
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that can change throughout the game by dificulty"""
        if self.difficulty == 'easy':
            self.ship_speed = 1.1 # 1.1
            self.bullet_speed = 1.5 # 1.5
            self.alien_speed = 0.1 # 0.2
            self.shooting_cooldown = 350 # miliseconds

            """Scoring"""
            self.alien_points = 50

        elif self.difficulty == 'normal':
            self.ship_speed = 1.3 # 1.1
            self.bullet_speed = 1.7 # 1.5
            self.alien_speed = 0.3 # 0.2
            self.shooting_cooldown = 250 # miliseconds

            """Scoring"""
            self.alien_points = 75

        elif self.difficulty == 'hard':
            self.ship_speed = 1.5 # 1.1
            self.bullet_speed = 2 # 1.5
            self.alien_speed = 0.5 # 0.2
            self.shooting_cooldown = 150 # miliseconds

            """Scoring"""
            self.alien_points = 100

        self.fleet_direction = 1 #fleet direction: 1 for going to the right and -1 for going to the left

    def increase_speed(self):
        """Increase speed settings and alien points"""
        self.ship_speed *= self.speedup_scale 
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.shooting_cooldown /= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

        """Make sure the values dont go past their max"""
        self.ship_speed = min(self.ship_speed, self.ship_max_speed)
        self.bullet_speed = min(self.bullet_speed, self.bullet_max_speed)
        self.alien_speed = min(self.alien_speed, self.alien_max_speed)
        self.shooting_cooldown = max(self.shooting_cooldown, self.shooting_min_cooldown)