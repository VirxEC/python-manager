"""Standalone Bot Script

Usage:
    standalone [--player-index=0] [--name=MyBot] [--team=0] [--spawn-id=23245] [--main-executable-path="../core/RLBotCS/bin/Release/"]

Options:
    --player-index=I             Index that the player is running under. Will be passed to your bot's constructor.
    --name=N                     Name that will be passed to your bot's constructor. Does not influence in-game name.
    --team=T                     Team the bot is playing on, 0 for blue, 1 for orange. Will be passed to your bot's constructor.
    --spawn-id=S                 Spawn identifier used to confirm the right car in the packet.
    --main-executable-path=M     Path to the main RLBot executable. Defaults to the executable path in the config file.
"""
from typing import Optional

from docopt import docopt, printable_usage


class StandaloneArgParser:
    def __init__(self, argv: list[str]):
        arguments = docopt(__doc__, argv[1:])
        self.name = arguments["--name"]
        self.team = self.int_or_none(arguments["--team"])
        self.player_index = self.int_or_none(arguments["--player-index"])
        self.spawn_id = self.int_or_none(arguments["--spawn-id"])
        self.main_executable_path = arguments["--main-executable-path"]

        if (
            self.name is None
            or self.team is None
            or self.player_index is None
            or self.spawn_id is None
        ):
            print("Standalone bot is missing required arguments!")
            print(printable_usage(__doc__))

    def int_or_none(self, val) -> Optional[int]:
        if val:
            return int(val)
        return None
