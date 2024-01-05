echo 'Generating flatbuffers for Python...'

# flatc overrides __init__.py with an empty file
# move it away and then back to avoid this
move .\rlbot\__init__.py .\

.\flatbuffers-schema\flatc.exe --python --gen-object-api -o .\ .\flatbuffers-schema\rlbot.fbs

# remove the flatc generated file and put ours back
DEL .\rlbot\__init__.py
move __init__.py .\rlbot
