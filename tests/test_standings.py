"""
Test script for core/standings.py
"""

from nfl_simulator.core.league_structure import create_league_structure, get_team_by_abbreviation
from nfl_simulator.models.game import Game
from nfl_simulator.models.season import Season
from nfl_simulator.core.standings import (
    calculate_team_records,
    calculate_division_standings,
    calculate_conference_standings,
    calculate_standings,
    TeamRecord
)

print("Testing NFL Standings Calculator...")
print("=" * 50)

# Create league structure
print("Setting up league and sample games...")
conferences, divisions, teams = create_league_structure()

# Create some sample games with results
sample_games = []

# AFC East games (Week 1)
bills = get_team_by_abbreviation(teams, "BUF")
patriots = get_team_by_abbreviation(teams, "NE")
dolphins = get_team_by_abbreviation(teams, "MIA")
jets = get_team_by_abbreviation(teams, "NYJ")

# AFC West games
chiefs = get_team_by_abbreviation(teams, "KC")
raiders = get_team_by_abbreviation(teams, "LV")
broncos = get_team_by_abbreviation(teams, "DEN")
chargers = get_team_by_abbreviation(teams, "LAC")

# NFC East games
eagles = get_team_by_abbreviation(teams, "PHI")
cowboys = get_team_by_abbreviation(teams, "DAL")
giants = get_team_by_abbreviation(teams, "NYG")
commanders = get_team_by_abbreviation(teams, "WAS")

# Create and play some games
games_data = [
    # AFC East matchups
    ("BUF_NE_W1", bills, patriots, 1, (24, 17)),  # Bills beat Patriots
    ("MIA_NYJ_W1", dolphins, jets, 1, (21, 14)),  # Dolphins beat Jets
    ("BUF_MIA_W2", bills, dolphins, 2, (31, 28)),  # Bills beat Dolphins
    ("NE_NYJ_W2", patriots, jets, 2, (20, 13)),  # Patriots beat Jets

    # AFC West matchups
    ("KC_LV_W1", chiefs, raiders, 1, (28, 21)),  # Chiefs beat Raiders
    ("DEN_LAC_W1", broncos, chargers, 1, (24, 17)),  # Broncos beat Chargers
    ("KC_DEN_W2", chiefs, broncos, 2, (35, 14)),  # Chiefs beat Broncos
    ("LV_LAC_W2", raiders, chargers, 2, (27, 20)),  # Raiders beat Chargers

    # NFC East matchups
    ("PHI_DAL_W1", eagles, cowboys, 1, (26, 17)),  # Eagles beat Cowboys
    ("NYG_WAS_W1", giants, commanders, 1, (21, 18)),  # Giants beat Commanders
    ("PHI_NYG_W2", eagles, giants, 2, (28, 14)),  # Eagles beat Giants
    ("DAL_WAS_W2", cowboys, commanders, 2, (24, 21)),  # Cowboys beat Commanders

    # Add a tie game for testing
    ("BUF_KC_W3", bills, chiefs, 3, (21, 21)),  # Bills tie Chiefs
]

# Create Game objects and set results
for game_id, home, away, week, score in games_data:
    game = Game(game_id, home, away, week)
    game.set_result(score[0], score[1])
    sample_games.append(game)

print(f"✅ Created {len(sample_games)} sample games with results")

# Create a test season
test_season = Season(2024, 3, sample_games, teams, False, None)
print("✅ Created test season")
print()

# Test individual functions
print("Testing calculate_team_records()...")
team_records = calculate_team_records(sample_games, teams)

# Show records for teams that played games
active_teams = ["BUF", "NE", "MIA", "NYJ", "KC", "LV", "DEN", "LAC", "PHI", "DAL", "NYG", "WAS"]
print("Team Records:")
for abbrev in active_teams:
    if abbrev in team_records:
        record = team_records[abbrev]
        print(f"  {record}")

print(f"\nTie game test - Bills record: {team_records['BUF']}")
print(f"Tie game test - Chiefs record: {team_records['KC']}")
print()

# Test division standings
print("Testing calculate_division_standings()...")
division_standings = calculate_division_standings(teams, team_records)

for div_standing in division_standings:
    # Only show divisions with games played
    if any(team.games_played > 0 for team in div_standing.teams):
        print(div_standing)

# Test conference standings
print("Testing calculate_conference_standings()...")
conference_standings = calculate_conference_standings(teams, team_records)

for conf_standing in conference_standings:
    # Only show if conference has games played
    has_games = any(
        any(team.games_played > 0 for team in div.teams)
        for div in conf_standing.division_standings
    )
    if has_games:
        print(conf_standing)

# Test main standings function
print("\nTesting main calculate_standings() function...")
all_records, all_conference_standings = calculate_standings(test_season)

print(f"✅ Processed {len([r for r in all_records.values() if r.games_played > 0])} teams with games")
print(f"✅ Generated standings for {len(all_conference_standings)} conferences")

# Test some specific scenarios
print("\nSpecific Tests:")
print(f"Bills win percentage (with tie): {team_records['BUF'].win_percentage:.3f}")
print(f"Chiefs win percentage (with tie): {team_records['KC'].win_percentage:.3f}")

# Verify AFC East standings order
afc_east_teams = [team_records[abbrev] for abbrev in ["BUF", "NE", "MIA", "NYJ"]]
afc_east_teams.sort(key=lambda x: x.win_percentage, reverse=True)
print("\nAFC East order by win percentage:")
for i, team in enumerate(afc_east_teams, 1):
    print(f"  {i}. {team}")

print("\n✅ All standings tests completed successfully!")