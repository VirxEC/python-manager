from pathlib import Path
from time import sleep

from rlbot.match_manager import MatchManager

if __name__ == "__main__":
    match_manager = MatchManager()

    current_directory = Path(__file__).absolute().parent
    match_manager.load_config_from_file(current_directory / "rlbot.toml")
    try:
        match_manager.connect_to_game()
        match_manager.start_match()

        print("Waiting before shutdown...")
        sleep(12)
    except KeyboardInterrupt:
        print("Shutting down early due to interrupt")
    except Exception as e:
        print(f"Shutting down early due to: {e}")
    match_manager.shut_down()
