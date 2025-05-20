import os
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# Set device
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Loading
model_id = "distil-whisper/distil-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
).to(device)

processor = AutoProcessor.from_pretrained(model_id)

# Create ASR pipeline
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
    return_timestamps=True,
    generate_kwargs={
        "language": "english",
        "condition_on_prev_tokens": False,
    }
)

# Sort audio files from dir
recordings_dir = "recordings"
output_file = "transcriptions.txt"

filenames = [f for f in os.listdir(recordings_dir) if f.endswith(".wav")]
filenames.sort()  # Sort by filename (assumes chronological order)

# Process
with open(output_file, "w") as outfile:
    for filename in filenames:
        print(f"\nProcessing file: {filename}")
        
        audio_path = os.path.join(recordings_dir, filename)
        result = pipe(audio_path)
        
        outfile.write(f"[{filename}]\n")
        for chunk in result.get("chunks", []):
            outfile.write(f"{chunk['text']}\n")
        outfile.write("\n")
        
        print(f"Transcription result for {filename}:")
        for chunk in result.get("chunks", []):
            print(chunk['text'])
        print("-" * 50)

print(f"\nProcessing complete!")
