from datetime import datetime, time, timedelta

import discord
from discord.ext import commands, tasks
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


@tasks.loop(hours=1)
async def process_reminders():
    reminders = db.get_reminders()

    print("checking reminders")
    for reminder in reminders:
        print(f"reminder: {reminder.id}, {reminder.reminder_datetime}")
        if datetime.now() >= reminder.reminder_datetime:
            reading = db.get_reading(reminder.reading_id)

            await bot.get_channel(text_channel_id).send(
                f"Chop chop time to discuss '{reading.title}'"
            )

            db.delete_reminder(reminder.id)


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

    for guild in bot.guilds:
        print(f"- Server: {guild.name} (id: {guild.id})")
        await create_text_channel(guild)

    print("Starting processing reminders task")
    if not process_reminders.is_running():
        process_reminders.start()


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
    reading = db.create_reading(title=title, duration=duration_days)

    now = datetime.now().date()
    today_8am = datetime.combine(now, time(hour=8, minute=0))
    due_date = today_8am + timedelta(days=duration_days)

    db.create_reminder(reading_id=reading.id, reminder_datetime=due_date)

    await ctx.send(f"New reading '{title}' added. Discussion set for {due_date}")


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
    db.update_reading(reading_id, status="done")
    in_progress_readings = db.get_readings(status="in_progress")

    if len(in_progress_readings) == 0:
        in_progress_table = ""
    else:
        in_progress_table = f"```\n{tabulate_db_objects(in_progress_readings)}\n```"

    await ctx.send(
        f"Reading with id {reading_id} marked as done.\nCurrent in-progress readings:{in_progress_table}"
    )


@bot.command()
async def mark_in_progress(ctx, reading_id):
    db.update_reading(reading_id, status="in_progress")
    in_progress_readings = db.get_readings(status="in_progress")

    if len(in_progress_readings) == 0:
        in_progress_table = ""
    else:
        in_progress_table = f"```\n{tabulate_db_objects(in_progress_readings)}\n```"

    await ctx.send(
        f"Reading with id {reading_id} marked as in-progress.\nCurrent in-progress readings:{in_progress_table}"
    )


@bot.command()
async def get_reminders(ctx):
    reminders = db.get_reminders()

    if len(reminders) == 0:
        await ctx.send("No reminders found")
        return

    enriched_reminders = []
    for reminder in reminders:
        reading = db.get_reading(reminder.reading_id)
        enriched_reminders.append(
            {
                "id": reminder.id,
                "reading_id": reading.id,
                "reading_title": reading.title,
                "reminder_datetime": reminder.reminder_datetime,
            }
        )

    table_str = tabulate(enriched_reminders, headers="keys")
    await ctx.send(f"```\n{table_str}\n```")


@bot.command()
async def delete_reminder(ctx, id):
    try:
        db.delete_reminder(id)
    except Exception as e:
        await ctx.send(f"Could not delete reminder id={id}.\n`{e}`")
        return

    await ctx.send(f"Reminder with id {id} deleted")
