"""
NFL Game Data Models

Contains Game class and related functionality for representing an NFL game
including the scores and outcomes
"""


from nfl_simulator.models.team import Team, Division, Conference

class Game:
    """Represents an NFL Game object"""
    def __init__(self, game_id: str, home_team, away_team, week: int):
        self.game_id = game_id
        self.home_team = home_team
        self.away_team = away_team
        self.week = week
        self.score = None
        self.outcome = None

    def set_result(self, home_score: int, away_score: int):
        """Set the the game result after it's been simulated"""
        self.score = (home_score, away_score)
        self.outcome = self.home_team if home_score > away_score else self.away_team

    def is_played(self) -> bool:
        """Check if the game is played"""
        return self.score is not None

    def __str__(self) -> str:
        """Display the game"""
        return f"{self.away_team} @ {self.home_team} - Week {self.week}"

    def __repr__(self):
        return f"Game(id='{self.game_id}', away={self.away_team.name}, home={self.home_team.name}, week={self.week})"

    def __eq__(self, other):
        return isinstance(other, Game) and self.game_id == other.game_id



# uncomment to test
#test_conf = Conference("Test Conference")
#test_div = Division("DIV1", "Test Division", test_conf)
#team1 = Team("HOM", "Home Team", "Home City", test_div)
#team2 = Team("AWY", "Away Team", "Away City", test_div)
#test_game = Game("GAME1", team1, team2, 1)
#print(test_game)
#print(test_game.is_played())
#test_game.set_result(21, 14)
#print(test_game.is_played())
#print(test_game.outcome)