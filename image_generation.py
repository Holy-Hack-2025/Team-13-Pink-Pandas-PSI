#pip install --quiet --upgrade diffusers transformers accelerate invisible_watermark mediapy
#pip install --upgrade transformers diffusers

use_refiner = False
import mediapy as media
import random
import sys
import torch

from diffusers import DiffusionPipeline

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


prompt="A futuristic steel manufacturing plant operating at peak efficiency. Engineers analyze production data on digital screens, optimizing metal refining processes. Molten steel pours into molds, casting high-quality industrial components. Advanced robotic arms and AI-driven machinery ensure precision in manufacturing. A consultant presents a strategy for improving sustainability and efficiency in metal production, highlighting innovative techniques for reducing waste and energy consumption. The scene is dynamic, with bright sparks and the hum of industrial activity filling the atmosphere."
seed = random.randint(0, sys.maxsize)

images = pipe(
    prompt = prompt,
    output_type = "latent" if use_refiner else "pil",
    generator = torch.Generator("cuda").manual_seed(seed),
    ).images

if use_refiner:
  images = refiner(
      prompt = prompt,
      image = images,
      ).images

print(f"Prompt:\t{prompt}\nSeed:\t{seed}")
media.show_images(images)
images[0].save("output.jpg")
print('')

