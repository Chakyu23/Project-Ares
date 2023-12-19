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
    if has_permission == False:
        return "ERROR;Vous n'avez pas les permission pour cette commande"
    
    return "OK"

def SType(Stype : str):
    vT = False
    for i in range(len(variable.StatType)):
        if variable.StatType[i] == Stype:
            vT = True

    if vT != True:
        embed_Error = discord.Embed(
            title="Type de Statistique",
            description="Liste de tous les type de Statistique disponible.",
            color= discord.Color.red()
        )
        for i in range(len(variable.StatType)):
            embed_Error.add_field(
            name="Type : " + variable.StatType[i] + " . " + variable.StatType_Desig[i],
            value=variable.StatType_descript[i]
            )
        return ["ERROR", embed_Error]

    return ["OK"]

def DType(disp : str):
    vDT = False
    for i in range(len(variable.displayType)):
        if variable.displayType[i] == disp:
            vDT = True
    if vDT != True:
        embed_Error = discord.Embed(
            title="Type de Display",
            description="Liste de tous les type de Display disponible.",
            color= discord.Color.red()
        )
        for i in range(len(variable.displayType)):
            embed_Error.add_field(
            name="Type : " + variable.displayType[i] + " . " + variable.displayType_Desig[i],
            value=variable.displayType_descript[i]
            )
        return ["ERROR", embed_Error]
    return ["OK"]

def TType(target : str):
    vDT = False
    for i in range(len(variable.CibleList)):
        if variable.CibleList[i] == target:
            vDT = True

    if vDT != True:
        embed_Error = discord.Embed(
            title="Type de cible",
            description="Liste de tous les types de Cibles disponible.",
            color= discord.Color.red()
        )
        for i in range(len(variable.CibleList)):
            embed_Error.add_field(
            name="Type : " + variable.CibleList[i] + " . " + variable.CibleList_Desig[i],
            value=variable.CibleList_descript[i]
            )
        return ["ERROR", embed_Error]
    
    return ["OK"]

class CogStat(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_ready")
    async def StatReady(self) -> None:
        print("Commande statistique : OK")

    @commands.hybrid_command(name="newstat")
    async def New(self, ctx : commands.Context, name : str, stattype : str, disp : str, target : str):
        sRet = AlphaPerm(ctx)
        if sRet != "OK" :
            return await ctx.send(sRet.split(";")[1])
        
        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Name = '" + name + "'")
        exist = c.fetchone()
        if exist[0]!= 0:
            c.close()
            return await ctx.send("La statistique existe déjà")
        c.close()

        sRet = SType(str(stattype))
        if sRet[0] != "OK":
            return await ctx.send(embed=sRet[1])
    
        sRet = DType(str(disp))
        if sRet[0] != "OK":
            return await ctx.send(embed=sRet[1])
    
        sRet = TType(str(target))
        if sRet[0] != "OK":
            return await ctx.send(embed=sRet[1])
        
        c.execute("Insert INTO statistique (Stat_ServID, Stat_Name, Stat_Type, Stat_DisplayType, Stat_Cible)" \
            "values ('"+str(ctx.guild.id)+"', '"+name+"', '"+stattype+"', '"+disp+"', '"+target+"')")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("mission Complete")
    


    @commands.hybrid_command(name="resumestat")
    async def Resume(self, ctx : commands.Context, stat : str, *, resume : str):
        sRet = AlphaPerm(ctx)
        if sRet != "OK" :
            return await ctx.send(sRet.split(";")[1])
    
        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Name = '" + stat + "'")
        exist = c.fetchone()
        if exist[0]!= 1:
            c.close()
            return await ctx.send("La statistique n'existe pas")
        c.close()

        c.execute("UPDATE statistique SET Stat_Resume = '" + resume + "' WHERE Stat_Name = '" + stat + "'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("mission Complete")

    @commands.hybrid_command(name="CalcStat")
    async def Resume(self, ctx : commands.Context, stat : str, *, resume : str):
        sRet = AlphaPerm(ctx)
        if sRet != "OK" :
            return await ctx.send(sRet.split(";")[1])
    
        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist, Stat_Type FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Name = '" + stat + "'")
        STnow = c.fetchone()
        if STnow[0] != 1:
            c.close()
            return await ctx.send("La statistique n'existe pas")
        if STnow[1] != "Cal" and STnow[1] != "Vit": 
            c.close()
            return await ctx.send("La statistique n'est pas calculé")
        c.close()

        


        c.execute("UPDATE statistique SET Stat_Resume = '" + resume + "' \
                  WHERE Stat_Name = '" + stat + "AND Stat_ServID = '" + str(ctx.guild.id) + "'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("mission Complete")



    @commands.hybrid_command(name="stat")
    async def Show(self, ctx : commands.context, stat : str):

        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Name = '" + stat + "'")
        exist = c.fetchone()
        if exist[0]!= 1:
            c.close()
            return await ctx.send("La statistique n'existe pas")
        c.close()

        embed_stat = discord.Embed(
            title="statName",
            description="Je suis une description de stat",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed_stat)
