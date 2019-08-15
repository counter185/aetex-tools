# aetex-tools
Python tools for importing and exporting .AETEX format files

This is a work-in-progress tool to import and export textures in the .AETEX (Atrophy Engine Texture File) format. Not much is known about the format, so we need to work out how it works.

The format was used in games running on the Atrophy Engine, which seems to be an in-house engine created by Gaijin Games (now known as Choice Provisions). The engine was used to make the entire Bit.Trip series of games, excluding Runner3, which uses the Unity engine.

While Runner2 also seems to be using AETEX textures, they are actually disguised DDS files with a different header. Those will not work with this script.

# Progress:
Importer:
Works on some files, while not on others. I got better luck with textures from the newer games.

Exporter:
Currently does not work. As I said, we need to work out the way the format works before we can export files in said format.

# Required python modules:
OpenCV2,
Numpy
