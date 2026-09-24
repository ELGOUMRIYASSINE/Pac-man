from .Parsing.parse_config_file import ParseConfig

class MetaData:
    def __init__(self, data) -> None:
        self.data = data

    def get_height(self, level: int)-> int:
        return self.data["levels"][level]["height"]

    def get_width(self, level: int)-> int:
        return self.data["levels"][level]["width"]

    def get_lives(self):
        return self.data["player_lives"]

    def get_pacgum_points(self):
        return self.data["pacgum_points"]

    def get_supgum_points(self):
        return self.data["supergum_points"]

    def get_ghostpoint(self):
        return self.data["gost_points"]
    