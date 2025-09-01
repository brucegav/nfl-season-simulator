"""
NFL Season data models

Represents NFL Season data and structure
"""

from typing import List, Optional
from nfl_simulator.models.team import Team
from nfl_simulator.models.game import Game

class Season:
    def __init__(self, year: int, current_week: int, games: List[Game], teams: List[Team], is_playoffs_started: bool, super_bowl_winner: Optional[Team]= None):
        self.year = year
        self.current_week = current_week
        self.games = games
        self.teams = teams
        self.is_playoffs_started = is_playoffs_started
        self.super_bowl_winner = super_bowl_winner

    def __str__(self):
        return f"{self.year} NFL Season - Week {self.current_week}"

    def __repr__(self):
        return f"Season(year={self.year}, week={self.current_week}, games={len(self.games)}, teams={len(self.teams)}, playoffs={self.is_playoffs_started})"

    def __eq__(self, other):
        return isinstance(other, Season) and self.year == other.year