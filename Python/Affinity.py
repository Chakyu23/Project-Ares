import discord
from discord.ext import commands
import Serveur
import variable
from Bdd import project_Ares_bdd



class CogAffinity(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_ready")
    async def stat_ready(self) -> None:
        print("Commande Affinity : OK")

    @commands.hybrid_command(name="affinity_new")
    async def Affinity_new(self, ctx : commands.context, name : str, tag : str):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])