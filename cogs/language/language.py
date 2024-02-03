import discord
from discord.commands import slash_command, Option
import ezcord





class LanguageDB(ezcord.DBHandler):
    def __init__(self):
        super().__init__("data/db/language.db")

    async def setup(self):
        await self.execute(
            """CREATE TABLE IF NOT EXISTS servers(
            server_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'English'
            )"""
        )

    async def get_server_language(self, server_id):
        result = await self.execute("SELECT language FROM servers WHERE server_id=?", (server_id,))
        return result['language'] if result else None

    async def set_server_language(self, server_id, language):
        await self.execute(
            "INSERT OR REPLACE INTO servers (server_id, language) VALUES (?, ?)",
            (server_id, language)
        )


db = LanguageDB()

class Language(ezcord.Cog):

    @slash_command()
    @discord.guild_only()
    @discord.default_permissions(administrator=True)
    async def set(
        self,
        ctx,
        language: Option(str, description="Choose the language", choices=["Deutsch", "English"])
    ):
        server_id = ctx.guild.id
        await db.set_server_language(server_id, language)
        await ctx.defer(ephemeral=True)
        await ctx.respond(embed=self.create_language_embed(ctx.author, language, ctx.guild), ephemeral=True)

    async def get_server_language(self, server_id):
        return await db.get_server_language(server_id) or 'English'

    def create_language_embed(self, user, language, guild):
        embed = discord.Embed(
            title="Bot Language Change",
            description=f"{user.mention} changed the bot's language to {language}! {self.get_language_emoji(language)}",
            color=0x3498db 
        )
        embed.set_footer(text=f"Bot Language Settings | Server: {guild.name}")

        return embed
    

def setup(bot):
    bot.add_cog(Language(bot))
