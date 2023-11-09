# This example requires the 'message_content' intent.
import mysql.connector
import discord
import Statistique
from discord.ext import commands
from Config import Config, connection_params
from Token import Token


bdd = mysql.connector.connect(
    host="localhost",
    user="Bot Ares",
    password="ARES1",
    database="project_ares"
)

class MyBot(commands.bot):
    def __init__(self) -> None:
        super().__init__(command_prefix= Config["Command_Prefix"], intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await self.tree.sync()
    
    async def on_ready(self) -> None:
        print(Project_Ares_Bot.user.name, " est en ligne avec l'id : ", Project_Ares_Bot.user.id )
    
Project_Ares_Bot = MyBot()

# @Project_Ares_Bot.event
# async def on_message(message : discord.Message):
#     if message.author.bot:
#         return
# 
#     if "bonjour" in message.content:
#         await message.channel.send("Bonjour !")

@commands.command()
async def Clear(ctx : commands.Context, amount : str = 5) -> discord.Message:
    is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_message:
        return await ctx.send("Impossible d'utiliser cette commande en message privé")
    
    has_permission = ctx.author.guild_permissions.manage_messages
    if has_permission:
        return await ctx.send("Vous n'avez pas les permission pour cette commande")
    
    is_limit_reached = amount > 100
    if is_limit_reached:
        return await ctx.send("Vous ne pouvez pas supprimer plus de 100 message")
    
    is_text_channel = isinstance(ctx.channel, discord.TextChannel)
    if not is_text_channel:
        return await ctx.send("Vous ne devez appellez cette commande que depuis un channel textuel")
    
    await ctx.channel.purge(limit=amount+1)

    return await ctx.send(f"{amount} messages supprimés.")


async def NewStat(ctx : commands.Context, name : str, Type : str, Disp : str, Target : str):
    is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_message:
        return await ctx.send("Impossible d'utiliser cette commande en message privé")
    
    has_permission = ctx.author.guild_permissions.administrator
    if has_permission:
        return await ctx.send("Vous n'avez pas les permission pour cette commande")
    return



async def ResumeStat(ctx : commands.Context, stat : str, *, resume : str):
    is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_message:
        return await ctx.send("Impossible d'utiliser cette commande en message privé")
    
    has_permission = ctx.author.guild_permissions.administrator
    if has_permission:
        return await ctx.send("Vous n'avez pas les permission pour cette commande")
    return

async def Stat(ctx : commands.context, stat : str):
    embed_stat = discord.embeds(
        title="statName",
        description="Je suis une description de stat",
        color=discord.Color.blue()
    )

    return ctx.send(embed=embed_stat)

Project_Ares_Bot.add_command(Clear)
Project_Ares_Bot.add_command(NewStat)
Project_Ares_Bot.add_command(ResumeStat)
Project_Ares_Bot.add_command(Stat)

















# guild_id = ""

# intents = discord.Intents.default()
# intents.message_content = True

# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')
    
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith(Config["Command_Prefix"] + "SaveID"):
#         await message.channel.send("Your ID is : " + str(message.author.id) + ", It will be now saved" )
#         c = bdd.cursor()  
#         c.execute("Insert INTO player (Player_ID)" \
#             "values ('" + str(message.author.id) + "')")
#         bdd.commit()

#     if message.content.startswith(Config["Command_Prefix"] + "ID_List"):
#         request = "select * from player"
#         c = bdd.cursor()
#         c.execute(request)
#         resultats = c.fetchall()
#         for utilisateur in resultats:
#             await message.channel.send(utilisateur[1] + " is a user")
           
if __name__ == "__main__":
    Project_Ares_Bot.run(Token)
