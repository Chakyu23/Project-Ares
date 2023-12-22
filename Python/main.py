# This example requires the 'message_content' intent.
import mysql.connector
import discord

import Statistique, Common, Serveur, Affinity

from discord.ext import commands
import Config
from Token import TOKEN
from Bdd import project_Ares_bdd

class MyBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix= Config.Config["Command_Prefix"], intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await self.add_cog(Serveur.CogServ(self))
        await self.add_cog(Statistique.CogStat(self))
        await self.add_cog(Affinity.CogAffinity(self))
        await self.add_cog(Common.CogCommon(self))
        await self.tree.sync()
    
    async def on_ready(self) -> None:
        print(Project_Ares_Bot.user.name, " est en ligne avec l'id : ", Project_Ares_Bot.user.id )

Project_Ares_Bot = MyBot()
           
if __name__ == "__main__":
    Project_Ares_Bot.run(TOKEN)


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
