import toml
from typing import Dict

def load_config(path: str) -> Dict:
    """从 TOML 文件加载配置。"""
    try:
        with open(path, 'r') as f:
            return toml.load(f)
    except FileNotFoundError:
        return {}