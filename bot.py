import os
import discord
import requests
import json
import locale

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
CMC_API_KEY = os.getenv('CMC_API_KEY')
base_url = 'https://api.coingecko.com/api/v3/coins/'
cmc_url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CMC_API_KEY
}
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return
    if 'cfaq' in message.content.lower() and 'cfaq $' not in message.content.lower():
        token = message.content.lower().split('cfaq ')[1]
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
    elif 'cfaq $' in message.content.lower():
        symbol = message.content.lower().split('cfaq $')[1]
        parameters = {
            'symbol': symbol
        }
        session = requests.Session()
        session.headers.update(headers)
        try:
            response = session.get(cmc_url, params=parameters)
            data = json.loads(response.text)
            print(symbol)
            print(data['data'][symbol.upper()][0])
            id = data['data'][symbol.upper()][0]['name']
            ticker = data['data'][symbol.upper()][0]['symbol']
            # price = response["market_data"]["current_price"]["usd"]
            # mcap = response["market_data"]["market_cap"]["usd"]
            # mcap_rank = response["market_data"]["market_cap_rank"]
            # fdv = response["market_data"]["fully_diluted_valuation"]["usd"]
            # vol = response["market_data"]["total_volume"]["usd"]
            desc = data['data'][symbol.upper()][0]['description']
            info = f"""
                ## {id} ({ticker})
                
                ### Description:
                {desc}
            """
            await message.channel.send(info[0:1999])
        except:
            print('Error fetching CMC data')

client.run(TOKEN)