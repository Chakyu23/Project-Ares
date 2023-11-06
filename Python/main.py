# This example requires the 'message_content' intent.

import discord
from Config import Config, connection_params
import mysql.connector

bdd = mysql.connector.connect(
    host="localhost",
    user="Bot Ares",
    password="ARES1",
    database="project_ares"
)



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(Config["Command_Prefix"] + "SaveID"):
        await message.channel.send("Your ID is : " + str(message.author.id) + ", It will be now saved" )
        c = bdd.cursor()  
        c.execute("Insert INTO player (Player_ID)" \
            "values ('" + str(message.author.id) + "')")
        bdd.commit()

    if message.content.startswith(Config["Command_Prefix"] + "ID_List"):
        request = "select * from player"
        c = bdd.cursor()
        c.execute(request)
        resultats = c.fetchall()
        for utilisateur in resultats:
            await message.channel.send(utilisateur[1] + " is a user")
           



client.run('MTE2NzQ1MzI4MTE5MTIxMTAwOQ.GkWYhc.KPRCi8MAKXc3GvXAeQZSpfmdCp3sPinzBZyqwI')