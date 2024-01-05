# python-manager

This repo communicates with RLBot v5.
It's more bloated than what the real python-manager will be in the future,
as it includes some code for launching Rocket League/RLBot from v4.
I only wanted to go v4 code -> v5 code and not also have to translate Python to C#.

## Dev setup

- Generate the Flatbuffers code
  - Windows: `generate_flatbuffers.bat`
  - Linux: `./generate_flatbuffers.sh`
- Ensure Python 3.11 is installed
- Create a virtual Python environment
  - `python3 -m venv venv`
- Activate the virtual environment
  - Windows: `venv\Scripts\activate.bat`
  - Linux: `source venv/bin/activate`
- Install the package
  - `pip install --editable .`
  - This will install the package in editable mode, meaning you can make changes to the code and they will be reflected in the installed package without having to run the command again

## Testing

- You can test launching a match with `python tests/runner.py`
