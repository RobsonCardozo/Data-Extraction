import os

# Get the current working directory


# Build the path to the settings.py file


# Read the contents of the settings.py file
with open(settings_path, 'r') as f:
    settings_contents = f.read()

# Replace instances of 'Data-Extraction' with 'Data_Extraction'


# Write the modified contents back to the settings.py file
