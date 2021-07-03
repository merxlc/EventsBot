import discord
from discord.ext import commands
from events import *

matchtable = {
    'rotmg': "Realm of the Mad God",
    'hearthstone': "Hearthstone",
}

tick_emoji = '<:tick:835557074090983434>'
history_id = 835552730563084299
tick_id = int( tick_emoji.strip('>')[7:] )#860853222864322571

async def start_event(ctx, category, name, description, time):

    """ MESSAGE """
    embed = discord.Embed(title=f'{matchtable[category]} Event', color=0x00ff00)
    embed.add_field(name='Event name', value=name, inline=True)
    embed.add_field(name='Event time', value=time, inline=True)
    embed.add_field(name='Event description', value=description, inline=False)
    embed.set_footer(text="React to the tick to participate")
    message = await ctx.send(embed=embed)
    await message.add_reaction(tick_emoji)

    """ ROLE """
    role = await ctx.guild.create_role(name=f"{ctx.author.display_name}'s Event")

    """ CATEGORY AND CHANNELS """
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        role: discord.PermissionOverwrite(read_messages=True)
    }
    channel_category = await ctx.guild.create_category_channel(f"{ctx.author.display_name}'s Event", overwrites=overwrites)
    plan = await channel_category.create_text_channel(f"Event plan")
    chat = await channel_category.create_text_channel(f"Event chat")

    """ EVENT SAVING """
    ids = IdInfo(sent_from=ctx.channel.id, message=message.id, role=role.id, category=channel_category.id, plan=plan.id, chat=chat.id)
    event = Event(category, name, description, time, ids)
    event.save_to_file()

    """ EXTRA FEEDBACK """
    print('Event started:')
    print(event)

async def end_event(ctx, turnout, client):
    
    """ EVENT IDENTIFICATION """
    channel_id = ctx.channel.id
    event = Event.find_prop(plan=channel_id)

    """ MESSAGES """
    events_channel = client.get_channel(event.ids.sent_from)
    event_message = await events_channel.fetch_message(event.ids.message)
    await event_message.delete()
    history_channel = client.get_channel(history_id)
    embed = discord.Embed(title=f'{matchtable[event.category]} Event Finished', color=0xff0000)
    embed.add_field(name='Event Name', value=event.name, inline=True)
    embed.add_field(name='Turnout', value=turnout, inline=True)
    await history_channel.send(embed=embed)

    """ CHANNELS """
    category = client.get_channel(event.ids.category)
    plan = client.get_channel(event.ids.plan)
    chat = client.get_channel(event.ids.chat)
    await category.delete()
    await plan.delete()
    await chat.delete()

    """ ROLE """
    role = ctx.guild.get_role(event.ids.role)
    await role.delete()

    event.delete()

async def reaction_added(payload, client):

    """ CHECK IF EMOJI IS A TICK """
    if payload.emoji.id == tick_id:

        """ GET CORRESPONDING EVENT """
        event = Event.find_prop(message=payload.message_id)

        """ CHECK IF EVENT EXISTS """
        if event:

            """ GIVES USER ROLE """
            guild = client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            role = guild.get_role(event.ids.role)
            await user.add_roles(role)

async def reaction_removed(payload, client):

    """ CHECK IF EMOJI IS A TICK """
    if payload.emoji.id == tick_id:

        """ GET CORRESPONDING EVENT """
        event = Event.find_prop(message=payload.message_id)

        """ CHECK IF EVENT EXISTS """
        if event:

            """ REMOVES USER ROLE """
            guild = client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            role = guild.get_role(event.ids.role)
            await user.remove_roles(role)