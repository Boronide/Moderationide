from discord.ext import commands, tasks
import json
import os
import time


class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ban_loop.start()

    @tasks.loop(seconds=5.0)
    async def ban_loop(self):
        for ban_list in os.listdir("./db/bans"):
            if ban_list.endswith(".json"):
                with open("./db/bans/" + f"{ban_list}", 'r') as bl:
                    json_file = json.load(bl)
                    ban_time = json_file["ban_time"]
                    if float(time.time()) >= float(ban_time):
                        user_to_unban = await self.bot.fetch_user(json_file["user_id"])
                        fetched_guild = await self.bot.fetch_guild(880536134491467787)
                        await fetched_guild.unban(user_to_unban)
                        os.remove(f"./db/bans/{ban_list}")


def setup(bot):
    bot.add_cog(Unban(bot))
