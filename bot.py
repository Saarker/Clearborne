# This example requires the 'message_content' intent.
import responses as resp
import os
from discord import Message, Intents, Client
from dotenv import load_dotenv

# TOKEN is stored in .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# BOT SETUP
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# BOT EVENTS
async def on_ready(): # When bot is ready
    print(f'{client.user} has connected to Discord!')
async def send_message(message: Message, user_message: str) -> None: # Send message to channel
    if not user_message or user_message[:1] != '^':
        return
    try:
        response = resp.get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)
         
# BOT STARTUP
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
         
# HANDLING MESSAGES
@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    await send_message(message, message.content)
            
# RUN BOT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
