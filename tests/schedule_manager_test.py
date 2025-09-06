#!/usr/bin/env python3
"""
Clean test script for schedule_manager.py
Focuses on the core functionality without overcomplicating
"""

import sys
import os
from pathlib import Path
import json
import csv
import tempfile

# Add the src directory to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from nfl_simulator.models.season import Season
from nfl_simulator.models.game import Game
from nfl_simulator.core.league_structure import create_league_structure
from nfl_simulator.core.schedule_manager import ScheduleManager, ScheduleLoadError


def test_basic_schedule_loading():
    """Test the most basic schedule loading functionality"""
    print("Testing basic schedule loading...")

    # Create league structure
    conferences, divisions, teams = create_league_structure()
    print(f"Created {len(teams)} teams")

    # Create season
    season = Season(
        year=2024,
        current_week=1,
        games=[],
        teams=teams,
        is_playoffs_started=False
    )
    print(f"Created season: {season}")

    # Create schedule manager
    manager = ScheduleManager(season)
    print("Created ScheduleManager")

    # Test data - simple game
    test_data = {
        "games": [
            {
                "week": 1,
                "home_team": "KC",
                "away_team": "BAL",
                "date": "2024-09-05",
                "time": "20:20"
            }
        ]
    }

    try:
        print("Loading test schedule...")
        manager.load_schedule('manual', source=test_data)

        if len(season.games) > 0:
            game = season.games[0]
            print(f"Success! Created game: {game}")
            print(f"Home team: {game.home_team.name} ({game.home_team.team_id})")
            print(f"Away team: {game.away_team.name} ({game.away_team.team_id})")
            print(f"Week: {game.week}")
            return True
        else:
            print("No games were created")
            return False

    except Exception as e:
        print(f"Failed to load schedule: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_csv_loading():
    """Test CSV loading"""
    print("\nTesting CSV loading...")

    # Create league structure
    conferences, divisions, teams = create_league_structure()
    season = Season(year=2024, current_week=1, games=[], teams=teams, is_playoffs_started=False)

    # Create CSV data
    csv_data = [
        ['week', 'home_team', 'away_team', 'date', 'time'],
        ['1', 'KC', 'BAL', '2024-09-05', '20:20'],
        ['1', 'GB', 'PHI', '2024-09-06', '20:15']
    ]

    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        csv_path = f.name
        writer = csv.writer(f)
        writer.writerows(csv_data)

    try:
        manager = ScheduleManager(season)
        manager.load_schedule('manual', source=csv_path)

        print(f"Loaded {len(season.games)} games from CSV")
        if season.games:
            print(f"First game: {season.games[0]}")
            return True
        return False

    except Exception as e:
        print(f"CSV loading failed: {e}")
        return False
    finally:
        os.unlink(csv_path)


def test_validation():
    """Test schedule validation"""
    print("\nTesting validation...")

    conferences, divisions, teams = create_league_structure()
    season = Season(year=2024, current_week=1, games=[], teams=teams, is_playoffs_started=False)

    # Add a few games manually
    kc = next(t for t in teams if t.team_id == "KC")
    bal = next(t for t in teams if t.team_id == "BAL")

    game1 = Game("BAL@KC_W1", kc, bal, 1)
    season.games.append(game1)

    manager = ScheduleManager(season)
    validation = manager.validate_schedule()

    print(f"Validation result: {validation}")
    return True


def main():
    """Run all tests"""
    print("Running Schedule Manager Tests")
    print("=" * 40)

    tests = [
        test_basic_schedule_loading,
        test_csv_loading,
        test_validation
    ]

    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
                print("PASSED")
            else:
                print("FAILED")
        except Exception as e:
            print(f"ERROR: {e}")

    print(f"\nResults: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("All tests passed! Schedule Manager is working.")
    else:
        print("Some tests failed.")


if __name__ == "__main__":
    main()