echo 'Generating flatbuffers for Python...'

# flatc overrides __init__.py with an empty file
# move it away and then back to avoid this
mv ./rlbot/__init__.py __init__.py

./flatbuffers-schema/flatc --python --gen-object-api -o ./ ./flatbuffers-schema/rlbot.fbs

# remove the flatc generated file and put ours back
rm ./rlbot/__init__.py
mv __init__.py ./rlbot/__init__.py
