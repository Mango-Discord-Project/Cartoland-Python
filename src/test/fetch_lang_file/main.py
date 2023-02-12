import json
from pathlib import Path

import requests

url = 'https://raw.githubusercontent.com/AlexCai2019/Cartoland/master/lang/{lang_code}.json'

for code in ('cn', 'en', 'hk', 'ta', 'tw'):
    data = requests.get(url.format(lang_code=code)).json()
    with open(Path(f'./src/test/fetch_lang_file/result/{code}.json'), 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)