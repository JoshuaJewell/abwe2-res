import os
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

def adjust_timestamps(chunks):
    acc = 0.0
    adjusted = []
    first = True

    for chunk in chunks:
        start, end = chunk["timestamp"]

        round(end, 2)
        round(start, 2)

        if not first and start == 0.0:
            acc += 30.0

        abs_start = start + acc if start is not None else None
        abs_end = end + acc if end is not None else None

        adjusted.append({
            "text": chunk["text"],
            "timestamp": (abs_start, abs_end)
        })

        if end == 0.0:
            acc += 30.0

        first = False

    return adjusted

# Set device and data type
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Load model and processor
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

# Process all audio files in the recordings directory
recordings_dir = "recordings"
output_file = "transcriptions.txt"

# Get and sort audio files
filenames = [f for f in os.listdir(recordings_dir) if f.endswith(".wav")]
filenames.sort()

# Process files and write output
with open(output_file, "w") as outfile:
    for filename in filenames:
        # Print progress information
        print(f"\nProcessing file: {filename}")
        
        # Process audio file
        audio_path = os.path.join(recordings_dir, filename)
        result = pipe(audio_path)
        chunks = adjust_timestamps(result["chunks"])
        
        # Print transcription result
        print(f"Transcription result for {filename}:\n")
        print("timestamp_start | timestamp_end | text\n")
        for chunk in chunks:
            start, end = chunk["timestamp"]
            text = chunk["text"]
            print(f"{start} | {end} | {text}\n")
        print("\n")
        print("-" * 50)  # Separator between files
        
        # Write to file
        outfile.write(f"[{filename}]\n")
        for chunk in chunks:
            start, end = chunk["timestamp"]
            text = chunk["text"]
            outfile.write(f"{start};{end};{text}\n")
        outfile.write("\n")

print(f"\nProcessing complete! Full transcript saved to {output_file}")
