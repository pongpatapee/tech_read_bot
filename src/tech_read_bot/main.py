"""
Main entry point for the Reading Bot Discord application.
"""

import os
import sys
from dotenv import load_dotenv

from .bot import bot

def main():
    # Load environment variables
    load_dotenv()
    
    # Get bot token from environment
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ Error: DISCORD_TOKEN not found in environment variables.")
        print("Please create a .env file with your Discord bot token:")
        print("DISCORD_TOKEN=your_bot_token_here")
        sys.exit(1)
    
    bot.run(token)


if __name__ == "__main__":
    main()
