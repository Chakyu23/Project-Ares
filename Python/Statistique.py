import discord
from discord.ext import commands
import Serveur
import variable
from Bdd import project_Ares_bdd
import re

###################################################################################################################################################
###### GESTION Class Statistique
###################################################################################################################################################

class Statistique():

    def __init__(self, Stat_ID, Tag, Disp, Targ):
        self.Stat_ID = Stat_ID
        self.Tag    = Tag
        self.disp   = Disp
        self.Targ   = Targ

class StatSimple(Statistique):

    def __init__(self, Stat_ID, Tag, Disp, Targ, Min, Max):
        super().__init__(Stat_ID, Tag, Disp, Targ)
        self.Min = Min
        self.Max = Max

class StatCalc(Statistique):

    def __init__(self, Stat_ID, Tag, Disp, Targ, Calc):
        super().__init__(Stat_ID, Tag, Disp, Targ, Calc)
        self.Calc = Calc

class StatVitale(StatCalc):

    def __init__(self, Stat_ID, Tag, Disp, Targ, Calc):
        super().__init__(Stat_ID, Tag, Disp, Targ, Calc)

class StatExeperience(Statistique):
    def __init__(self, Stat_ID, Tag, Disp, Targ, Max):
        super().__init__(Stat_ID, Tag, Disp, Targ, Max)
        self.Max = Max

###################################################################################################################################################
###### GESTION Fonction
###################################################################################################################################################

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

def Stat_exist(stat : str, guilId : str):
    c = project_Ares_bdd.cursor()
    c.execute("SELECT COUNT(*) as exist FROM statistique \
              WHERE Stat_ServID = '" + guilId + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
    STnow = c.fetchone()
    c.close()

    if STnow[0] == 1:
        return [STnow[0], "La Statistique existe déjà, vérifier Nom/Tag"]
    else:
        return [STnow[0], "La Statistique n'existe pas"]    
    
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

    # Création nouvelle Stat
    @commands.hybrid_command(name="stat_new")
    async def Stat_new(self, ctx : commands.Context, name : str, tag : str, stattype : str, disp : str, target : str):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])
        
        sRet = Stat_exist(tag, str(ctx.guild.id))
        if sRet[0] != 0:
            return await ctx.send(sRet[1])
        
        sRet = Stat_exist(name, str(ctx.guild.id))
        if sRet[0] != 0:
            return await ctx.send(sRet[1])
    
        sRet = Vtag(tag, str(ctx.guild.id))
        if sRet[0] != "OK":
            return await ctx.send(sRet[1])

        sRet = SType(stattype)
        if sRet[0] != "OK":
            return await ctx.send(embed=sRet[1])
    
        sRet = DType(disp)
        if sRet[0] != "OK":
            return await ctx.send(embed=sRet[1])
    
        sRet = TType(target)
        if sRet[0] != "OK":
            return await ctx.send(embed=sRet[1])
        
        c = project_Ares_bdd.cursor()
        c.execute("Insert INTO statistique (Stat_ServID, Stat_Name, Stat_Tag, Stat_Type, Stat_DisplayType, Stat_Cible)" \
            "values ('"+str(ctx.guild.id)+"', '"+name+"', '"+tag+"', '"+stattype+"', '"+disp+"', '"+target+"')")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("La statistique " + name + " a bien été enregistré.")

    # Définition Résumé Stat
    @commands.hybrid_command(name="stat_resume")
    async def Stat_resume(self, ctx : commands.Context, stat : str, *, resume : str):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])

        if len(resume) > 500:
            return await ctx.send("Le résumé est trop long, Limite 500 caractère")

        sRet = Stat_exist(str(stat), str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])

        c = project_Ares_bdd.cursor()
        c.execute("UPDATE statistique SET Stat_Resume = '" + resume + "' WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("Résumé de " + stat + " correctement enregistré.")

    # Définition Calcul Stat
    @commands.hybrid_command(name="stat_calcul")
    async def Stat_calcul(self, ctx : commands.Context, stat : str, *, calcul : str):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])

        sRet = Stat_exist(str(stat), str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])
        
        c = project_Ares_bdd.cursor()
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

        return await ctx.send("Calcul de " + stat + " correctement enregistré")

    # Définition Minimum Stat
    @commands.hybrid_command(name="stat_min")
    async def Stat_min(self, ctx : commands.context, stat : str, min : int):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])
        
        if min < 0: 
            return await ctx.send("Impossible, valeur inférieure ou égale à 0")

        sRet = Stat_exist(str(stat), str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])
        
        c = project_Ares_bdd.cursor()
        c.execute("SELECT Stat_Type, Stat_Max FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
        STnow = c.fetchone()
        if STnow[0] != "SPL": 
            c.close()
            if STnow[0] == "WPE":
                return await ctx.send("Les statistiques de type XPE (expérience) ne peuvent pas changer de min, le plafond maximum lui est modifiable.")
            return await ctx.send("La statistique n'est Pas Simple.")
        
        if STnow[1] < min:
            return await ctx.send("Le minimum est supérieur a l'actuel maximum, impossible de poursuivre.")
        
        c.execute("UPDATE statistique SET Stat_Min ='" + min + "'\
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("Minimum de " + stat + " correctement définie à : " + str(min))

    # Définition Maximum
    @commands.hybrid_command(name="stat_max")
    async def Stat_max(self, ctx : commands.context, stat : str, max : int):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])

        sRet = Stat_exist(str(stat), str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])

        c = project_Ares_bdd.cursor()
        c.execute("SELECT Stat_Type, Stat_Min FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
        STnow = c.fetchone()
        if STnow[0] != "SPL" and STnow[0] != "XPE": 
            c.close()
            return await ctx.send("La statistique n'est Pas Simple.")
        
        if STnow[1] > max:
            return await ctx.send("Le maximum est inférieur a l'actuel minimum, impossible de poursuivre.")
        
        c.execute("UPDATE statistique SET Stat_Max ='" + max + "'\
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("Minimum de " + stat + " correctement définie à : " + str(max))

    # Visualisation Statistique
    @commands.hybrid_command(name="stat_show")
    async def Stat_show(self, ctx : commands.context, stat : str):

        sRet = Stat_exist(str(stat), str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])
        
        c = project_Ares_bdd.cursor()
        c.execute("SELECT Stat_Name, Stat_Tag, Stat_Type, Stat_Calcul, Stat_Resume, Stat_DisplayType, Stat_Cible, Stat_Min, Stat_Max FROM statistique \
                  WHERE Stat_ServID = '" + str(ctx.guild.id) + "' AND Stat_Tag = '" + stat + "' OR Stat_Name = '" + stat + "'")
        Showing = c.fetchone()
        c.close()
        Name = Showing[0]
        Tag = Showing[1]
        Type = Showing[2]
        Calc = Showing[3]
        Resu = Showing[4]
        Disp = Showing[5]
        Targ = Showing[6]
        Min = Showing[7]
        Max = Showing[8]


        embed_stat = discord.Embed(
            title= Name + " [" + Tag + "]"
        )

        if Type == "SPL":
           embed_stat.color = discord.Color.green()
        elif Type == "VIT":
            embed_stat.color = discord.Color.blue()
        elif Type == "XPE":
            embed_stat.color = discord.Color.orange()
        elif Type == "CAL":
            embed_stat.color = discord.Color.purple()

        if Resu != None:
            embed_stat.description = Resu
        else:
            embed_stat.description = "Aucune description pour " + Tag

        embed_stat.add_field(
            name="Type de statistique : " + Type + " . " + variable.StatType_Desig[Type],
            value=variable.StatType_descript[Type]
            )
        
        embed_stat.add_field(
            name="Type d'affichage : " + Disp + " . " + variable.displayType_Desig[Disp],
            value=variable.displayType_descript[Disp]
            )
        
        embed_stat.add_field(
            name="Type d'affectation : " + Targ + " . " + variable.CibleList_Desig[Targ],
            value=variable.CibleList_descript[Targ]
            )
        
        if Type == "CAL" or Type == "VIT":
            if Calc != None:
                embed_stat.add_field(
                    name="Calcul de " + Name,
                    value= Calc 
                )
        elif Type == "SPL":
            embed_stat.add_field(
                name="Min/Max",
                value= "Maximum : " + str(Max) + "\nMinimum : " + str(Min)
            )
        elif Type == "XPE":
            embed_stat.add_field(
                name="Plafond expérience maximum",
                value= "Maximum : " + str(Max)
            )

        await ctx.send(embed=embed_stat)
 
###################################################################################################################################################
###### GESTION ERREUR
###################################################################################################################################################

    @Stat_new.error
    async def Stat_new_Error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error

    @Stat_resume.error
    async def Stat_resume_Error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error
    
    @Stat_calcul.error
    async def Stat_calcul_Error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error
    
    @Stat_min.error
    async def Stat_min_Error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error

    @Stat_max.error
    async def Stat_max_Error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error
    
    @Stat_show.error
    async def Stat_show_Error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error