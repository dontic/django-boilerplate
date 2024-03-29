import os
from discord_webhook import DiscordWebhook
import logging

# Initialize logger
log = logging.getLogger(__name__)


DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", None)


class Discord:
    """
    Usage:
    discord = Discord()
    discord.log("Title", "Description")

    You can set multiple webhooks for different purposes:
    def error(self, title, description=""):
        self._log(title, description, self.DISCORD_ERROR_WEBHOOK_URL)

    """

    def __init__(self):
        pass

    def _log(self, title, description="", webhook_url=None):
        if not webhook_url:
            log.warning("Discord webhook URL is not set")
            return

        try:
            log.debug(f"Notifying Discord: {title} - {description}")
            webhook = DiscordWebhook(
                url=webhook_url,
                content=f"**[{title}]**\n{description}",
            )
            webhook.execute()
        except Exception as e:
            log.error("An error occurred while notifying Discord:")
            log.error(e)

    def log(self, title, description=""):
        self._log(title, description, DISCORD_WEBHOOK_URL)

    # def error(self, title, description=""):
    #     self._log(title, description, self.DISCORD_ERROR_WEBHOOK_URL)
