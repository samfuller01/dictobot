import requests, os, discord, sys
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()


# Logging if in dev mode
if len(sys.argv) > 1 and sys.argv[1] == 'dev':
    import logging
    logging.basicConfig(level=logging.INFO)

class DictoBot(commands.Bot):
    async def on_ready(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Game('reading a dictionary (^help)'))
        print('Logged in as {0}!'.format(self.user))

def lookup_word(word):
    dictionary_api_key = os.getenv('API_KEY')
    api_url = f'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={dictionary_api_key}'
    r = requests.get(api_url)
    return r.json()

db = DictoBot(command_prefix=os.getenv('PREFIX'))

@db.command()
async def define(ctx, word):
    '''Define a word in Merriam Webster\'s Collegiate Dictonary''' 
    data = lookup_word(word)[0]
    try:
        embed_message = discord.Embed(title=word)
        j = 0
        for i in data['shortdef']:
            embed_message.add_field(name=j+1, value=i, inline=False)
            j += 1
        await ctx.send(embed=embed_message)
    except:
        await ctx.send('That word does not exist in the Merriam Webster Collegiate dictionary.')

db.run(os.getenv('TOKEN'))
