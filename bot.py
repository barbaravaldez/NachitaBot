import discord
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 
clientAI = OpenAI()
intents = discord.Intents.default()
intents.message_content = True
intents.emojis_and_stickers = True
intents.guild_messages = True
client = discord.Client(intents=intents)

def openAI_response(url, author):
    greetings_map = {
       '''
            Add discord username for further customization
       '''
    }
    
    greetings = greetings_map.get(author, "Hi, Friend!")
    
    response = clientAI.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "You are an orange pomeranian named Nachita. You are super cute, but also kind of witty as well. When you see a photo of an orange pomeranian, I want you to describe it in first person by saying how were you feeling or what were you thinking when the photo was taken. Please limit your response to 30 words. Please introduce this greeting to your response: " + greetings + " and make sure to use simple language." },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": url,
                        },
                    },
                ],
            }
        ],
        max_tokens=50,
    )
    return response.choices[0].message.content


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if not message.content.startswith('$describe'):
        return
    
    if message.attachments:
        for attachment in message.attachments:
            url = attachment.url
            response = openAI_response(url, message.author.name)
            await message.channel.send(response)

client.run(os.getenv('DISCORD_TOKEN'))



