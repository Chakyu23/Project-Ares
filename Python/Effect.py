import discord
from discord.ext import commands
import Serveur
import variable
from Bdd import project_Ares_bdd

###################################################################################################################################################
###### GESTION Class Effect
###################################################################################################################################################

class Effect:
    def __init__(self, Effect_ID, Tag, Type, Balance, EffTab : list) -> None:
        self.Effect_ID = Effect_ID
        self.Tag = Tag
        self.Type = Type
        self.Balance = Balance
        self.EffTab = EffTab

class Buff(Effect):
    def __init__(self, Effect_ID, Tag, Type, Balance, EffTab, Duration) -> None:
        super().__init__(Effect_ID, Tag, Type, Balance, EffTab)
        self.Duration = Duration

class InstantEffect(Effect):
    def __init__(self, Effect_ID, Tag, Type, Balance, EffTab) -> None:
        super().__init__(Effect_ID, Tag, Type, Balance, EffTab)

class LongEffect(Effect):
    def __init__(self, Effect_ID, Tag, Type, Balance, EffTab, Duration, Timer) -> None:
        super().__init__(Effect_ID, Tag, Type, Balance, EffTab)
        self.Duration = Duration
        self.Timer = Timer

###################################################################################################################################################
###### GESTION Fonction
###################################################################################################################################################

def Effect_exist(Effect : str, guilId : str):
    c = project_Ares_bdd.cursor()
    c.execute("SELECT COUNT(*) as exist FROM effect \
              WHERE Effect_ServID = '" + guilId + "' AND Effect_Tag = '" + Effect + "' OR Effect_Name = '" + Effect + "'")
    STnow = c.fetchone()
    c.close()

    if STnow[0] == 1:
        return [STnow[0], Effect + " existe déjà, vérifier Nom/Tag"]
    else:
        return [STnow[0], Effect + " n'existe pas"]

def Effect_type(target : str):
    vDT = False
    for i in range(len(variable.EffectType)):
        if variable.EffectType[i] == target:
            vDT = True

    if vDT != True:
        embed_Error = discord.Embed(
            title="Type de cible",
            description="Liste de tous les types de Cibles disponible.",
            color= discord.Color.red()
        )
        for i in range(len(variable.EffectType)):
            embed_Error.add_field(
            name="Type : " + variable.EffectType[i] + " . " + variable.EffectType_Desig[i],
            value=variable.EffectType_descript[i]
            )
        return ["ERROR", embed_Error]
    
    return ["OK"]

###################################################################################################################################################
###### GESTION Commandes
###################################################################################################################################################

class CogStat(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

    # Cog On
    @commands.Cog.listener(name="on_ready")
    async def Stat_ready(self) -> None:
        print("Commande Statistique : OK")

    @commands.hybrid_command(name="effect_new")
    async def Effect_New(self, ctx : commands.Context, name : str, tag : str, efftype : str):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])
        
        if len(tag) != 3:
            return await ctx.send("Longueur de Tag incorecte, il dois faire 3 caractère de longeur")

        sRet = Effect_exist(tag, str(ctx.guild.id))
        if sRet[0] != 0:
            return await ctx.send(sRet[1])
        
        sRet = Effect_exist(name, str(ctx.guild.id))
        if sRet[0] != 0:
            return await ctx.send(sRet[1])
        
        sRet = Effect_type(efftype)
        if sRet[0] != "OK":
            return await ctx.send(embed=sRet[1])

        c = project_Ares_bdd.cursor()
        c.execute("Insert INTO effect (Effect_ServID, Effect_Name, Effect_Tag)" \
            "values ('"+str(ctx.guild.id)+"', '"+ name +"', '"+ tag +"')")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("L'affinité " + name + " a bien été enregistré.")

###################################################################################################################################################
###### GESTION ERREUR
###################################################################################################################################################    
        
    @Effect_New.error
    async def Effect_New_error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error