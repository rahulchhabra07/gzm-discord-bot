# bot.py
import re
import os

import airtable
import discord

TOKEN = os.getenv('DISCORD_TOKEN')
AIRTABLE_BASE = os.getenv('AIRTABLE_BASE')
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')

TWITTERS_CHANNEL_ID = 734279723257036800
PUBLIC_TWITTER_CHANNEL_ID = 742495070242209832
TEST_CHANNEL_ID = 756025620588396566

client = discord.Client()
airtable = airtable.Airtable(AIRTABLE_BASE, 'twittermob', AIRTABLE_API_KEY)

# link to twitter handles: https://airtable.com/invite/l?inviteId=invQod2dDd1c8kJVU&inviteToken=ee4e274952d39e69a20938c531659f9b4075bb66fe358e27d6ab330aa292709a

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(msg: discord.Message):

    if msg.channel.id in [TWITTERS_CHANNEL_ID, PUBLIC_TWITTER_CHANNEL_ID, TEST_CHANNEL_ID]:
        words = msg.content.split()
        for word in words:
            if 'twitter.com/' in word:
                match = re.match(r'^https?://(www\.)?twitter\.com/(#!/)?(?P<name>[^/]+)(/\w+)*$', word)
                record = airtable.match('twitter', word)
                if not record:
                    airtable.insert({'twitter': word, 'discord_user': str(msg.author), 'handle': '@'+match.group('name')})


client.run(TOKEN)