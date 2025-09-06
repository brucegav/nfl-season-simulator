"""
NFL Data Collection Module

Handles collecting historical NFL data using nfl-data-py and storing as CSV files
in the appropriate data directories.
"""

import logging
import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

try:
    import nfl_data_py as nfl
except ImportError:
    raise ImportError("nfl-data-py is required for data collection. Install with: pip install nfl-data-py")


class NFLDataCollector:
    """Collects and stores NFL historical data"""

    def __init__(self, data_root: Path = None):
        """
        Initialize the data collector

        Args:
            data_root: Root directory for data storage (defaults to project data/ folder)
        """
        if data_root is None:

            self.data_root = Path("nfl-season-simulator/data")
        else:
            self.data_root = Path(data_root)


        for directory in [self.historical_dir, self.schedules_dir, self.rosters_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(__name__)

    def collect_game_results(self, years: List[int], save: bool = True) -> pd.DataFrame:
        """
        Collect game results and scores for specified years

        Args:
            years: List of years to collect data for
            save: Whether to save to CSV file

        Returns:
            DataFrame with game results
        """
        self.logger.info(f"Collecting game results for years: {years}")

        try:
            # Import schedules and scores
            games_df = nfl.import_schedules(years)

            if save:
                filename = f"game_results_{min(years)}-{max(years)}.csv"
                filepath = self.historical_dir / filename
                games_df.to_csv(filepath, index=False)
                self.logger.info(f"Saved game results to {filepath}")

            return games_df

        except Exception as e:
            self.logger.error(f"Error collecting game results: {e}")
            raise

    def collect_team_stats(self, years: List[int], save: bool = True) -> Dict[str, pd.DataFrame]:
        """
        Collect team-level statistics for specified years

        Args:
            years: List of years to collect data for
            save: Whether to save to CSV files

        Returns:
            Dictionary of DataFrames with different team stats
        """
        self.logger.info(f"Collecting team stats for years: {years}")

        team_stats = {}

        try:
            # Team descriptions/info
            team_desc = nfl.import_team_desc()
            team_stats['team_descriptions'] = team_desc

            # Weekly team stats (aggregated)
            weekly_stats = nfl.import_weekly_data(years)

            # Aggregate to season level
            season_stats = weekly_stats.groupby(['recent_team', 'season']).agg({
                'completions': 'sum',
                'attempts': 'sum',
                'passing_yards': 'sum',
                'passing_tds': 'sum',
                'interceptions': 'sum',
                'sacks': 'sum',
                'rushing_yards': 'sum',
                'rushing_tds': 'sum'
            }).reset_index()

            team_stats['season_stats'] = season_stats

            if save:
                for stat_type, df in team_stats.items():
                    filename = f"{stat_type}_{min(years)}-{max(years)}.csv"
                    filepath = self.historical_dir / filename
                    df.to_csv(filepath, index=False)
                    self.logger.info(f"Saved {stat_type} to {filepath}")

            return team_stats

        except Exception as e:
            self.logger.error(f"Error collecting team stats: {e}")
            raise

    def collect_player_stats(self, years: List[int], stat_type: str = 'seasonal', save: bool = True) -> pd.DataFrame:
        """
        Collect player statistics for specified years

        Args:
            years: List of years to collect data for
            stat_type: Type of stats ('seasonal' or 'weekly')
            save: Whether to save to CSV file

        Returns:
            DataFrame with player statistics
        """
        self.logger.info(f"Collecting {stat_type} player stats for years: {years}")

        try:
            if stat_type == 'seasonal':
                # Get seasonal stats for all players
                player_stats = nfl.import_seasonal_data(years)
            elif stat_type == 'weekly':
                # Get weekly stats (much larger dataset)
                player_stats = nfl.import_weekly_data(years)
            else:
                raise ValueError(f"Unknown stat_type: {stat_type}")

            if save:
                filename = f"player_stats_{stat_type}_{min(years)}-{max(years)}.csv"
                filepath = self.historical_dir / filename
                player_stats.to_csv(filepath, index=False)
                self.logger.info(f"Saved player stats to {filepath}")

            return player_stats

        except Exception as e:
            self.logger.error(f"Error collecting player stats: {e}")
            raise

    def collect_schedules(self, years: List[int], save: bool = True) -> pd.DataFrame:
        """
        Collect schedule data for specified years (for schedule generation training)

        Args:
            years: List of years to collect data for
            save: Whether to save to CSV file

        Returns:
            DataFrame with schedule information
        """
        self.logger.info(f"Collecting schedules for years: {years}")

        try:
            schedules_df = nfl.import_schedules(years)

            # Keep only relevant columns for schedule analysis
            schedule_cols = ['season', 'week', 'gameday', 'weekday', 'gametime',
                             'home_team', 'away_team', 'location']

            if all(col in schedules_df.columns for col in schedule_cols):
                schedules_clean = schedules_df[schedule_cols].copy()
            else:
                # Use available columns
                available_cols = [col for col in schedule_cols if col in schedules_df.columns]
                schedules_clean = schedules_df[available_cols].copy()

            if save:
                filename = f"schedules_{min(years)}-{max(years)}.csv"
                filepath = self.schedules_dir / filename
                schedules_clean.to_csv(filepath, index=False)
                self.logger.info(f"Saved schedules to {filepath}")

            return schedules_clean

        except Exception as e:
            self.logger.error(f"Error collecting schedules: {e}")
            raise

    def collect_rosters(self, years: List[int], save: bool = True) -> pd.DataFrame:
        """
        Collect roster data for specified years

        Args:
            years: List of years to collect data for
            save: Whether to save to CSV file

        Returns:
            DataFrame with roster information
        """
        self.logger.info(f"Collecting rosters for years: {years}")

        try:
            rosters_df = nfl.import_seasonal_rosters(years)

            if save:
                filename = f"rosters_{min(years)}-{max(years)}.csv"
                filepath = self.rosters_dir / filename
                rosters_df.to_csv(filepath, index=False)
                self.logger.info(f"Saved rosters to {filepath}")

            return rosters_df

        except Exception as e:
            self.logger.error(f"Error collecting rosters: {e}")
            raise

    def collect_all_data(self, years: List[int], include_weekly: bool = False) -> Dict[str, pd.DataFrame]:
        """
        Collect all available data types for specified years

        Args:
            years: List of years to collect data for
            include_weekly: Whether to include weekly player stats (large dataset)

        Returns:
            Dictionary of all collected DataFrames
        """
        self.logger.info(f"Starting comprehensive data collection for years: {years}")

        all_data = {}

        try:
            # Collect each data type
            all_data['games'] = self.collect_game_results(years)
            all_data['team_stats'] = self.collect_team_stats(years)
            all_data['player_stats_seasonal'] = self.collect_player_stats(years, 'seasonal')
            all_data['schedules'] = self.collect_schedules(years)
            all_data['rosters'] = self.collect_rosters(years)

            if include_weekly:
                all_data['player_stats_weekly'] = self.collect_player_stats(years, 'weekly')

            self.logger.info("Data collection completed successfully")
            return all_data

        except Exception as e:
            self.logger.error(f"Error in comprehensive data collection: {e}")
            raise

    def get_available_years(self) -> List[int]:
        """
        Get list of years available in nfl-data-py

        Returns:
            List of available years
        """
        try:
            # nfl-data-py typically has data from 1999 onwards
            current_year = datetime.now().year
            return list(range(1999, current_year + 1))
        except Exception as e:
            self.logger.error(f"Error getting available years: {e}")
            return []


# Convenience functions
def quick_collect_recent_data(years_back: int = 5, data_root: Path = None) -> Dict[str, pd.DataFrame]:
    """
    Quick function to collect recent NFL data

    Args:
        years_back: Number of years back from current year to collect
        data_root: Root directory for data storage

    Returns:
        Dictionary of collected DataFrames
    """
    current_year = datetime.now().year
    years = list(range(current_year - years_back, current_year))

    collector = NFLDataCollector(data_root)
    return collector.collect_all_data(years)


def collect_training_data(start_year: int = 2015, end_year: int = None, data_root: Path = None) -> Dict[
    str, pd.DataFrame]:
    """
    Collect data suitable for ML model training

    Args:
        start_year: Starting year for data collection
        end_year: Ending year (defaults to current year - 1)
        data_root: Root directory for data storage

    Returns:
        Dictionary of collected DataFrames
    """
    if end_year is None:
        end_year = datetime.now().year - 1

    years = list(range(start_year, end_year + 1))

    collector = NFLDataCollector(data_root)
    return collector.collect_all_data(years, include_weekly=False)  # Skip weekly for faster collection

if __name__ == "__main__":
    collector = NFLDataCollector()

    for start_year in range(2010, 2025, 3):
        end_year = min(start_year + 2, 2024)
        years = list(range(start_year, end_year + 1))
        print(f"start_year: {start_year}, end_year: {end_year}, years: {years}")  # Add this line
        print(f"Collecting {start_year} to {end_year}")
        collector.collect_all_data(years)