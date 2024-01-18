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

def TagExist(guildID : str, tag : str):
    c = project_Ares_bdd.cursor()
    c.execute("SELECT COUNT(*) as exist FROM tags \
               WHERE Tag_ServID = '" + guildID + "' AND Tag_Tag = '" + tag + "'")
    STnow = c.fetchone()
    c.close()

    if STnow[0] == 1:
         return [STnow[0], tag + " existe déjà, vérifier Nom/Tag"]
    else:
         return [STnow[0], tag + " n'existe pas"]
    
def NameExist(guildID : str, name : str):
    c = project_Ares_bdd.cursor()
    c.execute("SELECT COUNT(*) as exist FROM tags \
               WHERE Tag_ServID = '" + guildID + "' AND Tag_Name = '" + name + "'")
    STnow = c.fetchone()
    c.close()

    if STnow[0] == 1:
         return [STnow[0], name + " existe déjà, vérifier Nom/Tag"]
    else:
         return [STnow[0], name + " n'existe pas"]

def NewTag(guildID : str, name : str = "", tag : str = ""):

    c = project_Ares_bdd.cursor()
    if name != "" and tag != "":
        c.execute("Insert INTO tags (Tag_ServID, Tag_Tag, Tag_Name)" \
            "values ('"+guildID+"', '"+tag+"', '"+name+"')") 
    elif name == "" and tag != "":
        c.execute("Insert INTO tags (Tag_ServID, Tag_Tag)" \
            "values ('"+guildID+"', '"+tag+"')") 
    elif name != "" and tag == "":
        c.execute("Insert INTO tags (Tag_ServID, Tag_Name)" \
            "values ('"+guildID+"', '"+name+"')") 
    else:
        return ["ERROR", "Impossible de récupéré l'ID"]
    
    project_Ares_bdd.commit()
    c.close()

    newID = GetID(guildID, name, tag)

    return newID

def GetID(guildID : str, things):
    
    c = project_Ares_bdd.cursor()
    c.execute("SELECT Tag_ServID FROM Tags WHERE Tag_ServID = '"+ guildID +"' AND Tag_Tag = '"+ things +"' OR Tag_Name = '"+ things +"'")
    newID = c.fetchone()
    c.close()
    if newID[0] == "" or newID[0] == None:
        return ["ERROR", "Impossible de récupéré l'ID"]

    return ["OK", newID[0]]

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
        
        c.execute("DELETE FROM serveur  \
            WHERE Serv_ID ='"+str(ctx.guild.id)+"'")
        project_Ares_bdd.commit()
        c.close()

        return await ctx.send("Le serveur et ses données ont été supprimés")
