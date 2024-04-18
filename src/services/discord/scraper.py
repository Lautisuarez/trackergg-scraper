from discord.ext import commands
from services.scraper.ScraperTracker import ScraperTracker
import discord

class Scraper(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def stats(self, ctx, username):
        scraper = ScraperTracker(username=username)
        response = scraper.get_stats()
        if not ("error" in response.keys()):
            embed = discord.Embed(
                title=username,
                color=discord.Color.dark_blue()
            )
            for field in response.keys():
                embed.add_field(
                    name=field.capitalize(),
                    value=response[field],
                    inline=False
                )
            await ctx.send(embed=embed)
        else:
            await ctx.send(response["error"])

async def setup(bot):
    await bot.add_cog(Scraper(bot))