"""
NFL League Structure Factory

Creates complete NFL league structure with all teams, divisions, and conferences
using the canonical data from constants.py
"""

from typing import List, Dict, Tuple
from nfl_simulator.models.team import Team, Division, Conference
from nfl_simulator.utils.constants import (
    TEAM_NAMES,
    AFC_EAST, AFC_NORTH, AFC_SOUTH, AFC_WEST,
    NFC_EAST, NFC_NORTH, NFC_SOUTH, NFC_WEST
)


def create_league_structure() -> Tuple[List[Conference], List[Division], List[Team]]:
    """
    Create complete NFL league structure with all teams, divisions, and conferences.

    Returns:
        Tuple of (conferences, divisions, teams) lists
    """
    # Create conferences
    afc = Conference("AFC")
    nfc = Conference("NFC")
    conferences = [afc, nfc]

    # Create divisions with conference assignments
    divisions = [
        # AFC Divisions
        Division("AFC_EAST", "AFC East", afc),
        Division("AFC_NORTH", "AFC North", afc),
        Division("AFC_SOUTH", "AFC South", afc),
        Division("AFC_WEST", "AFC West", afc),
        # NFC Divisions
        Division("NFC_EAST", "NFC East", nfc),
        Division("NFC_NORTH", "NFC North", nfc),
        Division("NFC_SOUTH", "NFC South", nfc),
        Division("NFC_WEST", "NFC West", nfc),
    ]

    # Create division lookup for easy access
    division_map = {
        "AFC_EAST": divisions[0],
        "AFC_NORTH": divisions[1],
        "AFC_SOUTH": divisions[2],
        "AFC_WEST": divisions[3],
        "NFC_EAST": divisions[4],
        "NFC_NORTH": divisions[5],
        "NFC_SOUTH": divisions[6],
        "NFC_WEST": divisions[7],
    }

    # Team assignments to divisions
    division_assignments = {
        "AFC_EAST": AFC_EAST,
        "AFC_NORTH": AFC_NORTH,
        "AFC_SOUTH": AFC_SOUTH,
        "AFC_WEST": AFC_WEST,
        "NFC_EAST": NFC_EAST,
        "NFC_NORTH": NFC_NORTH,
        "NFC_SOUTH": NFC_SOUTH,
        "NFC_WEST": NFC_WEST,
    }

    # Create all teams
    teams = []
    for division_id, team_abbrevs in division_assignments.items():
        division = division_map[division_id]
        for abbrev in team_abbrevs:
            if abbrev in TEAM_NAMES:
                full_name = TEAM_NAMES[abbrev]
                # Split team name into city and team name
                # Handle multi-word cities (Kansas City, New England, etc.)
                parts = full_name.split()
                if len(parts) >= 2:
                    # Last word is always team name, everything else is city
                    name = parts[-1]
                    city = " ".join(parts[:-1])
                else:
                    # Single word team name (unusual case)
                    city = full_name
                    name = full_name

                team = Team(abbrev, name, city, division)
                teams.append(team)
            else:
                raise ValueError(f"Team abbreviation '{abbrev}' not found in TEAM_NAMES")

    return conferences, divisions, teams


def get_team_by_abbreviation(teams: List[Team], abbrev: str) -> Team:
    """
    Find a team by its abbreviation.

    Args:
        teams: List of all teams
        abbrev: Team abbreviation (e.g., "KC", "NE")

    Returns:
        Team object

    Raises:
        ValueError: If team not found
    """
    for team in teams:
        if team.team_id == abbrev:
            return team
    raise ValueError(f"Team with abbreviation '{abbrev}' not found")


def get_division_teams(teams: List[Team], division_name: str) -> List[Team]:
    """
    Get all teams in a specific division.

    Args:
        teams: List of all teams
        division_name: Division name (e.g., "AFC East", "NFC West")

    Returns:
        List of teams in that division
    """
    return [team for team in teams if team.division.name == division_name]


def get_conference_teams(teams: List[Team], conference_name: str) -> List[Team]:
    """
    Get all teams in a specific conference.

    Args:
        teams: List of all teams
        conference_name: Conference name ("AFC" or "NFC")

    Returns:
        List of teams in that conference
    """
    return [team for team in teams if team.conference.name == conference_name]