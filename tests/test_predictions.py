"""
Test script for predictions.py models
"""

from nfl_simulator.models.team import Team, Division, Conference
from nfl_simulator.models.game import Game
from nfl_simulator.models.season import Season
from nfl_simulator.models.player import Player
from nfl_simulator.models.predictions import GamePrediction, PlayerStatPrediction, SeasonPrediction

# Create test data
print("Setting up test data...")

# Create conferences and divisions
afc = Conference("AFC")
nfc = Conference("NFC")
afc_west = Division("AFCW", "AFC West", afc)
nfc_east = Division("NFCE", "NFC East", nfc)

# Create teams
chiefs = Team("KC", "Kansas City Chiefs", "Kansas City", afc_west)
raiders = Team("LV", "Las Vegas Raiders", "Las Vegas", afc_west)
eagles = Team("PHI", "Philadelphia Eagles", "Philadelphia", nfc_east)
cowboys = Team("DAL", "Dallas Cowboys", "Dallas", nfc_east)

# Create players
mahomes = Player(1, "Patrick Mahomes", "QB", chiefs)
adams = Player(2, "Davante Adams", "WR", raiders)

# Create a game
test_game = Game("KC_LV_W1", chiefs, raiders, 1)

# Create a season (minimal for testing)
all_teams = [chiefs, raiders, eagles, cowboys]
all_games = [test_game]
test_season = Season(2024, 1, all_games, all_teams, False, None)

print("Test data created successfully!\n")

# Test GamePrediction
print("Testing GamePrediction...")
game_pred = GamePrediction(test_game, chiefs, (28, 21), 0.75)
print(f"Game prediction created: {game_pred}")
print(f"Repr: {repr(game_pred)}")
print(f"Predicted winner: {game_pred.predicted_winner.name}")
print(f"Confidence: {game_pred.confidence}")
print()

# Test PlayerStatPrediction
print("Testing PlayerStatPrediction...")
mahomes_stats = {
    "passing_yards": 325,
    "passing_tds": 3,
    "interceptions": 1,
    "completions": 24,
    "attempts": 35
}
player_pred = PlayerStatPrediction(mahomes, test_game, mahomes_stats)
print(f"Player prediction created: {player_pred}")
print(f"Repr: {repr(player_pred)}")
print(f"Predicted passing yards: {player_pred.predicted_stats['passing_yards']}")
print()

# Test SeasonPrediction
print("Testing SeasonPrediction...")
playoff_teams = [chiefs, eagles, cowboys]  # Just 3 for testing
season_pred = SeasonPrediction(test_season, playoff_teams, chiefs)
print(f"Season prediction created: {season_pred}")
print(f"Repr: {repr(season_pred)}")
print(f"Number of playoff teams: {len(season_pred.playoff_teams)}")
print(f"Super Bowl winner: {season_pred.super_bowl_winner.name}")
print()

# Test equality methods
print("Testing equality methods...")
game_pred2 = GamePrediction(test_game, raiders, (21, 28), 0.60)
print(f"Same game predictions equal? {game_pred == game_pred2}")

player_pred2 = PlayerStatPrediction(mahomes, test_game, {"passing_yards": 280})
print(f"Same player/game predictions equal? {player_pred == player_pred2}")

season_pred2 = SeasonPrediction(test_season, [eagles], eagles)
print(f"Same season predictions equal? {season_pred == season_pred2}")

print("\nAll prediction tests completed successfully!")