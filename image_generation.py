#pip install --quiet --upgrade diffusers transformers accelerate invisible_watermark mediapy
#pip install --upgrade transformers diffusers

use_refiner = False
import mediapy as media
import random
import sys
import torch

from diffusers import DiffusionPipeline
import re

pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
    )

if use_refiner:
  refiner = DiffusionPipeline.from_pretrained(
      "stabilityai/stable-diffusion-xl-refiner-1.0",
      text_encoder_2=pipe.text_encoder_2,
      vae=pipe.vae,
      torch_dtype=torch.float16,
      use_safetensors=True,
      variant="fp16",
  )

  refiner = refiner.to("cuda")

  pipe.enable_model_cpu_offload()
else:
  pipe = pipe.to("cuda")

file = sys.argv[1]
with open(file,"r") as f:
    text = f.read()
    print(f"here's my text: {text}")

# Regex to extract each numbered step and its content
pattern = r"\**(?:Step\s*)?(\d+)[\.:]?\**\s*(.+)"
steps = re.findall(pattern, text)
# the generated output sometimes has different formatting
# steps = re.findall(r"\d+\.\s\*([A-Za-z\s]+)\*:\s([^\n]+)", text)

# Initialize the seed
seed = random.randint(0, sys.maxsize)

# Loop over each step to generate images
for idx, (instruction, step_description) in enumerate(steps, start=1):
    # Construct the prompt for each step
    prompt = f"Create an illustration of the process: {step_description}, focusing on {instruction.lower()}."

    # Generate the image for each step
    images = pipe(
        prompt=prompt,
        output_type="latent" if use_refiner else "pil",
        generator=torch.Generator("cuda").manual_seed(seed),
    ).images

    # Optionally refine the image
    if use_refiner:
        images = refiner(
            prompt=prompt,
            image=images,
        ).images

    # Print the step details
    print(f"Step {idx}: {instruction}")
    print(f"Prompt: {prompt}")
    print(f"Seed: {seed}")

    # Show and save the image
    media.show_images(images)
    images[0].save(f"output_step_{idx}.jpg")

    # Add a separator for clarity
    print('')
