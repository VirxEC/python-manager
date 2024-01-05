__version__ = "5.0.0"

RELEASE_NOTES = {
    "5.0.0": """
    Initial hopeful v5 work
    May be scrapped later
    """
}

RELEASE_BANNER = f"""
\x1b[32;1m
           ______ _     ______       _
     10100 | ___ \\ |    | ___ \\     | |   00101
    110011 | |_/ / |    | |_/ / ___ | |_  110011
  00110110 |    /| |    | ___ \\/ _ \\| __| 01101100
    010010 | |\\ \\| |____| |_/ / (_) | |_  010010
     10010 \\_| \\_\\_____/\\____/ \\___/ \\__| 01001
\x1b[0m

"""


def get_current_release_notes():
    if __version__ in RELEASE_NOTES:
        return RELEASE_NOTES[__version__]
    return ""


def get_help_text():
    return (
        "Trouble? Ask on Discord at https://discord.gg/5cNbXgG "
        "or report an issue at https://github.com/RLBot/RLBot/issues"
    )


def print_current_release_notes():
    print(RELEASE_BANNER)
    print(f"Version {__version__}")
    print(get_current_release_notes())
    print(get_help_text())
    print("")
