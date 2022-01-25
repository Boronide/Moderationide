from os import listdir
import discord
from discord.ext import commands
from settings import msglist, get

bot = commands.Bot(
    intents=discord.Intents.all(),
    command_prefix="-",
    help_command=None
)

for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_command_error(ctx, exception):
    if isinstance(exception, discord.ext.commands.errors.CommandNotFound):
        return None


@bot.event
async def on_ready():
    print(msglist.boronide_art)


bot.run(get.config("token"))
