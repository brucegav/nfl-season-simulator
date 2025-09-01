"""
NFL Team Data Models

Contains Team, Division and Conference classes that represent the structure
of NFL teams and their organizational hierarchy.
"""

class Team:
    """
    Represents a NFL team with basic identifying information and relationships.
    """
    def __init__(self, team_id: str, name: str, city: str, division) -> None:
        """
        Initializes a new Team object.

        Args:
            team_id (str): The ID of the team.
            name (str): The name of the team.
            city (str): The city of the team.
            division (str): The division of the team.

        Note:
            conference is automatically derived from the division parameter.
        """
        self.team_id = team_id
        self.name = name
        self.city = city
        self.division = division
        self.conference = division.conference

    def __str__(self) -> str:
        """ Return the team's full name."""
        return self.name


    def __repr__(self) -> str:
        """ Return a detailed string representation of the Team object for debugging."""
        return f"Team('{self.team_id}', '{self.name}', '{self.city}', '{self.division}')"


    def __eq__(self, other) -> bool:
        """
        Compare two Team objects for equality based on team_id.

        Args:
            other (Team): Team object to compare to.

        Returns:
            bool: True if both objects are Team instances with the same team_id.
        """
        if not isinstance(other, Team):
            return False
        return self.team_id == other.team_id


class Division:
    """
    Represents a NFL Division with identifying information and relationships.
    """
    def __init__(self, division_id: str, name: str, conference) -> None:
        """
        Initializes a new Division object.

        Args:
           division_id (str): Division identifier
           name (str): Full division name (e.g., 'NFC West')
           conference: Conference object this division belongs to
        """
        self.division_id = division_id
        self.name = name
        self.conference = conference

    def __str__(self) -> str:
        """Return the division's full name for display purposes."""
        return self.name

    def __repr__(self) -> str:
        """Return a detailed string representation of the Division object for debugging."""
        return f"Division('{self.division_id}', '{self.name}', {self.conference})"

    def __eq__(self, other) -> bool:
        """
        Compare two Division objects for equality based on division_id.

        Args:
            other: Another Division object or any other object

        Returns:
            bool: True if both objects are Division instances with the same division_id
        """
        if not isinstance(other, Division):
            return False
        return self.division_id == other.division_id

class Conference:
    """Represents a NFL Conference with identifying information and relationships."""
    def __init__(self, name: str) -> None:
        """
        Initializes a new Conference object.
        Args:
            name (str): Conference name (AFC or NFC)
        """
        self.name = name

    def __str__(self) -> str:
        """Return the conference name for display purposes."""
        return self.name

    def __repr__(self) -> str:
        """Return a detailed string representation of the Conference object for debugging."""
        return f"Conference('{self.name}')"

    def __eq__(self, other) -> bool:
        """
        Compare two Conference objects for equality based on name.

        Args:
            other: Another Conference object or any other object

        Returns:
            bool: True if both objects are Conference instances with the same name
        """
        if not isinstance(other, Conference):
            return False
        return self.name == other.name


#uncomment to test
#test_conf = Conference("NFL Test")
#test_division = Division("DIV1", "Test Division", test_conf)
#test_team = Team("TST", "Test Team", "Test City",test_division)

#print(test_team.conference.name)
#print(test_team == test_team)