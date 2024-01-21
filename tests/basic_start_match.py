from pathlib import Path

from rlbot.match_manager import MatchManager

if __name__ == "__main__":
    match_manager = MatchManager()

    current_directory = Path(__file__).absolute().parent
    match_manager.load_config_from_file(current_directory / "default.toml")
    match_manager.connect_to_game()
    match_manager.start_match()
