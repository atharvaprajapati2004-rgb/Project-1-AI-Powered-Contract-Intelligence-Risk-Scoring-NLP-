# Data Directory

This directory contains datasets used by the AI-Powered Contract Intelligence and Risk Scoring project.

## raw/

Contains original datasets such as the CUAD dataset without modification.

## processed/

Contains cleaned and preprocessed datasets generated from the raw data.

> The processed dataset is not final yet and may change during development.


## CUAD Data Processing Pipeline

The CUAD dataset is organized into separate raw and processed directories.

### Data Flow

Raw CUAD Dataset
        ↓
Dataset Validation
        ↓
CUAD Preprocessing
        ↓
Processed Dataset
        ↓
NLP / Machine Learning Pipeline

### Preprocessing

The `scripts/preprocess_cuad.py` utility prepares the CUAD dataset for
downstream NLP and machine learning tasks.

The preprocessing utility:

- Loads the CUAD JSON dataset.
- Checks the CUAD data structure.
- Extracts document titles.
- Extracts contract paragraph context.
- Extracts questions.
- Extracts answer information.
- Removes unnecessary whitespace.
- Handles missing or empty fields safely.
- Saves the structured output as JSON.

### Output

The processed dataset will be stored at:

`data/processed/cuad_processed.json`

The original/raw dataset is not modified during preprocessing.

This separation allows the team to experiment with different preprocessing
strategies while preserving the original CUAD data.