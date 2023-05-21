import discord, requests
from discord import app_commands

DISCORD_TOKEN = ""

if(DISCORD_TOKEN == "AUTH_TOKEN_HERE" or DISCORD_TOKEN == None or DISCORD_TOKEN == ""):
    print("[ERROR] Please add a valid Discord Bot Token!")
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
        # print(f"Logged in as {self.user}")


client = client()
tree = app_commands.CommandTree(client)
    
@tree.command(name = "check", description = "Used to check transaction confirmation status")
async def first_command(interaction, txid:str):
    res = requests.get(f'https://mempool.space/api/tx/{txid}/status')
    if(res.status_code != 200):
        await interaction.response.send_message(f"is {txid} a valid TXID? :'(")
    else:
        res = res.json()
        if(res['confirmed'] == False):
            await interaction.response.send_message(f"Transaction not confirmed yet :(")
        else:
            res2 = requests.get(f'https://blockchain.info/rawtx/{txid}')
            resp2 = res2.json()
            txheight = resp2['block_height']
        
            res3 = requests.get(f'https://blockchain.info/latestblock')
            resp3 = res3.json()
            curheight = resp3['height']

            confirmations = curheight - txheight + 1
            # print(confirmations)
            await interaction.response.send_message(f"Transaction has been confirmed :) [{confirmations} confirmation(s)]")

client.run(DISCORD_TOKEN)