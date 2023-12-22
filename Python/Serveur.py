import discord
from discord.ext import commands
from Bdd import project_Ares_bdd


def AlphaPerm(ctx : commands.Context) -> str:
    is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_message:
        return ["ERROR", "Impossible d'utiliser cette commande en message privé"]
    
    has_permission = ctx.author.guild_permissions.administrator
    if has_permission == False:
        return ["ERROR", "Vous n'avez pas les permission pour cette commande"]
    
    return ["OK"]


class CogServ(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_ready")
    async def Servready(self) -> None:
        print("Commande Serveur : OK")

    @commands.Cog.listener(name="on_guid_join")
    async def Guildjoin(self, guild) -> None:
        print(str(guild.id))
        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist FROM serveur \
                   WHERE Serv_ID = '" + str(guild.id) + "'")
        exist = c.fetchone()
        if exist[0]!= 0:
            c.close()
        
        c.execute("Insert INTO serveur (Serv_ID, Serv_Name)" \
            "values ('"+str(guild.id)+"','" + str(guild.name) + "')")
        project_Ares_bdd.commit()
        c.close()
        

    @commands.hybrid_command(name="serv_register")
    async def ServerREGISTER(self,  ctx : commands.Context):
        sRet = AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])
        
        print("Ajout :",str(ctx.guild.id))
        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist FROM serveur \
                   WHERE Serv_ID = '" + str(ctx.guild.id) + "'")
        exist = c.fetchone()
        if exist[0]!= 0:
            c.close()
            return await ctx.send("Le serveur est déja enregistrer")
        
        c.execute("Insert INTO serveur (Serv_ID, Serv_Name)" \
            "values ('"+str(ctx.guild.id)+"','" + str(ctx.guild.name) + "')")
        project_Ares_bdd.commit()
        c.close()

    @commands.hybrid_command(name="serv_delete")
    async def ServerDELETE(self,  ctx : commands.Context):
        print("Suprression :", str(ctx.guild.id))
        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist FROM serveur \
                   WHERE Serv_ID = '" + str(ctx.guild.id) + "'")
        exist = c.fetchone()
        if exist[0]!= 1:
            c.close()
            return await ctx.send("Le serveur n'est pas enregistrer")
        
        c.execute("DELETE FROM serveur (Serv_ID, Serv_Name)" \
            "values ('"+str(ctx.guild.id)+"')")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("Le serveur et ses données ont été supprimés")
