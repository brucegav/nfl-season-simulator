"""
Schedule Manager for NFL Season Simulator

Handles loading schedules from multiple sources:
1. Manual entry (CSV/JSON files)
2. API collection (ESPN, etc.)
3. Rule-based generation following NFL scheduling rules
"""

import csv
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union
from pathlib import Path

from nfl_simulator.models.game import Game
from nfl_simulator.models.season import Season
from nfl_simulator.utils.constants import TEAM_NAMES
from nfl_simulator.core.league_structure import get_team_by_abbreviation


class ScheduleLoadError(Exception):
    """Raised when there's an error loading schedule data"""
    pass


class ScheduleManager:
    """Manages loading and creating NFL season schedules from various sources"""

    def __init__(self, season: Season):
        """Initialize with a Season object to populate with games"""
        self.season = season
        self.logger = logging.getLogger(__name__)

    def load_schedule(self, mode: str, **kwargs) -> None:
        """
        Main entry point for loading schedules

        Args:
            mode: 'manual', 'api', or 'generate'
            **kwargs: Mode-specific arguments
        """
        if mode == 'manual':
            source = kwargs.get('source')
            if not source:
                raise ScheduleLoadError("Manual mode requires 'source' parameter")
            self.load_manual_schedule(source)
        elif mode == 'api':
            api_source = kwargs.get('api_source', 'espn')
            self.load_from_api(api_source)
        elif mode == 'generate':
            year = kwargs.get('year', datetime.now().year)
            self.generate_nfl_schedule(year)
        else:
            raise ScheduleLoadError(f"Unknown mode: {mode}")

    def load_manual_schedule(self, source: Union[str, Path, dict]) -> None:
        """
        Load schedule from manual input (CSV file, JSON file, or dict)

        Args:
            source: File path (str/Path) or dictionary data
        """
        try:
            if isinstance(source, dict):
                # Direct dictionary input
                self._load_from_dict(source)
            elif isinstance(source, (str, Path)):
                source_path = Path(source)
                if source_path.suffix.lower() == '.csv':
                    self._load_from_csv(source_path)
                elif source_path.suffix.lower() == '.json':
                    self._load_from_json(source_path)
                else:
                    raise ScheduleLoadError(f"Unsupported file format: {source_path.suffix}")
            else:
                raise ScheduleLoadError(f"Invalid source type: {type(source)}")

            self.logger.info(f"Successfully loaded {len(self.season.games)} games")

        except Exception as e:
            raise ScheduleLoadError(f"Error loading manual schedule: {str(e)}")

    def _load_from_csv(self, file_path: Path) -> None:
        """Load schedule from CSV file"""
        if not file_path.exists():
            raise ScheduleLoadError(f"File not found: {file_path}")

        games_loaded = 0
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Validate required columns
            required_columns = {'week', 'home_team', 'away_team'}
            if not required_columns.issubset(reader.fieldnames):
                missing = required_columns - set(reader.fieldnames)
                raise ScheduleLoadError(f"Missing required columns: {missing}")

            for row_num, row in enumerate(reader, 2):  # Start at 2 for header
                try:
                    game = self._create_game_from_data(row)
                    self.season.games.append(game)
                    games_loaded += 1
                except Exception as e:
                    self.logger.warning(f"Skipping row {row_num}: {str(e)}")

        if games_loaded == 0:
            raise ScheduleLoadError("No valid games loaded from CSV")

    def _load_from_json(self, file_path: Path) -> None:
        """Load schedule from JSON file"""
        if not file_path.exists():
            raise ScheduleLoadError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            self._load_from_dict(data)

    def _load_from_dict(self, data: dict) -> None:
        """Load schedule from dictionary data"""
        if 'games' not in data:
            raise ScheduleLoadError("Dictionary must contain 'games' key")

        games_data = data['games']
        if not isinstance(games_data, list):
            raise ScheduleLoadError("'games' must be a list")

        print(f"Loading {len(games_data)} games from dictionary")

        games_loaded = 0
        for i, game_data in enumerate(games_data):
            print(f"Processing game {i}: {game_data}")
            try:
                game = self._create_game_from_data(game_data)
                self.season.games.append(game)  # Direct append instead of add_game()
                games_loaded += 1
                print(f"Successfully loaded game {i}")
            except Exception as e:
                print(f"Failed to load game {i}: {e}")
                import traceback
                traceback.print_exc()
                self.logger.warning(f"Skipping game {i}: {str(e)}")

        if games_loaded == 0:
            raise ScheduleLoadError("No valid games loaded from data")

    def _create_game_from_data(self, game_data: dict) -> Game:
        """
        Create a Game object from raw data dictionary

        Args:
            game_data: Dictionary with game information

        Returns:
            Game object
        """
        # Validate required fields
        required_fields = {'week', 'home_team', 'away_team'}
        missing_fields = required_fields - set(game_data.keys())
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")

        # Validate week number
        try:
            week = int(game_data['week'])
            if week < 1 or week > 22:  # Regular season (1-18) + playoffs (19-22)
                raise ValueError(f"Week must be between 1-22, got: {week}")
        except (ValueError, TypeError):
            raise ValueError(f"Invalid week number: {game_data['week']}")

        # Validate and get team objects
        home_abbr = str(game_data['home_team']).upper()
        away_abbr = str(game_data['away_team']).upper()

        if home_abbr not in TEAM_NAMES:
            raise ValueError(f"Unknown home team abbreviation: {home_abbr}")
        if away_abbr not in TEAM_NAMES:
            raise ValueError(f"Unknown away team abbreviation: {away_abbr}")
        if home_abbr == away_abbr:
            raise ValueError("Home and away team cannot be the same")

        home_team = get_team_by_abbreviation(self.season.teams,home_abbr)
        away_team = get_team_by_abbreviation(self.season.teams, away_abbr)

        if not home_team or not away_team:
            raise ValueError("Could not find team objects")

        # Parse date/time if provided (store separately since Game class doesn't have datetime)
        game_datetime = None
        if 'date' in game_data and game_data['date']:
            try:
                date_str = str(game_data['date'])
                time_str = str(game_data.get('time', '13:00'))  # Default to 1 PM

                # Handle various date formats
                datetime_str = f"{date_str} {time_str}"
                for fmt in ['%Y-%m-%d %H:%M', '%m/%d/%Y %H:%M', '%Y-%m-%d %H:%M:%S']:
                    try:
                        game_datetime = datetime.strptime(datetime_str, fmt)
                        break
                    except ValueError:
                        continue

                if not game_datetime:
                    self.logger.warning(f"Could not parse datetime: {datetime_str}")

            except Exception as e:
                self.logger.warning(f"Error parsing game datetime: {e}")

        # Generate a unique game ID
        game_id = f"{away_abbr}@{home_abbr}_W{week}"

        # Create Game object (note: your Game class doesn't store datetime)
        game = Game(
            game_id=game_id,
            home_team=home_team,
            away_team=away_team,
            week=week
        )

        # Store datetime separately if needed (could add as custom attribute)
        if game_datetime:
            game.game_datetime = game_datetime

        return game

    def load_from_api(self, api_source: str = "espn") -> None:
        """
        Load current season schedule from API source

        Args:
            api_source: API to use ('espn', 'nfl', etc.)
        """
        # TODO: Implement API loading
        raise NotImplementedError("API loading not yet implemented")

    def generate_nfl_schedule(self, year: int) -> None:
        """
        Generate a realistic NFL schedule following official rules

        Args:
            year: Season year to generate
        """
        # TODO: Implement NFL schedule generation algorithm
        raise NotImplementedError("NFL schedule generation not yet implemented")

    def validate_schedule(self) -> Dict[str, Union[bool, List[str]]]:
        """
        Validate the loaded schedule for common issues

        Returns:
            Dictionary with validation results
        """
        issues = []

        # Check total games (should be 272 for regular season: 17 games * 32 teams / 2)
        regular_season_games = [g for g in self.season.games if g.week <= 18]
        expected_games = 17 * 32 // 2  # 272 games

        if len(regular_season_games) != expected_games:
            issues.append(f"Expected {expected_games} regular season games, found {len(regular_season_games)}")

        # Check each team has 17 regular season games
        team_game_counts = {}
        for game in regular_season_games:
            for team in [game.home_team, game.away_team]:
                team_abbr = team.team_id
                team_game_counts[team_abbr] = team_game_counts.get(team_abbr, 0) + 1

        for team_abbr, count in team_game_counts.items():
            if count != 17:
                issues.append(f"Team {team_abbr} has {count} games, should have 17")

        # Check for duplicate games
        game_signatures = set()
        for game in self.season.games:
            # Create signature regardless of home/away order
            teams = tuple(sorted([game.home_team.team_id, game.away_team.team_id]))
            signature = (game.week, teams)
            if signature in game_signatures:
                issues.append(f"Duplicate game found: {teams} in week {game.week}")
            game_signatures.add(signature)

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'total_games': len(self.season.games),
            'regular_season_games': len(regular_season_games)
        }


# Convenience functions for direct usage
def load_schedule_from_csv(season: Season, csv_path: Union[str, Path]) -> ScheduleManager:
    """Convenience function to load schedule from CSV"""
    manager = ScheduleManager(season)
    manager.load_schedule('manual', source=csv_path)
    return manager


def load_schedule_from_json(season: Season, json_path: Union[str, Path]) -> ScheduleManager:
    """Convenience function to load schedule from JSON"""
    manager = ScheduleManager(season)
    manager.load_schedule('manual', source=json_path)
    return manager