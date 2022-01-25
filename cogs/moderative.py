import discord
from discord.commands import slash_command
from discord.ext import commands
from settings import msglist, get
import time
import datetime

time_conv = "time.strftime('%Y-%m-%d %H:%M:%S', time.localtime({}))"

with open("./db/perms/" + "modids.txt", "r") as rdf:
    permissions = rdf.read().split('\n')


def add_log(a2, a3, a4, a5):
    with open("./db/log/" + "logs.txt", "r") as log_file:
        log2app = log_file.readlines()
        log2app.insert(0, msglist.log_format_txt.format(eval(time_conv.format(time.time())), a2, a3, a4, a5))
        with open("./db/log/" + "logs.txt", "w") as write_file:
            write_file.writelines(log2app)


def manipulate_file(method, key2change):  # test
    with open("./db/perms/" + "modids.txt", "r") as id_file:
        r_file = id_file.readlines()
        m = "add" if method == "add" else "remove"
        r_file.insert(0, f"{key2change}\n") if m == "add" else r_file.remove(f"{key2change}\n")
        permissions.append(str(key2change)) if m == "add" else permissions.remove(str(key2change))
        with open("./db/perms/" + "modids.txt", "w+") as write_fl:
            write_fl.writelines(r_file)


async def pun_shortener(ctx, member, mem):
    m = "immune" if str(member.id) in permissions else "no_perms"
    await ctx.respond(f"Can't {mem} **<@{member.id}>** **[Immunity]**!", ephemeral=True) if m == "immune" else \
        await ctx.respond(f"**<@{ctx.author.id}>** {msglist.no_permissions}", ephemeral=True)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=get.config("gid"), description="permanent banning a user")
    async def p_ban(self, ctx, member: discord.Member, reason):
        emb, author_avatar = get.embed, ctx.author.display_avatar
        emb.set_footer(text=f"ID: {ctx.author.id}"), emb.set_author(name=ctx.author, icon_url=author_avatar)
        if (
                str(ctx.author.id) in permissions
                and str(member.id) not in permissions
        ):
            emb.title, emb.description = "Ban Function", f"Banning **<@{member.id}>** \n**Reason**\n`{reason}`"
            add_log("Perm-Banned User", member.id, ctx.author.id, f"{ctx.author.name}#{ctx.author.discriminator}")
            await ctx.respond(embed=emb), await member.ban(delete_message_days=1, reason=reason)
        if (
                str(ctx.author.id) not in permissions
                or str(member.id) in permissions
        ):
            await pun_shortener(ctx, member, "ban")

    @slash_command(guild_ids=get.config("gid"), description="temporary banning a user for x hours")
    async def t_ban(self, ctx, member: discord.Member, reason, time_in_hours):
        emb, author_avatar = get.embed, ctx.author.display_avatar
        emb.set_footer(text=f"ID: {ctx.author.id}"), emb.set_author(name=ctx.author, icon_url=author_avatar)
        if (
                str(ctx.author.id) in permissions
                and str(member.id) not in permissions
        ):
            ban_timer = (float(time_in_hours) * 3600) + time.time()
            time_processor = eval(time_conv.format(ban_timer))
            t1, t2, b3 = '{\n', '}', f'  "user_id": {member.id}\n'
            b1, b2 = f'  "ban_time": {ban_timer},\n', f'  "user_tag": "{member.name}#{member.discriminator}",\n'
            emb.title, emb.description = "Ban Function", f"**Banning**\n**<@{member.id}>**\n**Until**\n" \
                                                         f"{time_processor}\n**Reason**\n`{reason}`"
            with open("./db/bans/" + f"{member.id}.json", 'x') as crt_ban:
                crt_ban.writelines([t1, b1, b2, b3, t2])
            add_log("Temp-Banned User", member.id, ctx.author.id, f"{ctx.author.name}#{ctx.author.discriminator}")
            await ctx.respond(embed=emb), await member.ban(reason=reason)
        if (
                str(ctx.author.id) not in permissions
                or str(member.id) in permissions
        ):
            await pun_shortener(ctx, member, "ban")

    @slash_command(guild_ids=get.config("gid"), description="add/remove Permission from User")
    async def permissions(self, ctx, member: discord.Member, method):
        emb, author_avatar = get.embed, ctx.author.display_avatar
        emb.set_footer(text=f"ID: {ctx.author.id}"), emb.set_author(name=ctx.author, icon_url=author_avatar)
        a = "add" if method.lower() == "add" and str(member.id) not in permissions else "remove" \
            if method.lower() == "remove" and str(member.id) in permissions else "invalid"
        if (
                str(ctx.author.id) in permissions
                and a in ["add", "remove"]
        ):
            c = f"**Action `{method}` | successfully called on <@{member.id}>**"
            manipulate_file(f"{method.lower()}", member.id)
            add_log(f"ID-Permission {method}", member.id, ctx.author.id,
                    f"{ctx.author.name}#{ctx.author.discriminator}")
            emb.title, emb.description = "Permissions Function", c
            await ctx.respond(embed=emb)
        elif (
                str(ctx.author.id) not in permissions
                or a == "invalid"
        ):
            c = msglist.mth.format(method) if a == "invalid" else msglist.no_permissions.format_map(ctx.author.id)
            emb.title, emb.description = "Permissions Function", c
            await ctx.respond(embed=emb)

    @slash_command(guild_ids=get.config("gid"), description="purge x messages")
    async def purge(self, ctx, amount):
        emb, author_avatar = get.embed, ctx.author.display_avatar
        emb.set_footer(text=f"ID: {ctx.author.id}"), emb.set_author(name=ctx.author, icon_url=author_avatar)
        emb.title, emb.description = "Purge Function", f"**<@{ctx.author.id}> Purge done, deleted `{amount}` messages**"
        if (
                str(ctx.author.id) in permissions
                and int(amount) <= 100
        ):
            await ctx.channel.purge(limit=int(amount), bulk=True), await ctx.respond(embed=emb)
        if (
                str(ctx.author.id) not in permissions
                or int(amount) >= 100
        ):
            m = "limit" if int(amount) >= 100 else "no_perms"
            await ctx.respond("Max Amount is 100") if m == "limit" else await ctx.respond(msglist.no_permissions)

    @slash_command(guild_ids=get.config("gid"), description="shutting user up for x minutes")
    async def timeout(self, ctx, member: discord.Member, minute):
        emb, author_avatar = get.embed, ctx.author.display_avatar
        emb.set_footer(text=f"ID: {ctx.author.id}"), emb.set_author(name=ctx.author, icon_url=author_avatar)
        emb.title, emb.description = "Timeout Function", f"**Timeout Successful on `{member}` for `{minute}` minutes**"
        if (
                str(ctx.author.id) in permissions
                and str(member.id) not in permissions
        ):
            await member.timeout_for(datetime.timedelta(minutes=int(minute))), await ctx.respond(embed=emb)
        if (
                str(ctx.author.id) not in permissions
                or str(member.id) in permissions
        ):
            await pun_shortener(ctx, member, "timeout")


def setup(bot):
    bot.add_cog(Moderation(bot))
