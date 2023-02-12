from pathlib import Path
from rich import print

print(['.'.join(path.parts[1:-1]+(path.stem,)) for path in Path('./src/bot/extensions').glob('*.py')])