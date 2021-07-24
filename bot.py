from eventHandler import *
import discord
from discord_slash import SlashCommand
import os
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option, create_choice
import keyHandler
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

client = commands.Bot(command_prefix="rb.", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

guild_ids = [835551754867179580, 831459694987575306]
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
    name="key",
    guild_ids=guild_ids,
    description="Logs a user's key",
    options = [
        create_option(
            name="user",
            description="The user to add a key for",
            option_type = 6,
            required = True
        )
    ],
    permissions = {
        835551754867179580: [
            create_permission(835952951847288844, SlashCommandPermissionType.ROLE, True),
            create_permission(851883206776193066, SlashCommandPermissionType.ROLE, False)
        ]
    }
)
async def _key(ctx, user):
    keyHandler.add_key(str(user.id))
    await ctx.send(f'Logged a key for {user.mention}')

@slash.slash(
    name="info",
    guild_ids=guild_ids,
    description="Displays your current key count",
    options = [
        create_option(
            name="user",
            description="The user to display the key count of",
            option_type = 6,
            required = False
        )
    ]
)
async def _info(ctx, user=None):
    if user:
        await ctx.send(f'{user.mention} has popped {keyHandler.get_keys(user.id)} key(s)')
    else:
        await ctx.send(f'You have popped {keyHandler.get_keys(ctx.author.id)} key(s)')

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
    ],
    permissions = {
        835551754867179580: [
            create_permission(835952951847288844, SlashCommandPermissionType.ROLE, True),
            create_permission(851883206776193066, SlashCommandPermissionType.ROLE, False)
        ]
    }
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
                create_choice(
                    name="Terraria",
                    value="terraria",
                )
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
    ],
    permissions = {
        835551754867179580: [
            create_permission(835952951847288844, SlashCommandPermissionType.ROLE, True),
            create_permission(851883206776193066, SlashCommandPermissionType.ROLE, False)
        ]
    }
)
async def _event(ctx, category, name, description, time):
    await start_event(ctx, category, name, description, time)

client.run(os.environ.get('EVENTS_BOT_TOKEN'))