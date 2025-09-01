"""
NFL Prediction data models

Represents prediction results and outcomes
"""

from typing import List, Optional, Dict, Tuple
from nfl_simulator.models.team import Team
from nfl_simulator.models.game import Game
from nfl_simulator.models.season import Season
from nfl_simulator.models.player import Player

class GamePrediction:
    """Represents game prediction results and outcomes"""
    def __init__(self, game: Game, predicted_winner: Team, predicted_score: tuple, confidence: float):
        self.game = game
        self.predicted_winner = predicted_winner
        self.predicted_score = predicted_score
        self.confidence = confidence

    def __str__(self):
        return f"Prediction: {self.predicted_winner.name} beats {self.game.away_team.name if self.game.home_team == self.predicted_winner else self.game.home_team.name} ({self.predicted_score[0]}-{self.predicted_score[1]})"

    def __repr__(self):
        return f"GamePrediction(game={self.game.game_id}, winner={self.predicted_winner.name}, confidence={self.confidence})"

    def __eq__(self, other):
        return isinstance(other, GamePrediction) and self.game == other.game

class PlayerStatPrediction:
    """Represents player game stat prediction results and outcomes"""
    def __init__(self, player: Player, game: Game, predicted_stats: dict):
        self.player = player
        self.game = game
        self.predicted_stats = predicted_stats

    def __str__(self):
        return f"{self.player.player_name} prediction: {self.predicted_stats}"

    def __repr__(self):
        return f"PlayerStatPrediction(player={self.player.player_name}, game={self.game.game_id}, stats={len(self.predicted_stats)} categories)"

    def __eq__(self, other):
        return isinstance(other, PlayerStatPrediction) and self.player == other.player and self.game == other.game

class SeasonPrediction:
    """Represents season prediction results and outcomes"""
    def __init__(self, season: Season, playoff_teams: List[Team], super_bowl_winner: Team):
        self.season = season
        self.playoff_teams = playoff_teams
        self.super_bowl_winner = super_bowl_winner

    def __str__(self):
        return f"{self.season.year} Season Prediction: {self.super_bowl_winner.name} wins Super Bowl"

    def __repr__(self):
        return f"SeasonPrediction(year={self.season.year}, playoff_teams={len(self.playoff_teams)}, sb_winner={self.super_bowl_winner.name})"

    def __eq__(self, other):
        return isinstance(other, SeasonPrediction) and self.season == other.season

