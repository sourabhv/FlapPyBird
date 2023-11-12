from .entities import Score

class GameResult(Score):
    def __init__(self, config) -> None:
        super().__init__(config)
        
    def get_game_score(self):
        return self.score