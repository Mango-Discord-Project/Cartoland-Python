import json
from pathlib import Path

import discord as pycord
from discord import commands, ApplicationContext, User, Option
from rich import print
import pretty_errors

with open(Path('./src/bot/config/lang/en.json'), encoding='utf8') as file:
    data = json.load(file)
options = {k: data[f'{k}.list'] for k in ('help', 'cmd', 'faq', 'dtp')}
options['lang'] = {
    "English": "en",
    "台灣正體": "tw",
    "台語文字": "ta",
    "粵語漢字": "hk",
    "简体中文": "cn"
}
del data

cmd_config = {
    "guild_ids": [
        518387456488505374,
        # 886936474723950603
    ]
}

class MinecraftCog(pycord.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot: pycord.Bot = bot
        self.user_lang_path = Path('./src/bot/config/user_lang.json')
        with open(self.user_lang_path) as file:
            self.user_lang = {int(k): v for k, v in json.load(file).items()}
        self.reload_user_lang_cache()
    
    def get_content(self, user_or_ctx: User | ApplicationContext, prefix: str, key: str = None, keys: tuple[str] = None) -> str | list:
        if isinstance(user_or_ctx, ApplicationContext):
            user = user_or_ctx.author
        else:
            user = user_or_ctx
        
        user_lang = self.get_or_create_user_lang(user)
        _key = f'{prefix}.{key}'
        if key:
            data = user_lang.get(_key, self.bot.lang['en'][_key])
            if isinstance(data, str) and data.startswith('&'):
                *prefix, key = data.removeprefix('&').split('.')
                return self.get_content(user, '.'.join(prefix), '.'.join(key))
            return data
        if keys:
            values = []
            for key in keys:
                _key = f'{prefix}.{key}'
                values.append(user_lang.get(_key, self.bot.lang['en'][_key]))
            return values
    
    def get_or_create_user_lang(self, user: User) -> dict:
        if user.id not in self.user_lang:
            self.user_lang[user.id] = 'en'
            self.reload_user_lang_cache()
            self.save_user_lang_config()
        return self._user_lang[user.id]
    
    def reload_user_lang_cache(self):
        self._user_lang = {k: self.bot.lang[v] for k, v in self.user_lang.items()}
    
    def save_user_lang_config(self):
        with open(self.user_lang_path, 'w') as file:
            json.dump({str(k): v for k, v in self.user_lang.items()}, file, indent=2)
    
    async def _cmd(self, ctx: ApplicationContext, command_name: str | bool = False):
        if command_name == False:
            begin, end, list = self.get_content(ctx, 'cmd', keys=('begin', 'end', 'list'))
            return await ctx.respond(f'{begin}{", ".join(list)}{end}')
        await ctx.respond(self.get_content(ctx, 'cmd.name', command_name))
    
    async def _faq(self, ctx: ApplicationContext, question: str | bool = False):
        if question == False:
            begin, end, list = self.get_content(ctx, 'faq', keys=('begin', 'end', 'list'))
            return await ctx.respond(f'{begin}{", ".join(list)}{end}')
        await ctx.respond(self.get_content(ctx, 'faq.name', question))
    
    async def _dtp(self, ctx: ApplicationContext, data_pack_feature: str | bool = False):
        if data_pack_feature == False:
            begin, end, list = self.get_content(ctx, 'dtp', keys=('begin', 'end', 'list'))
            return await ctx.respond(f'{begin}{", ".join(list)}{end}')
        await ctx.respond(self.get_content(ctx, 'dtp.name', data_pack_feature.removesuffix('s')))
        
    async def _lang(self, ctx: ApplicationContext, lang_code: str | bool = False):
        if lang_code == False:
            begin, end = self.get_content(ctx, 'lang', keys=('begin', 'end'))
            return await ctx.respond(f'{begin}{end}')
        
        lang_code = options['lang'][lang_code]
        self.user_lang[str(ctx.author.id)] = lang_code
        self.reload_user_lang_cache()
        self.save_user_lang_config()
        await ctx.respond(self.bot.lang['en'][f'lang.name.{lang_code}'])
    
    async def _help(self, ctx: ApplicationContext, command_name: str | bool = False):
        if command_name == False:
            begin, end, list = self.get_content(ctx, 'help', keys=('begin', 'end', 'list'))
            return await ctx.respond(f'{begin}{", ".join(list)}{end}')
        await ctx.respond(self.get_content(ctx, 'help.name', key=command_name))
    
    
    @commands.slash_command(**cmd_config)
    async def cmd(self, ctx: ApplicationContext, 
                  command_name: Option(str, default=False)):
        await self._cmd(ctx, command_name)
    
    @commands.slash_command(**cmd_config)
    async def faq(self, ctx: ApplicationContext, 
                  question: Option(str, choices=options['faq'], default=False)):
        await self._faq(ctx, question)
    
    @commands.slash_command(**cmd_config)
    async def dtp(self, ctx: ApplicationContext, 
                  data_pack_feature: Option(str, choices=options['dtp'], default=False)):
        await self._dtp(ctx, data_pack_feature)
    
    @commands.slash_command(**cmd_config)
    async def lang(self, ctx: ApplicationContext, 
                   lang_code: Option(str, choices=[*options['lang']], default=False)):
        await self._lang(ctx, lang_code)
    
    @commands.slash_command(**cmd_config)
    async def help(self, ctx: ApplicationContext, 
                   command_name: Option(str, choices=options['help'], default=False)):
        await self._help(ctx, command_name)
    

def setup(bot):
    bot.add_cog(MinecraftCog(bot))