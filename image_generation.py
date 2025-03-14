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


text = """
Create an illustration of an efficient cargo reception process in a warehouse setting, easily understood by a floor manager at a transport company. The image should depict the following:

1. *Pre-Arrangement*: A warehouse team preparing a designated area for incoming shipments, with clear labels and organized spaces.
2. *Communication Flow*: A digital screen or tablet displaying detailed information about incoming shipments, including consignment contents, volume, packing list, and waybill.
3. *Vehicle Coordination*: A truck approaching the warehouse, with a driver making a phone call to notify the warehouse team of arrival within one hour, as on a clock or timeline visual.
4. *Scheduled Offloading*: A busy storage facility with a schedule board showing specific times for vehicle offloading, managed by a floor manager.
5. *Problem Handling*: A designated area for damaged or expired items, clearly marked and separated from the main consignment, with a worker inspecting and tagging items for repair or disposal.
6. *Internal Transfers*: A seamless process between two warehouses, with a digital system transmitting advanced delivery information to the receiving location.
"""

# Regex to extract each numbered step and its content
steps = re.findall(r"\d+\.\s\*([A-Za-z\s]+)\*:\s([^\n]+)", text)

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
