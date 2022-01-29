import json
import discord
import requests
import datetime
from colorama import Fore, init
from discord.ext import tasks

token = 'TOKEN'

init(autoreset=True)
client = discord.Client()


@tasks.loop(hours=5)
async def updateList():
    contents = requests.get(
        "https://raw.githubusercontent.com/nikolaischunk/discord-phishing-links/main/domain-list.json").text
    f = open('./domains.json', 'wb')
    f.write(contents.encode())


@client.event
async def on_ready():
    if not hasattr(client, 'appinfo'):
        client.appinfo = await client.application_info()
    print(Fore.GREEN + 'Logged in as {0.user}'.format(client))
    print(Fore.BLUE + 'Starting list updater...')
    try:
        updateList.start()
    except Exception as e:
        print(e)
    print(Fore.GREEN + 'Finished getting links, bot is ready')
    print(Fore.BLUE +
          "Invite your bot via this link" + Fore.RED + " https://discord.com/api/oauth2/authorize?client_id=" + str(client.appinfo.id) + "&permissions=8&scope=bot")


@client.event
async def on_message(message):
    data = json.load(open('./domains.json'))
    now = datetime.datetime.today()
    date = now.strftime("%m:%d:%Y %H:%M:%S")

    if message.author == client.user:
        return

    for _ in data['domains']:
        if str(_) in message.content:
            await message.delete()
            print(Fore.GREEN + 'Deleted phishing link:')
            print(Fore.BLUE + 'Time: ' + date)
            print(Fore.BLUE + 'Message: ' + message.content)
            print(Fore.BLUE + 'User: ' + str(message.author))
            print(Fore.BLUE + 'User ID: ' + str(message.author.id))
            print(Fore.BLUE + 'Channel ID: ' + str(message.channel.id))
            break
        else:
            pass

try:
    client.run(token)
except Exception as e:
    print(e)
