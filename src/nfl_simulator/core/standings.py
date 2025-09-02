"""
NFL Standings Calculator

Calculates team standings, records, and playoff picture from game results
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from nfl_simulator.models.team import Team
from nfl_simulator.models.game import Game
from nfl_simulator.models.season import Season


@dataclass
class TeamRecord:
    """Represents a team's win-loss-tie record and standings info"""
    team: Team
    wins: int = 0
    losses: int = 0
    ties: int = 0

    @property
    def win_percentage(self) -> float:
        """Calculate winning percentage (ties count as 0.5 wins)"""
        games_played = self.wins + self.losses + self.ties
        if games_played == 0:
            return 0.0
        return (self.wins + 0.5 * self.ties) / games_played

    @property
    def games_played(self) -> int:
        """Total games played"""
        return self.wins + self.losses + self.ties

    def __str__(self) -> str:
        return f"{self.team.name}: {self.wins}-{self.losses}-{self.ties} ({self.win_percentage:.3f})"


@dataclass
class DivisionStandings:
    """Represents standings for a single division"""
    division_name: str
    teams: List[TeamRecord]

    def __str__(self) -> str:
        result = f"\n{self.division_name}:\n"
        for i, team_record in enumerate(self.teams, 1):
            result += f"  {i}. {team_record}\n"
        return result


@dataclass
class ConferenceStandings:
    """Represents standings for a conference with playoff picture"""
    conference_name: str
    division_standings: List[DivisionStandings]
    wild_card_teams: List[TeamRecord]
    playoff_teams: List[TeamRecord]  # All 7 playoff teams in seeding order

    def __str__(self) -> str:
        result = f"\n{self.conference_name} STANDINGS\n" + "="*30 + "\n"

        # Show division standings
        for div_standings in self.division_standings:
            result += str(div_standings)

        # Show wild card race
        result += "\nWild Card Race:\n"
        for i, team_record in enumerate(self.wild_card_teams, 1):
            result += f"  WC{i}. {team_record}\n"

        return result


def calculate_team_records(games: List[Game], teams: List[Team]) -> Dict[str, TeamRecord]:
    """
    Calculate win-loss records for all teams from completed games.

    Args:
        games: List of all games (only played games count)
        teams: List of all teams

    Returns:
        Dictionary mapping team_id to TeamRecord
    """
    # Initialize records for all teams
    records = {}
    for team in teams:
        records[team.team_id] = TeamRecord(team)

    # Process all played games
    for game in games:
        if game.is_played():
            home_score, away_score = game.score

            if home_score > away_score:
                # Home team wins
                records[game.home_team.team_id].wins += 1
                records[game.away_team.team_id].losses += 1
            elif away_score > home_score:
                # Away team wins
                records[game.away_team.team_id].wins += 1
                records[game.home_team.team_id].losses += 1
            else:
                # Tie game
                records[game.home_team.team_id].ties += 1
                records[game.away_team.team_id].ties += 1

    return records


def calculate_division_standings(teams: List[Team], team_records: Dict[str, TeamRecord]) -> List[DivisionStandings]:
    """
    Calculate standings within each division.

    Args:
        teams: List of all teams
        team_records: Team records dictionary

    Returns:
        List of DivisionStandings objects
    """
    # Group teams by division
    divisions = {}
    for team in teams:
        div_name = team.division.name
        if div_name not in divisions:
            divisions[div_name] = []
        divisions[div_name].append(team)

    # Create division standings
    division_standings = []
    for div_name, div_teams in divisions.items():
        # Get records for teams in this division
        div_records = [team_records[team.team_id] for team in div_teams]

        # Sort by win percentage (descending)
        # TODO: This is simplified - real NFL uses complex tiebreakers
        div_records.sort(key=lambda x: x.win_percentage, reverse=True)

        division_standings.append(DivisionStandings(div_name, div_records))

    return division_standings


def calculate_conference_standings(teams: List[Team], team_records: Dict[str, TeamRecord]) -> List[ConferenceStandings]:
    """
    Calculate conference standings with playoff picture.

    Args:
        teams: List of all teams
        team_records: Team records dictionary

    Returns:
        List of ConferenceStandings objects (AFC and NFC)
    """
    conference_standings = []

    for conf_name in ["AFC", "NFC"]:
        # Get teams in this conference
        conf_teams = [team for team in teams if team.conference.name == conf_name]

        # Calculate division standings for this conference
        div_standings = []
        division_winners = []

        # Group by division
        divisions = {}
        for team in conf_teams:
            div_name = team.division.name
            if div_name not in divisions:
                divisions[div_name] = []
            divisions[div_name].append(team)

        # Process each division
        for div_name, div_teams in divisions.items():
            div_records = [team_records[team.team_id] for team in div_teams]
            div_records.sort(key=lambda x: x.win_percentage, reverse=True)

            div_standings.append(DivisionStandings(div_name, div_records))
            division_winners.append(div_records[0])  # First place team

        # Calculate wild card teams (non-division winners)
        non_winners = []
        for team in conf_teams:
            team_record = team_records[team.team_id]
            # Check if this team is a division winner
            is_winner = any(winner.team.team_id == team.team_id for winner in division_winners)
            if not is_winner:
                non_winners.append(team_record)

        # Sort non-winners by win percentage for wild card race
        non_winners.sort(key=lambda x: x.win_percentage, reverse=True)
        wild_card_teams = non_winners[:3]  # Top 3 non-division winners

        # Create playoff teams list (4 division winners + 3 wild cards)
        # TODO: This needs proper seeding rules
        playoff_teams = division_winners + wild_card_teams
        playoff_teams.sort(key=lambda x: x.win_percentage, reverse=True)

        conference_standings.append(ConferenceStandings(
            conf_name, div_standings, wild_card_teams, playoff_teams[:7]
        ))

    return conference_standings


def calculate_standings(season: Season) -> Tuple[Dict[str, TeamRecord], List[ConferenceStandings]]:
    """
    Main function to calculate complete standings from a Season.

    Args:
        season: Season object containing games and teams

    Returns:
        Tuple of (team_records_dict, conference_standings_list)
    """
    # Calculate basic team records
    team_records = calculate_team_records(season.games, season.teams)

    # Calculate conference standings with playoff picture
    conference_standings = calculate_conference_standings(season.teams, team_records)

    return team_records, conference_standings