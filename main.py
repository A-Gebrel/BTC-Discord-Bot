import discord, requests, json, time, os.path
from discord import app_commands

def get_config():
    config = []
    with open('config.json', 'r', encoding='utf-8') as file_object:
        config = json.load(file_object)
    return config

config = get_config()

# Ask for Token on start
# Another way of using this would be a config file or env variables
DISCORD_TOKEN = config['discord_token']
API_KEY = config['api_key']

# Check if config.json exists in the directory
if(os.path.exists('config.json') == False):
    print("[ERROR] Config.json not found.")
    exit()

# Let's confirm Discord Token is -probably- valid from default config.json
if(DISCORD_TOKEN == "discord_bot_token_here" or DISCORD_TOKEN == None or DISCORD_TOKEN == ""):
    print("[ERROR] Please add a valid Discord Bot Token!")
    exit()

# Let's confirm API is -probably- valid from default config.json
if(API_KEY == "api_key_here" or API_KEY == None or API_KEY == ""):
    print("[ERROR] Please add a valid CoinMarketCap API Key!")
    exit()

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BTC Transactions ❤"))
        # print(f"Logged in as {self.user}")


client = client()
tree = app_commands.CommandTree(client)

# Grabbing Confirmations count using method mentioned here
# https://stackoverflow.com/questions/14989481/blockchain-api-to-determine-transaction-confirmations
@tree.command(name = "check", description = "Used to check transaction confirmation status")
async def check(interaction, txid:str):
    res = requests.get(f'https://mempool.space/api/tx/{txid}/status')
    if(res.status_code != 200):
        await interaction.response.send_message(f"is {txid} a valid TXID? :'(")
    else:
        res = res.json()
        if(res['confirmed'] == False):
            embed=discord.Embed(title="Transaction Status", url=f"https://mempool.space/tx/{txid}", description="Transaction has not been confirmed yet", color=0xFF0000)
            embed.add_field(name="Not Confirmed Yet", value=f"{txid}", inline=False)
            embed.set_footer(text="Made with ❤ by banonkiel#0001")
            await interaction.response.send_message(embed=embed)
        else:
            txheight = int(res['block_height'])
            res3 = requests.get(f'https://mempool.space/api/blocks/tip/height')
            curheight = int(res3.json())
            confirmations = curheight - txheight + 1
            embed=discord.Embed(title="Transaction Status", url=f"https://mempool.space/tx/{txid}", description="Transaction has been confirmed", color=0x04ff00)
            embed.add_field(name=f"Confirmed [{confirmations}]", value=f"{txid}", inline=False)
            embed.set_footer(text="Made with ❤ by banonkiel#0001")
            await interaction.response.send_message(embed=embed)

@tree.command(name = "fees", description = "Used to get optimal BTC fees")
async def fees(interaction):
    res = requests.get(f'https://mempool.space/api/v1/fees/recommended')
    if(res.status_code != 200):
        await interaction.response.send_message(f"Is mempool down? :'(")
    else:
        resp = res.json()
        embed=discord.Embed(title="Optimal Fees", url=f"https://mempool.space/", description="Below you can see all the suggested fees.\n Remember that mining blocks might take longer if the network is congested.", color=0x04ff00)
        embed.add_field(name=f"Within 10 mins (next block)", value=f"{resp['fastestFee']} sat/vB", inline=False)
        embed.add_field(name=f"Within 30 mins", value=f"{resp['halfHourFee']} sat/vB", inline=False)
        embed.add_field(name=f"Within 60 mins", value=f"{resp['hourFee']} sat/vB", inline=False)
        embed.add_field(name=f"Don't hold your breath ", value=f"{resp['economyFee']} sat/vB", inline=False)
        embed.add_field(name=f"Won't be purged: ", value=f"{resp['minimumFee']} sat/vB", inline=False)
        embed.add_field(name=f"Fetched at", value=f"<t:{int(time.time())}:R>")
        embed.set_footer(text="Made with ❤ by banonkiel#0001")
        await interaction.response.send_message(embed=embed)

@tree.command(name="price", description = "Used to get current BTC price")
async def price(interaction, crypto:str):
    headers = {
        'Accepts': 'application/json',
        "X-CMC_PRO_API_KEY": API_KEY
    }
    session = requests.Session()
    session.headers.update(headers)

    if(crypto == "BTC" or crypto == "ETH"):
        pass
    else:
        await interaction.response.send_message("Invalid/Unsupport Crypto | Currently we only support BTC/ETH")
        return
    
    res = session.get("https://pro-api.coinmarketcap.com/v1/tools/price-conversion", params={"amount": 1, "symbol": crypto})
    if(res.status_code != 200):
        await interaction.response.send_message("Can't reach Coinmarket API?")
    else:
        resp = res.json()
        price = resp['data']['quote']['USD']['price']
        # price = '%.2f'%(price)
        price = f"{price:,.2f}"
        if(id == 1):
            embed=discord.Embed(title="Current BTC Price", url=f"https://coinmarketcap.com/currencies/bitcoin/", description="Below you can see current Bitcoin Price", color=0x04ff00)
            embed.add_field(name=f"Bitcoin Price", value=f"${price} USD", inline=False)
        else:
            embed=discord.Embed(title="Current ETH Price", url=f"https://coinmarketcap.com/currencies/ethereum/", description="Below you can see current Ethereum Price", color=0x04ff00)
            embed.add_field(name=f"Ethereum Price", value=f"${price} USD", inline=False)
        embed.add_field(name=f"Fetched at", value=f"<t:{int(time.time())}:R>")
        embed.set_footer(text="Made with ❤ by banonkiel#0001")
        await interaction.response.send_message(embed=embed)

@tree.command(name = "help", description = "Bot help & Commands List")
async def help(interaction):
    embed=discord.Embed(title="Help & Commands List", description="Thank you for using this crappy bot, hope you liked it so far.", color=0x04ff00)
    embed.add_field(name=f"/help", value=f"Displays this message and currently supported commands", inline=False)
    embed.add_field(name=f"/fees", value=f"Shows BTC fees depending on how fast you need it confirmed", inline=False)
    embed.add_field(name=f"/price", value=f"used as /price <BTC/ETH> to list current price of BTC or ETH (more crypto support soon)", inline=False)
    embed.add_field(name=f"/check", value=f"used to check a BTC transaction for confirmations and list how many confirmations transaction has if confirmed.", inline=False)
    embed.set_footer(text="Made with ❤ by banonkiel#0001")
    await interaction.response.send_message(embed=embed)

client.run(DISCORD_TOKEN)