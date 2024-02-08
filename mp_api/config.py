from pydantic import BaseModel
import yaml


class Config(BaseModel):
    worldpath: str
    datapack: str
    namespace: str
    tps: int = 20


def load_config(path: str = 'config.yml') -> Config:
    with open(path, encoding='utf-8') as f:
        return Config.parse_obj(yaml.safe_load(f))