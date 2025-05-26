# Year 2 ABWE Project Resources
All scripts used for my year 2 ABWE project. I anticipate 3 primary steps will be required to convert my raw data into findings, laid out below.

## Process
### 1. Transcription, Python
Audio collected from the site, containing details of behaviours performed, meterological values, and covariates will be transcribed with timestamps using [Whisper Distil Large v3](https://huggingface.co/distil-whisper/distil-large-v3) (Gandhi _et al._). Human oversight will be required to ensure transcription accuracy, and to reliably clean the data.

My favourite part of this is when it acknowledges after some time:<br />
`You seem to be using the pipelines sequentially on GPU. In order to maximize efficiency please use a dataset`<br />
This shouldn't be difficult to implement, but I really can't see it providing a significant enough boost with such a small dataset. Nonetheless, this is a potential area for performance improvement alongside compilation/IO-aware attention/dusting off the RTX 3060.

### 2. Storage, SQL (until it wasn't)
Just use a spreadsheet, they said. It'll be easier, they said...
```
# What toy did the dog play with?
=IFERROR(MID(
  OFFSET(INDIRECT(H2),0,4),
  FIND(", ",OFFSET(INDIRECT(H2),0,4))+2,
  LEN(OFFSET(INDIRECT(H2),0,4))
),"")

# How long did the dog sit down?
=SUMIF(
  OFFSET(INDIRECT($H2), 1, 2, $I2, 1),
  M$1, OFFSET(INDIRECT($H2), 1, 4, $I2, 1)
)

# How hot was it on average?
=AVERAGE(
  VALUE(TRIM(MID(
    OFFSET(INDIRECT(H2), 0, 1),
    FIND(",", OFFSET(INDIRECT(H2), 0, 1)) + 1,
    FIND(",", OFFSET(INDIRECT(H2), 0, 1) & ",",
    FIND(",", OFFSET(INDIRECT(H2), 0, 1)) + 1)
    -FIND(",", OFFSET(INDIRECT(H2), 0, 1)) - 1))),
  VALUE(TRIM(MID(
    OFFSET(INDIRECT(H2), 0, 2),
    FIND(",", OFFSET(INDIRECT(H2), 0, 2)) + 1,
    FIND(",", OFFSET(INDIRECT(H2), 0, 2) & ",",
    FIND(",", OFFSET(INDIRECT(H2), 0, 2)) + 1)
    -FIND(",", OFFSET(INDIRECT(H2), 0, 2)) - 1)))
)

# What was the relative humidity?
=100*EXP(1.8096+((17.2694*Z2)/(237.3+Z2)))-(0.0007866*998.3*(Y2-Z2)*(1+(Z2/610))))
/(EXP(1.8096+((17.2694*Y2)/(237.3+Y2)))

# What was the heat index?
=(-8.78469475556)+(1.61139411*Y2)+(2.33854883889*AB2)
+(-0.14611605*Y2*AB2)+(-0.012308094*(Y2^2))+(-0.0164248277778*(AB2^2))
+(0.002211732*(Y2^2)*AB2)+(0.00085282*Y2*(AB2^2))
+(-0.000003582*(Y2^2)*(AB2^2))
```

### 3. Analysis, R
Analysis will be done by graphing the relationship between proportion of time spent playing to not-playing per dog against heat index, alongside some descriptive statistics and other fun graphs.

## How to
Step-by-step instructions to reproduce my method on various systems. Assumes Git, Python, pip, and python3-venv are installed.

### Debian (I did this)
#### Step 1: Initialise repo
Clone, enter, and install requirements for the repo:
```
git clone https://github.com/JoshuaJewell/abwe2-res.git
cd abwe2-res
python3 -m venv venv
pip install torch transformers
```

#### Step 2: Transcribe recordings
Copy recordings and run script:
```
cp -r /path/to/recordings /path/to/abwe2-res/transcription/recordings
python ./transcription/whisper.py
```

### Windows (You might want to do this)
#### Step 1: Initialise repo
Clone, enter, and install requirements for the repo:
```
git clone https://github.com/JoshuaJewell/abwe2-res.git
cd abwe2-res
python -m venv venv
venv\Scripts\pip.exe install torch transformers
```

#### Step 2: Transcribe recordings
Copy recordings and run script:
```
xcopy /E /I C:\path\to\recordings C:\path\to\abwe2-res\transcription\recordings
python .\transcription\whisper.py
```

### MacOS (Ew)
Basically use the Debian steps... I think.

## References
Gandhi, S., Platen, P. von, and Rush, A.M. (2023) ‘Distil-Whisper: Robust Knowledge Distillation via Large-Scale Pseudo Labelling’, available: https://doi.org/10.48550/arXiv.2311.00430.
