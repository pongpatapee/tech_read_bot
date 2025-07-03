import discord
from discord.ext import commands
from .database import TechReadDao

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
db = TechReadDao()

@bot.event
async def on_ready():
    print(f"logged in as {bot.user} test")

@bot.command(help="""
Adds a new reading.

Usage: 
    !add_reading "Title" "Duration (in days)"
    Note: default duration is 7 days

Example: 
    !add_reading "thonk more masterclass" "5"
""")
async def add_reading(ctx, title, duration_days=7):
    db.create_reading(title=title, duration=duration_days)
    await ctx.send(f'Title of reading is {title}. Duration of reading is {duration_days} days')

@bot.command()
async def get_readings(ctx):
    pass

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

