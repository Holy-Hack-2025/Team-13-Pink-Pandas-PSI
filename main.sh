#!/bin/bash

# Check if all required arguments are provided
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <file_name> <modality> <position> <company> <proposal>"
    echo "Example: $0 goods-flow-management.pdf image logistic-manager PSI summary.txt"
    exit 1
fi

# Assign command-line arguments to variables
file_name="$1"          # e.g., goods-flow-management.pdf
modality="$2"           # e.g., image
position="$3"           # e.g., logistic-manager
company="$4"            # e.g., PSI
proposal="$5"           # e.g., summary.txt

# Extract the base name (without .pdf) for the directory
base_name=$(basename "$file_name" .pdf)  # e.g., goods-flow-management

# Create a directory with the base name
mkdir -p "$base_name"

# Run the pdf_summary.py script with the input file
# Assuming pdf_summary.py saves the summary to output/summary_<base_name>.txt
python pdf_summary.py "pdf/$file_name"

# Move the generated summary to the new directory
mv "output/summary.txt" "$base_name/summary_$base_name.txt"

# Generate prompt(s)
python deepseek_promptgen.py --modality "$modality" \
    --position "$position"  \
    --company "$company"  \
    --proposal "$base_name/$proposal"

# Check if prompts_img.txt exists in the directory and process each line
prompts_img_file="$base_name/prompts_img.txt"
if [ -f "$prompts_img_file" ]; then
    echo "Found $prompts_img_file. Processing..."
    python image_generation.py "$prompt"
    
    # Move generated image files to the base_name directory
    echo "Moving generated images to $base_name/"
    mv output/output_step_*.jpg "$base_name/"
else
    echo "No $prompts_img_file found in $base_name/. Skipping image generation."
fi

# Check if prompts_audio.txt exists in the directory and process each line
prompts_audio_file="$base_name/prompts_audio.txt"
if [ -f "$prompts_audio_file" ]; then
    echo "Found $prompts_audio_file. Processing each prompt..."
    while IFS= read -r prompt; do
        # Skip empty lines
        [ -z "$prompt" ] && continue
        echo "Running audio_generator.py with prompt: '$prompt'"
        python audio_generator.py "$prompt"
    done < "$prompts_audio_file"
else
    echo "No $prompts_audio_file found in $base_name/. Skipping audio generation."
fi