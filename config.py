import json
from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    video_folder: str
    upload_interval: int
    category: str
    privacy: str
    tags: List[str]
    starting_title: str
    starting_description: str

def load_config(config_path: str = "config.json") -> Config:
    """Loads configuration from a JSON file into a Config object."""
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return Config(
        video_folder=data.get("video_folder", "YouTube Videos"),
        upload_interval=data.get("upload_interval", 180),
        category=data.get("category", "20"),
        privacy=data.get("privacy", "public"),
        tags=data.get("tags", []),
        starting_title=data.get("starting_title", ""),
        starting_description=data.get("starting_description", "")
    )
