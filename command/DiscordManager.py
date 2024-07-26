import discord

from discord.ext import commands


class DiscordManager(commands.Cog):
    """Description of what this file does"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="myaccount", brief="Return the discord avatar")
    async def myaccount(self, ctx, user: discord.Member = None):
        """If no user is given, default user is the command invoker"""

        if not user:
            user = ctx.author
        embed = discord.Embed(color=discord.Color.blue())
        embed.add_field(name=f"{user.name}#{user.discriminator}", value=user.display_name)
        embed.add_field(name="Registered", value=user.created_at)
        embed.set_image(url=user.avatar_url_as(size=128))
        embed.set_footer(text=f"Discord ID: {user.id}",
                         icon_url="https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DiscordManager(bot))
