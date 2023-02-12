from pathlib import Path

import discord as pycord
from discord import commands, ApplicationContext, Option
from discord.ext.commands import is_owner
import pretty_errors

cmd_config = {
    "guild_ids": [
        518387456488505374
    ]
}

class BotAdminCog(pycord.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot: pycord.Bot = bot
    
    def cog_unload(self) -> None:
        self.bot.load_extension('extensions.bot_admin')
    
    @commands.slash_command(**cmd_config)
    @is_owner()
    async def extension(self, ctx: ApplicationContext, 
                        extension_name: Option(str, choices=[i.stem for i in Path('./src/bot/extensions').glob('*.py')], default='minecraft'), 
                        action: Option(str, choices=['load', 'unload', 'reload'], default='reload')):
        getattr(self.bot, f'{action}_extension')(f'extensions.{extension_name}')
        await ctx.respond(f'Success {action} extension: {extension_name}')


def setup(bot):
    bot.add_cog(BotAdminCog(bot))