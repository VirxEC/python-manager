echo 'Generating flatbuffers for Python...'

./flatbuffers-schema/flatc --python --gen-object-api -o ./ ./flatbuffers-schema/rlbot.fbs
