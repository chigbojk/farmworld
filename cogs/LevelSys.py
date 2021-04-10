import discord
from discord.ext import commands
from pymongo import MongoClient

bot_channel = 827877854020763648

# general channel
talk_channels = [827843693041811489]

roles = ["Farmer I", "Farmer II", "Farmer III", "Farmer IV", "Farmer V"]
levelnum = [5, 10, 15, 20, 25]

cluster = MongoClient("mongodb+srv://admin:roseparkclose@mycluster.dsmyn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

levelling = cluster["discord"]["levelling"]

class LevelSys(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("LevelSys ready")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels:
            stats = levelling.find_one({"id": message.author.id})

            if not message.author.bot:
                if not stats:
                    newUser = {"id": message.author.id, "xp": 100}
                    levelling.insert_one(newUser)

                else:
                    xp = stats["xp"] + 5
                    levelling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0

                    while True:
                        if xp < ((50 * (lvl**2)) + (50 * (lvl))):
                            break
                        lvl += 1

                    xp = ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
                    if xp == 0:
                        await message.channel.send(f"Well done {message.author.mention}! You levelled up to **level: {lvl}**!")

                        for i in range(len(lvl)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                embed = discord.Embed(description=f"{message.author.mention} you have gotten role ** {level[i]}**!!!")
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed.embed)

    @commands.command()
    async def rank(self, ctx):
        if ctx.channel.id == bot_channel:
            stats = levelling.find_one({"id": ctx.author.id})

            if not stats:
                embed = discord.Embed(description="You haven't sent any messages, no rank!!!")
                await ctx.channel.send(embed=embed)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0

                while True:
                    if xp < ((50 * (lvl**2)) + (50 * (lvl))):
                        break
                    lvl += 1     

                xp -= ((50 * (lvl - 1)**2)) + (50 * (lvl - 1))
                boxes = int((xp/(200*((0.5) * lvl))) * 20)
                rankings = levelling.find().sort("xp", -1)

                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                
                embed = discord.Embed(title=f"{ctx.author.name}'s level stats")
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200*((0.5) * lvl))}", inline=True)
                embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name="Level", value=f"{lvl}", inline=True)
                embed.add_field(name="Progress Bar [lvl]", value=boxes*":blue_square: " + (20 - boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
                print("hey")

    @commands.command()
    async def leaderboard(self, ctx):
        if ctx.channel.id == bot_channel:
            rankings = levelling.find().sort("xp", -1)

            i = 1

            embed = discord.Embed(title="Rankings:")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=True)
                    i += 1
                except:
                    pass

                if i == 11:
                    break

                await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(LevelSys(client))