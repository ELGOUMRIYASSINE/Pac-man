"""Access validated game configuration values."""

from typing import Any


class MetaData:
    """Provide convenient access to the settings for each game level."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Store the validated configuration mapping."""
        self.data = data

    def get_level_count(self) -> int:
        """Return the number of configured levels."""
        return len(self.data["levels"])

    def get_height(self, level: int) -> int:
        """Return the maze height for ``level``."""
        return int(self.data["levels"][level]["height"])

    def get_width(self, level: int) -> int:
        """Return the maze width for ``level``."""
        return int(self.data["levels"][level]["width"])

    def get_lives(self) -> int:
        """Return the configured number of player lives."""
        return int(self.data["player_lives"])

    def get_pacgum_points(self) -> int:
        """Return the score awarded for collecting a regular gum."""
        return int(self.data["pacgum_points"])

    def get_supgum_points(self) -> int:
        """Return the score awarded for collecting a super gum."""
        return int(self.data["supergum_points"])

    def get_ghostpoint(self) -> int:
        """Return the score awarded for eating a weakened ghost."""
        return int(self.data["gost_points"])
