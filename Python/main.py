# This example requires the 'message_content' intent.
import mysql.connector
import discord
# import Statistique
from discord.ext import commands
from Config import Config, connection_params
from Token import Token

bdd = mysql.connector.connect(
    host=connection_params["host"],
    user=connection_params["user"],
    password=connection_params["password"],
    database=connection_params["database"]
)

class MyBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix= Config["Command_Prefix"], intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await self.add_cog(CogStat(self))
        await self.add_cog(CogCommon(self))
        await self.tree.sync()
    
    async def on_ready(self) -> None:
        print(Project_Ares_Bot.user.name, " est en ligne avec l'id : ", Project_Ares_Bot.user.id )
    
Project_Ares_Bot = MyBot()

class CogStat(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = Project_Ares_Bot

    @commands.Cog.listener(name="on_ready")
    async def StatReady(self) -> None:
        print("Commande statistique : OK")

    @commands.command(name="NewStat")
    async def New(self, ctx : commands.Context, name : str, Type : str, Disp : str, Target : str):
        is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
        if is_in_private_message:
            return await ctx.send("Impossible d'utiliser cette commande en message privé")

        has_permission = ctx.author.guild_permissions.administrator
        if has_permission:
            return await ctx.send("Vous n'avez pas les permission pour cette commande")
        return

    @commands.command(name="ResumeStat")
    async def Resume(self, ctx : commands.Context, stat : str, *, resume : str):
        is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
        if is_in_private_message:
            return await ctx.send("Impossible d'utiliser cette commande en message privé")

        has_permission = ctx.author.guild_permissions.administrator
        if has_permission:
            return await ctx.send("Vous n'avez pas les permission pour cette commande")
        return

    @commands.command(name="Stat")
    async def Show(self, ctx : commands.context):
        embed_stat = discord.Embed(
            title="statName",
            description="Je suis une description de stat",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed_stat)

class CogCommon(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = Project_Ares_Bot

    @commands.Cog.listener(name="on_ready")
    async def StatReady(self) -> None:
        print("Commande commune: OK")

    @commands.command(name="clear")
    async def Clear(self, ctx : commands.Context, amount : int = 5) -> discord.Message:
        is_in_private_message = ctx.guild is None and isinstance(ctx.author, discord.User)
        if is_in_private_message:
            return await ctx.send("Impossible d'utiliser cette commande en message privé")

        has_permission = ctx.author.guild_permissions.manage_messages
        if not has_permission:
            return await ctx.send("Vous n'avez pas les permission pour cette commande")

        is_limit_reached = amount > 100
        if is_limit_reached:
            return await ctx.send("Vous ne pouvez pas supprimer plus de 100 message")

        is_text_channel = isinstance(ctx.channel, discord.TextChannel)
        if not is_text_channel:
            return await ctx.send("Vous ne devez appellez cette commande que depuis un channel textuel")

        await ctx.channel.purge(limit=amount+1)

        return await ctx.send(f"{amount} messages supprimés.")
    
    @commands.command(name="example")
    async def Exemple(self, ctx : commands.context):
        embed_exmpl = discord.Embed(
            title="exemple",
            description="Je suis une description d'exemple'",
            color=discord.Color.red()
        )

        embed_exmpl.add_field(
            name="first field",
            value="first field content"
        )

        embed_exmpl.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed_exmpl.set_thumbnail(url=ctx.guild.icon.url)
        embed_exmpl.set_image(url=ctx.guild.icon.url)
        embed_exmpl.set_footer(icon_url=ctx.author.display_avatar.url, text=ctx.author.display_name)


        await ctx.send(embed=embed_exmpl)
           
if __name__ == "__main__":
    Project_Ares_Bot.run(Token)
