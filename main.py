import discord, requests
from discord import app_commands

DISCORD_TOKEN = "MTEwNzQzMDQ1NTA1NTIzNzEyMg.G4XYvX.f-4-HsA9ravFsyf3pAOMMiR1att0TmjWD91_Gs"

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

# Grabbing Confirmations count using method mentioned here
# https://stackoverflow.com/questions/14989481/blockchain-api-to-determine-transaction-confirmations
@tree.command(name = "check", description = "Used to check transaction confirmation status")
async def first_command(interaction, txid:str):
    res = requests.get(f'https://mempool.space/api/tx/{txid}/status')
    if(res.status_code != 200):
        await interaction.response.send_message(f"is {txid} a valid TXID? :'(")
    else:
        res = res.json()
        if(res['confirmed'] == False):
            embed=discord.Embed(title="Transaction Status", url=f"https://mempool.space/tx/{txid}", description="Transaction has not been confirmed yet", color=0xFF0000)
            embed.add_field(name="Not Confirmed Yet", value=f"{txid}", inline=False)
            embed.set_footer(text="Developed by banonkiel#0001")
            await interaction.response.send_message(embed=embed)
        else:
            res2 = requests.get(f'https://blockchain.info/rawtx/{txid}')
            resp2 = res2.json()
            txheight = resp2['block_height']
        
            res3 = requests.get(f'https://blockchain.info/latestblock')
            resp3 = res3.json()
            curheight = resp3['height']

            confirmations = curheight - txheight + 1
            # print(confirmations)
            # await interaction.response.send_message(f"Transaction has been confirmed :) [{confirmations} confirmation(s)]")
            embed=discord.Embed(title="Transaction Status", url=f"https://mempool.space/tx/{txid}", description="Transaction has been confirmed", color=0x04ff00)
            embed.add_field(name=f"Confirmed [{confirmations}]", value=f"{txid}", inline=False)
            embed.set_footer(text="Developed by banonkiel#0001")
            await interaction.response.send_message(embed=embed)

client.run(DISCORD_TOKEN)