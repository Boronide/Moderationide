import re

import discord
from discord.ext import commands
from settings import get
from mymodules.piston import PistonAPI

N_CHARS = 75


class RunCodeCog(commands.Cog, name="Runs Code"):

    def __init__(self, bot):
        self.bot = bot
        self.api = PistonAPI()

    @commands.command()
    async def run(self, ctx, *, args: str):
        if (
                ctx.channel.id != 882638621017010217
                or not (match := re.fullmatch(r"((```)?)([a-zA-Z\d]+)\n(.+?)\1", args, re.DOTALL))
        ):
            await ctx.send(f"<@{ctx.author.id}> Incorrect chanel! go to  <#882638621017010217>") if ctx.channel.id \
                != 882638621017010217 else await ctx.send("Code is not in a Language Assigned Markdown")
        if (
                ctx.channel.id == 882638621017010217
                and (match := re.fullmatch(r"((```)?)([a-zA-Z\d]+)\n(.+?)\1", args, re.DOTALL))
        ):
            try:
                await self.api.load_environments()
                *_, lang, source = match.groups()
                if not (language := self.api.get_language(lang)):
                    await ctx.send(f'Language **"{lang.capitalize()}"** not supported!')
                result = await self.api.run_code(language, source)
                output = result["run"]["output"]
                if len(output) > N_CHARS:
                    newline = output.find("\n", N_CHARS, N_CHARS + 20)
                    if newline == -1:
                        newline = N_CHARS
                    output = output[:newline] + "\n..."
                description = "```\n" + output.replace("`", "`\u200b") + "\n```"
                emb, author_avatar = get.embed, ctx.author.display_avatar
                emb.set_footer(text=f"ID: {ctx.author.id}"), emb.set_author(name=ctx.author, icon_url=author_avatar)
                emb.title, emb.description = f"{language.capitalize()} Code Execution Output:", description
                if result["run"]["code"] != 0:
                    emb.color = discord.Color.dark_red()
                await ctx.send(embed=emb)
                #await ctx.send("Something went wrong") if result["run"]["code"] != 0 else await ctx.send(embed=emb)
            except Exception:
                pass


def setup(bot):
    bot.add_cog(RunCodeCog(bot))
