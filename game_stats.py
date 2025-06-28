import os 
import json

class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        
        """Load the highscore from the data file"""
        self.high_score = self._load_highscore()
        
        """The game_active flag"""
        self.game_active = False

    def _save_highscore(self):
        """Save the highscore into the data folder"""
        os.makedirs(os.path.dirname(self.settings.filepath), exist_ok=True)
        with open(self.settings.filepath, 'w') as f:
            json.dump({"highscore": self.high_score}, f)

    def _load_highscore(self):
        """Loads the highscore from the data folder"""
        if os.path.exists(self.settings.filepath):
            try:
                with open(self.settings.filepath, 'r') as f:
                    data = json.load(f)
                    return data.get("highscore", 0)
            except (json.JSONDecodeError, ValueError, AttributeError):
                return 0
        else:
            return 0
            
    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        