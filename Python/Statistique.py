import mysql.connector
import discord
from discord.ext import commands
import variable
from Bdd import project_Ares_bdd

class Statistique:

    def __init__(self, name, displayType, cible, resume = ""):
        self.Name           = name
        self.displayType    = displayType
        self.cible          = cible
        self.Resume         = resume
        

def AlphaPerm(ctx : commands.Context) -> str:
    is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_message:
        return "ERROR;Impossible d'utiliser cette commande en message privé"
    
    has_permission = ctx.author.guild_permissions.administrator
    print(has_permission)
    if has_permission == False:
        return "ERROR;Vous n'avez pas les permission pour cette commande"
    
    return "OK"

def ST(Stype):
    vT = False
    for i in len(variable.StatType):
        if variable.StatType[i] == Stype:
            vT = True
    if vT != True:
        embed_Error = discord.Embed(
            title="Type de Statistique",
            description="Liste de tous les type de Statistique disponible.",
            color= discord.Color.red()
        )
        for i in len(variable.StatType):
            embed_Error.add_field(
            name="Type : " + variable.StatType + " . " + variable.StatType_Desig,
            value=variable.StatType_descript
            )
        return embed_Error

    return "OK"

def DT(disp):
    vDT = False
    for i in len(variable.displayType):
        if variable.displayType[i] == disp:
            vDT = True
    if vDT != True:
        embed_Error = discord.Embed(
            title="Type de Display",
            description="Liste de tous les type de Display disponible.",
            color= discord.Color.red()
        )
        for i in len(variable.displayType):
            embed_Error.add_field(
            name="Type : " + variable.displayType + " . " + variable.displayType_Desig,
            value=variable.displayType_descript
            )
        return embed_Error
    return "OK"

def TT(target):
    vDT = False
    for i in len(variable.displayType):
        if variable.CibleList[i] == target:
            vDT = True

    if vDT != True:
        embed_Error = discord.Embed(
            title="Type de cible",
            description="Liste de tous les types de Cibles disponible.",
            color= discord.Color.red()
        )
        for i in len(variable.displayType):
            embed_Error.add_field(
            name="Type : " + variable.CibleList + " . " + variable.CibleList_Desig,
            value=variable.CibleList_descript
            )
        return embed_Error
    
    return "OK"

class CogStat(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_ready")
    async def StatReady(self) -> None:
        print("Commande statistique : OK")

    @commands.hybrid_command(name="newstat")
    async def New(self, ctx : commands.Context, name : str, Stype : str, disp : str, target : str):
        sRet = AlphaPerm(ctx)
        if sRet != "OK" :
            return await ctx.send(sRet.split(";")[1])
        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Name = '" + name + "'")
        exist = c.fetchall()
        if exist[0][0] != 0:
            return await ctx.send("La statistique existe déjà")
        
        sRet = ST(Stype)
        if sRet != "OK":
            return await ctx.send(embed=sRet)
        
        sRet = DT(disp)
        if sRet != "OK":
            return await ctx.send(embed=sRet)
        
        sRet = TT(target)
        if sRet != "OK":
            return await ctx.send(embed=sRet)
        
        

        return
    


    @commands.hybrid_command(name="resumestat")
    async def Resume(self, ctx : commands.Context, stat : str, *, resume : str):
        sRet = AlphaPerm(ctx)
        if sRet != "OK" :
            return await ctx.send(sRet.split(";")[1])

    @commands.hybrid_command(name="stat")
    async def Show(self, ctx : commands.context, stat : str):
        embed_stat = discord.Embed(
            title="statName",
            description="Je suis une description de stat",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed_stat)
