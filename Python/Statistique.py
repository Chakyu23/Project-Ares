import mysql.connector
import discord
from discord.ext import commands
import variable
from Bdd import project_Ares_bdd

class Statistique:

    def __init__(self, name, displayType, cible):
        self.Name           = name
        self.Resume         = ""
        self.displayType    = displayType
        self.cible          = cible

class CogStat(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_ready")
    async def StatReady(self) -> None:
        print("Commande statistique : OK")

    @commands.hybrid_command(name="newstat")
    async def New(self, ctx : commands.Context, name : str, type : str, disp : str, target : str):
        is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
        if is_in_private_message:
            return await ctx.send("Impossible d'utiliser cette commande en message privé")

        has_permission = ctx.author.guild_permissions.administrator
        if has_permission:
            return await ctx.send("Vous n'avez pas les permission pour cette commande")
        return

    @commands.hybrid_command(name="resumestat")
    async def Resume(self, ctx : commands.Context, stat : str, *, resume : str):
        is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
        if is_in_private_message:
            return await ctx.send("Impossible d'utiliser cette commande en message privé")

        has_permission = ctx.author.guild_permissions.administrator
        if has_permission:
            return await ctx.send("Vous n'avez pas les permission pour cette commande")
        return

    @commands.hybrid_command(name="stat")
    async def Show(self, ctx : commands.context, stat : str):
        embed_stat = discord.Embed(
            title="statName",
            description="Je suis une description de stat",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed_stat)
