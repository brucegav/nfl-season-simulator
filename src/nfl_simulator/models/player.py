"""
NFL Player Data Models

Contains Player class and it's related attributes to represent NFL player data
"""

from nfl_simulator.models.team import Team

class Player:
    def __init__(self, player_id: int, player_name: str, position: str, team: Team):
        self.player_id = player_id
        self.player_name = player_name
        self.position = position
        self.team = team

    def __str__(self):
        return f"{self.player_name} ({self.position}) - {self.team.name}"

    def __repr__(self):
        return f"Player(id={self.player_id}, name='{self.player_name}', pos='{self.position}', team='{self.team.name}')"

    def __eq__(self, other):
        return isinstance(other, Player) and self.player_id == other.player_id