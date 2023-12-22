import discord
from discord.ext import commands
import Serveur
import variable
from Bdd import project_Ares_bdd

###################################################################################################################################################
###### GESTION Fonction
###################################################################################################################################################

def Affinity_exist(Affinity : str, guilId : str):
    c = project_Ares_bdd.cursor()
    c.execute("SELECT COUNT(*) as exist FROM affinity \
              WHERE Affinity_ServID = '" + guilId + "' AND Affinity_Tag = '" + Affinity + "' OR Affinity_Name = '" + Affinity + "'")
    STnow = c.fetchone()
    c.close()

    if STnow[0] == 1:
        return [STnow[0], "L'Affinitée existe déjà, vérifier Nom/Tag"]
    else:
        return [STnow[0], " n'existe pas"]
    
def Affinity_check(strong : str, weak : str, guildId : str):
    c = project_Ares_bdd.cursor()
    c.execute("SELECT COUNT(*) as exist FROM affinity_rel  \
              WHERE AffinityRel_ServID = '" + guildId + "' AND AffinityRel_Strong = '" + strong + "' AND AffinityRel_Weak = '" + weak + "'")
    STnow = c.fetchone()
    c.close()

    if STnow[0] == 1:
        return [STnow[0], "La relation d'affinité existe déjà"]
    else:
        return [STnow[0], "La relation d'affinité n'existe pas"]

###################################################################################################################################################
###### GESTION Commandes
###################################################################################################################################################

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
        
        if len(tag) != 3:
            return await ctx.send("Longueur de Tag incorecte, il dois faire 3 caractère de longeur")

        sRet = Affinity_exist(tag, str(ctx.guild.id))
        if sRet[0] != 0:
            return await ctx.send(sRet[1])
        
        sRet = Affinity_exist(name, str(ctx.guild.id))
        if sRet[0] != 0:
            return await ctx.send(sRet[1])

        c = project_Ares_bdd.cursor()
        c.execute("Insert INTO affinity (Affinity_ServID, Affinity_Name, Affinity_Tag)" \
            "values ('"+str(ctx.guild.id)+"', '"+ name +"', '"+ tag +"')")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("L'affinité " + name + " a bien été enregistré.")

    @commands.hybrid_command(name="affinity_strong_to")
    async def affinity_StrongTo(self, ctx : commands.context, strong : str, weak : str, ratio : int):
        
        sRet = Affinity_exist(strong, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(strong + sRet[1])

        sRet = Affinity_exist(weak, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(weak + sRet[1])
        
        sRet = Affinity_check(strong, weak, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])

        ratio = round(ratio, 2)

        if ratio > 10:
            return await ctx.send("Facteur trop important, veuillez entré un facteur entre 10 et 0.01")

        if ratio < 0.01:
            return await ctx.send("Facteur trop faible, veuillez entré un facteur entre 10 et 0.01")
        
        c = project_Ares_bdd.cursor()
        c.execute("Insert INTO affinity_rel (AffinityRel_ServID, AffinityRel_Strong, AffinityRel_Weak, AffinityRel_Factor)" \
            "values ('"+str(ctx.guild.id)+"', '"+ strong +"', '"+ weak +"', '"+ ratio +"')")
        project_Ares_bdd.commit()
        c.close()
        
        return await ctx.send("La relation d'affinité " + strong + " > " + ratio + " > " + weak + " a bien été enregistré.")

###################################################################################################################################################
###### GESTION ERREUR
###################################################################################################################################################

    @Affinity_new.error
    async def Affinity_new_error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error

    @affinity_StrongTo.error
    async def affinity_StrongTo_error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error