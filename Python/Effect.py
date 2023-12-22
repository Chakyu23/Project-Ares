import discord
from discord.ext import commands
import Serveur
import variable
from Bdd import project_Ares_bdd

###################################################################################################################################################
###### GESTION Class Effect
###################################################################################################################################################

class Effect:
    def __init__(self, Effect_ID, Tag, Type, Balance, EffTab : list) -> None:
        self.Effect_ID = Effect_ID
        self.Tag = Tag
        self.Type = Type
        self.Balance = Balance
        self.EffTab = EffTab

class Buff(Effect):
    def __init__(self, Effect_ID, Tag, Type, Balance, EffTab, Duration) -> None:
        super().__init__(Effect_ID, Tag, Type, Balance, EffTab)
        self.Duration = Duration

class InstantEffect(Effect):
    def __init__(self, Effect_ID, Tag, Type, Balance, EffTab) -> None:
        super().__init__(Effect_ID, Tag, Type, Balance, EffTab)

class LongEffect(Effect):
    def __init__(self, Effect_ID, Tag, Type, Balance, EffTab, Duration, Timer) -> None:
        super().__init__(Effect_ID, Tag, Type, Balance, EffTab)
        self.Duration = Duration
        self.Timer = Timer

###################################################################################################################################################
###### GESTION Fonction
###################################################################################################################################################



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

    @commands.hybrid_command(name="effect_new")
    async def Effect_New(self, ctx : commands.Context, name : str, tag : str, efftype : str):
        ""

###################################################################################################################################################
###### GESTION ERREUR
###################################################################################################################################################    
        
    @Effect_New.error
    async def Effect_New_error(Cog, ctx : commands.Context, error : commands.CommandError):
        raise error