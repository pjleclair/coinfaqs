import os
import discord
import requests
import json
import locale

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
base_url = 'https://api.coingecko.com/api/v3/coins/'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
locale.setlocale(locale.LC_ALL, '')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return
    if 'cfaq' in message.content:
        token = message.content.split('cfaq ')[1]
        res = requests.get(base_url + token)
        response = json.loads(res.text)
        id = response["name"]
        ticker = response["symbol"]
        price = response["market_data"]["current_price"]["usd"]
        mcap = response["market_data"]["market_cap"]["usd"]
        mcap_rank = response["market_data"]["market_cap_rank"]
        fdv = response["market_data"]["fully_diluted_valuation"]["usd"]
        vol = response["market_data"]["total_volume"]["usd"]
        desc = response['description']['en']
        info = f"""
            ## {id} ({ticker.upper()})
            
            ### Market Stats:
            **Current Price:**
                {locale.currency(price, grouping=True)}
            **Market Cap Rank:**
                {mcap_rank} 
            **Market Cap:**
                {locale.currency(mcap, grouping=True)} 
            **FDV:**
                {locale.currency(fdv, grouping=True)} 
            **Volume:**
                {locale.currency(vol, grouping=True)} 
            
            ### Description:
            {desc}
        """
        await message.channel.send(info[0:1999])

client.run(TOKEN)