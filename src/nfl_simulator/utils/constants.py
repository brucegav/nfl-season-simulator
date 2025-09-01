"""
NFL League Constraints and Configuration

Contains canonical team data, aliases, historical names, and league structure
constants used throughout the NFL season simulator
"""


#map team abbreviations to full team names (canonical source)
TEAM_NAMES = {
    'ARI': 'Arizona Cardinals',
    'ATL': 'Atlanta Falcons',
    'BAL': 'Baltimore Ravens',
    'BUF': 'Buffalo Bills',
    'CAR': 'Carolina Panthers',
    'CHI': 'Chicago Bears',
    'CIN': 'Cincinnati Bengals',
    'CLE': 'Cleveland Browns',
    'DAL': 'Dallas Cowboys',
    'DEN': 'Denver Broncos',
    'DET': 'Detroit Lions',
    'GB': 'Green Bay Packers',
    'HOU': 'Houston Texans',
    'IND': 'Indianapolis Colts',
    'JAX': 'Jacksonville Jaguars',
    'KC': 'Kansas City Chiefs',
    'LV': 'Las Vegas Raiders',
    'LAC': 'Los Angeles Chargers',
    'LAR': 'Los Angeles Rams',
    'MIA': 'Miami Dolphins',
    'MIN': 'Minnesota Vikings',
    'NE': 'New England Patriots',
    'NO': 'New Orleans Saints',
    'NYG': 'New York Giants',
    'NYJ': 'New York Jets',
    'PHI': 'Philadelphia Eagles',
    'PIT': 'Pittsburgh Steelers',
    'SF': "San Francisco 49ers",
    'SEA': 'Seattle Seahawks',
    'TB': 'Tampa Bay Buccaneers',
    'TEN': 'Tennessee Titans',
    'WAS': 'Washington Commanders',
}

#TEAM ALIASES: variations in use
TEAM_ALIASES = {
    'ARI': 'ARI',
    'ARIZ': 'ARI',
    'ARIZONA': 'ARI',
    'ATL': 'ATL',
    'ATLANTA': 'ATL',
    'NE': 'NE',
    'NEP': 'NE',
    'PATS': 'NE',
}

#handles historical name changes
HISTORICAL_NAMES = {
    ('WAS', (1937, 2019)): 'Washington Redskins',
    ('WAS', (2020, 2021)): 'Washington Football Team',
    ('WAS', (2022, None)): 'Washington Commanders',
    # los angeles/oakland/las vegas raiders
    #baltimore/indianapolis colts
    #sandiego/los angeles chargers
    #st louis/los angeles rams
    #houston oilers/tennessee titans
}

#league rules constants
REGULAR_SEASON_WEEKS = 18
PLAYOFF_TEAMS_PER_CONFERENCE = 7
SUPER_BOWL_WEEK = 22
GAMES_PER_SEASON = 17

#tiebreak criteria
TIEBREAKER_CRITERIA = [
    'head_to_head',
    'division_record',
    'conference_record',
]


#league conference structure
AFC_TEAMS = ['BUF', 'MIA', 'NYJ', 'NE','BAL', 'PIT', 'CLE', 'CIN','BAL', 'PIT', 'CLE', 'CIN', 'BAL', 'PIT', 'CLE', 'CIN' ]
NFC_TEAMS = ['DAL', 'NYG', 'PHI', 'WAS','MIN', 'GB', 'DET', 'CHI', 'CAR', 'TB', 'ATL', 'NO', 'SEA', 'SF', 'LAR', 'ARI']

#league division structure
AFC_EAST = ['BUF', 'MIA', 'NYJ', 'NE']
AFC_NORTH = ['BAL', 'PIT', 'CLE', 'CIN']
AFC_SOUTH = ['HOU', 'JAX', 'IND', 'TEN']
AFC_WEST = ['KC', 'DEN', 'LAC', 'LV']
NFC_EAST = ['DAL', 'NYG', 'PHI', 'WAS']
NFC_NORTH = ['MIN', 'GB', 'DET', 'CHI']
NFC_SOUTH = ['CAR', 'TB', 'ATL', 'NO']
NFC_WEST = ['SEA', 'SF', 'LAR', 'ARI']


#function to align historical teams to canonical source
def get_historical_name(team, year):
    for key, name in HISTORICAL_NAMES.items():
        if key[0] == team:
            start, end = key[1]
            if end is None:  # current/ongoing
                if year >= start:
                    return name
            else:  # specific range
                if start <= year <= end:
                    return name
    else:
        return TEAM_NAMES.get(team, f"Unknown team: {team}")

