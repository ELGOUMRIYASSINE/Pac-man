from dataclasses import dataclass
from Parsing.parse_config_file import ParseConfig, Dict, Any

@dataclass
class MetaData:
    data: Dict[str, Any] = ParseConfig().load_json
    lives: int = data["player_lives"]
    pacgum_points:int= data["pacgum_points"]
    supergum_points:int= data["supergum_points"]
    gost_points:int= data["gost_points"]
    
    def get_height(self, level: int)-> int:
        return self.data["levels"][level]["height"]

    def get_width(self, level: int)-> int:
        return self.data["levels"][level]["width"]
