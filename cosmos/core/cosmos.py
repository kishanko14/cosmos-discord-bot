import discord

from discord.ext import commands
from cosmos.core.utilities.time import Time
from cosmos.core.functions.configs.handler import ConfigHandler
from cosmos.core.functions.logger.handler import LoggerHandler
from cosmos.core.functions.plugins.handler import PluginHandler
from cosmos.core.functions.database.database import Database
from cosmos.core.functions.exceptions.handler import ExceptionHandler


class Cosmos(commands.Bot):

    def __init__(self, token=None, client_id=None, prefixes=None):
        self.time = None
        self.configs = None
        self.eh = None
        self.log = None
        self.db = None
        self.plugins = None
        self._init_time()
        self._init_configs()
        super().__init__(
            command_prefix=commands.when_mentioned_or(*self.configs.cosmos.prefixes)
        )
        self._init_logger()
        self._init_exception_handler()
        self._init_database()
        self._init_plugins()
        self.configs.discord.token = token or self.configs.discord.token
        self.configs.discord.client_id = client_id or self.configs.discord.client_id
        self.configs.discord.prefixes = prefixes or self.configs.cosmos.prefixes

    def _init_time(self):
        print("Initialising Cosmos time.")
        self.time = Time()
        print("Done.", end="\n\n")

    def _init_configs(self):
        print("Initialising configs.")
        start_time = self.time.time()
        self.configs = ConfigHandler(self)
        print(f"Done. [{round(self.time.time() - start_time, 3)}s].\n\n")

    def _init_logger(self):
        print("Initialising logger.")
        start_time = self.time.time()
        self.log = LoggerHandler(self)
        self.log.info(f"Done. [{round(self.time.time() - start_time, 3)}s].\n\n")

    def _init_exception_handler(self):
        self.log.info("Initialising exception handler.")
        start_time = self.time.time()
        self.eh = ExceptionHandler(self)
        self.log.info(f"Done. [{round(self.time.time() - start_time, 3)}s].\n\n")

    def _init_database(self):
        self.log.info("Initialising database.")
        start_time = self.time.time()
        self.db = Database(self)
        self.log.info(f"Done. [{round(self.time.time() - start_time, 3)}s].\n\n")

    def _init_plugins(self):
        self.log.info("Initialising plugins.")
        start_time = self.time.time()
        self.plugins = PluginHandler(self)
        self.log.info(f"Done. [{round(self.time.time() - start_time, 3)}s].\n\n")

    def run(self):
        try:
            super().run(self.configs.discord.token)
        except discord.LoginFailure:
            self.log.info("Invalid token provided.")

    async def on_ready(self):
        self.log.info(f"{self.user.name}#{self.user.discriminator} Ready! [{self.time.round_time()} seconds.]")
        self.log.info(f"User Id: {self.user.id}")
        self.log.info("-------")