# This example requires the 'message_content' intent.
import os
from disnake import Message, Intents, Client, Embed
from disnake.ext import commands
from dotenv import load_dotenv
import profiles, misc

# TOKEN is stored in .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot()

@bot.event      # bot is online
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
@bot.slash_command(
    name="help",
    description="List of commands and their respective uses"
)
async def help(inter):
    await inter.response.defer()
    await inter.edit_original_response(embed=misc.help())
    
@bot.slash_command(
    name="lookup",
    description="Lookup a PSN user"
)
async def lookup(inter, online_id: str):
    await inter.response.defer()
    await inter.edit_original_response(embed=profiles.lookup(online_id))
            


# RUN BOT
def main() -> None:
    bot.run(token=TOKEN)
    
if __name__ == '__main__':
    main()

