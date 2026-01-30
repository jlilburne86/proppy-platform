import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def site_url() -> str:
    cfg = ROOT / 'data' / 'site.json'
    try:
        data = json.loads(cfg.read_text(encoding='utf-8'))
        url = (data.get('site_url') or '').strip().rstrip('/')
        if url:
            return url
    except Exception:
        pass
    return 'https://jlilburne86.github.io/proppy-platform'

