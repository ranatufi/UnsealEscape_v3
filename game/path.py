import sys
from enum import Enum
from pathlib import Path

def resource_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[1]

def asset_path(dir: Path, filename: str) -> Path:
    return dir / filename

ASSET_DIR = resource_root() / "asset"
AUDIO_DIR = ASSET_DIR / "audio"
FONT_DIR = ASSET_DIR / "font"
IMAGE_DIR = ASSET_DIR / "image"
CHARACTER_DIR = IMAGE_DIR / "character"
MAP_DIR = IMAGE_DIR / "map"

class AudioPath(Enum):
    BGM = AUDIO_DIR / "bgm"
    SE = AUDIO_DIR / "se"

class FontPath(Enum):
    GENKAI = FONT_DIR / "Genkai-Mincho-Font"
    KOWAI = FONT_DIR / "kowaiFont"
    ORADANO = FONT_DIR / "OradanoGSRR2018"
    POINTERS = FONT_DIR / "pointers"

class ImagePath(Enum):
    BACKGROUND = IMAGE_DIR / "background"
    MATERIAL = IMAGE_DIR / "material"
    UI = IMAGE_DIR / "ui"

class CharacterPath(Enum):
    RIRI = CHARACTER_DIR / "riri"
    SHO = CHARACTER_DIR / "sho"
    TEKI = CHARACTER_DIR / "teki"

class MapPath(Enum):
    COLLISION = MAP_DIR / "collision"
    VIEW = MAP_DIR / "view"