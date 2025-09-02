"""
Test script for core/league_structure.py
"""

from nfl_simulator.core.league_structure import (
    create_league_structure,
    get_team_by_abbreviation,
    get_division_teams,
    get_conference_teams
)

print("Testing NFL League Structure Creation...")
print("=" * 50)

# Test main league creation
print("Creating complete league structure...")
conferences, divisions, teams = create_league_structure()

print(f"✅ Created {len(conferences)} conferences")
print(f"✅ Created {len(divisions)} divisions")
print(f"✅ Created {len(teams)} teams")
print()

# Test conferences
print("Testing Conferences:")
for conf in conferences:
    print(f"  - {conf.name}")
print()

# Test divisions
print("Testing Divisions:")
for div in divisions:
    print(f"  - {div.name} ({div.conference.name})")
print()

# Test some specific teams
print("Testing Sample Teams:")
sample_teams = ["KC", "NE", "DAL", "SF", "BUF"]
for abbrev in sample_teams:
    try:
        team = get_team_by_abbreviation(teams, abbrev)
        print(f"  - {abbrev}: {team.city} {team.name} - {team.division.name}, {team.conference.name}")
    except ValueError as e:
        print(f"  - ❌ {abbrev}: {e}")
print()

# Test division lookup
print("Testing Division Lookup:")
test_divisions = ["AFC East", "NFC West", "AFC North"]
for div_name in test_divisions:
    div_teams = get_division_teams(teams, div_name)
    print(f"  - {div_name}: {len(div_teams)} teams")
    for team in div_teams:
        print(f"    • {team.team_id} - {team.name}")
print()

# Test conference lookup
print("Testing Conference Lookup:")
for conf_name in ["AFC", "NFC"]:
    conf_teams = get_conference_teams(teams, conf_name)
    print(f"  - {conf_name}: {len(conf_teams)} teams")
print()

# Test team relationships
print("Testing Team Relationships:")
chiefs = get_team_by_abbreviation(teams, "KC")
print(f"Kansas City Chiefs:")
print(f"  - Team ID: {chiefs.team_id}")
print(f"  - Full Name: {chiefs.name}")
print(f"  - City: {chiefs.city}")
print(f"  - Division: {chiefs.division.name}")
print(f"  - Conference: {chiefs.conference.name}")
print()

# Verify total counts
print("Final Verification:")
print(f"  - Expected 32 teams, got: {len(teams)}")
print(f"  - Expected 8 divisions, got: {len(divisions)}")
print(f"  - Expected 2 conferences, got: {len(conferences)}")

afc_count = len(get_conference_teams(teams, "AFC"))
nfc_count = len(get_conference_teams(teams, "NFC"))
print(f"  - AFC teams: {afc_count}, NFC teams: {nfc_count}")

# Check that each division has 4 teams
print("  - Teams per division:")
for div in divisions:
    div_teams = get_division_teams(teams, div.name)
    print(f"    {div.name}: {len(div_teams)} teams")

print("\n✅ League structure test completed!")