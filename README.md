# Year 2 ABWE Project Resources
All scripts used for my year 2 ABWE project. I anticipate 3 primary steps will be required to convert my raw data into findings, laid out below.

## Process
### 1. Transcription, Python
Audio collected from the site, containing details of behaviours performed, meterological values, and covariates will be transcribed with timestamps using [Whisper Distil Large v3](https://huggingface.co/distil-whisper/distil-large-v3) (Gandhi _et al._). Human oversight will be required to ensure transcription accuracy, and to reliably clean the data into CSV for insertion into database.

My favourite part of this is when it acknowledges after some time:<br />
`You seem to be using the pipelines sequentially on GPU. In order to maximize efficiency please use a dataset`<br />
This shouldn't be difficult to implement, but I really can't see it providing a significant enough boost with such a small dataset. Nonetheless, this is a potential area for performance improvement alongside compilation/IO-aware attention/dusting off the RTX 3060. 

### 2. Storage, SQL
Database will be configured and data inserted into it. ERD will be displayed at later date, but basically: Day has many Batch (mean dry/wet bulb readings), Batch has many Dog (size, bark_freq, elim_freq), Dog has Behaviours (mode, timestamps).

### 3. Analysis, R
Analysis will be done by graphing the relationship between proportion of time spent playing to not-playing per dog against heat index, alongside some descriptive statistics and other fun graphs.

## How to
Step-by-step instructions to reproduce my method on various systems. Assumes Git, Python, pip, and python3-venv are installed.

## Debian (I did this)
### Step 1: Initialise repo
Clone, enter, and install requirements for the repo:
```
git clone https://github.com/JoshuaJewell/abwe2-res.git
cd abwe2-res
python3 -m venv venv
pip install torch transformers
```

### Step 2: Transcribe recordings
Copy recordings and run script:
```
cp -r /path/to/recordings /path/to/abwe2-res/transcription/recordings
python ./transcription/whisper.py
```

## Windows (You might want to do this)

## MacOS (Ew)

## References
Gandhi, S., Platen, P. von, and Rush, A.M. (2023) ‘Distil-Whisper: Robust Knowledge Distillation via Large-Scale Pseudo Labelling’, available: https://doi.org/10.48550/arXiv.2311.00430.
