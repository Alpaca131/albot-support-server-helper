import aiohttp
import asyncio
import discord
from os import environ
from datetime import timedelta

client = discord.Client()


@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    pass


@client.event
async def on_guild_channel_create(channel: discord.TextChannel):
    if channel.guild.id != 731467468341510184:
        return
    if channel.category_id != 942706945675132978:
        return
    await asyncio.sleep(5)
    messages: discord.Message = await channel.history(oldest_first=True, limit=1).flatten()
    first_message = messages[0]
    user: discord.Member = first_message.mentions[0]
    date = first_message.created_at
    # 期限をチケットオープンの一日後に設定
    date += timedelta(days=1)
    card_info = {
        "name": f"{user.name} {user.id}",
        "desc": f"\#{channel.name}",
        "urlSource": f"https://discord.com/channels/731467468341510184/{channel.id}",
        "due": date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "pos": "top"
    }
    await add_card_to_trello(card_info)


async def add_card_to_trello(card_info: dict):
    url = 'https://api.trello.com/1/cards'
    params = {
        'idList': '61d921f29b60868dd4b62f72',
        'key': environ["TRELLO_KEY"],
        'token': environ["TRELLO_TOKEN"]
    }
    params.update(card_info)
    res = await post(url, params)
    print(res)


async def post(url, params: dict):
    async with aiohttp.request("POST", url, params=params) as resp:
        assert resp.status == 200
        return await resp.json()

client.run(environ["DISCORD_TOKEN"])
