# Year 2 ABWE Project Resources
All scripts used for my year 2 ABWE project. I anticipate 3 primary steps will be required to convert my raw data into findings, laid out below.

## Process
### 1. Transcription, Python
Audio collected from the site, containing details of behaviours performed, meterological values, and covariates will be transcribed with timestamps using [Whisper Distil Large v3](https://huggingface.co/distil-whisper/distil-large-v3) (Gandhi _et al._ 2023). Human oversight was required to ensure transcription accuracy, and to reliably clean the data.

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

# What was the relative humidity? (Abbott and Tabony 1985)
=100*EXP(1.8096+((17.2694*Z2)/(237.3+Z2)))-(0.0007866*998.3*(Y2-Z2)*(1+(Z2/610))))
/(EXP(1.8096+((17.2694*Y2)/(237.3+Y2)))

# What was the heat index? (Rothfusz 1990)
=(-8.78469475556)+(1.61139411*Y2)+(2.33854883889*AB2)
+(-0.14611605*Y2*AB2)+(-0.012308094*(Y2^2))+(-0.0164248277778*(AB2^2))
+(0.002211732*(Y2^2)*AB2)+(0.00085282*Y2*(AB2^2))
+(-0.000003582*(Y2^2)*(AB2^2))
```

### 3. Analysis, R
Analysis mainly performed in GraphPad Prism, however beta regression, correlation matrix, and FAMD were done in R.

Expected inputs:
```
> head(propdata)
  Temperature Proportion
1          36       0.23
2          36       0.00
3          36       0.06
4          37       0.16
5          36       0.00
6          36       0.79

> head(corrdata)
    Size ToyState PantState    DL DD DH   DF AS    AH    AD NV NE NF Location Day  Hour Cloud HeatIndex TotalDur TotalPlay
1 Medium        0         0 98.00  0  0 0.00  0  0.00 29.74  0  0  0 TQ275839   5 16:28     5        36   127.74     29.74
2 Medium        0         0 89.00  0  0 0.00  0  0.00  0.00  0  0  0 TQ275839   5 16:32     7        36    89.00      0.00
3  Small        1         0 30.00  0  0 0.00  2  0.00  0.00  0  0  0 TQ275839   5 16:32     7        36    32.00      2.00
4  Small        0         0 76.40  0  0 6.48  0  0.00 16.00  0  0  0 TQ275839   5 16:36     7        37    98.88     16.00
5 Medium        1         0 36.00  0  0 0.00  0  0.00  0.00  0  0  0 TQ275839   5 16:59     7        36    36.00      0.00
6  Large        0         0 20.06  0  0 0.00  0 73.48  0.00  0  0  1 TQ275839   5 16:59     7        36    93.54     73.48

> head(famddata)
    Size ToyState PantState    DL DD DH   DF AS    AH    AD NV NE NF Location Cloud HeatIndex
1 Medium        0         0 98.00  0  0 0.00  0  0.00 29.74  0  0  0 TQ275839     5        36
2 Medium        0         0 89.00  0  0 0.00  0  0.00  0.00  0  0  0 TQ275839     7        36
3  Small        1         0 30.00  0  0 0.00  2  0.00  0.00  0  0  0 TQ275839     7        36
4  Small        0         0 76.40  0  0 6.48  0  0.00 16.00  0  0  0 TQ275839     7        37
5 Medium        1         0 36.00  0  0 0.00  0  0.00  0.00  0  0  0 TQ275839     7        36
6  Large        0         0 20.06  0  0 0.00  0 73.48  0.00  0  0  1 TQ275839     7        36
```

## How to
Step-by-step instructions to reproduce my method on various systems. Assumes Git, Python, pip, python3-venv, R (v4.4 or higher), and RStudio are installed.

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

#### Step 3: Clean data
Paste csv data from transcriptions.txt into a spreadsheet:
```
ctrl-c
ctrl-v
``` 
Then spend a couple hours filtering out your unnecessary thoughts from the data and formatting for spreadsheet to take care of (as above).

#### Step 4: Analyse
Open breg-corr-famd.R in RStudio. Install requirements:
```
> install.packages(c("corrplot", "FactoMineR", "factoextra", "lmtest", "sandwich"))
```
Adjust paths in breg-corr-famd.R:
```
propdata <- read.csv('/path/to/propdata.csv')
corrdata <- read.csv('/path/to/corrdata.csv')
famddata <- read.csv('/path/to/famddata.csv')
```
Run script.

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

#### Step 3: Clean data
Paste csv data from transcriptions.txt into a spreadsheet and format accordingly.

#### Step 4: Analyse
Open breg-corr-famd.R in RStudio. Install requirements:
```
> install.packages(c("corrplot", "FactoMineR", "factoextra", "lmtest", "sandwich"))
```
Adjust paths in breg-corr-famd.R:
```
propdata <- read.csv('/path/to/propdata.csv')
corrdata <- read.csv('/path/to/corrdata.csv')
famddata <- read.csv('/path/to/famddata.csv')
```
Run script.

### MacOS
Basically use the Debian steps... I think.

## References
- Abbott, P.F. and Tabony, R.C. (1985) ‘The estimation of humidity parameters’, _Meteorological Magazine_, 114(1351), 49–56.
- Gandhi, S., Platen, P. von, and Rush, A.M. (2023) ‘Distil-Whisper: Robust Knowledge Distillation via Large-Scale Pseudo Labelling’, available: https://doi.org/10.48550/arXiv.2311.00430.
- GraphPad Software Inc. (2023) _GraphPad Prism_ (Version 10.4.2 for Windows), available: http://www.graphpad.com.
- Judd, C.M., McClelland, G.H., and Ryan, C.S. (2011) _Data Analysis_ [online], 0 ed., Routledge, available: https://doi.org/10.4324/9780203892053.
- Pagès, J. (2004) ‘Analyse factorielle de données mixtes’, _Revue de Statistique Appliquée_, 52(4), 93–111.
- Rothfusz, L. (1990) ‘The heat index “equation”or more than you ever wanted to know about heat index: National weather service southern region technical attachment sr/ssd 90-23’, _Fort Worth: National Weather Service_, 1–2.

