import json
from pathlib import Path
from os import environ

import discord as pycord
from dotenv import load_dotenv
from rich import print
import pretty_errors

class Bot(pycord.Bot):
    def __init__(self, ):
        super().__init__(
            intents = pycord.Intents.all(),
            debug_guilds = [518387456488505374]
        )
        self.lang = {}
        for filepath in Path('./src/bot/config/lang').glob('*.json'):
            with open(filepath, 'r', encoding='utf8') as file:
                self.lang[filepath.stem] = json.load(file)
        
        self.load_extensions(*('.'.join((path.parts[-2], path.stem)) for path in Path('./src/bot/extensions').glob('*.py')))
    
    async def on_ready(self):
        print('Bot is Ready')

if __name__ == '__main__':
    load_dotenv(Path('./src/bot/config/secret.env'))
    bot = Bot()
    bot.run(environ.get('TOKEN'))