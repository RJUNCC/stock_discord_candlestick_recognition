from discord import Intents, TextChannel, DMChannel, GroupChannel, Forbidden, HTTPException
from discord.ext import commands
from dotenv import load_dotenv
import os
import time
import hydra
from omegaconf import DictConfig, OmegaConf
from pathlib import Path
from loguru import logger
from typing import Optional, Union, cast
from dataclasses import dataclass

# mandatory config init
WORKSPACE_DIR = Path(__file__).parents[2]
ChannelType = Union[TextChannel, DMChannel, GroupChannel]
cfg = OmegaConf.load(WORKSPACE_DIR / "conf" / "config.yaml")
load_dotenv()

@dataclass
class BotConfig:
    command_prefix: str
    channel_id: int
    token: str

class TypedDiscordBot(commands.Bot):
    def __init__(self, config: BotConfig) -> None:
        intents = Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix=config.command_prefix,
            intents=intents
        )

        self.config = config
        self.startup_time: Optional[float] = None

    async def setup_hook(self) -> None:
        logger.info("Bot is initializing...")
        self.startup_time = time.time()

def create_bot() -> TypedDiscordBot:
    try:
        config = BotConfig(
            command_prefix=cfg.discord.command_prefix,
            channel_id=cfg.discord.channel_id,
            token= cfg.discord.token
        )

        return TypedDiscordBot(config)
    except Exception as e:
        logger.error(f"Failed to create bot: {e}")
        raise

# init bot
# bot = commands.Bot(command_prefix=cfg.discord.command_prefix, intents=intents)
bot = create_bot()

# send activation message to specified channel
@bot.event
async def on_ready():
    """Send activation message to specified channel"""
    channel_id = int(cfg.discord.channel_id)
    channel: Optional[ChannelType] = bot.get_channel(channel_id)

    if channel:
        logger.success(f"Bot has successfully activated in channel id {cfg.discord.channel_id}")
        await channel.send(f"{str(bot.user).replace(r'/d', '')} is activated")

@bot.command()
async def test(ctx, *, arg: Optional[str] = None) -> None:
    logger.info("!test command has been sent")
    try:
        if arg is None:
            await ctx.send("> Need a message: !test <message>")
            logger.success("Sent info message about the command: !test")
        else:
            await ctx.send(arg)
            logger.success("Command successfully called!")
    except HTTPException as e:
        logger.error(f"Failed to send activation message: {e}")
    except Exception as e:
        logger.error(f"There has been an unexpected error: {e}")

bot.run(cfg.discord.token)