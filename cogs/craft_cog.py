import discord
from discord.ext import commands
import shlex
import argparse
from core.math_engine import MathEngine
from core.formatter import Formatter

class CraftArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)

class CraftingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="craft")
    async def craft_cmd(self, ctx, *, raw_args: str):
        parser = CraftArgumentParser(add_help=False)
        parser.add_argument('tier', type=str)
        parser.add_argument('item_name', type=str)
        parser.add_argument('-q', '--quantity', type=int, default=1)
        parser.add_argument('-v', '--value', type=float, default=0.0)
        parser.add_argument('-s', action='store_true')
        parser.add_argument('-selfless', action='store_true')
        parser.add_argument('-self2', action='store_true')
        parser.add_argument('-notax', action='store_true')
        parser.add_argument('-reforge', action='store_true')
        parser.add_argument('-silver', action='store_true')
        parser.add_argument('-consumable', action='store_true')
        parser.add_argument('-mia', action='store_true')
        parser.add_argument('-ms', action='store_true')
        parser.add_argument('-sims', type=int, default=0)
        parser.add_argument('-w', '--wage', type=float, default=50.0)
        parser.add_argument('-barding', type=str, default=None)
        parser.add_argument('-sacrifice', type=str, default=None)
        parser.add_argument('-recipient', type=str, default=None)
        parser.add_argument('-monster_part', type=str, default=None)

        try:
            parsed_args, unknown = parser.parse_known_args(shlex.split(raw_args))
        except ValueError as e:
            await ctx.send(f"**Argument Parsing Error:** {e}\n*Usage example:* `!craft rare \"Flaming Sword\" -s -sims 1 <@12345>`")
            return

        assistants = [tag for tag in unknown if tag.startswith('<@') and tag.endswith('>')]
        unpaid = 0 if parsed_args.selfless else (2 if parsed_args.self2 else 1)

        try:
            data = MathEngine.calculate(
                tier=parsed_args.tier,
                value=parsed_args.value,
                quantity=parsed_args.quantity,
                reforge=parsed_args.reforge,
                silver=parsed_args.silver,
                barding_size=parsed_args.barding,
                consumable=parsed_args.consumable,
                sacrifice_tier=parsed_args.sacrifice,
                mia=parsed_args.mia,
                ms=parsed_args.ms,
                sims=parsed_args.sims,
                assistants_count=len(assistants),
                wage_rate=parsed_args.wage,
                unpaid_workers_count=unpaid,
                notax=parsed_args.notax
            )
        except Exception as e:
            await ctx.send(f"**Calculation Error:** {e}")
            return

        parsed_args.recipient_ping = parsed_args.recipient

        ledger = Formatter.render(
            data=data,
            lead_ping=ctx.author.mention,
            item_name=parsed_args.item_name,
            args=parsed_args,
            assistants=assistants
        )

        await ctx.send(ledger)

async def setup(bot):
    await bot.add_cog(CraftingCog(bot))
