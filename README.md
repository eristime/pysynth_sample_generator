Generate multiple samples with varying tempo, length, pattern and gaussian noise-levels using PySynth.

## Installation:

Install PySynth from https://github.com/mdoege/PySynth

Install requirements with pip:

```
pip install -r requirements.txt
```

## Running
Run script to generate samples. Parameters can be modified also in main.py

```
python main.py sample_folder
```

## Defining parameters:

```
parameters = {
    'tempo': {
        'start': 100,
        'end': 110,
        'interval': 5},  # (bpm_start, bpm_end, interval)
    'length': {
        'start': 1,
        'end': 1,
        'interval': 0},  # (start, end, interval) note: length in bars not in seconds
    'patterns': {
        'defined': ['8th-note', '4th-note'],
        'random': 3},  # ('random'), generate 5 random patterns
    'std': {
        'start': 1000,
        'end': 3000,
        'interval': 1000}
}
```

### Notes:
Input folder is relative to main.py. Every key has to have a value defined.
Ranges function the same as Python range()-function.

No support for one sample generation.