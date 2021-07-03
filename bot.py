from eventHandler import *
import discord
from discord_slash import SlashCommand
import os
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option, create_choice

client = commands.Bot(command_prefix="rb.", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

guild_ids = [835551754867179580]
categories = [
    create_choice(
        name="Realm of the mad god",
        value="rotmg",
    ),
    create_choice(
        name="Hearthstone",
        value="hearthstone",
    ),
]

@client.event
async def on_ready():
    print("Ready!")

@client.event
async def on_raw_reaction_add(payload):
    await reaction_added(payload, client)
@client.event
async def on_raw_reaction_remove(payload):
    await reaction_removed(payload, client)

@slash.slash(
    name="end",
    guild_ids=guild_ids,
    description="Ends an event.",
    options = [
        create_option(
            name = "turnout",
            description = "The number of people that attended",
            option_type = 4,
            required = True,
        ),
    ]
)
async def _end(ctx, turnout):
    await end_event(ctx, turnout, client)

@slash.slash(
    name="event",
    guild_ids=guild_ids,
    description="Starts a event and creates a category.",
    options = [
        create_option(
            name = "category",
            description = "The category the event is in",
            option_type = 3,
            required = True,
            choices = [
            create_choice(
                name="Realm of the mad god",
                value="rotmg",
            ),
            create_choice(
                name="Hearthstone",
                value="hearthstone",
            ),
            ]
        ),
        create_option(
            name = "name",
            description = "The display name for the event",
            option_type = 3,
            required = True,
        ),
        create_option(
            name = "description",
            description = "Information and details about the event",
            option_type = 3,
            required = True,
        ),
        create_option(
            name = "time",
            description = "When the event will occur",
            option_type = 3,
            required = True,
        ),
    ]
)
async def _event(ctx, category, name, description, time):
    await start_event(ctx, category, name, description, time)

client.run(os.environ.get('EVENTS_BOT_TOKEN'))