from discord.ext import commands
import discord
import Serveur
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
        return [STnow[0], Affinity + " existe déjà"]
    else:
        return [STnow[0], Affinity + " n'existe pas"]
    
def Affinity_check(strong : str, weak : str, guildId : str):
    c = project_Ares_bdd.cursor()
    c.execute("SELECT COUNT(*) as exist FROM affinity_rel  \
              WHERE AffinityRel_ServID = '" + guildId + "' AND (AffinityRel_Strong = '" + strong + "' AND AffinityRel_Weak = '" + weak + "') \
              OR (AffinityRel_Strong = '" +  weak + "' AND AffinityRel_Weak = '" + strong + "')  ")
    STnow = c.fetchone()
    c.close()

    if STnow[0] == 1:
        return [STnow[0], "La relation d'affinité existe déjà"]
    else:
        return [STnow[0], "La relation d'affinité n'existe pas"]

def Rel_Affinity_Exist(rel_id : str, guilId : str):
    c = project_Ares_bdd.cursor()
    c.execute("SELECT COUNT(*) as exist FROM affinity_rel \
              WHERE Affinity_ServID = '" + guilId + "' AND AffinityRel_ID = '" + rel_id  + "'")
    STnow = c.fetchone()
    c.close()

    if STnow[0] == 1:
        return [STnow[0], rel_id + " existe déjà"]
    else:
        return [STnow[0], rel_id + " n'existe pas"]

###################################################################################################################################################
###### GESTION Commandes
###################################################################################################################################################

class CogAffinity(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_ready")
    async def stat_ready(self) -> None:
        print("Commande Affinity : OK")

    @commands.hybrid_command(name="new_affinity")
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
    async def Affinity_StrongTo(self, ctx : commands.context, strong : str, weak : str, ratio : int):
        
        if len(weak) > 3 or len(strong) > 3:
            return await ctx.send("Uniquement des tag sont accepter lors de la création de relation d'affinité, \
                                   utilisé /affinity_all pour récupéré la liste de toutes les affinité")

        sRet = Affinity_exist(strong, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])

        sRet = Affinity_exist(weak, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])
        
        sRet = Affinity_check(strong, weak, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])

        ratio = round(ratio, 2)

        if ratio > 10:
            return await ctx.send("Facteur trop important, veuillez entré un facteur entre 10 et 1")

        if ratio < 1:
            return await ctx.send("Facteur trop faible, veuillez entré un facteur entre 10 et 1")
        
        c = project_Ares_bdd.cursor()
        c.execute("Insert INTO affinity_rel (AffinityRel_ServID, AffinityRel_Strong, AffinityRel_Weak, AffinityRel_Factor, AffinityRel_ID)" \
            "values ('"+str(ctx.guild.id)+"', '"+ strong +"', '"+ weak +"', '"+ ratio +"', '"+ strong+weak +"')")
        project_Ares_bdd.commit()
        c.close()
        
        return await ctx.send("La relation d'affinité " + strong + " : " + ratio + " contre " + weak + " a bien été enregistré.")

    @commands.hybrid_command(name="affinity_rel")
    async def Affinity_StrongTo(self, ctx : commands.context, affinity : str):
        sRet = Affinity_exist(affinity, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[2])
        
        c = project_Ares_bdd.cursor()
        c.execute("SELECT Affinity_Tag, Affinity_Name, Affinity_Resume FROM affinity \
          WHERE Affinity_ServID = '" + ctx.guild.id + "' AND Affinity_Tag = '" + affinity + "' OR Affinity_Name = '" + affinity + "'")

        aff = c.fetchone()

        embed_AffinityRelList = discord.Embed(
            title="Liste des Relation d'affinité de " + aff[1] + " - " + aff[0],
            description= aff[2],
            color= discord.Color.green()
        )

        c.execute("SELECT AffinityRel_ID, AffinityRel_weak, AffinityRel_Factor, AffinityRel_Imune FROM affinity_rel \
                  WHERE AffinityRel_ServID = '"+ ctx.guild.id +"' AND AffinityRel_Strong = '"+ aff[0] +"'")
        weaker = c.fetchall()
        for i in range(len(weaker)):

            if weaker[i][0] == 1:
                imn = "oui"
            else:
                imn = "non"

            embed_AffinityRelList.add_field(
            name="Fort contre : " +  + " - " + weaker[i][1],
            value="ID : " + weaker[i][0] + " \n\r \
                Ratio : " + weaker[i][2] + " \n\r \
                Imune : " + imn
            )
        
        c.execute("SELECT AffinityRel_ID, AffinityRel_Strong, AffinityRel_Factor, AffinityRel_Imune FROM affinity_rel \
                  WHERE AffinityRel_ServID = '"+ ctx.guild.id +"' AND AffinityRel_Weak = '"+ aff[0] +"'")
        stronger = c.fetchall()
        for i in range(len(stronger)):

            if stronger[i][0] == 1:
                imn = "oui"
            else:
                imn = "non"

            embed_AffinityRelList.add_field(
            name="Faible contre : " +  + " - " + stronger[i][1],
            value="ID : " + stronger[i][0] + " \n\r \
                Ratio : " + stronger[i][2] + " \n\r \
                Imune : " + imn
            )

        c.close()

        return ctx.send(embed=embed_AffinityRelList)

    @commands.hybrid_command(name="affinity_ratio")
    async def Affinity_Ratio(self, ctx : commands.context, affinity_relation_id : str, ratio : str):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])

        sRet = Affinity_exist(affinity_relation_id, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[2])

        ratio = round(ratio, 2)

        if ratio > 10:
            return await ctx.send("Facteur trop important, veuillez entré un facteur entre 10 et 1")

        if ratio < 1:
            return await ctx.send("Facteur trop faible, veuillez entré un facteur entre 10 et 1")
        
        c = project_Ares_bdd.cursor()
        c.execute("UPDATE affinity_rel SET AffinityRel_Factor = '" + ratio + "' \
                  WHERE AffinityRel_ServID = '" + str(ctx.guild.id) + "' AND AffinityRel_ID = '" + affinity_relation_id +"'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("Ratio mis à jour")

    @commands.hybrid_command(name="affinity_imune")
    async def Affinity_Imune(self, ctx : commands.context, affinity_relation_id : str, imune : str):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])

        sRet = Affinity_exist(affinity_relation_id, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[2])

        if imune == "oui":
            imn = 1
        elif imune == "non":
            imn = 0
        else:
            return await ctx.send("Réponse invalide, seul oui/non est accepter pour l'imunitée")
        
        c = project_Ares_bdd.cursor()
        c.execute("UPDATE affinity_rel SET AffinityRel_Imune = '" + imn + "' \
                  WHERE AffinityRel_ServID = '" + str(ctx.guild.id) + "' AND AffinityRel_ID = '" + affinity_relation_id +"'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("immunité mise à jour")

    @commands.hybrid_command(name="affinity_remove_rel")
    async def Affinity_Rel_Suppr(self, ctx : commands.context, affinity_relation_id : str):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])

        sRet = Affinity_exist(affinity_relation_id, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[2])
        
        c = project_Ares_bdd.cursor()
        c.execute("DELETE FROM affinity_rel WHERE AffinityRel_ServID = '" + str(ctx.guild.id) + "' AND AffinityRel_ID = '" + affinity_relation_id +"'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("relation Supprimée")

    @commands.hybrid_command(name="affinity_img")
    async def Affinity_Resume(self, ctx : commands.context, affinity : str, link : str):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])

        sRet = Affinity_exist(affinity, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])
        
        

        c = project_Ares_bdd.cursor()
        c.execute("UPDATE affinity SET Affinity_Img = '" + link + "' \
                  WHERE Affinity_ServID = '" + str(ctx.guild.id) + "' AND Affinity_Tag = '" + affinity + "' OR Affinity_Name = '" + affinity + "'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("Résumé de " + affinity + " correctement enregistré.")


    @commands.hybrid_command(name="affinity_resume")
    async def Affinity_Resume(self, ctx : commands.context, affinity : str, *, resume : str):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])

        sRet = Affinity_exist(affinity, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])

        if len(resume) > 1500:
            return await ctx.send("Le résumé est trop long, Limite 1500 caractère")


        c = project_Ares_bdd.cursor()
        c.execute("UPDATE affinity SET Affinity_Resume = '" + resume + "' \
                  WHERE Affinity_ServID = '" + str(ctx.guild.id) + "' AND Affinity_Tag = '" + affinity + "' OR Affinity_Name = '" + affinity + "'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("Résumé de " + affinity + " correctement enregistré.")

    @commands.hybrid_command(name="suppr_affinity")
    async def Affinity_Suppr(self, ctx : commands.context, affinity : str):
        sRet = Serveur.AlphaPerm(ctx)
        if sRet[0] != "OK" :
            return await ctx.send(sRet[1])

        sRet = Affinity_exist(affinity, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])

        c = project_Ares_bdd.cursor()
        c.execute("DELETE FROM affinity WHERE Affinity_ServID = '"+ ctx.guild.id +"' AND Affinity_Tag = '"+ affinity +"' OR Affinity_affinity = '"+ affinity +"'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("L'affinité " + affinity + " a bien été Supprimé.")

    @commands.hybrid_command(name="affinity_all")
    async def Affinity_All(self, ctx : commands.context):
        c = project_Ares_bdd.cursor()
        c.execute("SELECT Affinity_Tag, Affinity_Name, FROM affinity \
          WHERE Affinity_ServID = '" + ctx.guild.id +"'")

        listAff = ""

        aff = c.fetchall()
        for i in range(len(aff)):
            listAff += aff[i][1] +" - "+ aff[i][0] +"\n\r"

        embed_AffinityList = discord.Embed(
            title="Affinités",
            description= listAff,
            color= discord.Color.green()
        )

        c.close()

        return await ctx.send(embed=embed_AffinityList)
    
    @commands.hybrid_command(name="affinity")
    async def Affinity_All(self, ctx : commands.context, affinity : str):

        sRet = Affinity_exist(affinity, str(ctx.guild.id))
        if sRet[0] != 1:
            return await ctx.send(sRet[1])

        c = project_Ares_bdd.cursor()
        c.execute("SELECT Affinity_Tag, Affinity_Name, Afinity_Resume, Affinity_img FROM affinity \
          WHERE Affinity_ServID = '" + ctx.guild.id +"'  AND Affinity_Tag ='"+ affinity +"' OR Affinity_Name='"+ affinity +"'" )

        aff = c.fetchone()

        if aff[3] != None:
            img = aff[3]

        embed_Affinity = discord.Embed(
            title="**"+aff[1]+"** - " + aff[0],
            description= aff[2],
            color= discord.Color.green()
        )
        embed_Affinity.set_thumbnail = img

        c.close()

        return await ctx.send(embed=embed_Affinity)
    


###################################################################################################################################################
###### GESTION ERREUR
###################################################################################################################################################

    @Affinity_new.error
    async def Affinity_new_error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error

    @Affinity_StrongTo.error
    async def affinity_StrongTo_error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error
    
    @Affinity_Resume.error
    async def Affinity_Resume_error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error

    @Affinity_Suppr.error
    async def Affinity_Suppr_error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error