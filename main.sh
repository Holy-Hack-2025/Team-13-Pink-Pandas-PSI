#!/bin/bash

# Check if all required arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <file_name> <modality> <position> <company>"
    echo "Example: $0 goods-flow-management.pdf image logistic-manager PSI summary.txt"
    exit 1
fi

# Assign command-line arguments to variables
file_name="$1"          # e.g., goods-flow-management.pdf
modality="$2"           # e.g. your desired modality for information communication (text, image, or audio)
position="$3"           # e.g., your position (floor manager, cargo driver, project manager, ect)
company="$4"            # e.g., what kind of company you work at (business, logistics, transport, etc)

# Extract the base name (without .pdf) for the directory
base_name=$(basename "$file_name" .pdf)  # e.g., goods-flow-management

# Create a directory with the base name
mkdir -p "$base_name"

# Run the pdf_summary.py script with the input file
# Assuming pdf_summary.py saves the summary to output/summary_<base_name>.txt
python pdf_summary.py "$file_name"

# Move the generated summary to the new directory
mv "output/summary.txt" "$base_name/summary.txt"

# Generate prompt(s)
python deepseek_promptgen.py --modality "$modality" \
    --position "$position"  \
    --company "$company"  \
    --proposal "$base_name/summary.txt"

mv prompts_*.txt "$base_name/"

# Check if prompts_img.txt exists in the directory and process each line
prompts_img_file="$base_name/prompts_image.txt"
if [ -f "$prompts_img_file" ]; then
    echo "Found $prompts_img_file. Processing..."
    python image_generation.py "$prompts_img_file"

    # Move generated image files to the base_name directory
    echo "Moving generated images to $base_name/"
    mv output_step_*.jpg "$base_name/"
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
    mv *.wav "$base_name/"
else
    echo "No $prompts_audio_file found in $base_name/. Skipping audio generation."
fi
