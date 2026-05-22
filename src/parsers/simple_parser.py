"""A minimal example parser that extracts key:value pairs from text.

Example input:
"""

from typing import Dict


def parse_key_values(text: str) -> Dict[str, str]:
    """Parse lines of the form `Key: Value` into a dict.

    Ignores empty lines and strips whitespace.
    """
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, val = line.split(":", 1)
        out[key.strip()] = val.strip()
    return out
