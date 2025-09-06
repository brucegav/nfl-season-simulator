#!/usr/bin/env python3
"""
Minimal test to isolate the schedule manager issue
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from nfl_simulator.models.season import Season
from nfl_simulator.core.league_structure import create_league_structure, get_team_by_abbreviation

print("Creating league structure...")
conferences, divisions, teams = create_league_structure()
print(f"Created {len(teams)} teams")

print("Creating season...")
season = Season(year=2024, current_week=1, games=[], teams=teams, is_playoffs_started=False)
print(f"Season created: {season}")

print("Testing get_team_by_abbreviation manually...")
try:
    kc_team = get_team_by_abbreviation(teams, "KC")
    bal_team = get_team_by_abbreviation(teams, "BAL")
    print(f"Found KC: {kc_team}")
    print(f"Found BAL: {bal_team}")
except Exception as e:
    print(f"Error finding teams: {e}")
    sys.exit(1)

print("Creating game manually...")
from nfl_simulator.models.game import Game

try:
    game = Game(
        game_id="BAL@KC_W1",
        home_team=kc_team,
        away_team=bal_team,
        week=1
    )
    print(f"Game created: {game}")

    # Add to season manually
    season.games.append(game)
    print(f"Season now has {len(season.games)} games")

except Exception as e:
    print(f"Error creating game: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("✅ All basic functionality works!")
print("The issue is specifically in the schedule_manager.py file.")
print("Please check your actual schedule_manager.py file and make sure the get_team_by_abbreviation calls")
print("include both arguments: get_team_by_abbreviation(self.season.teams, abbreviation)")