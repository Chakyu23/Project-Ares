import discord
from discord.ext import commands
import Config


class CogCommon(commands.Cog):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_ready")
    async def Commonready(self) -> None:
        print("Commande commune: OK")

    @commands.hybrid_command(name="clear")
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
    
    @commands.hybrid_command(name="example")
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

        await ctx.defer()
        await ctx.send(embed=embed_exmpl)