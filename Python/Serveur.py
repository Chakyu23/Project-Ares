import mysql.connector
import discord
from discord.ext import commands
import variable
from Bdd import project_Ares_bdd
import ast


class CogServ(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="serv_register")
    async def ServerREGISTER(self,  ctx : commands.Context):

        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist FROM serveur \
                   WHERE Serv_ID = '" + str(ctx.guild.id) + "'")
        exist = c.fetchone()
        if exist[0]!= 0:
            c.close()
            return await ctx.send("Le serveur est déja enregistrer")
        
        c.execute("Insert INTO serveur (Serv_ID)" \
            "values ('"+str(ctx.guild.id)+"')")
        project_Ares_bdd.commit()
        c.close()
    
