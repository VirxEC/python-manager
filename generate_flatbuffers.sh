echo 'Generating flatbuffers for Python...'

./flatbuffers-schema/flatc --python -o ./ ./flatbuffers-schema/rlbot.fbs
