import mysql.connector
import discord
from discord.ext import commands
import variable
from Bdd import project_Ares_bdd
import ast
import re

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

def Vtag(Tag : str, guildId : str):
    if len(Tag) != 3:
        return ["ERROR", "Un tag ne doit 3 caractère et doit être unique"]
    
    if Tag.isalpha() != True:
        return ["ERROR", "Un tag ne peu contenir aucun chiffre ni caractère spécial"]
    
    c = project_Ares_bdd.cursor()
    c.execute("SELECT COUNT(*) as exist FROM statistique \
              WHERE Stat_ServID = '" + guildId + "' AND Stat_Tag = '" + Tag + "'")
    exist = c.fetchone()
    if exist[0]!= 0:
        c.close()
        return ["ERROR", "Le Tag existe déjà"]
    c.close()

    return ["OK"]

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

def getCalc(calc : str, guildId : str):
    valid = False
    regV = r"[\d +\-*/()]+"

    c = project_Ares_bdd.cursor()
    c.execute("SELECT Stat_Tag, Stat_Type FROM statistique \
              WHERE Stat_ServID = '" + guildId + "'")
    TagList = c.fetchall()
    c.close()
    for i in range(len(TagList)):
        if calc.find(TagList[i][0]) != -1:
            if TagList[i][1] == "CAL" or TagList[i][1] == "VIT":
                return ["ERROR", "Impossible d'Imbriqué deux statistique calculé ou Vitale"]
            else:
                valid = True
                calc = calc.replace(TagList[i][0], "5")
    
    list = re.findall(regV, calc)

    if len(list) == len(calc):
        valid = valid
    else:
        return ["ERROR", "Tag incorecte et/ou caractère invalide"]

    if valid == True:
        return ["OK", calc]
    else: 
        return ["ERROR", "Aucun Tag trouvé"]  

class CogStat(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_ready")
    async def Statready(self) -> None:
        print("Commande statistique : OK")

    @commands.hybrid_command(name="newstat")
    async def New(self, ctx : commands.Context, name : str, tag : str, stattype : str, disp : str, target : str):
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

        sRet = Vtag(str(tag), str(ctx.guild.id))
        if sRet[0] != "OK":
            c.close()
            return await ctx.send(sRet[1])

        sRet = SType(str(stattype))
        if sRet[0] != "OK":
            c.close()
            return await ctx.send(embed=sRet[1])
    
        sRet = DType(str(disp))
        if sRet[0] != "OK":
            c.close()
            return await ctx.send(embed=sRet[1])
    
        sRet = TType(str(target))
        if sRet[0] != "OK":
            c.close()
            return await ctx.send(embed=sRet[1])
        
        c.execute("Insert INTO statistique (Stat_ServID, Stat_Name, Stat_Tag, Stat_Type, Stat_DisplayType, Stat_Cible)" \
            "values ('"+str(ctx.guild.id)+"', '"+name+"', '"+tag+"', '"+stattype+"', '"+disp+"', '"+target+"')")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("Statistique Correctement Enregistré")
    

    @commands.hybrid_command(name="resumestat")
    async def Resume(self, ctx : commands.Context, stat : str, *, resume : str):
        sRet = AlphaPerm(ctx)
        if sRet != "OK" :
            return await ctx.send(sRet.split(";")[1])
    
        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
        exist = c.fetchone()
        if exist[0]!= 1:
            c.close()
            return await ctx.send("La statistique n'existe pas")
        c.close()

        c.execute("UPDATE statistique SET WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("mission Complete")

    @commands.hybrid_command(name="calcstat")
    async def StatCalcul(self, ctx : commands.Context, stat : str, *, calcul : str):
        sRet = AlphaPerm(ctx)
        if sRet != "OK" :
            return await ctx.send(sRet.split(";")[1])
    
        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
        STnow = c.fetchone()
        if STnow[0] != 1:
            c.close()
            return await ctx.send("La statistique n'existe pas")
        
        c.execute("SELECT Stat_Type FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
        STnow = c.fetchone()
        if STnow[0] != "CAL" and STnow[0] != "VIT": 
            c.close()
            return await ctx.send("La statistique n'est pas calculé")
        

        expVerif = getCalc(calcul, str(ctx.guild.id))

        if expVerif[0] != "OK":
            return await ctx.send("Erreur lors de la lecture des tag : \n" + expVerif[1])

        try: 
            result = eval(str(expVerif[1]))
        except Exception as e:
            return await ctx.send("Erreur lors de la lecture du calcul : \n" + str(e))
    
            

        print(result)

        c.execute("UPDATE statistique SET Stat_Calcul = '" + calcul + "' \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("Statistique Correctement Enregistré")

    @StatCalcul.error
    async def StatCalcul_Error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error



    @commands.hybrid_command(name="stat")
    async def Show(self, ctx : commands.context, stat : str):

        c = project_Ares_bdd.cursor()
        c.execute("SELECT COUNT(*) as exist,  FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
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
