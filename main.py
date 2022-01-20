import json
import os
os.system("pip install nextcord")
os.system("pip install mcstatus")
import platform
import random
import sys
import nextcord
from nextcord.ext import tasks, commands
from nextcord.ext.commands import Bot, has_permissions, MissingPermissions
from mcstatus import MinecraftServer
from datetime import datetime
import time

with open('token.txt') as f:
    lines = f.readlines()
    token12235709 = lines[0]

config = {
    "token": token12235709,
    "prefix": "!",
    "status": "with people",
    "java-mc-ip": "curvy-finger.auto.playit.gg",
    "bedrock-mc-ip": "wealthy-riddle.auto.playit.gg Port: 44997",
    "dynmap-ip": "empty untill bucket <@780862748603056169> fixes it",
    "log_channel": 933458519145984120,
    "joinleavechannel": 933459417054208030,
    "suggestions-channel": 933459679969935370
}

bot = Bot(command_prefix=config["prefix"], intents=nextcord.Intents.default())

@bot.event
async def on_ready():
    print("-------------------")
    print(f"Logged in as {bot.user.name}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    await bot.change_presence(activity=nextcord.Game(config["status"]))
    """
    #mc_stats.start()

@tasks.loop(minutes=1.0)
async def mc_stats():
    upd_at = round(datetime.utcnow().timestamp())
    server = MinecraftServer.lookup("curvy-finger.auto.playit.gg")
    status = server.status()
    latency = server.ping()
    query = server.query()
    channel = bot.get_channel(932858491700400238)
    msg = await channel.fetch_message(932858538085212190)
    server = mc.lookup(SERVERIP)
    status = server.status()
    players =""
    if status.players.sample is not None:
        for player in status.players.sample:
            players+= '\n ' + str(player.name)
    else:
        players="No players online"
    msg = (f"The Server has {status.players.online}/{status.players.max} players online.")
        
    embed = discord.Embed(title=server.name, description='Server Info', color=0xEE8700)
    embed.set_thumbnail(url=server.icon.url)
    embed.add_field(name="Players:", value=players, inline=True)
    embed.add_field(name="Ping:", value=str(latency), inline=True)
    await msg.edit(embed = embed)
    """


@bot.command(brief="Send a embed")
@has_permissions(administrator=True)
async def embed(ctx, title, description):
    embed=nextcord.Embed(title=f"{title}", description=description, color=0xff8040)
    embed.set_footer(text=f"{ctx.guild.name} • Posted by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(administrator=True)
async def edit(ctx):
    channel = bot.get_channel(932858491700400238)
    msg = await channel.fetch_message(932858538085212190)
    content = ctx.message.content
    content = content.replace(config["prefix"] + "update ", "")
    await msg.edit(content)


@bot.command(description="Shows MC Server Status")
async def mc(ctx):
    server = MinecraftServer.lookup(config['java-mc-ip'])
    status = server.status()
    embed = nextcord.Embed(title="Server Status", color=0xFFFFF)
    embed.add_field(name="Players Online", value=f"{status.players.online}", inline=False)
    embed.add_field(name="Latency (if 0 down for maintenance)", value = round(status.latency, 1),inline=False)
    await ctx.send(embed=embed)

@bot.command(brief="See the minecraft servers info")
async def info(ctx):
    embed = nextcord.Embed(title=f"Minecraft Info", description="", color=0xFFFFF)
    embed.add_field(name="Java IP", value="```\n" + config["java-mc-ip"] + "\n```", inline=True)
    embed.add_field(name="Bedrock IP", value="```\n" + config["bedrock-mc-ip"] + "\n```", inline=True)
    embed.add_field(name="Dynmap URL", value="```\n" + config["dynmap-ip"] + "\n```", inline=True)
    await ctx.send(embed=embed)


@bot.command(brief="Sends a poll in the current channel")
@has_permissions(administrator=True)
async def poll(ctx, optiona, optionb):
    await ctx.message.delete()
    embed=nextcord.Embed(title=f"A new poll has started! :tada:", description=f":one: {optiona}\n:two: {optionb}", color=0xff8040)
    embed.set_footer(text=f"Poll created by {ctx.author}")
    message = await ctx.send(embed=embed)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")

    

@bot.command(brief="update the info in #live-status")
async def pingnow(ctx):"""
    upd_at = round(datetime.utcnow().timestamp())
    server = MinecraftServer.lookup("curvy-finger.auto.playit.gg")
    status = server.status()
    latency = server.ping()
    query = server.query()
    channel = bot.get_channel(932858491700400238)
    msg = await channel.fetch_message(932858538085212190)
    server = mc.lookup(SERVERIP)
    status = server.status()
    players =""
    if status.players.sample is not None:
        for player in status.players.sample:
            players+= '\n ' + str(player.name)
    else:
        players="No players online"
    msg = (f"The Server has {status.players.online}/{status.players.max} players online.")
        
    embed = discord.Embed(title=server.name, description='Server Info', color=0xEE8700)
    embed.set_thumbnail(url=server.icon.url)
    embed.add_field(name="Players:", value=players, inline=True)
    embed.add_field(name="Ping:", value=str(latency), inline=True)
    await msg.edit(embed = embed)"""
    

@bot.command(brief="Kicks a user")
async def kick(ctx, member : nextcord.Member , *, reason = None):
    if reason == None:
        reason=f'Kicked by {ctx.author}'
    embed = nextcord.Embed(title=f"Kicked user {member}", description=f"Reason: {reason}", color = 0xFFFFF)
    user = member
    invite = await ctx.channel.create_invite(max_age = 0, max_uses = 0)
    await user.send(f"You were kicked from Inferno SMP for:```\n{reason}\n```. You may rejoin as this is only a kick. {invite}")
    await asyncio.sleep(1)
    await member.kick(reason=reason)
    await ctx.send(embed=embed)


@bot.command(aliases=["ava", "av"])
async def avatar(ctx):
    em = nextcord.Embed(title=f"Avitar of {ctx.author}", description="", color=0xff8040)
    em.set_image(url=ctx.author.avatar.url)
    await ctx.send(embed=em)

@bot.command(brief="Test Discords ping")
async def ping(ctx):
    start_time = time.time()
    message = await ctx.send("Testing Ping...")
    end_time = time.time()
    await message.edit(content=f"Pong!\nAPI there: {round(bot.latency * 1000)}ms\nAPI there and back: {round((end_time - start_time) * 1000)}ms")

@bot.command(name='eval', pass_context=True)
async def eval_(ctx, *, command):
    res = eval(command)
    if inspect.isawaitable(res):
        await ctx.send(await res)
    else:
        await ctx.send(res)

@bot.command(brief="Send a message from the bot")
@has_permissions(administrator=True)
async def send(ctx, arg):
    await ctx.send(arg)

@bot.command(brief="Delete messages")
@has_permissions(manage_messages=True)
async def purge(ctx, ammount):
    ammount = int(ammount)
    if ammount > 100:
        await ctx.send("You can not purge more then 100 messages at a time.")
    elif ammount < 1:
        await ctx.send("You need to purge more then 0 messages.")
    else:
        ammount = int(ammount)
        await ctx.channel.purge(limit=ammount)


@bot.command(brief="Info about the current server")
async def serverinfo(ctx):
    embed = nextcord.Embed(title=f"{ctx.guild.name}'s info'", description="", color=0xFFFFF)
    embed.add_field(name="Member Count", value=str(ctx.guild.member_count), inline=True)
    embed.add_field(name="Rules Channel", value=str(ctx.guild.rules_channel), inline=True)
    embed.add_field(name="Server Owner:", value=str(ctx.guild.owner), inline=True)
    embed.add_field(name="Guild Region", value=str(ctx.guild.region), inline=True)
    embed.add_field(name="Verification Level", value=str(ctx.guild.verification_level), inline=True)
    embed.add_field(name="AFK Channel", value=str(ctx.guild.afk_channel), inline=True)
    embed.add_field(name="AFK Timeout (in seconds)", value=str(ctx.guild.afk_timeout), inline=True)
    embed.add_field(name="Guild Description", value=str(ctx.guild.description), inline=True)
    embed.add_field(name="Nitro Boosts", value=str(ctx.guild.premium_subscription_count), inline=True)
    embed.add_field(name="System Messages Channel", value=str(ctx.guild.system_channel), inline=True)
    embed.add_field(name="Server Booster Role", value=str(ctx.guild.premium_subscriber_role), inline=True)
    embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

@bot.command()
async def suggest(ctx,*,suggestion):
    embed=nextcord.Embed(title=f"New suggestion!", description=suggestion, color=ctx.guild.me.color)
    embed.set_footer(text=f"Suggestion created by {ctx.author}")
    suggChnl = bot.get_channel(config['suggestions-channel'])
    message = await suggChnl.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    await ctx.message.delete()
    await ctx.send("Thank you for your suggestion!", delete_after=4)


@bot.event
async def on_message(message):
    if message.channel.id == 933459679969935370:
        if message.author.id != 924477997287882753:
            await message.delete()
            embed=nextcord.Embed(title=f"New suggestion!", description=message.content)
            embed.set_footer(text=f"Suggestion created by {message.author}")
            msg = await message.channel.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
    await bot.process_commands(message)

@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Do"  + config['prefix'] + "help")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing a required argument.  Do"  + config['prefix'] + "help")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the correct permissions to run this command.")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have sufficient permissions!")
    else:
        print("error not caught")
        print(error) 


@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(config['log_channel'])
    embed=nextcord.Embed(title=f"Message deleted by {message.author}", color=0xff8040)
    embed.add_field(name=f"Message:", value=f"{message.content}", inline=False)
    await channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    if not before.content == after.content:
        logChnl = bot.get_channel(config['log_channel'])
        embed=nextcord.Embed(title=f"Message edit by {before.author}", color=0xff8040)
        embed.add_field(name=f"Old message:", value=f"{before.content}", inline=False)
        embed.add_field(name=f"New message:", value=f"{after.content}", inline=False)
        await logChnl.send(embed=embed)


@bot.event
async def on_member_join(member):
    chnl = bot.get_channel(config['joinleavechannel'])
    embed=nextcord.Embed(description=f"**{member}** just joined the server.", color=member.guild.me.color)
    embed.set_footer(text=f"Member #{len(member.guild.members)}")
    await chnl.send(content=f"Hey {member.mention}, welcome to **{member.guild.name}**!", embed=embed)


@bot.event
async def on_member_remove(member):
    chnl = bot.get_channel(config['joinleavechannel'])
    await chnl.send(f"{member} just left!")
bot.run(config["token"])
