from TTS.api import TTS
import argparse

def text_to_speech(text, output_file="output.wav", model_name="tts_models/en/ljspeech/tacotron2-DDC"):
    """
    Convert input text to speech and save it as an audio file.
    
    :param text: The text to convert to speech.
    :param output_file: The output WAV file path.
    :param model_name: The pretrained TTS model to use.
    """
    tts = TTS(model_name)
    tts.tts_to_file(text=text, file_path=output_file)
    print(f"TTS done! Saved to '{output_file}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text to speech using Coqui TTS.")
    parser.add_argument("text", type=str, help="Text to be converted to speech.")
    parser.add_argument("--output", type=str, default="output.wav", help="Output file name.")
    parser.add_argument("--model", type=str, default="tts_models/en/ljspeech/tacotron2-DDC", help="Pretrained model name.")
    
    args = parser.parse_args()
    text_to_speech(args.text, args.output, args.model)


