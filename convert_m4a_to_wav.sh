#!/bin/bash  
  
# Directory containing m4a files  
SOURCE_DIR="/workspace/real_data_V2/m4a"  
  
# Directory where you want to save wav files  
OUTPUT_DIR="/workspace/real_data_V2/wav"  
  
# Create output directory if it does not exist  
mkdir -p "$OUTPUT_DIR"  
  
# Loop through each m4a file in the source directory  
for FILE in "$SOURCE_DIR"/*.m4a; do  
    # Extract the filename without the extension  
    BASENAME=$(basename "$FILE" .m4a)  
      
    # Define the output filename  
    OUTPUT_FILE="$OUTPUT_DIR/$BASENAME.wav"  
      
    # Convert m4a to wav using ffmpeg  
    ffmpeg -i "$FILE" -acodec pcm_s16le -ar 44100 "$OUTPUT_FILE"  
done  
  
echo "Conversion complete."  
