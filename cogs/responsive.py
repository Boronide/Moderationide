from discord.commands import slash_command
from discord.ext import commands
from settings import msglist, get


class Responsive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=get.config("gid"), description="Boronide ASCII Art")
    async def boronide(self, ctx):
        art_style = [msglist.boronide_art, msglist.boronide_art2, msglist.boronide_art3, msglist.boronide_art4]
        await ctx.respond(f"```{art_style[get.ran_num(x=1,y=0,z=(len(art_style))-1)[0]]}```")

    @slash_command(guild_ids=get.config("gid"), description="Runtime Information")
    async def run_time(self, ctx):
        b, c = get.bot_platform, "@BordComputer"
        await ctx.respond(msglist.bot_runtime_txt.format(b, c))

    @slash_command(guild_ids=get.config("gid"), description="Bot Information")
    async def info(self, ctx):
        await ctx.respond(msglist.bot_info_text)

    @slash_command(guild_ids=get.config("gid"), description="Admin-Only Boronide-Deobfuscator")
    async def deobfuscate(self, ctx):
        await ctx.respond(msglist.msg_deobfuscate, ephemeral=True)


def setup(bot):
    bot.add_cog(Responsive(bot))
