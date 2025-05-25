import json
import pathlib
from functools import lru_cache

# caminho relativo ao pacote
_CRITERIOS_PATH = pathlib.Path(__file__).parent.parent / "data" / "questionario.json"

@lru_cache(maxsize=1)
def get_criterios_base() -> dict:
    """Lê o JSON de critérios apenas 1 vez por processo."""
    with _CRITERIOS_PATH.open(encoding="utf-8") as fp:
        return json.load(fp)
