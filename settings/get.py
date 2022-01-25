import json
import discord
import platform
import time
import datetime
import random


def config(name):
    with open("./settings/" + "config.json", "r") as b_cfg:
        json_file = json.load(b_cfg)
        return json_file[name]


bot_platform = platform.system()

time_epoche = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

embed = discord.Embed(
    title="",
    description="",
    color=discord.Color.purple(),
    timestamp=datetime.datetime.utcnow(),
)

send_msg = 'await ctx.send("{}")'


def ran_num(x: int, y: int, z: int):
    return [random.randint(y, z) for _ in range(x)]
