import discord
from discord.ext import commands
from tabulate import tabulate

from .database.dao import TechReadDao
from .utils import tabulate_db_objects

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

TEXT_CHANNEL_NAME = "tech_read"
text_channel_id = None

bot = commands.Bot(command_prefix="!", intents=intents)
db = TechReadDao()


async def create_text_channel(guild):
    global text_channel_id

    text_channel = discord.utils.get(guild.text_channels, name=TEXT_CHANNEL_NAME)
    if text_channel:
        print(
            f"text channel {TEXT_CHANNEL_NAME} already exists, channel_id = {text_channel.id}"
        )
        text_channel_id = text_channel.id
    else:
        category = discord.utils.get(guild.categories, name="Text Channels")
        text_channel = await guild.create_text_channel(
            TEXT_CHANNEL_NAME, category=category
        )
        print(
            f"created text channel {TEXT_CHANNEL_NAME}, channel_id = {text_channel.id}"
        )
        text_channel_id = text_channel.id

    return text_channel


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

    for guild in bot.guilds:
        print(f"- Server: {guild.name} (id: {guild.id})")
        await create_text_channel(guild)


@bot.command(
    help="""
Adds a new reading.

Usage: 
    !add_reading "Title" "Duration (in days)"
    Note: default duration is 7 days

Example: 
    !add_reading "thonk more masterclass" "5"
"""
)
async def add_reading(ctx, title, duration_days=7):
    db.create_reading(title=title, duration=duration_days)
    await ctx.send(
        f"Title of reading is {title}. Duration of reading is {duration_days} days"
    )


@bot.command()
async def get_readings(ctx, status="in_progress"):
    # status = ("in_progress", "done", "all")
    readings = db.get_readings(status=status)
    if len(readings) == 0:
        if status == "all":
            await ctx.send("No readings found")
        else:
            await ctx.send(f"No {status} readings found")

        return

    table_str = tabulate_db_objects(readings)

    await ctx.send(f"```\n{table_str}\n```")


@bot.command()
async def mark_done(ctx, reading_id):
    reading = db.update_reading(reading_id, status="done")
    await ctx.send(f"Reading with id {reading_id} marked as done\n.`{reading}`")


@bot.command()
async def mark_in_progress(ctx, reading_id):
    reading = db.update_reading(reading_id, status="in_progress")
    await ctx.send(f"Reading with id {reading_id} marked as in_progress\n.`{reading}`")


@bot.command()
async def add_reminder(ctx):
    pass


@bot.command()
async def get_reminders(ctx):
    pass


@bot.command()
async def add_note(ctx):
    pass


@bot.command()
async def get_notes(ctx):
    pass
