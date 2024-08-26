#!/bin/bash  
  
# Directory containing opus files  
SOURCE_DIR="/workspace/ATC_recordings_johanna/opus"  
  
# Directory where you want to save wav files  
OUTPUT_DIR="/workspace/ATC_recordings_johanna/wav"  
  
# Create output directory if it does not exist  
mkdir -p "$OUTPUT_DIR"  
  
# Loop through each opus file in the source directory  
for FILE in "$SOURCE_DIR"/*.opus; do  
    # Extract the filename without the extension  
    BASENAME=$(basename "$FILE" .opus)  
  
    # Define the output filename  
    OUTPUT_FILE="$OUTPUT_DIR/$BASENAME.wav"  
  
    # Convert opus to wav using ffmpeg  
    ffmpeg -i "$FILE" -acodec pcm_s16le -ar 44100 "$OUTPUT_FILE"  
done  
  
echo "Conversion complete."  
