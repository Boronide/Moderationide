from discord.ext import commands
from settings import get
import datetime

emb = get.embed


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if (
                any(item in message.content.split() for item in ["-obf", "-obfuscate", "```lua"])
                or message.author.id == 880537188843016245
                or message.author.id == 932320101489836073
        ):
            return None
        if (
                message.author.id != 880537188843016245
                or message.author.id != 932320101489836073
        ):
            channel = self.bot.get_channel(get.config("lig"))
            emb.title, emb.timestamp = "Message Deleted", datetime.datetime.utcnow()
            emb.description = f"**Channel: {message.channel.mention}**\n **Content:**\n`{message.content}`"
            emb.set_author(name=f"{message.author}", icon_url=message.author.avatar)
            emb.set_footer(text=f"ID: {message.author.id}")
            await channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if (
                before.author.id != 932320101489836073
        ):
            channel = self.bot.get_channel(get.config("lig"))
            emb.title, emb.timestamp = "Message Edited", datetime.datetime.utcnow()
            emb.description = f"**Channel: {before.channel.mention}**\n **Original:**\n`{before.content}`\n **New:**\n" \
                              f"`{after.content}`"
            emb.set_author(name=f"{before.author}", icon_url=before.author.avatar)
            emb.set_footer(text=f"ID: {before.author.id}")
            await channel.send(embed=emb)

        # @commands.Cog.listener()
        # async def


def setup(bot):
    bot.add_cog(Logging(bot))
